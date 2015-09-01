%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

# NOTE: This package contains only C source and header files and pkg-config
# *.pc files, and does not contain any ELF binaries or DSOs, so we disable
# debuginfo generation.
%define debug_package %{nil}

Summary: X.Org X11 developmental X transport library
Name: xorg-x11-xtrans-dev
Version: 1.3.5
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org
BuildArch: noarch

Source0: http://xorg.freedesktop.org/archive/individual/lib/xtrans-%{version}.tar.bz2

# Fedora specific patch
Patch1: xtrans-1.0.3-avoid-gethostname.patch

BuildRequires: freedesktop-sdk-base
BuildRequires: xorg-x11-util-macros

%description
X.Org X11 developmental X transport library

%prep
%setup -q -n xtrans-%{version}
%patch1 -p1 -b .my-name-is-unix

%build
# yes, this looks horrible, but it's to get the .pc file in datadir
%configure --libdir=%{_datadir} --docdir=%{_pkgdocdir}
# Running 'make' not needed.

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
install -pm 644 AUTHORS ChangeLog COPYING README $RPM_BUILD_ROOT%{_pkgdocdir}

%files
%{_pkgdocdir}
%dir %{_includedir}/X11
%dir %{_includedir}/X11/Xtrans
%{_includedir}/X11/Xtrans/Xtrans.c
%{_includedir}/X11/Xtrans/Xtrans.h
%{_includedir}/X11/Xtrans/Xtransint.h
%{_includedir}/X11/Xtrans/Xtranslcl.c
%{_includedir}/X11/Xtrans/Xtranssock.c
%{_includedir}/X11/Xtrans/Xtransutil.c
%{_includedir}/X11/Xtrans/transport.c
%{_datadir}/aclocal/xtrans.m4
%{_datadir}/pkgconfig/xtrans.pc

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.3.5-1
- Initial version based on f21
