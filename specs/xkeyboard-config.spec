# INFO: Package contains data-only, no binaries, so no debuginfo is needed
%define debug_package %{nil}

Summary:    X Keyboard Extension configuration data
Name:       xkeyboard-config
Version:    2.13
Release:    1%{?dist}
License:    MIT
URL:        http://www.freedesktop.org/wiki/Software/XKeyboardConfig

Source0:    http://xorg.freedesktop.org/archive/individual/data/%{name}/%{name}-%{version}.tar.bz2

BuildArch:  noarch

BuildRequires: freedesktop-sdk-base
BuildRequires: glib2-dev
BuildRequires: libX11-dev
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-dev
#BuildRequires: xkbcomp


%description
This package contains configuration data used by the X Keyboard Extension (XKB),
which allows selection of keyboard layouts when using a graphical interface.

%package dev
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}

%description dev
Development files for %{name}.

%prep
%setup -q -n %{name}-%{version}

%build
AUTOPOINT="intltoolize --automake --copy" autoreconf -v --force --install || exit 1
%configure \
    --enable-compat-rules \
    --with-xkb-base=%{_datadir}/X11/xkb \
    --with-xkb-rules-symlink=xorg

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# Remove unnecessary symlink
rm -f $RPM_BUILD_ROOT%{_datadir}/X11/xkb/compiled
%find_lang %{name} 

# Create filelist
{
   FILESLIST=${PWD}/files.list
   pushd $RPM_BUILD_ROOT
   find .%{_datadir}/X11/xkb -type d | sed -e "s/^\./%dir /g" > $FILESLIST
   find .%{_datadir}/X11/xkb -type f | sed -e "s/^\.//g" >> $FILESLIST
   popd
}

%files -f files.list -f %{name}.lang
%doc AUTHORS README NEWS TODO COPYING docs/README.* docs/HOWTO.*
%{_datadir}/X11/xkb/rules/xorg
%{_datadir}/X11/xkb/rules/xorg.lst
%{_datadir}/X11/xkb/rules/xorg.xml
%{_mandir}/man7/xkeyboard-config.*

%files dev
%{_datadir}/pkgconfig/xkeyboard-config.pc

%changelog
* Mon Jan 19 2015 Alexander Larsson <alexl@redhat.com> - 2.13-1
- Initial version

