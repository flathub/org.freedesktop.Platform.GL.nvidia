# Patented subpixel rendering disabled by default.
# Pass '--with subpixel_rendering' on rpmbuild command-line to enable.
%{!?_with_subpixel_rendering: %{!?_without_subpixel_rendering: %define _without_subpixel_rendering --without-subpixel_rendering}}

Summary: A free and portable font rendering engine
Name: freetype
Version: 2.5.5
Release: 1%{?dist}
License: (FTL or GPLv2+) and BSD and MIT and Public Domain and zlib with acknowledgement
Group: System Environment/Libraries
URL: http://www.freetype.org
Source:  http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.bz2

Patch21:  freetype-2.3.0-enable-spr.patch

# Enable otvalid and gxvalid modules
Patch46:  freetype-2.2.1-enable-valid.patch

Buildroot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)

BuildRequires:  freedesktop-sdk-base

Provides: %{name}-bytecode
%if %{?_with_subpixel_rendering:1}%{!?_with_subpixel_rendering:0}
Provides: %{name}-subpixel
%endif

%description
The FreeType engine is a free and portable font rendering
engine, developed to provide advanced font support for a variety of
platforms and environments. FreeType is a library which can open and
manages font files as well as efficiently load, hint and render
individual glyphs. FreeType is not a font server or a complete
text-rendering library.


%package dev
Summary: FreeType development libraries and header files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
The freetype-dev package includes the static libraries and header files
for the FreeType font rendering engine.

Install freetype-dev if you want to develop programs which will use
FreeType.


%prep
%setup -q

%if %{?_with_subpixel_rendering:1}%{!?_with_subpixel_rendering:0}
%patch21  -p1 -b .enable-spr
%endif

%patch46  -p1 -b .enable-valid

%build

%configure --disable-static \
           --with-zlib=yes \
           --with-bzip2=yes \
           --with-png=yes \
           --with-harfbuzz=no
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' builds/unix/libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' builds/unix/libtool
make %{?_smp_mflags}


%install
%makeinstall gnulocaledir=$RPM_BUILD_ROOT%{_datadir}/locale

# Don't package static a or .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.{a,la}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libfreetype.so.*
%doc README
%doc docs/LICENSE.TXT docs/FTL.TXT docs/GPLv2.TXT
%doc docs/CHANGES docs/VERSION.DLL docs/formats.txt

%files dev
%defattr(-,root,root)
%dir %{_includedir}/freetype2
%{_datadir}/aclocal/freetype2.m4
%{_includedir}/freetype2/*
%{_libdir}/libfreetype.so
%{_bindir}/freetype-config
%{_libdir}/pkgconfig/freetype2.pc
%{_mandir}/man1/*

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 2.5.3-1
- Initial version based on f21

