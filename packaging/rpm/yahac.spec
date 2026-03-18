%global tagver %(echo %{version} | tr '.' '-')

Name:           yahac
Version:        2026.03.15
Release:        1%{?dist}
Summary:        Yet Another Home Assistant Client

License:        GPL-3.0-only
URL:            https://github.com/dseichter/yahac
Source0:        %{url}/archive/refs/tags/v%{tagver}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-build
BuildRequires:  python3-installer

Requires:       python3 >= 3.12
Requires:       python3-pyside6
Requires:       python3-urllib3
Requires:       python3-paho-mqtt

%description
Yahac is a desktop application that provides a system tray interface
for Home Assistant. It allows monitoring sensors and controlling
switches directly from the desktop.

%prep
%autosetup -n yahac-%{tagver}

%build
python3 -m build --wheel --no-isolation

%install
python3 -m installer --destdir=%{buildroot} dist/*.whl

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/*.py
%{python3_sitelib}/__pycache__/
%{python3_sitelib}/yahac-*.dist-info/
%{_bindir}/yahac
%{_datadir}/applications/io.github.dseichter.yahac.desktop
%{_datadir}/icons/hicolor/48x48/apps/io.github.dseichter.yahac.png

%changelog
* Sun Mar 15 2026 Daniel Seichter <daniel.seichter@dseichter.de> - 2026.03.15-1
- Build package from source tarball
