%global pkg desktop-file-utils
%global pkgname desktop-file-utils

Summary: Utilities for manipulating .desktop files
Name: desktop-file-utils
Version: 0.22
Release: 1%{?dist}
URL: http://www.freedesktop.org/software/desktop-file-utils
Source0: http://www.freedesktop.org/software/desktop-file-utils/releases/%{name}-%{version}.tar.xz
License: GPLv2+
Group: Development/Tools

BuildRequires: freedesktop-sdk-base
BuildRequires: glib2-dev

%description
.desktop files are used to describe an application for inclusion in
GNOME or KDE menus.  This package contains desktop-file-validate which
checks whether a .desktop file complies with the specification at
http://www.freedesktop.org/standards/, and desktop-file-install
which installs a desktop file to the standard directory, optionally
fixing it up in the process.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%files
%doc AUTHORS COPYING README NEWS
%{_bindir}/*
%{_mandir}/man1/desktop-file-install.1.gz
%{_mandir}/man1/desktop-file-validate.1.gz
%{_mandir}/man1/update-desktop-database.1.gz
%{_mandir}/man1/desktop-file-edit.1.gz

%changelog
* Tue Nov 25 2014 Alexander Larsson <alexl@redhat.com> - 0.22-1
- Initial version, based on F21
