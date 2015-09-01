Summary: X.Org X11 libXpm runtime library
Name: libXpm
Version: 3.5.11
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: freedesktop-sdk-base
BuildRequires: xorg-x11-util-macros
BuildRequires: libXt-dev
BuildRequires: libXext-dev
BuildRequires: libXau-dev

%description
X.Org X11 libXpm runtime library

%package dev
Summary: X.Org X11 libXpm development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
X.Org X11 libXpm development package

%prep
%setup -q

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
%doc AUTHORS COPYING ChangeLog
%{_libdir}/libXpm.so.4
%{_libdir}/libXpm.so.4.11.0

%files dev
%defattr(-,root,root,-)
%{_bindir}/cxpm
%{_bindir}/sxpm
%{_includedir}/X11/xpm.h
%{_libdir}/libXpm.so
%{_libdir}/pkgconfig/xpm.pc
#%dir %{_mandir}/man1x
%{_mandir}/man1/*.1*
#%{_mandir}/man1/*.1x*

%changelog
* Thu Feb 12 2015 Alexander Larsson <alexl@redhat.com> - 3.5.11-1
- Initial version
