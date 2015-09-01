Summary: Basic requirement for icon themes
Name: hicolor-icon-theme
Version: 0.15
Release: 1%{?dist}
License: GPL+
Group: User Interface/Desktops
URL: http://icon-theme.freedesktop.org/wiki/HicolorTheme
Source: http://icon-theme.freedesktop.org/releases/%{name}-%{version}.tar.xz
BuildArch: noarch

BuildRequires: freedesktop-sdk-base

%description
Contains the basic directories and files needed for icon theme support.

%prep
%setup -q

# for some reason this file is executable in the tarball
chmod 0644 COPYING

%build
%configure

%install
make DESTDIR=$RPM_BUILD_ROOT PREFIX=/usr install

touch $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/icon-theme.cache

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(-,root,root,-)
%doc README COPYING ChangeLog
%{_datadir}/icons/hicolor
%ghost %{_datadir}/icons/hicolor/icon-theme.cache

%changelog
* Wed Nov 12 2014 Alexander Larsson <alexl@redhat.com> - 0.13-1
- Initial version based on F21
