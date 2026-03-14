# Debian / Ubuntu Package (.deb)

## Overview

The `packaging/debian/` directory contains Debian packaging metadata for YAHAC.
The workflow builds binary `.deb` packages for Debian, Ubuntu, and derivatives.

### Version strategy

The version in `debian/changelog` is **updated automatically by CI** on each release package build.
Tag format: `v0.5.0` → package version `0.5.0-1`.

You never need to manually edit the version in `changelog`.

---

## Availability note

`python3-pyside6` must be available in the target distro repository.
Recommended baseline: **Ubuntu 24.04** or **Debian 13**.

---

## One-time setup — GitHub Releases (recommended)

No registration is needed. The workflow builds `.deb` files and attaches them to the GitHub Release.
Users install with:

```bash
sudo apt install ./yahac_0.5.0-1_amd64.deb
```

---

## Automation

The workflow `.github/workflows/debian.yml` runs on release tags (and on manual dispatch):

1. Checks out the tagged source revision.
2. Copies `packaging/debian/` to `debian/`.
3. Updates `debian/changelog` with `dch`.
4. Builds `.deb` packages from source and uploads them.
5. Attaches `.deb` artifacts to the GitHub Release.

---

## Manual build

Requires Debian/Ubuntu with build tools:

```bash
sudo apt-get update
sudo apt-get install -y devscripts debhelper dh-python python3-all python3-setuptools python3-wheel fakeroot

cp -r packaging/debian debian
chmod +x debian/rules
dpkg-buildpackage -b -us -uc -rfakeroot

ls ../*.deb
```
