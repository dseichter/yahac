# Debian / Ubuntu Package (.deb)

## Overview

The `packaging/debian/` directory contains the standard Debian packaging metadata.  
It produces a binary `.deb` for Debian, Ubuntu, and all their derivatives.

Desktop integration files for YAHAC are provided through the Debian packaging files in this directory,
including `yahac.desktop`.

### Version strategy

The version in `debian/changelog` is **updated automatically by the CI workflow** on each release.  
Tag format: `v2026-03-15` → Debian package version `2026.03.15-1`.

You never need to manually edit the version in `changelog`.

---

## Availability note

`python3-pyside6` must be present in the target distro's apt repositories.  
Minimum recommended versions: **Ubuntu 24.04 (Noble)** or **Debian 13 (Trixie)**.

---

## One-time setup — GitHub Releases (recommended, no registration required)

No registration is needed. The CI workflow builds a `.deb` and attaches it to the GitHub Release automatically. Users install it with:

```bash
sudo dpkg -i yahac_2026.03.15-1_all.deb
sudo apt-get install -f   # resolve any missing dependencies
```

---

## One-time setup — Ubuntu PPA (optional, for `apt` integration)

A PPA lets users add a single apt source and receive updates via `apt upgrade`.

### 1. Create a Launchpad account and PPA

1. Sign up at <https://launchpad.net>
2. Upload your GPG key to Launchpad
3. Create a new PPA: _My PPAs → Create a new PPA_

### 2. Configure GitHub Actions secrets

| Secret | Value |
|---|---|
| `LAUNCHPAD_GPG_PRIVATE_KEY` | ASCII-armored GPG private key (base64-encoded) |
| `LAUNCHPAD_GPG_PASSPHRASE` | Passphrase for the GPG key |
| `LAUNCHPAD_EMAIL` | Email address associated with the GPG key on Launchpad |

### 3. User installation

```bash
sudo add-apt-repository ppa:dseichter/yahac
sudo apt update
sudo apt install yahac
```

---

## Automation

The GitHub Actions workflow `.github/workflows/deb.yml` runs on every release tag and:

1. Updates `debian/changelog` with the new version and date (`dch`).
2. Builds a binary `.deb` (`dpkg-buildpackage -b -us -uc`).
3. Attaches the `.deb` to the GitHub Release as a downloadable asset.

*(PPA upload via `dput` is described in the workflow file as an optional step.)*

---

## Manual build

Requires a Debian/Ubuntu system with build tools installed.

```bash
# Install build dependencies
sudo apt-get install debhelper dh-python python3-all python3-setuptools devscripts

# From the repo root: copy debian/ metadata into place and build
cp -r packaging/debian debian/
chmod +x debian/rules
dpkg-buildpackage -b -us -uc

# The .deb appears in the parent directory
ls ../*.deb
```
