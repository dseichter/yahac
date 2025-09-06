# Compatibility

## Home Assistant

yahac is compatible with [Home Assistant](https://www.home-assistant.io/) 2025.x.

## Operating System

### Windows

| Operation System | Supported | Special notes |
| ---------------- | --------- | ------------- |
| Windows 11       | ✅       | Windows Defender reports false positive |
| Windows 10       | ✅       | Windows Defender reports false positive |

Please whitelist yahac within Windows Defender to ensure, yahac is running. With [#34](https://github.com/dseichter/yahac/issues/34) I am working on a solution.

### Linux

Linux is my favorite operating system, but providing a binary release needs a little bit more work and testing.
My goal is to provide a running binary for every distribution, I am able to test (see [#36](https://github.com/dseichter/yahac/issues/36)).

The name of the binaries will match the corresponding Linux Distribution, like yahac-ubuntu-25-04-v0.1.2, which is tested on Ubuntu 25.04.

| Distribution   | Desktop Environment | Supported | [yahac release](https://github.com/dseichter/yahac/releases) | Special notes                       |
| -------------- | ------------------- | :-------: | ---------------- | ----------------------------------- |
| Ubuntu 24.04   | GNOME               | ❌        | -               | GNOME itself provides no Tray Menu |
| Ubuntu 24.04   | Cinnamon Desktop    | ✅        | 0.1.2           |                                    |
| Ubuntu 25.04   | GNOME               | ❌        | -               | GNOME itself provides no Tray Menu |
| Ubuntu 25.04   | Cinnamon Desktop    | ✅        | 0.1.2           |                                    |
| Manjaro (Arch) | XFCE                | ✅        | 0.1.2           | use ubuntu 25.04 version, but see [#38](https://github.com/dseichter/yahac/issues/38) |
| Manjaro (Arch) | KDE                 | ✅        | 0.1.2           | use ubuntu 25.04 version, but see [#38](https://github.com/dseichter/yahac/issues/38) |

If you are able to test yahac on other distributions, please provide the information to [#36](https://github.com/dseichter/yahac/issues/36).
The added yahac release provides the information, since the environment is supported.
