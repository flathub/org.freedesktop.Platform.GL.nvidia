Summary: X.Org X11 libXrandr runtime library
Name: libXrandr
Version: 1.4.2
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2

Requires: libX11

BuildRequires: freedesktop-sdk-base
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-dev
BuildRequires: libXrender-dev
BuildRequires: libXext-dev
BuildRequires: libX11-dev

%description
X.Org X11 libXrandr runtime library

%package dev
Summary: X.Org X11 libXrandr development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
X.Org X11 libXrandr development package

%prep
%setup -q -n libXrandr-%{version}

%build
autoreconf -v --install --force
%configure  --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_libdir}/libXrandr.so.2
%{_libdir}/libXrandr.so.2.2.0

%files dev
%defattr(-,root,root,-)
%{_includedir}/X11/extensions/Xrandr.h
%{_libdir}/libXrandr.so
%{_libdir}/pkgconfig/xrandr.pc
#%dir %{_mandir}/man3x
%{_mandir}/man3/*.3*

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.4.2-1
- Initial version based on f21
