Summary: Sample Authorization Protocol for X
Name: libXau
Version: 1.0.8
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: freedesktop-sdk-base
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-dev

%description
This is a very simple mechanism for providing individual access to an X Window
System display.It uses existing core protocol and library hooks for specifying
authorization data in the connection setup block to restrict use of the display
to only those clients that show that they know a server-specific key 
called a "magic cookie".

%package dev
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: xorg-x11-proto-dev
BuildRequires: xorg-x11-proto-dev

%description dev
X.Org X11 libXau development package

%prep
%setup -q

%build
autoreconf -v --install --force

%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ChangeLog
%{_libdir}/libXau.so.6
%{_libdir}/libXau.so.6.0.0

%files dev
%defattr(-,root,root,-)
%{_includedir}/X11/Xauth.h
%{_libdir}/libXau.so
%{_libdir}/pkgconfig/xau.pc
#%dir %{_mandir}/man3x
%{_mandir}/man3/*.3*

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.0.8-1
- Initial version based on f21
