%define debug_package %{nil}
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}

Name:           xcb-proto
Version:        1.11
Release:        1%{?dist}
Summary:        XCB protocol descriptions

Group:          Development/Libraries
License:        MIT
URL:            http://xcb.freedesktop.org/
Source0:        http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2
BuildArch:      noarch

BuildRequires: freedesktop-sdk-base

%description
XCB is a project to enable efficient language bindings to the X11 protocol.
This package contains the protocol descriptions themselves.  Language
bindings use these protocol descriptions to generate code for marshalling
the protocol.

%prep
%setup -q

%build
# Bit of a hack to get the pc file in /usr/share, so we can be noarch.
%configure --libdir=%{_datadir}
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING NEWS README TODO doc/xml-xcb.txt
%{_datadir}/pkgconfig/xcb-proto.pc
%dir %{_datadir}/xcb/
%{_datadir}/xcb/*.xsd
%{_datadir}/xcb/*.xml
%{python_sitelib}/xcbgen

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.11-1
- Initial version based on f21
