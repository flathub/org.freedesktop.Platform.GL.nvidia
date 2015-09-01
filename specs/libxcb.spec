%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:           libxcb
Version:        1.11
Release:        1%{?dist}
Summary:        A C binding to the X11 protocol

Group:          System Environment/Libraries
License:        MIT
URL:            http://xcb.freedesktop.org/
Source0:        http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2
# This is stolen straight from the pthread-stubs source:
# http://cgit.freedesktop.org/xcb/pthread-stubs/blob/?id=6900598192bacf5fd9a34619b11328f746a5956d
# we don't need the library because glibc has working pthreads, but we need
# the pkgconfig file so libs that link against libxcb know this...
Source1:	pthread-stubs.pc.in

BuildRequires:  freedesktop-sdk-base
BuildRequires:  libXau-dev
BuildRequires:  xcb-proto
BuildRequires:  xorg-x11-proto-dev
BuildRequires:  xorg-x11-util-macros

%description
The X protocol C-language Binding (XCB) is a replacement for Xlib featuring a
small footprint, latency hiding, direct access to the protocol, improved
threading support, and extensibility.

%package        dev
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    dev
The %{name}-dev package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation for %{name}
Group:          Documentation
BuildArch:	noarch

%description    doc
The %{name}-doc package contains documentation for the %{name} library.

%prep
%setup -q 

%build
sed -i 's/pthread-stubs //' configure.ac
autoreconf -v --install
%configure --disable-static --docdir=%{_pkgdocdir} \
	   --disable-selinux --enable-xkb --disable-xprint
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
install -pm 644 COPYING NEWS README $RPM_BUILD_ROOT%{_pkgdocdir}
sed 's,@libdir@,%{_libdir},;s,@prefix@,%{_prefix},;s,@exec_prefix@,%{_exec_prefix},' %{SOURCE1} > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/pthread-stubs.pc

find $RPM_BUILD_ROOT -name '*.la' -delete

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libxcb-composite.so.0*
%{_libdir}/libxcb-damage.so.0*
%{_libdir}/libxcb-dpms.so.0*
%{_libdir}/libxcb-dri2.so.0*
%{_libdir}/libxcb-dri3.so.0*
%{_libdir}/libxcb-glx.so.0*
%{_libdir}/libxcb-present.so.0*
%{_libdir}/libxcb-randr.so.0*
%{_libdir}/libxcb-record.so.0*
%{_libdir}/libxcb-render.so.0*
%{_libdir}/libxcb-res.so.0*
%{_libdir}/libxcb-screensaver.so.0*
%{_libdir}/libxcb-shape.so.0*
%{_libdir}/libxcb-shm.so.0*
%{_libdir}/libxcb-sync.so.1*
%{_libdir}/libxcb-xevie.so.0*
%{_libdir}/libxcb-xf86dri.so.0*
%{_libdir}/libxcb-xfixes.so.0*
%{_libdir}/libxcb-xinerama.so.0*
%{_libdir}/libxcb-xkb.so.1*
%{_libdir}/libxcb-xtest.so.0*
%{_libdir}/libxcb-xv.so.0*
%{_libdir}/libxcb-xvmc.so.0*
%{_libdir}/libxcb.so.1*

%files dev
%defattr(-,root,root,-)
%{_includedir}/xcb
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*.3*

%files doc
%defattr(-,root,root,-)
%{_pkgdocdir}

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.11-2
- Initial version based on f21
