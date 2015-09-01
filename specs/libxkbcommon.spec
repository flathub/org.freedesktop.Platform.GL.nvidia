Name:           libxkbcommon
Version:        0.5.0
Release:        1%{?dist}
Summary:        X.Org X11 XKB parsing library
License:        MIT
URL:            http://www.x.org

Source0:        http://xkbcommon.org/download/%{name}-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base
BuildRequires:  xorg-x11-util-macros
BuildRequires:  xorg-x11-proto-dev libX11-dev libxcb-dev
BuildRequires:  xkeyboard-config-dev

Requires:       xkeyboard-config

%description
%{name} is the X.Org library for compiling XKB maps into formats usable by
the X Server or other display servers.

%package dev
Summary:        X.Org X11 XKB parsing development package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description dev
X.Org X11 XKB parsing development package

%package x11
Summary:        X.Org X11 XKB keymap creation library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description x11
%{name}-x11 is the X.Org library for creating keymaps by querying the X
server.

%package x11-dev
Summary:        X.Org X11 XKB keymap creation library
Requires:       %{name}-x11%{?_isa} = %{version}-%{release}

%description x11-dev
X.Org X11 XKB keymap creation library development package

%prep
%setup -q -n %{name}-%{version}

autoreconf -v --install || exit 1

%build
%configure \
  --disable-silent-rules \
  --disable-static \
  --enable-x11

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

find $RPM_BUILD_ROOT -name '*.la' -exec rm -fv {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_libdir}/libxkbcommon.so.0.0.0
%{_libdir}/libxkbcommon.so.0

%files dev
%{_libdir}/libxkbcommon.so
%dir %{_includedir}/xkbcommon/
%{_includedir}/xkbcommon/xkbcommon.h
%{_includedir}/xkbcommon/xkbcommon-compat.h
%{_includedir}/xkbcommon/xkbcommon-compose.h
%{_includedir}/xkbcommon/xkbcommon-keysyms.h
%{_includedir}/xkbcommon/xkbcommon-names.h
%{_libdir}/pkgconfig/xkbcommon.pc

%post x11 -p /sbin/ldconfig
%postun x11 -p /sbin/ldconfig

%files x11
%{_libdir}/libxkbcommon-x11.so.0.0.0
%{_libdir}/libxkbcommon-x11.so.0

%files x11-dev
%{_libdir}/libxkbcommon-x11.so
%{_includedir}/xkbcommon/xkbcommon-x11.h
%{_libdir}/pkgconfig/xkbcommon-x11.pc

%changelog
* Mon Jan 19 2015 Alexander Larsson <alexl@redhat.com> - 0.5.0-1
- Initial version
