Summary: X.Org X11 libXv runtime library
Name:    libXv
Version: 1.0.10
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2

Requires: libX11

BuildRequires: freedesktop-sdk-base
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-dev
BuildRequires: libXext-dev
BuildRequires: libX11-dev

%description
X.Org X11 libXv runtime library

%package dev
Summary: X.Org X11 libXv development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
X.Org X11 libXv development package

%prep
%setup -q -n libXv-%{version}

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
%doc AUTHORS COPYING
%{_libdir}/libXv.so.1
%{_libdir}/libXv.so.1.0.0

%files dev
%defattr(-,root,root,-)
%doc man/xv-library-v2.2.txt
%{_includedir}/X11/extensions/Xvlib.h
%{_libdir}/libXv.so
%{_libdir}/pkgconfig/xv.pc
#%dir %{_mandir}/man3x
%{_mandir}/man3/*.3*

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.0.10-1
- Initial version based on f21
