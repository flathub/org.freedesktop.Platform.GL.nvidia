Name:           SDL2
Version:        2.0.3
Release:        1%{?dist}
Summary:        A cross-platform multimedia library
Group:          System Environment/Libraries
URL:            http://www.libsdl.org/
License:        zlib and MIT
Source0:        http://www.libsdl.org/release/%{name}-%{version}.tar.gz

BuildRequires: freedesktop-sdk-base
BuildRequires: dbus-dev
BuildRequires: libX11-dev
BuildRequires: libXScrnSaver-dev
BuildRequires: libXcursor-dev
BuildRequires: libXext-dev
BuildRequires: libXi-dev
BuildRequires: libXinerama-dev
BuildRequires: libXrandr-dev
BuildRequires: libXrender-dev
BuildRequires: libwayland-client-dev
BuildRequires: libwayland-cursor-dev
BuildRequires: mesa-libwayland-egl-dev
BuildRequires: libxkbcommon-dev
BuildRequires: mesa-libEGL-dev
BuildRequires: mesa-libGL-dev
BuildRequires: pulseaudio-libs-dev

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device.

%package dev
Summary:    Files needed to develop Simple DirectMedia Layer applications
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   mesa-libGL-dev
#Requires:   mesa-libGLU-dev
Requires:   mesa-libEGL-dev
Requires:   libX11-dev
Requires:   libXi-dev
Requires:   libXext-dev
Requires:   libXrandr-dev
Requires:   libXrender-dev
Requires:   libXScrnSaver-dev
Requires:   libXinerama-dev
Requires:   libXcursor-dev
# Wayland
Requires:   libwayland-client-dev
Requires:   mesa-libwayland-egl-dev
Requires:   libwayland-cursor-dev
Requires:   libxkbcommon-dev

%description dev
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device. This
package provides the libraries, include files, and other resources needed for
developing SDL applications.

%prep
%setup -q
# Compilation without ESD
sed -i -e 's/.*AM_PATH_ESD.*//' configure.in
sed -i -e 's/\r//g' TODO.txt README.txt WhatsNew.txt BUGS.txt COPYING.txt CREDITS.txt README-SDL.txt

%build
%configure \
    --enable-sdl-dlopen \
    --disable-arts \
    --disable-esd \
    --disable-nas \
    --enable-pulseaudio \
    --disable-alsa \
    --disable-oss \
    --disable-sndio \
    --disable-libudev \
    --enable-video-wayland \
    --disable-rpath
make %{?_smp_mflags}

%install
%make_install

# remove libtool .la file
rm -f %{buildroot}%{_libdir}/*.la
# remove static .a file
rm -f %{buildroot}%{_libdir}/*.a

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc BUGS.txt CREDITS.txt COPYING.txt README-SDL.txt
%{_libdir}/lib*.so.*

%files dev
%doc README.txt TODO.txt WhatsNew.txt
%{_bindir}/*-config
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/sdl2.pc
%{_includedir}/SDL2
%{_datadir}/aclocal/*

%changelog
* Thu Feb 12 2015 Alexander Larsson <alexl@redhat.com> - 2.0.3-1
- Initial version

