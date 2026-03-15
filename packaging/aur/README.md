# AUR Package (Arch Linux)

## Overview

The `PKGBUILD` in this directory defines the Arch Linux User Repository (AUR) package for YAHAC.

### Version strategy

The `pkgver` field is **automatically derived from the git tag** by the CI workflow.
Tag format: `v2026-03-15` → `pkgver=2026.03.15` (dashes replaced by dots, `v` prefix stripped).
The reverse conversion (`${pkgver//./-}`) reconstructs the original tag for the source URL.

You never need to manually update the version in `PKGBUILD`.

---

## One-time setup

### 1. Create an AUR account

Sign up at <https://aur.archlinux.org>.

### 2. Add an SSH key

Generate a key (if you don't have one) and add the **public key** to your AUR account under
_My Account → SSH Public Key_.

### 3. Register the package on AUR

The first time, clone the (empty) AUR repo for your package name:

```bash
git clone ssh://aur@aur.archlinux.org/yahac.git aur-yahac
cp packaging/aur/PKGBUILD aur-yahac/
cd aur-yahac
makepkg --printsrcinfo > .SRCINFO
git add PKGBUILD .SRCINFO
git commit -m "Initial release"
git push
```

### 4. Configure GitHub Actions secrets

Add the following secrets to your GitHub repository (_Settings → Secrets and variables → Actions_):

| Secret | Value |
|---|---|
| `AUR_SSH_PRIVATE_KEY` | The private SSH key paired with the public key on AUR |
| `AUR_USERNAME` | Your AUR username |
| `AUR_EMAIL` | Your AUR email address |

---

## Automation

The workflow `.github/workflows/aur.yml` handles AUR publishing on release tags:

1. Computes `pkgver` from the tag.
2. Downloads the source tarball and computes its `sha256sum`.
3. Patches `PKGBUILD` with version and checksum.
4. Pushes the update to AUR.

---

## Manual release (without CI)

```bash
cd packaging/aur

PKGVER="2026.03.15"
sed -i "s/^pkgver=.*/pkgver=$PKGVER/" PKGBUILD
SHA256=$(curl -fsSL "https://github.com/dseichter/yahac/archive/refs/tags/v${PKGVER//./-}.tar.gz" | sha256sum | cut -d' ' -f1)
sed -i "s/^sha256sums=.*/sha256sums=('$SHA256')/" PKGBUILD

makepkg -si
makepkg --printsrcinfo > .SRCINFO
```
