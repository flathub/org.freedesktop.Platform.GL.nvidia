Name:		xcb-util-cursor
Version:	0.1.2
Release:	1%{?dist}
Summary:	Cursor library on top of libxcb
Group:		System Environment/Libraries
License:	MIT
URL:		http://xcb.freedesktop.org
Source0:	http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2

BuildRequires:  freedesktop-sdk-base
BuildRequires:	libxcb-dev
BuildRequires:	xcb-util-dev
BuildRequires:	xcb-util-image-dev
BuildRequires:	xcb-util-renderutil-dev

%description
XCB util-cursor module provides the following libraries:

  - cursor: port of libxcursor

%package        dev
Summary:	Development and header files for xcb-util-cursos
Group:		System Environment/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	dev
Development files for xcb-util-cursor.

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
%doc README
%license COPYING
%{_libdir}/*.so.*

%files dev
%doc NEWS
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/xcb/*.h

%changelog
* Mon Nov 30 2015 Alexander Larsson <alexl@redhat.com> - 0.1.2-1
- Initial version
