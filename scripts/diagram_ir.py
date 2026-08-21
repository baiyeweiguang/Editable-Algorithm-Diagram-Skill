#!/usr/bin/env python3
"""Validate Algorithm Diagram Semantic IR and render a coordinate debug SVG."""

from __future__ import annotations

import argparse
import html
import json
import math
import sys
from itertools import combinations
from pathlib import Path
from typing import Any


SCHEMA_PATH = Path(__file__).resolve().parent.parent / "references" / "diagram-ir.schema.json"


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("IR root must be a JSON object")
    return value


def schema_issues(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        import jsonschema
    except ModuleNotFoundError:
        warnings.append("jsonschema is unavailable; running semantic validation only")
        return errors, warnings

    schema = load_json(SCHEMA_PATH)
    validator = jsonschema.Draft202012Validator(schema)
    for issue in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
        location = "/".join(str(x) for x in issue.absolute_path) or "(root)"
        errors.append(f"schema {location}: {issue.message}")
        if len(errors) >= 50:
            errors.append("schema: additional errors omitted")
            break
    return errors, warnings


class Diagram:
    def __init__(self, data: dict[str, Any], ir_path: Path):
        self.data = data
        self.ir_path = ir_path
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.elements_list = data.get("elements", []) if isinstance(data.get("elements", []), list) else []
        self.elements: dict[str, dict[str, Any]] = {}
        self._abs_cache: dict[str, tuple[float, float, float, float]] = {}

    def validate(self) -> tuple[list[str], list[str]]:
        schema_errors, schema_warnings = schema_issues(self.data)
        self.errors.extend(schema_errors)
        self.warnings.extend(schema_warnings)
        self._index_elements()
        self._check_hierarchy()
        self._check_frames_and_assets()
        self._check_ports_and_connectors()
        self._check_constraints()
        self._check_qa_regions()
        self._check_z_order()
        return self.errors, self.warnings

    def _index_elements(self) -> None:
        for index, element in enumerate(self.elements_list):
            if not isinstance(element, dict):
                self.errors.append(f"elements[{index}] is not an object")
                continue
            element_id = element.get("id")
            if not isinstance(element_id, str) or not element_id:
                self.errors.append(f"elements[{index}] has no valid id")
                continue
            if element_id in self.elements:
                self.errors.append(f"duplicate element id: {element_id}")
                continue
            self.elements[element_id] = element

    def _check_hierarchy(self) -> None:
        for element_id, element in self.elements.items():
            parent_id = element.get("parent")
            if parent_id is None:
                continue
            if parent_id == element_id:
                self.errors.append(f"{element_id}: parent cannot reference itself")
                continue
            parent = self.elements.get(parent_id)
            if parent is None:
                self.errors.append(f"{element_id}: unknown parent {parent_id}")
            elif parent.get("kind") != "group":
                self.errors.append(f"{element_id}: parent {parent_id} is not a group")

        for element_id in self.elements:
            seen: set[str] = set()
            current = element_id
            while current in self.elements:
                if current in seen:
                    self.errors.append(f"hierarchy cycle involving {element_id}")
                    break
                seen.add(current)
                parent = self.elements[current].get("parent")
                if not isinstance(parent, str):
                    break
                current = parent

    def absolute_frame(self, element_id: str, stack: set[str] | None = None) -> tuple[float, float, float, float] | None:
        if element_id in self._abs_cache:
            return self._abs_cache[element_id]
        element = self.elements.get(element_id)
        if not element or element.get("kind") == "connector":
            return None
        frame = element.get("frame")
        if not isinstance(frame, dict):
            return None
        try:
            x, y, w, h = (float(frame[k]) for k in ("x", "y", "w", "h"))
        except (KeyError, TypeError, ValueError):
            return None
        stack = set() if stack is None else set(stack)
        if element_id in stack:
            return None
        stack.add(element_id)
        parent_id = element.get("parent")
        if isinstance(parent_id, str):
            parent_frame = self.absolute_frame(parent_id, stack)
            if parent_frame is None:
                return None
            x += parent_frame[0]
            y += parent_frame[1]
        result = (x, y, w, h)
        self._abs_cache[element_id] = result
        return result

    def parent_origin(self, element: dict[str, Any]) -> tuple[float, float]:
        parent_id = element.get("parent")
        if not isinstance(parent_id, str):
            return 0.0, 0.0
        frame = self.absolute_frame(parent_id)
        return (frame[0], frame[1]) if frame else (0.0, 0.0)

    def _check_frames_and_assets(self) -> None:
        canvas = self.data.get("canvas", {})
        try:
            canvas_w = float(canvas["width"])
            canvas_h = float(canvas["height"])
        except (KeyError, TypeError, ValueError):
            self.errors.append("canvas width/height must be numeric")
            return

        assets = self.data.get("assets", {})
        assets = assets if isinstance(assets, dict) else {}
        for asset_id, asset in assets.items():
            if not isinstance(asset, dict):
                continue
            src = asset.get("src")
            if isinstance(src, str) and src and not src.startswith(("http://", "https://", "data:")):
                candidate = (self.ir_path.parent / src).resolve()
                if not candidate.exists():
                    self.warnings.append(f"asset {asset_id}: source does not exist relative to IR: {src}")

        for element_id, element in self.elements.items():
            if element.get("kind") == "connector":
                continue
            frame = self.absolute_frame(element_id)
            if frame is None:
                self.errors.append(f"{element_id}: invalid or unresolved frame")
                continue
            x, y, w, h = frame
            if w <= 0 or h <= 0:
                self.errors.append(f"{element_id}: frame width and height must be positive")
            if element.get("allow_overflow") is not True:
                parent_id = element.get("parent")
                local = element.get("frame", {})
                if isinstance(parent_id, str) and parent_id in self.elements:
                    parent = self.absolute_frame(parent_id)
                    if parent and isinstance(local, dict):
                        lx, ly = float(local.get("x", 0)), float(local.get("y", 0))
                        lw, lh = float(local.get("w", 0)), float(local.get("h", 0))
                        if lx < -1e-6 or ly < -1e-6 or lx + lw > parent[2] + 1e-6 or ly + lh > parent[3] + 1e-6:
                            self.errors.append(f"{element_id}: frame exceeds parent {parent_id}; set allow_overflow only if deliberate")
                elif x < -1e-6 or y < -1e-6 or x + w > canvas_w + 1e-6 or y + h > canvas_h + 1e-6:
                    self.errors.append(f"{element_id}: root frame exceeds canvas")

            if element.get("kind") == "image":
                asset_id = element.get("asset_id")
                if asset_id not in assets:
                    self.errors.append(f"{element_id}: unknown asset_id {asset_id}")
                if element.get("fit") == "stretch":
                    self.warnings.append(f"{element_id}: stretch may distort scientific content")
            if element.get("kind") == "group" and abs(float(element.get("rotation", 0) or 0)) > 1e-9:
                self.warnings.append(f"{element_id}: rotated groups require renderer-specific transform handling")

    def _ports(self, element_id: str) -> dict[str, dict[str, Any]]:
        element = self.elements.get(element_id, {})
        result: dict[str, dict[str, Any]] = {}
        for port in element.get("ports", []) if isinstance(element.get("ports", []), list) else []:
            if not isinstance(port, dict) or not isinstance(port.get("id"), str):
                continue
            port_id = port["id"]
            if port_id in result:
                self.errors.append(f"{element_id}: duplicate port id {port_id}")
            result[port_id] = port
        return result

    def port_point(self, element_id: str, port_id: str) -> tuple[float, float] | None:
        frame = self.absolute_frame(element_id)
        port = self._ports(element_id).get(port_id)
        if frame is None or port is None:
            return None
        x, y, w, h = frame
        if "x" in port and "y" in port:
            return x + float(port["x"]), y + float(port["y"])
        side = port.get("side")
        offset = float(port.get("offset", 0.5))
        if side == "left":
            return x, y + offset * h
        if side == "right":
            return x + w, y + offset * h
        if side == "top":
            return x + offset * w, y
        if side == "bottom":
            return x + offset * w, y + h
        return None

    def connector_points(self, connector: dict[str, Any]) -> list[tuple[float, float]]:
        start_ref = connector.get("from", {})
        end_ref = connector.get("to", {})
        start = self.port_point(str(start_ref.get("element")), str(start_ref.get("port")))
        end = self.port_point(str(end_ref.get("element")), str(end_ref.get("port")))
        if start is None or end is None:
            return []
        ox, oy = self.parent_origin(connector)
        waypoints = []
        for point in connector.get("waypoints", []) if isinstance(connector.get("waypoints", []), list) else []:
            if isinstance(point, dict) and "x" in point and "y" in point:
                waypoints.append((ox + float(point["x"]), oy + float(point["y"])))
        if not waypoints and connector.get("route") == "orthogonal":
            mid_x = (start[0] + end[0]) / 2
            waypoints = [(mid_x, start[1]), (mid_x, end[1])]
        return [start, *waypoints, end]

    def _check_ports_and_connectors(self) -> None:
        for element_id, element in self.elements.items():
            ports = self._ports(element_id)
            frame = element.get("frame", {})
            for port_id, port in ports.items():
                if "x" in port and isinstance(frame, dict):
                    x, y = float(port["x"]), float(port["y"])
                    w, h = float(frame.get("w", 0)), float(frame.get("h", 0))
                    if x < 0 or y < 0 or x > w or y > h:
                        self.warnings.append(f"{element_id}.{port_id}: explicit port lies outside the element frame")

        for connector_id, connector in self.elements.items():
            if connector.get("kind") != "connector":
                continue
            for end_name in ("from", "to"):
                endpoint = connector.get(end_name, {})
                target_id = endpoint.get("element") if isinstance(endpoint, dict) else None
                port_id = endpoint.get("port") if isinstance(endpoint, dict) else None
                target = self.elements.get(target_id) if isinstance(target_id, str) else None
                if target is None:
                    self.errors.append(f"{connector_id}: {end_name} references unknown element {target_id}")
                    continue
                if target.get("kind") not in {"group", "shape"}:
                    self.errors.append(f"{connector_id}: {end_name} target {target_id} cannot own ports")
                    continue
                if port_id not in self._ports(target_id):
                    self.errors.append(f"{connector_id}: {end_name} references unknown port {target_id}.{port_id}")
            if connector.get("route") in {"polyline", "curve"} and not connector.get("waypoints"):
                self.warnings.append(f"{connector_id}: {connector.get('route')} route has no explicit waypoints")
            for avoid_id in connector.get("avoid", []) if isinstance(connector.get("avoid", []), list) else []:
                if avoid_id not in self.elements:
                    self.errors.append(f"{connector_id}: avoid references unknown element {avoid_id}")

    @staticmethod
    def _edge(frame: tuple[float, float, float, float], axis: str) -> float:
        x, y, w, h = frame
        return {
            "left": x,
            "right": x + w,
            "top": y,
            "bottom": y + h,
            "center_x": x + w / 2,
            "center_y": y + h / 2,
        }[axis]

    def _constraint_frames(self, constraint: dict[str, Any]) -> list[tuple[str, tuple[float, float, float, float]]]:
        result = []
        for element_id in constraint.get("items", []) if isinstance(constraint.get("items", []), list) else []:
            frame = self.absolute_frame(element_id)
            if frame is None:
                self.errors.append(f"constraint {constraint.get('kind')}: unknown or frameless item {element_id}")
            else:
                result.append((element_id, frame))
        return result

    def _check_constraints(self) -> None:
        constraints = self.data.get("constraints", [])
        if not isinstance(constraints, list):
            return
        for index, constraint in enumerate(constraints):
            if not isinstance(constraint, dict):
                continue
            kind = constraint.get("kind")
            tolerance = float(constraint.get("tolerance", 1.0))
            frames = self._constraint_frames(constraint)
            label = f"constraint[{index}] {kind}"
            if kind == "align" and len(frames) >= 2:
                axis = constraint.get("axis")
                values = [self._edge(frame, axis) for _, frame in frames]
                if max(values) - min(values) > tolerance:
                    self.errors.append(f"{label}: {axis} differs by {max(values) - min(values):.2f} > {tolerance}")
            elif kind == "equal_gap" and len(frames) >= 3:
                axis = constraint.get("axis")
                gaps = []
                for (_, first), (_, second) in zip(frames, frames[1:]):
                    gaps.append(second[0] - (first[0] + first[2]) if axis == "x" else second[1] - (first[1] + first[3]))
                expected = float(constraint["gap"]) if "gap" in constraint else sum(gaps) / len(gaps)
                if any(abs(gap - expected) > tolerance for gap in gaps):
                    self.errors.append(f"{label}: gaps {', '.join(f'{g:.2f}' for g in gaps)} do not match {expected:.2f}±{tolerance}")
            elif kind == "same_size" and len(frames) >= 2:
                dimension = constraint.get("dimension")
                widths = [frame[2] for _, frame in frames]
                heights = [frame[3] for _, frame in frames]
                if dimension in {"width", "both"} and max(widths) - min(widths) > tolerance:
                    self.errors.append(f"{label}: widths differ by {max(widths) - min(widths):.2f}")
                if dimension in {"height", "both"} and max(heights) - min(heights) > tolerance:
                    self.errors.append(f"{label}: heights differ by {max(heights) - min(heights):.2f}")
            elif kind == "contain":
                container_id = constraint.get("container")
                container = self.absolute_frame(container_id) if isinstance(container_id, str) else None
                if container is None:
                    self.errors.append(f"{label}: unknown container {container_id}")
                    continue
                padding = float(constraint.get("padding", 0))
                cx, cy, cw, ch = container
                for element_id, frame in frames:
                    x, y, w, h = frame
                    if x < cx + padding - tolerance or y < cy + padding - tolerance or x + w > cx + cw - padding + tolerance or y + h > cy + ch - padding + tolerance:
                        self.errors.append(f"{label}: {element_id} is not contained in {container_id} with padding {padding}")
            elif kind == "no_overlap" and len(frames) >= 2:
                gap = float(constraint.get("gap", 0))
                for (first_id, first), (second_id, second) in combinations(frames, 2):
                    fx, fy, fw, fh = first
                    sx, sy, sw, sh = second
                    separated = fx + fw + gap <= sx + tolerance or sx + sw + gap <= fx + tolerance or fy + fh + gap <= sy + tolerance or sy + sh + gap <= fy + tolerance
                    if not separated:
                        self.errors.append(f"{label}: {first_id} overlaps or violates gap with {second_id}")

    def _check_qa_regions(self) -> None:
        for region in self.data.get("qa_regions", []) if isinstance(self.data.get("qa_regions", []), list) else []:
            if not isinstance(region, dict):
                continue
            region_id = region.get("id", "(unnamed)")
            for element_id in region.get("element_ids", []) if isinstance(region.get("element_ids", []), list) else []:
                if element_id not in self.elements:
                    self.errors.append(f"qa_region {region_id}: unknown element {element_id}")

    def _check_z_order(self) -> None:
        siblings: dict[str, dict[int, list[str]]] = {}
        for element_id, element in self.elements.items():
            parent = str(element.get("parent", "__root__"))
            z = element.get("z")
            if isinstance(z, int):
                siblings.setdefault(parent, {}).setdefault(z, []).append(element_id)
        for parent, z_map in siblings.items():
            for z, ids in z_map.items():
                if len(ids) > 1:
                    self.warnings.append(f"siblings under {parent} share z={z}: {', '.join(ids)}")


def print_report(errors: list[str], warnings: list[str], as_json: bool) -> None:
    if as_json:
        print(json.dumps({"ok": not errors, "errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2))
        return
    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}")
    if not errors:
        print(f"OK — {len(warnings)} warning(s)")


def svg_style(element: dict[str, Any], styles: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    ref = element.get("style_ref")
    if isinstance(ref, str) and isinstance(styles.get(ref), dict):
        result.update(styles[ref])
    if isinstance(element.get("style"), dict):
        result.update(element["style"])
    return result


def debug_svg(diagram: Diagram, output: Path, grid: float | None) -> None:
    data = diagram.data
    canvas = data["canvas"]
    width, height = float(canvas["width"]), float(canvas["height"])
    background = canvas.get("background", "#FFFFFF")
    spacing = grid or float(canvas.get("grid", 50))
    styles = data.get("styles", {}) if isinstance(data.get("styles", {}), dict) else {}
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:g}" height="{height:g}" viewBox="0 0 {width:g} {height:g}">',
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#334155"/></marker></defs>',
        f'<rect x="0" y="0" width="{width:g}" height="{height:g}" fill="{html.escape(str(background))}"/>',
    ]
    if spacing > 0:
        x = 0.0
        while x <= width + 1e-6:
            major = math.isclose((x / spacing) % 2, 0, abs_tol=1e-6)
            color = "#CBD5E1" if major else "#E2E8F0"
            parts.append(f'<line x1="{x:g}" y1="0" x2="{x:g}" y2="{height:g}" stroke="{color}" stroke-width="0.7"/>')
            if major:
                parts.append(f'<text x="{x + 3:g}" y="14" font-size="11" fill="#64748B">{x:g}</text>')
            x += spacing
        y = 0.0
        while y <= height + 1e-6:
            major = math.isclose((y / spacing) % 2, 0, abs_tol=1e-6)
            color = "#CBD5E1" if major else "#E2E8F0"
            parts.append(f'<line x1="0" y1="{y:g}" x2="{width:g}" y2="{y:g}" stroke="{color}" stroke-width="0.7"/>')
            if major and y > 0:
                parts.append(f'<text x="3" y="{y - 3:g}" font-size="11" fill="#64748B">{y:g}</text>')
            y += spacing

    for region in data.get("qa_regions", []) if isinstance(data.get("qa_regions", []), list) else []:
        frame = region.get("frame", {}) if isinstance(region, dict) else {}
        if all(key in frame for key in ("x", "y", "w", "h")):
            parts.append(f'<rect x="{frame["x"]}" y="{frame["y"]}" width="{frame["w"]}" height="{frame["h"]}" fill="none" stroke="#A855F7" stroke-width="2" stroke-dasharray="8 5"/>')
            parts.append(f'<text x="{float(frame["x"]) + 5:g}" y="{float(frame["y"]) + 16:g}" font-size="12" fill="#7E22CE">qa:{html.escape(str(region.get("id", "")))}</text>')

    connectors = [e for e in diagram.elements_list if isinstance(e, dict) and e.get("kind") == "connector" and e.get("visible", True)]
    for connector in sorted(connectors, key=lambda e: e.get("z", 0)):
        points = diagram.connector_points(connector)
        if len(points) < 2:
            continue
        style = svg_style(connector, styles)
        stroke = style.get("stroke", "#334155")
        stroke_width = style.get("stroke_width", 2)
        dash = ' stroke-dasharray="8 5"' if style.get("dash") in {"dash", "dash_dot"} else ''
        marker = ' marker-end="url(#arrow)"' if style.get("end_arrow", "triangle") != "none" else ''
        point_text = " ".join(f"{x:g},{y:g}" for x, y in points)
        parts.append(f'<polyline points="{point_text}" fill="none" stroke="{stroke}" stroke-width="{stroke_width}"{dash}{marker}/>')
        mx, my = points[len(points) // 2]
        parts.append(f'<text x="{mx + 4:g}" y="{my - 4:g}" font-size="11" fill="#0F172A">{html.escape(str(connector.get("id", "")))}</text>')

    colors = {"group": "#2563EB", "shape": "#475569", "text": "#16A34A", "image": "#EA580C"}
    boxes = [e for e in diagram.elements_list if isinstance(e, dict) and e.get("kind") != "connector" and e.get("visible", True)]
    for element in sorted(boxes, key=lambda e: (e.get("z", 0), e.get("id", ""))):
        element_id = str(element.get("id", ""))
        frame = diagram.absolute_frame(element_id)
        if frame is None:
            continue
        x, y, w, h = frame
        kind = str(element.get("kind"))
        color = colors.get(kind, "#64748B")
        dash = ' stroke-dasharray="7 4"' if kind in {"group", "text", "image"} else ''
        parts.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="{color}" fill-opacity="0.035" stroke="{color}" stroke-width="1.4"{dash}/>')
        label = element_id
        if kind == "text":
            text_value = str(element.get("text", "")).replace("\n", " ")
            label += f": {text_value[:32]}"
        parts.append(f'<text x="{x + 4:g}" y="{y + 14:g}" font-size="11" fill="{color}">{html.escape(label)}</text>')
        for port_id, port in diagram._ports(element_id).items():
            point = diagram.port_point(element_id, port_id)
            if point:
                px, py = point
                parts.append(f'<circle cx="{px:g}" cy="{py:g}" r="4" fill="#FFFFFF" stroke="#DC2626" stroke-width="1.5"/>')
                parts.append(f'<text x="{px + 6:g}" y="{py - 5:g}" font-size="10" fill="#B91C1C">{html.escape(port_id)}</text>')

    parts.append("</svg>")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(parts) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="validate schema, hierarchy, coordinates, ports, and constraints")
    validate_parser.add_argument("ir", type=Path)
    validate_parser.add_argument("--json", action="store_true", dest="as_json")

    debug_parser = subparsers.add_parser("debug-svg", help="render a coordinate/grid overlay SVG")
    debug_parser.add_argument("ir", type=Path)
    debug_parser.add_argument("-o", "--output", type=Path, required=True)
    debug_parser.add_argument("--grid", type=float, default=None)

    args = parser.parse_args(argv)
    try:
        data = load_json(args.ir)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    diagram = Diagram(data, args.ir.resolve())
    errors, warnings = diagram.validate()
    if args.command == "validate":
        print_report(errors, warnings, args.as_json)
        return 1 if errors else 0

    print_report(errors, warnings, False)
    if errors:
        return 1
    if args.grid is not None and args.grid <= 0:
        print("error: --grid must be positive", file=sys.stderr)
        return 2
    debug_svg(diagram, args.output, args.grid)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
