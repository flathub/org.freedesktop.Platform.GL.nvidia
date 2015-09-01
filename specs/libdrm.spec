Summary: Direct Rendering Manager runtime library
Name: libdrm
Version: 2.4.61
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://dri.sourceforge.net
Source0: http://dri.freedesktop.org/libdrm/%{name}-%{version}.tar.bz2

BuildRequires: freedesktop-sdk-base
BuildRequires: libxcb-dev
BuildRequires: libpciaccess-dev
BuildRequires: xorg-x11-util-macros

%description
Direct Rendering Manager runtime library

%package dev
Summary: Direct Rendering Manager development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
Direct Rendering Manager development package

%prep
%setup -q

%build
autoreconf -v --install || exit 1
%configure \
	--disable-udev
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
# SUBDIRS=libdrm

# NOTE: We intentionally don't ship *.la files
find $RPM_BUILD_ROOT -type f -name '*.la' | xargs rm -f -- || :
for i in r300_reg.h via_3d_reg.h
do
rm -f $RPM_BUILD_ROOT/usr/include/libdrm/$i
done

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README
%{_libdir}/libdrm.so.2
%{_libdir}/libdrm.so.2.4.0
%ifarch %{ix86} x86_64 ia64
%{_libdir}/libdrm_intel.so.1
%{_libdir}/libdrm_intel.so.1.0.0
%endif
%{_libdir}/libdrm_radeon.so.1
%{_libdir}/libdrm_radeon.so.1.0.1
%{_libdir}/libdrm_nouveau.so.2
%{_libdir}/libdrm_nouveau.so.2.0.0
%{_libdir}/libkms.so.1
%{_libdir}/libkms.so.1.0.0

%files dev
%defattr(-,root,root,-)
# FIXME should be in drm/ too
%{_includedir}/xf86drm.h
%{_includedir}/xf86drmMode.h
%dir %{_includedir}/libdrm
%{_includedir}/libdrm/drm.h
%{_includedir}/libdrm/drm_fourcc.h
%{_includedir}/libdrm/drm_mode.h
%{_includedir}/libdrm/drm_sarea.h
%ifarch %{ix86} x86_64 ia64
%{_includedir}/libdrm/intel_aub.h
%{_includedir}/libdrm/intel_bufmgr.h
%{_includedir}/libdrm/intel_debug.h
%endif
%{_includedir}/libdrm/radeon_bo.h
%{_includedir}/libdrm/radeon_bo_gem.h
%{_includedir}/libdrm/radeon_bo_int.h
%{_includedir}/libdrm/radeon_cs.h
%{_includedir}/libdrm/radeon_cs_gem.h
%{_includedir}/libdrm/radeon_cs_int.h
%{_includedir}/libdrm/radeon_surface.h
%{_includedir}/libdrm/r600_pci_ids.h
%{_includedir}/libdrm/nouveau.h
%{_includedir}/libdrm/*_drm.h
%{_includedir}/libkms
%{_libdir}/libdrm.so
%ifarch %{ix86} x86_64 ia64
%{_libdir}/libdrm_intel.so
%endif
%{_libdir}/libdrm_radeon.so
%{_libdir}/libdrm_nouveau.so
%{_libdir}/libkms.so
%{_libdir}/pkgconfig/libdrm.pc
%ifarch %{ix86} x86_64 ia64
%{_libdir}/pkgconfig/libdrm_intel.pc
%endif
%{_libdir}/pkgconfig/libdrm_radeon.pc
%{_libdir}/pkgconfig/libdrm_nouveau.pc
%{_libdir}/pkgconfig/libkms.pc

%changelog
* Tue Dec  9 2014 Alexander Larsson <alexl@redhat.com> - 2.4.58-1
- Initial version, based on F21
