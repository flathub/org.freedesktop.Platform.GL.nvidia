Summary: X Composite Extension library
Name: libXcomposite
Version: 0.4.4
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: freedesktop-sdk-base
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-dev
BuildRequires: libXfixes-dev
BuildRequires: libXext-dev

%description
X Composite Extension library

%package dev
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
X.Org X11 libXcomposite development package

%prep
%setup -q

%build
autoreconf -v --install --force
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ChangeLog
%{_libdir}/libXcomposite.so.1
%{_libdir}/libXcomposite.so.1.0.0

%files dev
%defattr(-,root,root,-)
%{_includedir}/X11/extensions/Xcomposite.h
%{_libdir}/libXcomposite.so
%{_libdir}/pkgconfig/xcomposite.pc
%{_mandir}/man3/X?omposite*.3*

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 0.4.4-1
- Initial version based on f21
