Summary: X.Org X11 libXtst runtime library
Name: libXtst
Version: 1.2.2
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
BuildRequires: libXi-dev

%description
X.Org X11 libXtst runtime library

%package dev
Summary: X.Org X11 libXtst development package
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libXi-dev%{?_isa}

%description dev
X.Org X11 libXtst development package

%prep
%setup -q -n libXtst-%{version}

%build
autoreconf -v --install --force

%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

rm -rf $RPM_BUILD_ROOT%{_docdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libXtst.so.6
%{_libdir}/libXtst.so.6.1.0

%files dev
%defattr(-,root,root,-)
%{_includedir}/X11/extensions/XTest.h
%{_includedir}/X11/extensions/record.h
%{_libdir}/libXtst.so
%{_libdir}/pkgconfig/xtst.pc
%{_mandir}/man3/XTest*.3*

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.2.2-1
- Initial version based on f21
