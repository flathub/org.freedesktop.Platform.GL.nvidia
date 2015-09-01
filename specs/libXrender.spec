Summary: X.Org X11 libXrender runtime library
Name: libXrender
Version: 0.9.8
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2

Requires: libX11

BuildRequires: freedesktop-sdk-base
BuildRequires: xorg-x11-util-macros
BuildRequires: libX11-dev

%description
X.Org X11 libXrender runtime library

%package dev
Summary: X.Org X11 libXrender development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description dev
X.Org X11 libXrender development package

%prep
%setup -q -n libXrender-%{version}

%build
autoreconf -v --install --force
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
# undo this, we'll add it ourselves in %%doc
rm $RPM_BUILD_ROOT/%{_docdir}/*/libXrender.txt

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_libdir}/libXrender.so.1
%{_libdir}/libXrender.so.1.3.0

%files dev
%defattr(-,root,root,-)
%doc doc/libXrender.txt
%{_includedir}/X11/extensions/Xrender.h
%{_libdir}/libXrender.so
%{_libdir}/pkgconfig/xrender.pc

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 0.9.8-1
- Initial version based on f21
