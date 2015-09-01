Name:           graphite2
Version:        1.2.4
Release:        1%{?dist}
Summary:        Font rendering capabilities for complex non-Roman writing systems
Group:          Development/Tools

License:        (LGPLv2+ or GPLv2+ or MPL) and (Netscape or GPLv2+ or LGPLv2+)
URL:            http://sourceforge.net/projects/silgraphite/
Source0:        http://downloads.sourceforge.net/silgraphite/graphite2-%{version}.tgz

BuildRequires: freedesktop-sdk-base
BuildRequires: freetype-dev

%description
Graphite2 is a project within SIL’s Non-Roman Script Initiative and Language
Software Development groups to provide rendering capabilities for complex
non-Roman writing systems. Graphite can be used to create “smart fonts” capable
of displaying writing systems with various complex behaviors. With respect to
the Text Encoding Model, Graphite handles the "Rendering" aspect of writing
system implementation.

%package dev
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: Files for developing with graphite2
Group: Development/Libraries

%description dev
Includes and definitions for developing with graphite2.

%prep
%setup -q

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
%{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;} \
/usr/bin/cmake \
        -DCMAKE_C_FLAGS_RELEASE:STRING="-DNDEBUG" \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="-DNDEBUG" \
        -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
        -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
        -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
        -DLIB_INSTALL_DIR:PATH=%{_libdir} \
        -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
        -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
        -DBUILD_SHARED_LIBS:BOOL=ON \
        -DGRAPHITE2_COMPARE_RENDERER=OFF  .

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

%check
ctest

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE COPYING ChangeLog
%{_bindir}/gr2fonttest
%{_libdir}/libgraphite2.so.3
%{_libdir}/libgraphite2.so.3.0.1

%files dev
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/graphite2-release.cmake
%{_datadir}/%{name}/graphite2.cmake
%{_includedir}/%{name}
%{_libdir}/libgraphite2.so
%{_libdir}/pkgconfig/graphite2.pc

%changelog
* Wed Nov 12 2014 Alexander Larsson <alexl@redhat.com> - 1.2.4-1
- Initial version based on F21
