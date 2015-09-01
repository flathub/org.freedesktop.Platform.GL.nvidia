Summary: X.Org X11 libXvMC runtime library
Name: libXvMC
Version: 1.0.8
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
BuildRequires: libXv-dev

%description
X.Org X11 libXvMC runtime library

%package dev
Summary: X.Org X11 libXvMC development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
X.Org X11 libXvMC development package

%prep
%setup -q -n libXvMC-%{version}

%build
autoreconf -v --install --force
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# do this ourself in %%doc so we get %%version
rm $RPM_BUILD_ROOT%{_docdir}/*/*.txt

# Touch XvMCConfig for rpm to package the ghost file. (#192254)
{
    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11
    touch $RPM_BUILD_ROOT%{_sysconfdir}/X11/XvMCConfig
}

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README 
%{_libdir}/libXvMC.so.1
%{_libdir}/libXvMC.so.1.0.0
%{_libdir}/libXvMCW.so.1
%{_libdir}/libXvMCW.so.1.0.0
%ghost %config(missingok,noreplace) %verify (not md5 size mtime) %{_sysconfdir}/X11/XvMCConfig

%files dev
%defattr(-,root,root,-)
%doc XvMC_API.txt
%{_includedir}/X11/extensions/XvMClib.h
%{_libdir}/libXvMC.so
%{_libdir}/libXvMCW.so
%{_libdir}/pkgconfig/xvmc.pc

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.0.8-1
- Initial version based on f21
