# RPM Package (Fedora / openSUSE / RHEL)

## Overview

The `yahac.spec` file in this directory defines an RPM package for Fedora, openSUSE, RHEL, CentOS Stream, and any other RPM-based distribution.

### Version strategy

The `Version:` field in the spec is **updated automatically by the CI workflow** on each release.  
Tag format: `v2026-03-15` → `Version: 2026.03.15` (dashes replaced by dots, `v` stripped).  
The macro `%{tagver}` inside the spec reverses this to reconstruct the source tarball URL.

You never need to manually update the version in the spec file.

---

## Availability note

`python3-pyside6` must be present in the target distro's package manager. Minimum recommended: **Fedora 40+** or **openSUSE Tumbleweed**.

---

## One-time setup — GitHub Releases (recommended, no registration required)

No registration needed. The CI workflow builds an `.rpm` and attaches it to the GitHub Release. Users install it with:

```bash
sudo rpm -i yahac-2026.03.15-1.noarch.rpm
# or
sudo dnf install yahac-2026.03.15-1.noarch.rpm
```

---

## One-time setup — Fedora COPR (optional, for `dnf` integration)

COPR is the equivalent of Ubuntu's PPA — a community build service for RPM packages.

### 1. Create a COPR project

1. Sign up at <https://copr.fedorainfracloud.org> (uses Fedora single sign-on)
2. Create a new project, e.g. `yahac`
3. Under _Settings → Packages_, add a package with **SCM type: git**  
	- Clone URL: `https://github.com/dseichter/yahac`
	- Spec file: `packaging/rpm/yahac.spec`
	- Buildir: `/` (repo root)

### 2. Trigger builds automatically via webhook

In your COPR project under _Settings → Integrations_, copy the GitHub webhook URL and add it to your GitHub repository under _Settings → Webhooks_. COPR will rebuild on every push to the configured branch or tag.

### 3. User installation

```bash
sudo dnf copr enable dseichter/yahac
sudo dnf install yahac
```

---

## One-time setup — openSUSE OBS (optional, cross-distro)

OBS (Open Build Service) can produce packages for Fedora, openSUSE, Debian, and Ubuntu from a single spec:

1. Sign up at <https://build.opensuse.org>
2. Create a home project, e.g. `home:dseichter`
3. Add a package and upload `yahac.spec` plus the source tarball
4. OBS builds automatically for all configured target repos

---

## Automation (GitHub Actions)

The workflow `.github/workflows/rpm.yml` runs on every release tag and:

1. Updates `Version:` in the spec file from the git tag.
2. Builds the `.rpm` inside a Fedora container.
3. Attaches the resulting `.rpm` to the GitHub Release.

*(COPR API rebuild trigger is included in the workflow as an optional step.)*

---

## Manual build

Requires a Fedora/RHEL system or a Fedora container.

```bash
# Install build tools
sudo dnf install rpm-build python3-devel python3-setuptools python3-wheel rpmdevtools

# Set up RPM tree
rpmdev-setuptree

# Copy the spec and download sources
cp packaging/rpm/yahac.spec ~/rpmbuild/SPECS/
spectool -g -R ~/rpmbuild/SPECS/yahac.spec

# Build
rpmbuild -bb ~/rpmbuild/SPECS/yahac.spec

# Find the result
ls ~/rpmbuild/RPMS/noarch/
```
