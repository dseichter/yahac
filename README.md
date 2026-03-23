# YAHAC - Yet Another Home Assistant Client

**Desktop system tray client for Home Assistant** - Monitor sensors and control switches directly from your desktop. Cross-platform support for Windows and Linux with native packaging.

<p align="center">
  <img src="icons/home_app_logo_48dp_1976D2_FILL0_wght400_GRAD0_opsz48.png" alt="YAHAC Logo"/>
</p>

<p align="center">
  <img src="https://img.shields.io/github/v/release/dseichter/yahac?style=flat-square" alt="Release">
  <img src="https://img.shields.io/github/downloads/dseichter/yahac/total?style=flat-square" alt="Downloads">
  <img src="https://img.shields.io/github/license/dseichter/yahac?style=flat-square" alt="License">
</p>

<p align="center">
  <b><a href="https://dseichter.github.io/yahac/">Documentation</a></b> •
  <b><a href="https://github.com/dseichter/yahac/releases">Downloads</a></b> •
  <b><a href="https://github.com/dseichter/yahac/issues">Issues</a></b>
</p>

<p align="center">
<img src="https://github.com/dseichter/yahac/actions/workflows/ruff.yml/badge.svg" alt="ruff">
<img src="https://github.com/dseichter/yahac/actions/workflows/bandit.yml/badge.svg" alt="bandit">
<img src="https://github.com/dseichter/yahac/actions/workflows/trivy.yml/badge.svg" alt="trivy">
<a href="https://sonarcloud.io/summary/new_code?id=dseichter_yahac"><img src="https://sonarcloud.io/api/project_badges/measure?project=dseichter_yahac&metric=alert_status" alt="Quality Gate Status"></a>
</p>

---

![yahac in tray Icon](docs/docs/assets/screenshots/yahac_traymenu_with_entities.png)

## ✨ Features

- 📊 **Real-time sensor monitoring** - View current values/states
- 🔄 **One-click switch control** - Toggle switches instantly
- 💻 **Computer integration** - Register as HA binary sensor via MQTT
- 📦 **Linux distributions** - Debian/Ubuntu (.deb), Arch Linux (AUR), RPM (.rpm), and AppImage
- 🚀 **Portable binaries** - No installation required
- 🎨 **System tray integration** - Minimal desktop footprint

## 🚀 Quick Start

### Linux Package Installation (Recommended)
```bash
# Debian/Ubuntu/Mint - auto-installs dependencies
sudo apt install ./yahac-*.deb

# Arch/Manjaro (AUR)
yay -S yahac-bin

# Fedora/openSUSE/RHEL (RPM-based)
sudo rpm -i yahac-*.rpm
```

### Linux AppImage (Portable)
1. Download `yahac-appimage-v*-x86_64.AppImage` from [**Releases**](https://github.com/dseichter/yahac/releases)
2. Make executable: `chmod +x yahac-appimage-v*-x86_64.AppImage`
3. Run: `./yahac-appimage-v*-x86_64.AppImage`

### Portable Binaries
1. Download from [**Releases**](https://github.com/dseichter/yahac/releases)
2. Make executable: `chmod +x yahac-linux-x86_64-v*`
3. Run: `./yahac-linux-x86_64-v*`

### Dependencies
- **Qt6**: `python3-pyside6` (Debian) / `pyside6` (Arch)
- **MQTT**: `python3-paho-mqtt` (Debian) / `python-paho-mqtt` (Arch)
- **HTTP**: `python3-urllib3` (Debian) / `python-urllib3` (Arch)
- **HA MQTT discovery**: `python3-ha-mqtt-discoverable` (Debian) / `python-ha-mqtt-discoverable` (Arch)

## Release packaging checklist (Linux)

This repository publishes Linux artifacts via GitHub Actions:

- Binary release workflow: `.github/workflows/release.yml`
- Release orchestrator: `.github/workflows/release-orchestrator.yml`
- AppImage workflow: `.github/workflows/appimage.yml`
- AUR publish workflow: `.github/workflows/aur.yml`
- Debian package workflow: `.github/workflows/deb.yml`
- RPM package workflow: `.github/workflows/rpm.yml`

For an AUR packaging-only hotfix of an existing release, run `.github/workflows/release-orchestrator.yml` manually with `publish_mode=aur-hotfix`, the existing `release_tag`, and an incremented `aur_pkgrel` such as `2`.

Before creating a release tag, verify:

1. Tray icon and screenshots are up to date.
2. Linux binaries (`linux-x86_64` and `archlinux-x86_64`) start correctly.
3. Debian and RPM source packaging workflows run successfully for the target tag.
4. Packaging metadata under `packaging/` is synchronized with current dependencies.

> [!NOTE]  
> Windows Defender may flag the executable as false positive ([#34](https://github.com/dseichter/yahac/issues/34)). See [compatibility guide](https://dseichter.github.io/yahac/compatibility/) for details.

## 🏠 About Home Assistant

Open source home automation that puts local control and privacy first.  
**Learn more**: [home-assistant.io](https://www.home-assistant.io/)

## 📄 License & Credits

- **License**: GPL-3.0 - see [LICENSE](LICENSE)
- **Icons**: [Google Material Symbols](https://fonts.google.com/icons) ([Apache 2.0](https://github.com/google/material-design-icons/blob/master/LICENSE))
- **Framework**: Built with Qt6 (PySide6) for cross-platform compatibility
