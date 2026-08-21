# Updating the bundled pptfast integration

Read this reference only when the user explicitly asks to check, update, upgrade, or synchronize pptfast. Do not load or execute this procedure during ordinary algorithm-diagram generation.

## Update policy

- Track released `@liustack/pptfast` versions, not an arbitrary moving `main` snapshot.
- Treat every pre-1.0 minor release as potentially breaking even when IR changes are described as additive.
- Keep the launcher scripts, retained upstream operating guide, lock file, and tested package version from the same release.
- Never replace the working pin until the candidate version passes the compatibility checks below.
- Do not vendor the complete pptfast source tree or `node_modules` into this skill.

## Candidate update procedure

1. Read `pptfast.lock.json` and inspect the official release, package metadata, changelog, agent skill, and launcher scripts.
2. Stage the candidate in an isolated cache or temporary workspace. Do not overwrite the installed working integration.
3. Update candidate copies of:
   - `references/pptfast-upstream-skill.md`;
   - `scripts/pptfast/run.sh`;
   - `scripts/pptfast/run.ps1`;
   - `pptfast.lock.json`.
4. Confirm that the two launchers pin the same version recorded in the lock file and that the recorded Node floor matches the upstream package.
5. Run the compatibility matrix through the candidate launcher:

```bash
pptfast --version
pptfast doctor --json
pptfast schema
pptfast validate <fixture>
pptfast asset-brief <fixture>
pptfast audit <fixture>
pptfast preview <fixture> -o <preview-dir> --html
pptfast render <fixture> -o <candidate.pptx>
```

6. Test at least these representative fixtures: a linear pipeline, a branch/merge diagram, a training-only branch, multiple image assets, transparent PNGs, formulas, and SVG-preview-to-final-SVG replacement.
7. Compare candidate and accepted output for slide count, stable layout with the same seed, missing content, object bounds, asset frames, preview rendering, and final PowerPoint rendering. Do not require byte identity across different pptfast versions.
8. If upstream now accepts external SVG assets through `assets.images`, verify that behavior with a real render before removing the PNG-preview finalization path. Feature-detect; do not assume it from the fact that pptfast internally renders through SVG.
9. Only after all checks pass, replace the working files, validate the skill, save the installed copy, and synchronize any maintained external GitHub copy in the same update operation. Verify the four version-bearing files agree after synchronization.

If a candidate fails, retain the previous pin and report the incompatibility. Do not partially update the upstream guide or one launcher.
