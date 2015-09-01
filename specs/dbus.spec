%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%define gettext_package dbus

%define expat_version           1.95.5
%define dbus_common_config_opts --with-init-scripts=redhat --with-system-pid-file=%{_localstatedir}/run/messagebus.pid --with-dbus-user=dbus --libdir=/%{_lib} --bindir=/bin --sysconfdir=/etc --exec-prefix=/ --libexecdir=/%{_lib}/dbus-1 --docdir=%{_pkgdocdir} --disable-silent-rules

Summary: D-BUS message bus
Name: dbus
Version: 1.8.16
Release: 1%{?dist}
URL: http://www.freedesktop.org/software/dbus/
#VCS: git:git://git.freedesktop.org/git/dbus/dbus
Source0: http://dbus.freedesktop.org/releases/dbus/%{name}-%{version}.tar.gz
License: GPLv2+ or AFL
Group: System Environment/Libraries

BuildRequires: freedesktop-sdk-base
BuildRequires: libX11-dev
Requires: dbus-libs%{?_isa} = %{version}-%{release}

%description
D-BUS is a system for sending messages between applications. It is
used both for the system-wide message bus service, and as a
per-user-login-session messaging facility.

%package libs
Summary: Libraries for accessing D-BUS
Group: Development/Libraries

%description libs
This package contains lowlevel libraries for accessing D-BUS.

%package doc
Summary: Developer documentation for D-BUS
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
This package contains developer documentation for D-Bus along with
other supporting documentation such as the introspect dtd file.

%package dev
Summary: Development files for D-BUS
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
This package contains libraries and header files needed for
developing software that uses D-BUS.

%package x11
Summary: X11-requiring add-ons for D-BUS
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description x11
D-BUS contains some tools that require Xlib to be installed, those are
in this separate package so server systems need not install X.

%prep
%setup -q -n %{name}-%{version}

%build
if test -f autogen.sh; then env NOCONFIGURE=1 ./autogen.sh; else autoreconf -v -f -i; fi
%configure %{dbus_common_config_opts} --disable-tests --disable-asserts
make

%install
make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}/%{_libdir}/pkgconfig

#change the arch-deps.h include directory to /usr/lib[64] instead of /lib[64]
sed -e 's@-I${libdir}@-I${prefix}/%{_lib}@' %{buildroot}/%{_lib}/pkgconfig/dbus-1.pc > %{buildroot}/%{_libdir}/pkgconfig/dbus-1.pc
rm -f %{buildroot}/%{_lib}/pkgconfig/dbus-1.pc

mkdir -p %{buildroot}/%{_bindir}
mv -f %{buildroot}/bin/dbus-launch %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_libdir}/dbus-1.0/include/
mv -f %{buildroot}/%{_lib}/dbus-1.0/include/* %{buildroot}/%{_libdir}/dbus-1.0/include/
rm -rf %{buildroot}/%{_lib}/dbus-1.0

rm -f %{buildroot}/%{_lib}/*.a
rm -f %{buildroot}/%{_lib}/*.la

mkdir -p %{buildroot}%{_datadir}/dbus-1/interfaces

## %find_lang %{gettext_package}
# Delete the old legacy sysv init script
rm -rf %{buildroot}%{_initrddir}

mkdir -p %{buildroot}/var/lib/dbus

install -pm 644 -t %{buildroot}%{_pkgdocdir} \
    doc/introspect.dtd doc/introspect.xsl doc/system-activation.txt

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
# Strictly speaking, we could remove the COPYING from this subpackage and 
# just have it be in libs, because dbus Requires dbus-libs
# However, since it lived here before, I left it in place.
# Maintainer, feel free to remove it from here if you wish.
%{!?_licensedir:%global license %%doc}
%license COPYING
%dir %{_pkgdocdir}
%dir %{_sysconfdir}/dbus-1
%config %{_sysconfdir}/dbus-1/*.conf
%dir %{_sysconfdir}/dbus-1/system.d
%dir %{_sysconfdir}/dbus-1/session.d
%ghost %dir %{_localstatedir}/run/dbus
%dir %{_localstatedir}/lib/dbus/
/bin/dbus-daemon
/bin/dbus-send
/bin/dbus-cleanup-sockets
/bin/dbus-run-session
/bin/dbus-monitor
/bin/dbus-uuidgen
%dir %{_datadir}/dbus-1
%{_datadir}/dbus-1/services
%{_datadir}/dbus-1/system-services
%{_datadir}/dbus-1/interfaces
%dir /%{_lib}/dbus-1
# See doc/system-activation.txt in source tarball for the rationale
# behind these permissions
%attr(4750,root,dbus) /%{_lib}/dbus-1/dbus-daemon-launch-helper

%files libs
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
/%{_lib}/*dbus-1*.so.*

%files x11
%defattr(-,root,root)

%{_bindir}/dbus-launch

%files doc
%defattr(-,root,root)
%{_pkgdocdir}/*

%files dev
%defattr(-,root,root)

/%{_lib}/lib*.so
%dir %{_libdir}/dbus-1.0
%{_libdir}/dbus-1.0/include/
%{_libdir}/pkgconfig/dbus-1.pc
%{_includedir}/*

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1:1.8.6-1
- Initial version based on f21
