Summary: X.Org X11 libXxf86vm runtime library
Name: libXxf86vm
Version: 1.1.3
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2

Requires: libX11

BuildRequires: freedesktop-sdk-base
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-dev
BuildRequires: libX11-dev
BuildRequires: libXext-dev

%description
X.Org X11 libXxf86vm runtime library

%package dev
Summary: X.Org X11 libXxf86vm development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
X.Org X11 libXxf86vm development package

%prep
%setup -q -n libXxf86vm-%{version}

%build
autoreconf -v --install --force
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README COPYING
%{_libdir}/libXxf86vm.so.1
%{_libdir}/libXxf86vm.so.1.0.0

%files dev
%defattr(-,root,root,-)
%{_libdir}/libXxf86vm.so
%{_libdir}/pkgconfig/xxf86vm.pc
%{_mandir}/man3/*.3*
%{_includedir}/X11/extensions/xf86vmode.h

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.1.3-1
- Initial version based on f21
