Summary: X.Org X11 libXft runtime library
Name: libXft
Version: 2.3.2
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: freedesktop-sdk-base
BuildRequires: xorg-x11-util-macros
BuildRequires: libXrender-dev
BuildRequires: freetype-dev
BuildRequires: fontconfig-dev

Requires: fontconfig

%description
X.Org X11 libXft runtime library

%package dev
Summary: X.Org X11 libXft development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
X.Org X11 libXft development package

%prep
%setup -q

%build
autoreconf -v --install --force

%configure --disable-static
make %{?_smp_mflags} 

%install
make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: There's no real good reason to ship these anymore, as pkg-config
# is the official way to detect flags, etc. now.
rm -f $RPM_BUILD_ROOT%{_bindir}/xft-config
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/xft-config*

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ChangeLog
%{_libdir}/libXft.so.2*

%files dev
%defattr(-,root,root,-)
#%{_bindir}/xft-config
%dir %{_includedir}/X11/Xft
%{_includedir}/X11/Xft/Xft.h
%{_includedir}/X11/Xft/XftCompat.h
%{_libdir}/libXft.so
%{_libdir}/pkgconfig/xft.pc
#%{_mandir}/man1/xft-config.1.gz
#%dir %{_mandir}/man3x
%{_mandir}/man3/Xft.3*

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 2.3.2-1
- Initial version based on f21
