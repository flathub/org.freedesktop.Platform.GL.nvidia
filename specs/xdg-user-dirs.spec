Name:		xdg-user-dirs
Version:	0.15
Release:	1%{?dist}
Summary:	Handles user special directories

Group:		User Interface/Desktops
License:	GPLv2+ and MIT
URL:		http://freedesktop.org/wiki/Software/xdg-user-dirs
Source0:	http://user-dirs.freedesktop.org/releases/%{name}-%{version}.tar.gz

BuildRequires: freedesktop-sdk-base

%description
Contains xdg-user-dirs-update that updates folders in a users
homedirectory based on the defaults configured by the administrator.

%prep
%setup -q

%build
%configure --disable-documentation
make %{?_smp_mflags} SUBDIRS=po

%install
make install DESTDIR=$RPM_BUILD_ROOT SUBDIRS=po

%find_lang %name

%files -f %{name}.lang
%doc NEWS AUTHORS README COPYING
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/xdg/user-dirs.conf
%config(noreplace) %{_sysconfdir}/xdg/user-dirs.defaults

%changelog
* Tue Sep 22 2015 Alexander Larsson <alexl@redhat.com> - 0.15-1
- Initial version
