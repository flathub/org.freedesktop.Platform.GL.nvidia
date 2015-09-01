%define base_drivers swrast,nouveau
#,radeon,r200

%ifarch %{ix86} x86_64
%define platform_drivers ,i915,i965
%endif

%define _default_patch_fuzz 2

Summary: Mesa graphics libraries
Name: mesa
Version: 10.5.5
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.mesa3d.org

Source0: ftp://ftp.freedesktop.org/pub/mesa/%{version}/mesa-%{version}.tar.xz

Patch1: mesa-no-typeid.patch

BuildRequires: freedesktop-sdk-base
BuildRequires: libdrm-dev
BuildRequires: libXxf86vm-dev
BuildRequires: xorg-x11-proto-dev
BuildRequires: libXext-dev
BuildRequires: libXfixes-dev
BuildRequires: libXdamage-dev
BuildRequires: libXi-dev
BuildRequires: libxshmfence-dev
BuildRequires: libwayland-client-dev
BuildRequires: libwayland-server-dev
BuildRequires: llvm-dev

%description
Mesa

%package libGL
Summary: Mesa libGL runtime libraries and DRI drivers
Group: System Environment/Libraries
Provides: libGL

%description libGL
Mesa libGL runtime library.

%package libEGL
Summary: Mesa libEGL runtime libraries
Group: System Environment/Libraries

%description libEGL
Mesa libEGL runtime libraries

%package libGLES
Summary: Mesa libGLES runtime libraries
Group: System Environment/Libraries

%description libGLES
Mesa GLES runtime libraries

%package filesystem
Summary: Mesa driver filesystem
Group: User Interface/X Hardware Support
%description filesystem
Mesa driver filesystem

%package dri-drivers
Summary: Mesa-based DRI drivers
Group: User Interface/X Hardware Support
Requires: mesa-filesystem%{?_isa}
%description dri-drivers
Mesa-based DRI drivers.

%package libGL-dev
Summary: Mesa libGL development package
Group: Development/Libraries
Requires: mesa-libGL = %{version}-%{release}

%description libGL-dev
Mesa libGL development package

%package libEGL-dev
Summary: Mesa libEGL development package
Group: Development/Libraries
Requires: mesa-libEGL = %{version}-%{release}

%description libEGL-dev
Mesa libEGL development package

%package libGLES-dev
Summary: Mesa libGLES development package
Group: Development/Libraries
Requires: mesa-libGLES = %{version}-%{release}

%description libGLES-dev
Mesa libGLES development package

%package libgbm
Summary: Mesa gbm library
Group: System Environment/Libraries

%description libgbm
Mesa gbm runtime library.

%package libgbm-dev
Summary: Mesa libgbm development package
Group: Development/Libraries
Requires: mesa-libgbm%{?_isa} = %{version}-%{release}

%description libgbm-dev
Mesa libgbm development package

%package libglapi
Summary: Mesa shared glapi
Group: System Environment/Libraries

%description libglapi
Mesa shared glapi

%package libwayland-egl
Summary: Mesa libwayland-egl library
Group: System Environment/Libraries
Provides: libwayland-egl

%description libwayland-egl
Mesa libwayland-egl runtime library.

%package libwayland-egl-dev
Summary: Mesa libwayland-egl development package
Group: Development/Libraries
Requires: mesa-libwayland-egl%{?_isa} = %{version}-%{release}
Provides: libwayland-egl-dev

%description libwayland-egl-dev
Mesa libwayland-egl development package

%prep
%setup -q -n mesa-%{version}
%patch1 -p1 -b .no-typeid

%build

autoreconf --install --force

export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS -fno-rtti -fno-exceptions"
%ifarch %{ix86}
# i do not have words for how much the assembly dispatch code infuriates me
%define asm_flags --disable-asm
%endif

%configure \
    --libdir=%{_libdir}/GL \
    %{?asm_flags} \
    --disable-selinux \
    --disable-osmesa \
    --with-dri-driverdir=%{_libdir}/GL/dri \
    --enable-egl \
    --disable-gles1 \
    --enable-gles2 \
    --disable-xvmc \
    --with-egl-platforms=x11,drm,wayland \
    --enable-shared-glapi \
    --enable-gbm \
    --disable-opencl \
    --enable-glx-tls \
    --enable-texture-float=yes \
    --enable-gallium-llvm \
    --enable-llvm-shared-libs \
    --enable-dri \
    --enable-sysfs \
    --with-gallium-drivers=svga,swrast,nouveau,r600,r300,radeonsi \
    --with-dri-drivers=%{?base_drivers}%{?platform_drivers}

make %{?_smp_mflags} MKDEP=/bin/true

%install
make install DESTDIR=$RPM_BUILD_ROOT

# We moved everything into a GL subdir to allow easy override
# Need to set up symlinks and otherwise clean this up a bit
mv -f $RPM_BUILD_ROOT%{_libdir}/GL/pkgconfig $RPM_BUILD_ROOT%{_libdir}
for I in libEGL.so.1 libGLESv2.so.2 libGL.so.1 libwayland-egl.so.1; do \
    ln -s GL/$I $RPM_BUILD_ROOT%{_libdir}/$I; \
    B=`echo $I | sed "s/\\.[0-9]$//"`; \
    ln -s $I $RPM_BUILD_ROOT%{_libdir}/$B; \
    rm $RPM_BUILD_ROOT%{_libdir}/GL/$B; \
