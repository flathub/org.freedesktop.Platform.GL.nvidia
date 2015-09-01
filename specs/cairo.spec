Summary:	A 2D graphics library
Name:		cairo
Version:	1.14.2
Release:	1%{?dist}
URL:		http://cairographics.org
#VCS:		git:git://git.freedesktop.org/git/cairo
Source0:	http://cairographics.org/releases/%{name}-%{version}.tar.xz

License:	LGPLv2 or MPLv1.1
Group:		System Environment/Libraries

BuildRequires: freedesktop-sdk-base
BuildRequires: libXrender-dev
BuildRequires: libXext-dev
BuildRequires: libX11-dev
BuildRequires: pixman-dev
BuildRequires: freetype-dev
BuildRequires: fontconfig-dev
BuildRequires: glib2-dev
#BuildRequires: librsvg2-dev
#BuildRequires: mesa-libGL-dev
#BuildRequires: mesa-libEGL-dev

%description
Cairo is a 2D graphics library designed to provide high-quality display
and print output. Currently supported output targets include the X Window
System, OpenGL (via glitz), in-memory image buffers, and image files (PDF,
PostScript, and SVG).

Cairo is designed to produce consistent output on all output media while
taking advantage of display hardware acceleration when available (e.g.
through the X Render Extension or OpenGL).

%package dev
Summary: Development files for cairo
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libXrender-dev
Requires: pixman-dev
Requires: freetype-dev
Requires: fontconfig-dev

%description dev
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains libraries, header files and developer documentation
needed for developing software which uses the cairo graphics library.

%package gobject
Summary: GObject bindings for cairo
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description gobject
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains functionality to make cairo graphics library
integrate well with the GObject object system used by GNOME.

%package gobject-dev
Summary: Development files for cairo-gobject
Group: Development/Libraries
Requires: %{name}-dev = %{version}-%{release}
Requires: %{name}-gobject = %{version}-%{release}

%description gobject-dev
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains libraries, header files and developer documentation
needed for developing software which uses the cairo Gobject library.

%package tools
Summary: Development tools for cairo
Group: Development/Tools

%description tools
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains tools for working with the cairo graphics library.
 * cairo-trace: Record cairo library calls for later playback

%prep
%setup -q

%build
export CFLAGS="%{optflags} -flto -ffat-lto-objects"

%configure --disable-static	\
	--enable-xlib		\
	--enable-ft		\
	--enable-svg		\
	--enable-ps		\
	--enable-pdf		\
	--enable-tee		\
	--enable-gobject	\
	--disable-gtk-doc
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make V=1 %{?_smp_mflags}

#	--enable-gl		\

%install
make install V=1 DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%check
make check V=1 %{?_smp_mflags} ||:

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post gobject -p /sbin/ldconfig
%postun gobject -p /sbin/ldconfig

%files
%doc AUTHORS BIBLIOGRAPHY BUGS COPYING COPYING-LGPL-2.1 COPYING-MPL-1.1 NEWS README
%{_libdir}/libcairo.so.*
%{_libdir}/libcairo-script-interpreter.so.*
%{_bindir}/cairo-sphinx

%files dev
%doc ChangeLog PORTING_GUIDE
%dir %{_includedir}/cairo/
%{_includedir}/cairo/cairo-deprecated.h
%{_includedir}/cairo/cairo-features.h
%{_includedir}/cairo/cairo-ft.h
%{_includedir}/cairo/cairo.h
%{_includedir}/cairo/cairo-pdf.h
%{_includedir}/cairo/cairo-ps.h
%{_includedir}/cairo/cairo-script-interpreter.h
%{_includedir}/cairo/cairo-svg.h
%{_includedir}/cairo/cairo-tee.h
%{_includedir}/cairo/cairo-version.h
%{_includedir}/cairo/cairo-xlib-xrender.h
%{_includedir}/cairo/cairo-xlib.h
#%{_includedir}/cairo/cairo-gl.h
%{_includedir}/cairo/cairo-script.h
%{_includedir}/cairo/cairo-xcb.h
%{_libdir}/libcairo.so
%{_libdir}/libcairo-script-interpreter.so
%{_libdir}/pkgconfig/cairo-fc.pc
%{_libdir}/pkgconfig/cairo-ft.pc
%{_libdir}/pkgconfig/cairo.pc
%{_libdir}/pkgconfig/cairo-pdf.pc
%{_libdir}/pkgconfig/cairo-png.pc
%{_libdir}/pkgconfig/cairo-ps.pc
%{_libdir}/pkgconfig/cairo-svg.pc
%{_libdir}/pkgconfig/cairo-tee.pc
%{_libdir}/pkgconfig/cairo-xlib.pc
%{_libdir}/pkgconfig/cairo-xlib-xrender.pc
#%{_libdir}/pkgconfig/cairo-egl.pc
#%{_libdir}/pkgconfig/cairo-gl.pc
#%{_libdir}/pkgconfig/cairo-glx.pc
%{_libdir}/pkgconfig/cairo-script.pc
%{_libdir}/pkgconfig/cairo-xcb-shm.pc
%{_libdir}/pkgconfig/cairo-xcb.pc
%{_datadir}/gtk-doc/html/cairo

%files gobject
%{_libdir}/libcairo-gobject.so.*

%files gobject-dev
%{_includedir}/cairo/cairo-gobject.h
%{_libdir}/libcairo-gobject.so
%{_libdir}/pkgconfig/cairo-gobject.pc

%files tools
%{_bindir}/cairo-trace
%{_libdir}/cairo/

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.14.0-1
- Initial version based on f21
