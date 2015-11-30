Name:		xcb-util
Version:	0.4.0
Release:	1%{?dist}
Summary:	Convenience libraries sitting on top of libxcb
Group:		System Environment/Libraries
License:	MIT
URL:		http://xcb.freedesktop.org
Source0:	http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2
BuildRequires:  freedesktop-sdk-base
BuildRequires:	libxcb-dev


%description
The xcb-util module provides a number of libraries which sit on top of
libxcb, the core X protocol library, and some of the extension
libraries. These experimental libraries provide convenience functions
and interfaces which make the raw X protocol more usable. Some of the
libraries also provide client-side code which is not strictly part of
the X protocol but which have traditionally been provided by Xlib.


%package        dev
Summary:	Development and header files for xcb-util
Group:		System Environment/Libraries
Requires:	%{name}%{?isa} = %{version}-%{release}

%description	dev
Development files for xcb-util.


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
%{_libdir}/libxcb-util.so.1*


%files dev
%doc NEWS
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/xcb/*.h


%changelog
* Mon Nov 30 2015 Alexander Larsson <alexl@redhat.com> - 0.4.0-1
- Initial version
