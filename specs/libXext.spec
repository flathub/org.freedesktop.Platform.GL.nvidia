Summary: X.Org X11 libXext runtime library
Name: libXext
Version: 1.3.3
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2

Requires: libX11

BuildRequires: freedesktop-sdk-base
BuildRequires: xorg-x11-proto-dev
BuildRequires: libX11-dev
BuildRequires: libXau-dev
BuildRequires: xorg-x11-util-macros

%description
X.Org X11 libXext runtime library

%package dev
Summary: X.Org X11 libXext development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
X.Org X11 libXext development package

%prep
%setup -q -n libXext-%{version}

%build
autoreconf -v --install --force
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# do this with %%doc below
rm -rf $RPM_BUILD_ROOT%{_docdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_libdir}/libXext.so.6
%{_libdir}/libXext.so.6.4.0

%files dev
%defattr(-,root,root,-)
%{_includedir}/X11/extensions/MITMisc.h
%{_includedir}/X11/extensions/XEVI.h
%{_includedir}/X11/extensions/XLbx.h
%{_includedir}/X11/extensions/XShm.h
%{_includedir}/X11/extensions/Xag.h
%{_includedir}/X11/extensions/Xcup.h
%{_includedir}/X11/extensions/Xdbe.h
%{_includedir}/X11/extensions/Xext.h
%{_includedir}/X11/extensions/Xge.h
%{_includedir}/X11/extensions/dpms.h
%{_includedir}/X11/extensions/extutil.h
%{_includedir}/X11/extensions/multibuf.h
%{_includedir}/X11/extensions/security.h
%{_includedir}/X11/extensions/shape.h
%{_includedir}/X11/extensions/sync.h
%{_includedir}/X11/extensions/xtestext1.h
%{_libdir}/libXext.so
%{_libdir}/pkgconfig/xext.pc
#%dir %{_mandir}/man3x
%{_mandir}/man3/*.3*

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.3.3-1
- Initial version based on f21
