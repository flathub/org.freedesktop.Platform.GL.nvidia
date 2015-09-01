Name:           wayland
Version:        1.7.0
Release:        1%{?dist}
Summary:        Wayland Compositor Infrastructure

Group:          User Interface/X
License:        MIT
URL:            http://%{name}.freedesktop.org/
Source0:        http://wayland.freedesktop.org/releases/%{name}-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base

%description
Wayland is a protocol for a compositor to talk to its clients as well as a C
library implementation of that protocol. The compositor can be a standalone
display server running on Linux kernel modesetting and evdev input devices,
an X application, or a wayland client itself. The clients can be traditional
applications, X servers (rootless or fullscreen) or other display servers.

%package dev
Summary: Common headers for wayland
License: MIT
%description dev
Common headers for wayland

%package -n libwayland-client
Summary: Wayland client library
License: MIT
%description -n libwayland-client
Wayland client library

%package -n libwayland-cursor
Summary: Wayland cursor library
License: MIT
%description -n libwayland-cursor
Wayland cursor library

%package -n libwayland-server
Summary: Wayland server library
License: MIT
%description -n libwayland-server
Wayland server library

%package -n libwayland-client-dev
Summary: Headers and symlinks for developing wayland client applications
License: MIT
Requires: libwayland-client%{?_isa} = %{version}-%{release}
Requires: wayland-dev%{?_isa} = %{version}-%{release}
%description -n libwayland-client-dev
Headers and symlinks for developing wayland client applications.

%package -n libwayland-cursor-dev
Summary: Headers and symlinks for developing wayland cursor applications
License: MIT
Requires: libwayland-cursor%{?_isa} = %{version}-%{release}
Requires: wayland-dev%{?_isa} = %{version}-%{release}
%description -n libwayland-cursor-dev
Headers and symlinks for developing wayland cursor applications.

%package -n libwayland-server-dev
Summary: Headers and symlinks for developing wayland server applications
License: MIT
Requires: libwayland-server%{?_isa} = %{version}-%{release}
Requires: wayland-dev%{?_isa} = %{version}-%{release}
%description -n libwayland-server-dev
Headers and symlinks for developing wayland server applications.

%prep
%setup -q -n %{name}-%{version}

%build
autoreconf -v --install
%configure --disable-static --disable-documentation
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name \*.la | xargs rm -f

%post -n libwayland-client -p /sbin/ldconfig
%postun -n libwayland-client -p /sbin/ldconfig

%post -n libwayland-cursor -p /sbin/ldconfig
%postun -n libwayland-cursor -p /sbin/ldconfig

%post -n libwayland-server -p /sbin/ldconfig
%postun -n libwayland-server -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README TODO
#doc %{_datadir}/doc/wayland/*

%files dev
%defattr(-,root,root,-)
%{_bindir}/wayland-scanner
%{_includedir}/wayland-util.h
%{_includedir}/wayland-egl.h
%{_includedir}/wayland-version.h
%{_datadir}/aclocal/wayland-scanner.m4
%{_libdir}/pkgconfig/wayland-scanner.pc
%dir %{_datadir}/wayland
%{_datadir}/wayland/wayland-scanner.mk
%{_datadir}/wayland/wayland.xml
%{_datadir}/wayland/wayland.dtd

%files -n libwayland-client
%defattr(-,root,root,-)
%{_libdir}/libwayland-client.so.0*

%files -n libwayland-cursor
%defattr(-,root,root,-)
%{_libdir}/libwayland-cursor.so.0*

%files -n libwayland-server
%defattr(-,root,root,-)
%{_libdir}/libwayland-server.so.0*

%files -n libwayland-client-dev
%defattr(-,root,root,-)
%{_includedir}/wayland-client*.h
%{_libdir}/libwayland-client.so
%{_libdir}/pkgconfig/wayland-client.pc

%files -n libwayland-cursor-dev
%defattr(-,root,root,-)
%{_includedir}/wayland-cursor*.h
%{_libdir}/libwayland-cursor.so
%{_libdir}/pkgconfig/wayland-cursor.pc

%files -n libwayland-server-dev
%defattr(-,root,root,-)
%{_includedir}/wayland-server*.h
%{_libdir}/libwayland-server.so
%{_libdir}/pkgconfig/wayland-server.pc

%changelog
* Mon Jan 19 2015 Alexander Larsson <alexl@redhat.com> - 1.6.0-1
- Initial version
