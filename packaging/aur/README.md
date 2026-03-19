# AUR Package (Arch Linux)

## Overview

The `PKGBUILD` in this directory defines the Arch Linux User Repository (AUR) package for YAHAC (`yahac-bin`).

## Package variants

- `yahac` (source): builds from source and uses Arch/Python system dependencies.
- `yahac-bin` (binary): installs prebuilt release binaries and is recommended when source dependencies are unavailable in Arch repos.

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
git clone ssh://aur@aur.archlinux.org/yahac-bin.git aur-yahac-bin
cp packaging/aur/PKGBUILD aur-yahac-bin/
cd aur-yahac-bin
git switch -c master
makepkg --printsrcinfo > .SRCINFO
git add PKGBUILD .SRCINFO
git commit -m "Initial release"
git push -u origin master
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

After the one-time setup, the GitHub Actions workflow `.github/workflows/aur.yml` handles everything automatically when you push a tag:

1. Computes the new `pkgver` from the tag.
2. Downloads the prebuilt Linux binary release asset and computes its `sha256sum`.
3. Patches `PKGBUILD` with the new version and checksum.
4. Pushes the updated `PKGBUILD` + `.SRCINFO` to AUR.

---

## Manual release (without CI)

```bash
cd packaging/aur

# Update version and checksum manually
PKGVER="2026.03.15"
sed -i "s/^pkgver=.*/pkgver=$PKGVER/" PKGBUILD
SHA256=$(curl -fsSL "https://github.com/dseichter/yahac/releases/download/v${PKGVER//./-}/yahac-ubuntu-24-04-v${PKGVER//./-}" | sha256sum | cut -d' ' -f1)
sed -i "s/^sha256sums=.*/sha256sums=('$SHA256' 'SKIP' 'SKIP')/" PKGBUILD

# Test the build locally (requires an Arch Linux machine or container)
makepkg -si

# Push to AUR
makepkg --printsrcinfo > .SRCINFO
# Then copy PKGBUILD + .SRCINFO to your local AUR clone and push
```
