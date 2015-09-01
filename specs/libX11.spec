Summary: Core X11 protocol client library
Name: libX11
Version: 1.6.2
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2

Patch0: 0001-Fix-XNextRequest-after-direct-usage-of-XCB.patch
Patch2: dont-forward-keycode-0.patch
BuildRequires: freedesktop-sdk-base
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-dev
BuildRequires: xorg-x11-xtrans-dev
BuildRequires: libxcb-dev
BuildRequires: libXau-dev libXdmcp-dev

Requires: %{name}-common >= %{version}-%{release}

%description
Core X11 protocol client library.

%package common
Summary: Common data for libX11
Group: System Environment/Libraries
BuildArch: noarch

%description common
libX11 common data

%package dev
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
X.Org X11 libX11 development package

%prep
%setup -q -n libX11-%{version}
%patch0 -p1 -b .xcb
%patch2 -p1 -b .dont-forward-keycode-0

%build
# sodding libtool
autoreconf -v --install --force
%configure --disable-static

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# We intentionally don't ship *.la files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

# FIXME: Don't install Xcms.txt - find out why upstream still ships this.
find $RPM_BUILD_ROOT -name 'Xcms.txt' -delete

# FIXME package these properly
rm -rf $RPM_BUILD_ROOT%{_docdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libX11.so.6
%{_libdir}/libX11.so.6.3.0
%{_libdir}/libX11-xcb.so.1
%{_libdir}/libX11-xcb.so.1.0.0

%files common
%defattr(-,root,root,-)
%doc AUTHORS COPYING README NEWS
%{_datadir}/X11/locale/
%{_datadir}/X11/XErrorDB

%files dev
%defattr(-,root,root,-)
%{_includedir}/X11/ImUtil.h
%{_includedir}/X11/XKBlib.h
%{_includedir}/X11/Xcms.h
%{_includedir}/X11/Xlib.h
%{_includedir}/X11/XlibConf.h
%{_includedir}/X11/Xlibint.h
%{_includedir}/X11/Xlib-xcb.h
%{_includedir}/X11/Xlocale.h
%{_includedir}/X11/Xregion.h
%{_includedir}/X11/Xresource.h
%{_includedir}/X11/Xutil.h
%{_includedir}/X11/cursorfont.h
%{_libdir}/libX11.so
%{_libdir}/libX11-xcb.so
%{_libdir}/pkgconfig/x11.pc
%{_libdir}/pkgconfig/x11-xcb.pc
%{_mandir}/man3/*.3*
%{_mandir}/man5/*.5*

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.6.2-1
- Initial version based on f21
