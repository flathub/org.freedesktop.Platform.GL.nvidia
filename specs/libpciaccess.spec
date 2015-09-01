Name:           libpciaccess
Version:        0.13.2
Release:        1%{?dist}
Summary:        PCI access library

Group:          System Environment/Libraries
License:        MIT
URL:            http://gitweb.freedesktop.org/?p=xorg/lib/libpciaccess.git

Source0:	http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2

Patch1:		libpciaccess-sysfs.patch
Patch2:		libpciaccess-rom-size.patch

BuildRequires: freedesktop-sdk-base
BuildRequires: xorg-x11-util-macros

%description
libpciaccess is a library for portable PCI access routines across multiple
operating systems.

%package dev
Summary:        PCI access library development package
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description dev
Development package for libpciaccess.

%prep
%setup -q -n %{name}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}
%patch2 -p1 -b .rom-size

%build
autoreconf -v --install
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS
%{_libdir}/libpciaccess.so.0
%{_libdir}/libpciaccess.so.0.11.*

%files dev
%defattr(-,root,root,-)
%{_includedir}/pciaccess.h
%{_libdir}/libpciaccess.so
%{_libdir}/pkgconfig/pciaccess.pc

%changelog
* Tue Dec  9 2014 Alexander Larsson <alexl@redhat.com> - 0.13.2-1
- Initial version
