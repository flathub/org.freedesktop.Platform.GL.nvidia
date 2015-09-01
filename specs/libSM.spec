Summary: X.Org X11 SM runtime library
Name: libSM
Version: 1.2.2
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: freedesktop-sdk-base
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-dev
BuildRequires: xorg-x11-xtrans-dev
BuildRequires: libICE-dev

%description
The X.Org X11 SM (Session Management) runtime library.

%package dev
Summary: X.Org X11 SM development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
The X.Org X11 SM (Session Management) development package.

%prep
%setup -q

%build
autoreconf -v --install --force

%configure --with-libuuid --disable-static
make %{_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# we %%doc these ourselves, later, and only the text versions
rm -rf $RPM_BUILD_ROOT%{_docdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog
%{_libdir}/libSM.so.6
%{_libdir}/libSM.so.6.*

%files dev
%defattr(-,root,root,-)
%dir %{_includedir}/X11/SM
%{_includedir}/X11/SM/SM.h
%{_includedir}/X11/SM/SMlib.h
%{_includedir}/X11/SM/SMproto.h
%{_libdir}/libSM.so
%{_libdir}/pkgconfig/sm.pc

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.2.2-1
- Initial version based on f21
