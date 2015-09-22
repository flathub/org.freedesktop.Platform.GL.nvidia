%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name:           gobject-introspection
Version:        1.46.0
Release:        1%{?dist}
Summary:        Introspection system for GObject-based libraries

Group:      Development/Libraries
License:        GPLv2+, LGPLv2+, MIT
URL:            http://live.gnome.org/GObjectIntrospection
#VCS:           git:git://git.gnome.org/gobject-introspection
Source0:        http://download.gnome.org/sources/gobject-introspection/%{release_version}/%{name}-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base
BuildRequires: glib2-dev
BuildRequires: gtk-doc-stub

%description
GObject Introspection can scan C header and source files in order to
generate introspection "typelib" files.  It also provides an API to examine
typelib files, useful for creating language bindings among other
things.

%package dev
Summary: Libraries and headers for gobject-introspection
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description dev
Libraries and headers for gobject-introspection

%prep
%setup -q

%build
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; fi;)
%configure --disable-gtk-doc

make V=1 %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Die libtool, die.
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING

%{_libdir}/lib*.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/*.typelib

%files dev
%{_libdir}/lib*.so
%dir %{_libdir}/gobject-introspection
%{_libdir}/gobject-introspection/*
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_bindir}/g-ir-*
%{_datadir}/gir-1.0
%dir %{_datadir}/gobject-introspection-1.0
%{_datadir}/gobject-introspection-1.0/*
%{_datadir}/aclocal/introspection.m4
%{_mandir}/man1/*.gz

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.42.0-1
- Initial version imported from f21
