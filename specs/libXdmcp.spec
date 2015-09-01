Summary: X Display Manager Control Protocol library
Name: libXdmcp
Version: 1.1.1
Release: 7%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires:  freedesktop-sdk-base
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-dev

%description
X Display Manager Control Protocol library.

%package dev
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
libXdmcp development package.

%prep
%setup -q

%build
autoreconf -v --install --force
%configure --disable-static
make V=1 %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# manual fixup later
rm -rf $RPM_BUILD_ROOT%{_docdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog Wraphelp.README.crypto
%{_libdir}/libXdmcp.so.6
%{_libdir}/libXdmcp.so.6.0.0

%files dev
%defattr(-,root,root,-)
%doc README
%{_includedir}/X11/Xdmcp.h
%{_libdir}/libXdmcp.so
%{_libdir}/pkgconfig/xdmcp.pc

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.1.1-7
- Initial version based on f21
