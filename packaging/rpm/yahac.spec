Name:           yahac
Version:        0.5.0
Release:        1%{?dist}
Summary:        Yet Another Home Assistant Client

License:        GPL-3.0-only
URL:            https://github.com/dseichter/yahac
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel

Requires:       python3 >= 3.12
Requires:       python3-pyside6
Requires:       python3-urllib3
Requires:       python3-paho-mqtt

%description
Yahac is a desktop application that provides a system tray interface
for Home Assistant. It allows monitoring sensors and controlling
switches directly from the desktop.

%prep
%autosetup -n yahac-%{version}

%build
%py3_build

%install
%py3_install
install -Dpm0644 packaging/debian/yahac.desktop %{buildroot}%{_datadir}/applications/yahac.desktop

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/*.py
%{python3_sitelib}/__pycache__/
%{python3_sitelib}/*.egg-info/
%{_bindir}/yahac
%{_datadir}/applications/yahac.desktop

%changelog
* Sat Mar 14 2026 Daniel Seichter <daniel.seichter@dseichter.de> - 0.5.0-1
- Build package from source tarball
