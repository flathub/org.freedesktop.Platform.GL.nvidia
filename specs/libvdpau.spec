Name:           libvdpau
Version:        1.1.1
Release:        1%{?dist}
Summary:        Wrapper library for the Video Decode and Presentation API
License:        MIT
URL:            http://freedesktop.org/wiki/Software/VDPAU
Source0:        http://cgit.freedesktop.org/~aplattner/%{name}/snapshot/%{name}-%{version}.tar.bz2

BuildRequires: freedesktop-sdk-base
BuildRequires:  libX11-dev
BuildRequires:  libXext-dev
BuildRequires:  xorg-x11-proto-dev

%description
VDPAU is the Video Decode and Presentation API for UNIX. It provides an
interface to video decode acceleration and presentation hardware present in
modern GPUs.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libX11-dev

%description    dev
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%prep
%setup -q

%build
autoreconf -vif
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -name '*.la' -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING
%config(noreplace) %{_sysconfdir}/vdpau_wrapper.cfg
%{_libdir}/*.so.*
%dir %{_libdir}/vdpau
%{_libdir}/vdpau/%{name}_trace.so*

%files dev
%{_includedir}/vdpau/
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/vdpau.pc

%changelog
* Mon Sep 21 2015 Alexander Larsson <alexl@redhat.com> - 1.1.1-1
- Initial version
