%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name: libsoup
Version: 2.50.0
Release: 1%{?dist}
License: LGPLv2
Group: Development/Libraries
Summary: Soup, an HTTP library implementation
URL: http://live.gnome.org/LibSoup
#VCS: git:git://git.gnome.org/libsoup
Source: http://download.gnome.org/sources/libsoup/%{release_version}/libsoup-%{version}.tar.xz

BuildRequires: glib2-dev
BuildRequires: glib-networking
BuildRequires: gobject-introspection-dev

Requires: glib2%{?_isa}
Requires: glib-networking%{?_isa}

%description
Libsoup is an HTTP library implementation in C. It was originally part
of a SOAP (Simple Object Access Protocol) implementation called Soup, but
the SOAP and non-SOAP parts have now been split into separate packages.

libsoup uses the Glib main loop and is designed to work well with GTK
applications. This enables GNOME applications to access HTTP servers
on the network in a completely asynchronous fashion, very similar to
the Gtk+ programming model (a synchronous operation mode is also
supported for those who want it).

%package dev
Summary: Header files for the Soup library
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description dev
Libsoup is an HTTP library implementation in C. This package allows
you to develop applications that use the libsoup library.

%prep
%setup -q

%build
%configure --disable-static

# Omit unused direct shared library dependencies.
sed --in-place --expression 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

%find_lang libsoup

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f libsoup.lang
%doc README COPYING NEWS AUTHORS
%{_libdir}/lib*.so.*
%{_libdir}/girepository-1.0/Soup*2.4.typelib

%files dev
%{_includedir}/%{name}-2.4
%{_includedir}/%{name}-gnome-2.4
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/Soup*2.4.gir
%{_datadir}/gtk-doc/html/%{name}-2.4

%changelog
* Mon Nov 24 2014 Alexander Larsson <alexl@redhat.com> - 2.48.0-1
- Initial version, based on F21
