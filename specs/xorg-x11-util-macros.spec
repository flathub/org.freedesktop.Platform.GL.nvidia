%define pkgname util-macros
%define debug_package %{nil}

Summary: X.Org X11 Autotools macros
Name: xorg-x11-util-macros
Version: 1.19.0
Release: 1%{?dist}
License: MIT
Group: Development/System
URL: http://www.x.org
BuildArch: noarch
Source0:  ftp://ftp.x.org/pub/individual/util/util-macros-%{version}.tar.bz2

BuildRequires: freedesktop-sdk-base

%description
X.Org X11 autotools macros required for building the various packages that
comprise the X Window System.

%prep
%setup -q -n %{pkgname}-%{version}

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog
%{_datadir}/aclocal/xorg-macros.m4
%{_datadir}/pkgconfig/xorg-macros.pc
%{_datadir}/util-macros

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.19.0-1
- Initial version based on f21
