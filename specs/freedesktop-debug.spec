Name:           freedesktop-debug
Version:        0.1
Release:        1%{?dist}
Summary:        Freedesktop sdk debug info

License: Various
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

BuildRequires: freedesktop-sdk

Requires: cairo-debuginfo
Requires: dbus-debuginfo
Requires: fontconfig-debuginfo
Requires: freetype-debuginfo
Requires: glib2-debuginfo
Requires: gobject-introspection-debuginfo
Requires: graphite2-debuginfo
Requires: gstreamer1-debuginfo
Requires: gstreamer1-plugins-base-debuginfo
Requires: harfbuzz-debuginfo
Requires: hunspell-debuginfo
Requires: llvm-debuginfo
Requires: libICE-debuginfo
Requires: libX11-debuginfo
Requires: libXScrnSaver-debuginfo
Requires: libXau-debuginfo
Requires: libXcomposite-debuginfo
Requires: libXcursor-debuginfo
Requires: libXdamage-debuginfo
Requires: libXdmcp-debuginfo
Requires: libXext-debuginfo
Requires: libXfixes-debuginfo
Requires: libXft-debuginfo
Requires: libXi-debuginfo
Requires: libXinerama-debuginfo
Requires: libXpm-debuginfo
Requires: libXrandr-debuginfo
Requires: libXrender-debuginfo
Requires: libXt-debuginfo
Requires: libXtst-debuginfo
Requires: libXv-debuginfo
Requires: libXxf86vm-debuginfo
Requires: libepoxy-debuginfo
Requires: libproxy-debuginfo
Requires: wayland-debuginfo
Requires: libxcb-debuginfo
Requires: libxkbcommon-debuginfo
Requires: mesa-debuginfo
Requires: orc-debuginfo
Requires: pixman-debuginfo
Requires: pulseaudio-debuginfo
Requires: SDL2-debuginfo
Requires: SDL2_image-debuginfo
Requires: SDL2_net-debuginfo
Requires: SDL2_ttf-debuginfo
Requires: SDL2_mixer-debuginfo

%description
Meta package for debug info

%prep


%build


%install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm/
mkdir -p $RPM_BUILD_ROOT%{_libdir}/debug

%files
%doc
%{_libdir}/debug

%changelog
* Fri Nov  7 2014 Alexander Larsson <alexl@redhat.com>
- Initial version
