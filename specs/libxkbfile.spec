Summary: X.Org X11 libxkbfile runtime library
Name: libxkbfile
Version: 1.0.8
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: freedesktop-sdk-base
BuildRequires: xorg-x11-proto-dev
BuildRequires: libX11-dev

%description
X.Org X11 libxkbfile runtime library

%package dev
Summary: X.Org X11 libxkbfile development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
X.Org X11 libxkbfile development package

%prep
%setup -q

%build
# FIXME: We use -fno-strict-aliasing, to work around the following bug:
# maprules.c:1373: warning: dereferencing type-punned pointer will break strict-aliasing rules)
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
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
%doc COPYING ChangeLog
%{_libdir}/libxkbfile.so.1
%{_libdir}/libxkbfile.so.1.0.2

%files dev
%defattr(-,root,root,-)
%{_includedir}/X11/extensions/XKBbells.h
%{_includedir}/X11/extensions/XKBconfig.h
%{_includedir}/X11/extensions/XKBfile.h
%{_includedir}/X11/extensions/XKBrules.h
%{_includedir}/X11/extensions/XKM.h
%{_includedir}/X11/extensions/XKMformat.h
%{_libdir}/libxkbfile.so
%{_libdir}/pkgconfig/xkbfile.pc

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.0.8-1
- Initial version based on f21
