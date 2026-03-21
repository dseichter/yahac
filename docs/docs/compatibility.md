# Compatibility

## Home Assistant

yahac is compatible with [Home Assistant](https://www.home-assistant.io/) 2025.x.

## Operating System

### Windows

| Operation System | Supported | Special notes |
| ---------------- | --------- | ------------- |
| Windows 11       | ✅       | Windows Defender reports false positive |
| Windows 10       | ✅       | Windows Defender reports false positive |

!!! warning
    Please whitelist yahac within Windows Defender to ensure, yahac is running. With [#34](https://github.com/dseichter/yahac/issues/34) I am working on a solution.

### Linux

YAHAC supports multiple Linux distributions through native packages, portable binaries, and AppImage.

## Package Support

### Debian-based Distributions
| Distribution | Version | Package Type | Status |
| ------------ | ------- | ------------ | ------ |
| Debian | 12 (Bookworm) | .deb | ✅ |
| Ubuntu | 22.04 LTS (Jammy) | .deb | ✅ |
| Ubuntu | 24.04 LTS (Noble) | .deb | ✅ |
| Linux Mint | 21.x | .deb | ✅ |
| Linux Mint | 22.x | .deb | ✅ |

### Arch-based Distributions
| Distribution | Package Type | Status |
| ------------ | ------------ | ------ |
| Arch Linux | AUR | ✅ |
| Manjaro | AUR | ✅ |
| EndeavourOS | AUR | ✅ |
| ArcoLinux | AUR | ✅ |

## Desktop Environment Compatibility

| Distribution | Desktop Environment | Binary Support | Package Support | Special notes |
| ------------ | ------------------- | :------------: | :-------------: | ------------- |
| Ubuntu 24.04 | GNOME | ❌ | ✅ | GNOME needs extension for tray |
| Ubuntu 24.04 | KDE Plasma | ✅ | ✅ | |
| Ubuntu 24.04 | Cinnamon | ✅ | ✅ | |
| Ubuntu 24.04 | XFCE | ✅ | ✅ | |
| Manjaro | KDE Plasma | ✅ | ✅ | |
| Manjaro | XFCE | ✅ | ✅ | |
| Debian 12 | GNOME | ❌ | ✅ | GNOME needs extension for tray |
| Debian 12 | KDE Plasma | ✅ | ✅ | |

!!! tip "GNOME Users"
    Install the "AppIndicator and KStatusNotifierItem Support" extension to enable system tray functionality.

!!! note "Package vs Binary"
    - **Packages**: Automatic dependency resolution, system integration, desktop files
    - **Binaries/AppImage**: Portable, no installation required, manual dependency management

## Installation Methods by Distribution

### Recommended Installation
- **Debian/Ubuntu/Mint**: Use `.deb` packages for best integration
- **Arch/Manjaro**: Use AUR (`yay -S yahac-bin`)
- **Other distributions**: Use AppImage first, then portable binaries or build from source

If you test yahac on other distributions, please report compatibility at [#36](https://github.com/dseichter/yahac/issues/36).
