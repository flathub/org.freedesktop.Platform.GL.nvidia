Name:           harfbuzz
Version:        0.9.40
Release:        1%{?dist}
Summary:        Text shaping library

License:        MIT
URL:            http://freedesktop.org/wiki/Software/HarfBuzz
Source0:        http://www.freedesktop.org/software/harfbuzz/release/harfbuzz-%{version}.tar.bz2

BuildRequires:  freedesktop-sdk-base
BuildRequires:  cairo-dev
BuildRequires:  freetype-dev
BuildRequires:  glib2-dev
BuildRequires:  graphite2-dev

%description
HarfBuzz is an implementation of the OpenType Layout engine.


%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-icu%{?_isa} = %{version}-%{release}

%description    dev
The %{name}-dev package contains libraries and header files for
developing applications that use %{name}.

%package        icu
Summary:        Harfbuzz ICU support library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    icu
This package contains Harfbuzz ICU support library.

%prep
%setup -q


%build
%configure --disable-static --with-graphite2

# Remove lib64 rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post icu -p /sbin/ldconfig
%postun icu -p /sbin/ldconfig


%files
%doc NEWS AUTHORS COPYING README
%{_libdir}/libharfbuzz.so.*

%files dev
%doc %{_datadir}/gtk-doc
%{_bindir}/hb-view
%{_bindir}/hb-ot-shape-closure
%{_bindir}/hb-shape
%{_includedir}/harfbuzz/
%{_libdir}/libharfbuzz.so
%{_libdir}/pkgconfig/harfbuzz.pc
%{_libdir}/libharfbuzz-icu.so
%{_libdir}/pkgconfig/harfbuzz-icu.pc

%files icu
%{_libdir}/libharfbuzz-icu.so.*

%changelog
* Wed Nov 12 2014 Alexander Larsson <alexl@redhat.com> - 0.9.34-1
- Initial version based on F21
