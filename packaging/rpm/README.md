# RPM Package (Fedora / openSUSE / RHEL)

## Overview

The `packaging/rpm/yahac.spec` file defines the RPM package for YAHAC.

### Version strategy

The `Version:` field in the spec is **updated automatically by CI** on each release package build.
Tag format: `v2026-03-15` → `Version: 2026.03.15` (dashes replaced by dots, `v` stripped).
The macro `%{tagver}` inside the spec reverses this to reconstruct the source tarball URL.

You never need to manually update the version in the spec file.

---

## Availability note

`python3-pyside6` must be available in your target RPM distribution.
Recommended baseline: **Fedora 40+** or **openSUSE Tumbleweed**.

---

## One-time setup — GitHub Releases (recommended)

No registration required. The workflow builds `.rpm` artifacts and attaches them to GitHub Releases.
Users install with:

```bash
sudo rpm -i yahac-2026.03.15-1.noarch.rpm
# or
sudo dnf install yahac-2026.03.15-1.noarch.rpm
```

---

## Automation

The workflow `.github/workflows/rpm.yml` runs on release tags (and on manual dispatch):

1. Resolves the release tag and version.
2. Checks out the tagged source revision.
3. Patches the spec `Version:` field.
4. Downloads the source tarball via `spectool` and builds an `.rpm` in a Fedora container.
5. Attaches the artifact to the GitHub Release.

---

## Manual build

Requires Fedora/RHEL system or container:

```bash
sudo dnf install -y rpm-build python3-devel python3-setuptools python3-wheel rpmdevtools curl
rpmdev-setuptree

cp packaging/rpm/yahac.spec ~/rpmbuild/SPECS/
spectool -g -R ~/rpmbuild/SPECS/yahac.spec
rpmbuild -bb ~/rpmbuild/SPECS/yahac.spec

ls ~/rpmbuild/RPMS/noarch/
```
