Name:           wayland-protocols
Version:        1.0
Release:        1%{?dist}
Summary:        Wayland protocols that adds functionality not available in the core protocol

License:        MIT
URL:            http://wayland.freedesktop.org/
Source0:        http://wayland.freedesktop.org/releases/%{name}-%{version}.tar.xz

BuildArch:      noarch
BuildRequires: freedesktop-sdk-base

%description
wayland-protocols contains Wayland protocols that adds functionality not
available in the Wayland core protocol. Such protocols either adds
completely new functionality, or extends the functionality of some other
protocol either in Wayland core, or some other protocol in
wayland-protocols.

%package dev
Summary:        Wayland protocols that adds functionality not available in the core protocol

%description dev
wayland-protocols contains Wayland protocols that adds functionality not
available in the Wayland core protocol. Such protocols either adds
completely new functionality, or extends the functionality of some other
protocol either in Wayland core, or some other protocol in
wayland-protocols.

%prep
%setup -q -n %{name}-%{version}

%build
%configure

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files dev
%license COPYING
%doc README
%{_datadir}/pkgconfig/%{name}.pc
%{_datadir}/%{name}/

%changelog
* Wed Jan 20 2016 Alexander Larsson <alexl@redhat.com>
- Initial version