done

# libvdpau opens the versioned name, don't bother including the unversioned
rm -f $RPM_BUILD_ROOT%{_libdir}/vdpau/*.so

# strip out useless headers
rm -f $RPM_BUILD_ROOT%{_includedir}/GL/w*.h

# We're not building osmesa
rm -f $RPM_BUILD_ROOT%{_includedir}/GL/osmesa.h

# remove .la files
find $RPM_BUILD_ROOT -name \*.la | xargs rm -f

%check

%post libGL -p /sbin/ldconfig
%postun libGL -p /sbin/ldconfig
%post libEGL -p /sbin/ldconfig
%postun libEGL -p /sbin/ldconfig
%post libGLES -p /sbin/ldconfig
%postun libGLES -p /sbin/ldconfig
%post libglapi -p /sbin/ldconfig
%postun libglapi -p /sbin/ldconfig
%post libgbm -p /sbin/ldconfig
%postun libgbm -p /sbin/ldconfig
%post libwayland-egl -p /sbin/ldconfig
%postun libwayland-egl -p /sbin/ldconfig

%files libGL
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/libGL.so.1
%{_libdir}/GL/libGL.so.1
%{_libdir}/GL/libGL.so.1.*

%files libEGL
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/libEGL.so.1
%{_libdir}/GL/libEGL.so.1
%{_libdir}/GL/libEGL.so.1.*

%files libGLES
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/libGLESv2.so.2
%{_libdir}/GL/libGLESv2.so.2
%{_libdir}/GL/libGLESv2.so.2.*

%files filesystem
%defattr(-,root,root,-)
%dir %{_libdir}/GL
%dir %{_libdir}/GL/dri

%files libglapi
%{_libdir}/GL/libglapi.so.0
%{_libdir}/GL/libglapi.so.0.*

%files dri-drivers
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/drirc
%{_libdir}/GL/dri/nouveau_vieux_dri.so
#%{_libdir}/GL/dri/radeon_dri.so
#%{_libdir}/GL/dri/r200_dri.so
#%{_libdir}/GL/dri/r300_dri.so
#%{_libdir}/GL/dri/r600_dri.so
#%{_libdir}/GL/dri/radeonsi_dri.so
%ifarch %{ix86} x86_64
%{_libdir}/GL/dri/i915_dri.so
%{_libdir}/GL/dri/i965_dri.so
%endif
%{_libdir}/GL/dri/nouveau_dri.so
%{_libdir}/GL/dri/vmwgfx_dri.so
%{_libdir}/GL/dri/kms_swrast_dri.so
%{_libdir}/GL/dri/swrast_dri.so
%{_libdir}/GL/dri/r300_dri.so
%{_libdir}/GL/dri/r600_dri.so
%{_libdir}/GL/dri/radeonsi_dri.so

%files libGL-dev
%defattr(-,root,root,-)
%{_includedir}/GL/gl.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glx_mangle.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/glcorearb.h
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h
%{_libdir}/pkgconfig/dri.pc
%{_libdir}/libGL.so
%{_libdir}/GL/libglapi.so
%{_libdir}/pkgconfig/gl.pc

%files libEGL-dev
%defattr(-,root,root,-)
%dir %{_includedir}/EGL
%{_includedir}/EGL/eglext.h
%{_includedir}/EGL/egl.h
%{_includedir}/EGL/eglmesaext.h
%{_includedir}/EGL/eglplatform.h
%{_includedir}/EGL/eglextchromium.h
%dir %{_includedir}/KHR
%{_includedir}/KHR/khrplatform.h
%{_libdir}/pkgconfig/egl.pc
%{_libdir}/libEGL.so

%files libGLES-dev
%defattr(-,root,root,-)
%dir %{_includedir}/GLES2
%{_includedir}/GLES2/gl2platform.h
%{_includedir}/GLES2/gl2.h
%{_includedir}/GLES2/gl2ext.h
%{_includedir}/GLES3/gl3platform.h
%{_includedir}/GLES3/gl3.h
%{_includedir}/GLES3/gl3ext.h
%{_includedir}/GLES3/gl31.h
%{_libdir}/pkgconfig/glesv2.pc
%{_libdir}/libGLESv2.so

%files libgbm
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/GL/libgbm.so.1
%{_libdir}/GL/libgbm.so.1.*

%files libgbm-dev
%defattr(-,root,root,-)
%{_libdir}/GL/libgbm.so
%{_includedir}/gbm.h
%{_libdir}/pkgconfig/gbm.pc

%files libwayland-egl
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/libwayland-egl.so.1
%{_libdir}/GL/libwayland-egl.so.1
%{_libdir}/GL/libwayland-egl.so.1.*

%files libwayland-egl-dev
%defattr(-,root,root,-)
%{_libdir}/libwayland-egl.so
%{_libdir}/pkgconfig/wayland-egl.pc

%changelog
* Tue Dec  9 2014 Alexander Larsson <alexl@redhat.com> - 10.3.5-1
- Initial version, based on F21
