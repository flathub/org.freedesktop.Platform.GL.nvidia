Name:           SDL2_image
Version:        2.0.0
Release:        1%{?dist}
Summary:        Image loading library for SDL

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.libsdl.org/projects/SDL_image/
Source0:        http://www.libsdl.org/projects/SDL_image/release/%{name}-%{version}.tar.gz

BuildRequires:	freedesktop-sdk-base
BuildRequires:  SDL2-dev

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio
device.  This package contains a simple library for loading images of
various formats (BMP, PPM, PCX, GIF, JPEG, PNG) as SDL surfaces.

%package dev
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       SDL2-dev

%description dev
The %{name}-dev package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
rm -rf external/
sed -i -e 's/\r//g' README.txt CHANGES.txt COPYING.txt

%build
%configure --disable-dependency-tracking \
           --disable-jpg-shared \
           --disable-png-shared \
           --disable-tif-shared \
           --disable-webp-shared \
           --disable-static
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags}

%install
%make_install
mkdir -p %{buildroot}%{_bindir}
./libtool --mode=install /usr/bin/install showimage %{buildroot}%{_bindir}/showimage

rm -f %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc CHANGES.txt COPYING.txt
%{_libdir}/lib*.so.*

%files dev
%doc README.txt
%{_bindir}/showimage
%{_libdir}/lib*.so
%{_includedir}/SDL2/*
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Fri Feb 13 2015 Alexander Larsson <alexl@redhat.com> - 2.0.0-1
- Initial version
