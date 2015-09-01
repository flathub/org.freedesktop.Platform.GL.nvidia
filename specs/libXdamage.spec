Summary: X Damage extension library
Name: libXdamage
Version: 1.1.4
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: freedesktop-sdk-base
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-dev
BuildRequires: libXfixes-dev

%description
X.Org X11 libXdamage runtime library.

%package dev
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
X.Org X11 libXdamage development package.

%prep
%setup -q

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
%doc AUTHORS COPYING README ChangeLog
%{_libdir}/libXdamage.so.1
%{_libdir}/libXdamage.so.1.1.0

%files dev
%defattr(-,root,root,-)
%{_includedir}/X11/extensions/Xdamage.h
%{_libdir}/libXdamage.so
%{_libdir}/pkgconfig/xdamage.pc

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.1.4-1
- Initial version based on f21
