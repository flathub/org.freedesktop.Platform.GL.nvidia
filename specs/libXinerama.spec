Summary: X.Org X11 libXinerama runtime library
Name: libXinerama
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
X.Org X11 libXinerama runtime library

%package dev
Summary: X.Org X11 libXinerama development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
X.Org X11 libXinerama development package

%prep
%setup -q -n libXinerama-%{version}

%build
autoreconf -v --install --force

%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libXinerama.so.1
%{_libdir}/libXinerama.so.1.0.0

%files dev
%defattr(-,root,root,-)
%{_libdir}/libXinerama.so
%{_libdir}/pkgconfig/xinerama.pc
%{_mandir}/man3/*.3*
%{_includedir}/X11/extensions/Xinerama.h
%{_includedir}/X11/extensions/panoramiXext.h

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.1.3-1
- Initial version based on f21
