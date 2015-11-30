Name:		xcb-util-wm
Version:	0.4.1
Release:	1%{?dist}
Summary:	Client and window-manager helper library on top of libxcb
Group:		System Environment/Libraries
License:	MIT
URL:		http://xcb.freedesktop.org
Source0:	http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2

BuildRequires:  freedesktop-sdk-base
BuildRequires:	libxcb-dev
BuildRequires:	xcb-util-dev

%description
XCB util-wm module provides the following libraries:

  - ewmh: Both client and window-manager helpers for EWMH.
  - icccm: Both client and window-manager helpers for ICCCM.

%package        dev
Summary:	Development and header files for xcb-util-vm
Group:		System Environment/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	dev
Development files for xcb-util-wm.

%prep
%setup -q

%build
%configure --with-pic --disable-static --disable-silent-rules
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
rm %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README COPYING
%{_libdir}/*.so.*

%files dev
%doc NEWS
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/xcb/*.h

%changelog
* Mon Nov 30 2015 Alexander Larsson <alexl@redhat.com> - 0.4.1-1
- Initial version
