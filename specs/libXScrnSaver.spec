Summary: X.Org X11 libXss runtime library
Name: libXScrnSaver
Version: 1.2.2
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: freedesktop-sdk-base
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-dev
BuildRequires: libX11-dev
BuildRequires: libXext-dev

%description
X.Org X11 libXss runtime library

%package dev
Summary: X.Org X11 libXScrnSaver development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
X.Org X11 libXss development package

%prep
%setup -q

%build
autoreconf -v --install --force
# FIXME: XScrnSaver.c:429: warning: dereferencing type-punned pointer will break strict-aliasing rules
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README ChangeLog
%{_libdir}/libXss.so.1
%{_libdir}/libXss.so.1.0.0

%files dev
%defattr(-,root,root,-)
%{_libdir}/libXss.so
%{_libdir}/pkgconfig/xscrnsaver.pc
%{_mandir}/man3/*.3*
%{_includedir}/X11/extensions/scrnsaver.h

%changelog
* Thu Feb 12 2015 Alexander Larsson <alexl@redhat.com> - 1.2.2-1
- Initial version

