# Version and Dependency Sync

## Automatic Sync

The project uses `sync_version.py` to keep versions and dependencies synchronized across:
- `src/helper.py` (source of truth for version)
- `setup.py` (Python package metadata)
- `PKGBUILD` (Arch Linux package)
- `src/requirements.txt` (source of truth for dependencies)

### Pre-commit Hook

A git pre-commit hook automatically runs the sync script before each commit:

```bash
git config core.hooksPath .githooks
```

This is already configured if you cloned the repository.

## Manual Sync

Run the sync script manually:

```bash
python3 sync_version.py
```

## Updating Version

1. Update `VERSION` in `src/helper.py`
2. Run `python3 sync_version.py` (or commit and the hook runs automatically)
3. All files are updated automatically

## Updating Dependencies

1. Update `src/requirements.txt`
2. Run `python3 sync_version.py` (or commit and the hook runs automatically)
3. `setup.py` is updated automatically
