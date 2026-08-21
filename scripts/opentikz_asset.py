#!/usr/bin/env python3
"""Search, copy, and compile assets from the vendored OpenTikZ catalog."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = SKILL_ROOT / "assets" / "opentikz"
LOCK_PATH = SKILL_ROOT / "opentikz.lock.json"


def fail(message: str, code: int = 2) -> None:
    print(json.dumps({"error": message}, ensure_ascii=False), file=sys.stderr)
    raise SystemExit(code)


def load_catalog(root: Path) -> list[dict[str, Any]]:
    catalog_path = root / "catalog.json"
    if not catalog_path.is_file():
        fail(f"OpenTikZ catalog not found: {catalog_path}")
    try:
        data = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"Cannot read OpenTikZ catalog: {exc}")
    if not isinstance(data, list):
        fail("OpenTikZ catalog must contain a JSON list")
    return data


def upstream_commit() -> str:
    try:
        lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
        commit = lock.get("commit")
    except (OSError, json.JSONDecodeError):
        commit = None
    return str(commit) if commit else "unknown"


def safe_item_dir(root: Path, item: dict[str, Any]) -> Path:
    rel = item.get("path")
    if not isinstance(rel, str) or not rel:
        fail(f"Catalog item {item.get('id', '<unknown>')} has no path")
    root_resolved = root.resolve()
    candidate = (root / rel).resolve()
    if candidate != root_resolved and root_resolved not in candidate.parents:
        fail(f"Catalog item path escapes OpenTikZ root: {rel}")
    return candidate


def tokenize(value: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", value.casefold())


def rank_item(item: dict[str, Any], query: str) -> int:
    q = query.casefold().strip()
    q_tokens = set(tokenize(q))
    item_id = str(item.get("id", "")).casefold()
    name = str(item.get("name", "")).casefold()
    tags = [str(tag).casefold() for tag in item.get("tags", [])]
    domains = [str(domain).casefold() for domain in item.get("domain", [])]
    description = str(item.get("description", "")).casefold()

    score = 0
    if q == item_id:
        score += 1000
    if q == name:
        score += 900
    if q in tags:
        score += 700
    if item_id.startswith(q) or name.startswith(q):
        score += 400
    if q and (q in item_id or q in name):
        score += 250
    if q and any(q in tag for tag in tags):
        score += 180
    if q and any(q in domain for domain in domains):
        score += 80
    if q and q in description:
        score += 60

    searchable = " ".join([item_id, name, *tags, *domains, description])
    overlap = q_tokens.intersection(tokenize(searchable))
    score += 25 * len(overlap)
    if q_tokens and overlap == q_tokens:
        score += 100
    return score


def find_item(catalog: list[dict[str, Any]], item_id: str) -> dict[str, Any]:
    matches = [item for item in catalog if item.get("id") == item_id]
    if not matches:
        fail(f"No OpenTikZ item with id '{item_id}'")
    if len(matches) > 1:
        fail(f"OpenTikZ id is ambiguous: '{item_id}'")
    return matches[0]


def candidate_file(item_dir: Path, item: dict[str, Any], kind: str) -> Path:
    item_id = str(item.get("id", ""))
    names: list[str]
    if kind == "svg":
        names = [str(item.get("preview", "")), "preview.svg", f"{item_id}.svg"]
    elif kind == "tex":
        names = ["template.tex", "figure.tex", f"{item_id}.tex"]
    elif kind == "meta":
        names = ["template.meta.json", "figure.meta.json", f"{item_id}.meta.json"]
    else:
        fail(f"Unsupported asset format: {kind}")
    for name in names:
        if name and (item_dir / name).is_file():
            return item_dir / name
    fail(f"No {kind} file found for OpenTikZ item '{item_id}'")
    raise AssertionError("unreachable")


def output_path(out: Path, source: Path) -> Path:
    if out.exists() and out.is_dir():
        return out / source.name
    if out.suffix:
        out.parent.mkdir(parents=True, exist_ok=True)
        return out
    out.mkdir(parents=True, exist_ok=True)
    return out / source.name


def emit(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def command_search(args: argparse.Namespace) -> None:
    catalog = load_catalog(args.root)
    results: list[tuple[int, dict[str, Any]]] = []
    for item in catalog:
        if args.type != "any" and item.get("type") != args.type:
            continue
        domains = [str(domain).casefold() for domain in item.get("domain", [])]
        if args.domain and args.domain.casefold() not in domains:
            continue
        score = rank_item(item, args.query)
        if score > 0:
            results.append((score, item))
    results.sort(key=lambda pair: (-pair[0], str(pair[1].get("id", ""))))
    compact = []
    for score, item in results[: args.limit]:
        compact.append(
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "type": item.get("type"),
                "domain": item.get("domain", []),
                "tags": item.get("tags", []),
                "path": item.get("path"),
                "preview": item.get("preview"),
                "score": score,
            }
        )
    emit({"query": args.query, "count": len(compact), "results": compact})


def command_info(args: argparse.Namespace) -> None:
    item = find_item(load_catalog(args.root), args.id)
    item_dir = safe_item_dir(args.root, item)
    files = sorted(str(path.relative_to(args.root)) for path in item_dir.iterdir() if path.is_file())
    emit({"item": item, "files": files, "upstream_commit": upstream_commit()})


def copy_kind(root: Path, item_id: str, kind: str, out: Path) -> None:
    item = find_item(load_catalog(root), item_id)
    source = candidate_file(safe_item_dir(root, item), item, kind)
    target = output_path(out, source)
    shutil.copy2(source, target)
    emit(
        {
            "id": item_id,
            "format": kind,
            "source": str(source),
            "output": str(target.resolve()),
            "license": item.get("license"),
        }
    )


def command_copy(args: argparse.Namespace) -> None:
    copy_kind(args.root, args.id, args.format, args.out)


def command_copy_source(args: argparse.Namespace) -> None:
    copy_kind(args.root, args.id, "tex", args.out)


def run_checked(command: list[str], cwd: Path) -> None:
    try:
        result = subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)
    except FileNotFoundError:
        fail(f"Required command is not installed: {command[0]}")
    except subprocess.CalledProcessError as exc:
        details = "\n".join((exc.stdout or "", exc.stderr or "")).strip().splitlines()[-40:]
        fail(
            f"Command failed with exit code {exc.returncode}: {' '.join(command)}"
            + ("\n" + "\n".join(details) if details else "")
        )
    if result.stderr and "warning" in result.stderr.casefold():
        print(result.stderr.strip(), file=sys.stderr)


def command_compile(args: argparse.Namespace) -> None:
    tex = args.tex.resolve()
    if not tex.is_file():
        fail(f"TikZ source not found: {tex}")
    destination = args.out.resolve()
    if destination.suffix.casefold() != ".svg":
        destination.mkdir(parents=True, exist_ok=True)
        destination = destination / f"{tex.stem}.svg"
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)

    latexmk = shutil.which("latexmk")
    pdflatex = shutil.which("pdflatex")
    converter = shutil.which("pdftocairo") or shutil.which("dvisvgm")
    if not latexmk and not pdflatex:
        fail("Install latexmk or pdflatex to compile editable OpenTikZ sources")
    if not converter:
        fail("Install pdftocairo or dvisvgm to convert the compiled PDF to SVG")

    with tempfile.TemporaryDirectory(prefix="opentikz-build-") as tmp:
        build_dir = Path(tmp)
        if latexmk:
            run_checked(
                [latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error", f"-outdir={build_dir}", tex.name],
                tex.parent,
            )
        else:
            run_checked(
                [pdflatex, "-interaction=nonstopmode", "-halt-on-error", f"-output-directory={build_dir}", tex.name],
                tex.parent,
            )
        pdf = build_dir / f"{tex.stem}.pdf"
        if not pdf.is_file():
            fail(f"LaTeX completed without producing the expected PDF: {pdf}")
        if Path(converter).name == "pdftocairo":
            run_checked([converter, "-svg", str(pdf), str(destination)], tex.parent)
        else:
            run_checked([converter, "--pdf", "--bbox=papersize", f"--output={destination}", str(pdf)], tex.parent)

    if not destination.is_file() or "<svg" not in destination.read_text(encoding="utf-8", errors="ignore")[:4096]:
        fail(f"SVG conversion did not produce a valid SVG: {destination}")
    emit({"source": str(tex), "output": str(destination), "converter": Path(converter).name})


def command_validate(args: argparse.Namespace) -> None:
    catalog = load_catalog(args.root)
    problems: list[str] = []
    seen: set[str] = set()
    counts: dict[str, int] = {}
    for item in catalog:
        item_id = str(item.get("id", ""))
        if not item_id:
            problems.append("catalog item without id")
            continue
        if item_id in seen:
            problems.append(f"duplicate id: {item_id}")
        seen.add(item_id)
        item_type = str(item.get("type", "unknown"))
        counts[item_type] = counts.get(item_type, 0) + 1
        item_dir = safe_item_dir(args.root, item)
        if not item_dir.is_dir():
            problems.append(f"missing item directory: {item.get('path')}")
            continue
        for kind in ("svg", "tex", "meta"):
            try:
                candidate_file(item_dir, item, kind)
            except SystemExit:
                problems.append(f"{item_id}: missing {kind}")
    if problems:
        emit({"ok": False, "problems": problems})
        raise SystemExit(1)
    emit({"ok": True, "items": len(catalog), "types": counts, "upstream_commit": upstream_commit()})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="OpenTikZ library root")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="rank matching catalog entries")
    search.add_argument("--query", required=True)
    search.add_argument("--type", choices=["any", "icon", "template", "example"], default="any")
    search.add_argument("--domain")
    search.add_argument("--limit", type=int, default=5)
    search.set_defaults(func=command_search)

    info = subparsers.add_parser("info", help="show metadata and available files")
    info.add_argument("--id", required=True)
    info.set_defaults(func=command_info)

    copy = subparsers.add_parser("copy", help="copy an SVG, TikZ source, or metadata file")
    copy.add_argument("--id", required=True)
    copy.add_argument("--format", choices=["svg", "tex", "meta"], default="svg")
    copy.add_argument("--out", type=Path, required=True)
    copy.set_defaults(func=command_copy)

    copy_source = subparsers.add_parser("copy-source", help="copy editable TikZ source")
    copy_source.add_argument("--id", required=True)
    copy_source.add_argument("--out", type=Path, required=True)
    copy_source.set_defaults(func=command_copy_source)

    compile_parser = subparsers.add_parser("compile", help="compile a copied TikZ source to SVG")
    compile_parser.add_argument("--tex", type=Path, required=True)
    compile_parser.add_argument("--out", type=Path, required=True)
    compile_parser.set_defaults(func=command_compile)

    validate = subparsers.add_parser("validate", help="validate the vendored catalog and asset paths")
    validate.set_defaults(func=command_validate)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.root = args.root.resolve()
    args.func(args)


if __name__ == "__main__":
    main()
