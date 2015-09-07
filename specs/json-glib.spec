%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name:		json-glib
Version:	1.0.4
Release:	1%{?dist}
Summary:	Library for JavaScript Object Notation format

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		https://wiki.gnome.org/Projects/JsonGlib
#VCS:		git:git://git.gnome.org/json-glib
Source0:	http://download.gnome.org/sources/%{name}/%{release_version}/%{name}-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base
BuildRequires: glib2-dev
BuildRequires: gobject-introspection-dev


%description
%{name} is a library providing serialization and deserialization support
for the JavaScript Object Notation (JSON) format.


%package dev
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}%{_isa} = %{version}-%{release}

%description dev
The %{name}-dev package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{version}


%build
%configure --enable-static=no
make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%find_lang json-glib-1.0

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig

%files -f json-glib-1.0.lang
%doc COPYING NEWS
%{_libdir}/lib%{name}*.so.*
%{_libdir}/girepository-1.0/Json-1.0.typelib

%files dev
%{_libdir}/lib%{name}*.so
%{_libdir}/pkgconfig/%{name}-1.0.pc
%{_includedir}/%{name}-1.0/
%{_datadir}/gtk-doc/
%{_datadir}/gir-1.0/Json-1.0.gir
%{_bindir}/json-glib-format
%{_bindir}/json-glib-validate


%changelog
* Tue Nov 25 2014 Alexander Larsson <alexl@redhat.com> - 1.0.2-1
- Initial version, based on F21
