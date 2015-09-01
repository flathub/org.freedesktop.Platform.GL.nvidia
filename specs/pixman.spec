Name:           pixman
Version:        0.32.6
Release:        1%{?dist}
Summary:        Pixel manipulation library

Group:          System Environment/Libraries
License:        MIT
URL:            http://cgit.freedesktop.org/pixman/
#VCS:		git:git://git.freedesktop.org/git/pixman
Source0:	http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires:  freedesktop-sdk-base

%description
Pixman is a pixel manipulation library for X and cairo.

%package dev
Summary: Pixel manipulation library development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
Development library for pixman.

%prep
%setup -q

%build
%configure \
%ifarch %{arm}
  --disable-arm-iwmmxt --disable-arm-iwmmxt2 \
%endif
%ifarch ppc64le
  --disable-vmx \
%endif
  --disable-static

make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

find %{buildroot} -type f -name "*.la" -delete

%check
make check %{?_smp_mflags} V=1 ||:

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_libdir}/libpixman-1*.so.*

%files dev
%dir %{_includedir}/pixman-1
%{_includedir}/pixman-1/pixman.h
%{_includedir}/pixman-1/pixman-version.h
%{_libdir}/libpixman-1*.so
%{_libdir}/pkgconfig/pixman-1.pc

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 0.32.6-1
- Initial version based on f21
