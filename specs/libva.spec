Name:		libva
Version:	1.6.1
Release:	1%{?dist}
Summary:	Video Acceleration (VA) API for Linux
Group:		System Environment/Libraries
License:	MIT
URL:		http://freedesktop.org/wiki/Software/vaapi
Source0:	http://www.freedesktop.org/software/vaapi/releases/libva/libva-%{version}.tar.bz2

BuildRequires: freedesktop-sdk-base
BuildRequires: libXext-dev
BuildRequires: libXfixes-dev
BuildRequires: libdrm-dev
BuildRequires: libpciaccess-dev
BuildRequires: mesa-libEGL-dev
BuildRequires: mesa-libGL-dev
BuildRequires: mesa-libGLES-dev
BuildRequires: wayland-dev
BuildRequires: libwayland-client-dev
BuildRequires: libwayland-cursor-dev
BuildRequires: libwayland-server-dev

%description
Libva is a library providing the VA API video acceleration API.

%package	dev
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}%{_isa} = %{version}-%{release}
Requires:	pkgconfig

%description	dev
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	utils
Summary:	Tools for %{name} (including vainfo)
Group:		Development/Libraries
Requires:	%{name}%{_isa} = %{version}-%{release}

%description	utils
The %{name}-utils package contains tools that are provided as part
of %{name}, including the vainfo tool for determining what (if any)
%{name} support is available on a system.


%prep
%setup -q

%build
%configure --disable-static \
  --enable-glx

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -regex ".*\.la$" | xargs rm -f --

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_libdir}/libva*.so.*
%{_libdir}/dri/dummy_drv_video.so

%files dev
%{_includedir}/va
%{_libdir}/libva*.so
%{_libdir}/pkgconfig/libva*.pc

%files utils
%{_bindir}/vainfo
%{_bindir}/loadjpeg
%{_bindir}/jpegenc
%{_bindir}/avcenc
%{_bindir}/h264encode
%{_bindir}/mpeg2vldemo
%{_bindir}/mpeg2vaenc
%{_bindir}/putsurface
%{_bindir}/putsurface_wayland

%changelog
* Mon Sep 21 2015 Alexander Larsson <alexl@redhat.com> - 1.6.1-1
- Initial version
