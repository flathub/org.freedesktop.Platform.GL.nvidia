Summary: Direct Rendering Manager runtime library
Name: libepoxy
Version: 1.2
Release: 1%{?dist}
License: MIT
URL: http://github.com/anholt/libepoxy
Source0: https://github.com/anholt/libepoxy/archive/v%{version}.tar.gz
BuildRequires: freedesktop-sdk-base
BuildRequires: mesa-libGL-dev
BuildRequires: mesa-libEGL-dev
BuildRequires: mesa-libGLES-dev
BuildRequires: xorg-x11-util-macros

%description
A library for handling OpenGL function pointer management.

%package dev
Summary: Development files for libepoxy
Requires: %{name}%{?_isa} = %{version}-%{release}

%description dev
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
autoreconf -vif || exit 1
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# NOTE: We intentionally don't ship *.la files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete -print

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md
%{_libdir}/libepoxy.so.0
%{_libdir}/libepoxy.so.0.0.0

%files dev
%dir %{_includedir}/epoxy/
%{_includedir}/epoxy/*
%{_libdir}/libepoxy.so
%{_libdir}/pkgconfig/epoxy.pc

%changelog
* Thu Dec 11 2014 Alexander Larsson <alexl@redhat.com> - 1.2-1
- Initial version
