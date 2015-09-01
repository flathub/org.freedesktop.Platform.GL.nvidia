Summary: X Fixes library
Name: libXfixes
Version: 5.0.1
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2

Requires: libX11 >= 1.5.99.902

BuildRequires: freedesktop-sdk-base
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-dev
BuildRequires: libX11-dev

%description
X Fixes library.

%package dev
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
libXfixes development package

%prep
%setup -q -n libXfixes-%{version}

%build
autoreconf -v --install --force
%configure --disable-static
make V=1 %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/libXfixes.so.3
%{_libdir}/libXfixes.so.3.1.0

%files dev
%defattr(-,root,root,-)
%{_includedir}/X11/extensions/Xfixes.h
%{_libdir}/libXfixes.so
%{_libdir}/pkgconfig/xfixes.pc
%{_mandir}/man3/Xfixes.3*

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 5.0.1-1
- Initial version based on f21
