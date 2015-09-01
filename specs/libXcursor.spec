Summary: Cursor management library
Name: libXcursor
Version: 1.1.14
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2
Source1: index.theme

Requires: libX11

BuildRequires: freedesktop-sdk-base
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-dev
BuildRequires: libX11-dev
BuildRequires: libXfixes-dev
BuildRequires: libXrender-dev

%description
This is  a simple library designed to help locate and load cursors.
Cursors can be loaded from files or memory. A library of common cursors
exists which map to the standard X cursor names.Cursors can exist in
several sizes and the library automatically picks the best size.

%package dev
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
libXcursor development package.

%prep
%setup -q -n libXcursor-%{version}
iconv --from=ISO-8859-2 --to=UTF-8 COPYING > COPYING.new && \
touch -r COPYING COPYING.new && \
mv COPYING.new COPYING

# Disable static library creation by default.
%define with_static 0

%build
autoreconf -v --install --force
#export CFLAGS="$RPM_OPT_FLAGS -DICONDIR=\"%{_datadir}/icons\""
%configure \
%if ! %{with_static}
 --disable-static
%endif
make V=1 %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/default
install -m 644 -p %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/icons/default/index.theme

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/libXcursor.so.1
%{_libdir}/libXcursor.so.1.0.2
%dir %{_datadir}/icons/default
%{_datadir}/icons/default/index.theme

%files dev
%defattr(-,root,root,-)
%dir %{_includedir}/X11/Xcursor
%{_includedir}/X11/Xcursor/Xcursor.h
%if %{with_static}
%{_libdir}/libXcursor.a
%endif
%{_libdir}/libXcursor.so
%{_libdir}/pkgconfig/xcursor.pc
#%dir %{_mandir}/man3x
%{_mandir}/man3/Xcursor*.3*

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.1.14-1
- Initial version based on f21
