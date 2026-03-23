# Version and Dependency Maintenance

This project no longer uses `sync_version.py`.

## Version Updates

Update versions explicitly in packaging files as needed:
- `pyproject.toml`
- `packaging/rpm/yahac.spec`
- `packaging/debian/changelog` (via `dch` in packaging workflow)
- `packaging/aur/PKGBUILD` (updated in workflow)

Release tags (`v*`) drive CI packaging and release automation.

For an AUR packaging-only hotfix without a new upstream release, trigger `.github/workflows/release-orchestrator.yml` manually with the existing tag, `publish_mode=aur-hotfix`, and a bumped `aur_pkgrel`.

## Dependency Updates

Update dependencies where they are consumed:
- Runtime Python dependencies in `pyproject.toml`
- App/runtime dependency list in `src/requirements.txt`
- Distribution-specific dependencies in packaging manifests/spec files
