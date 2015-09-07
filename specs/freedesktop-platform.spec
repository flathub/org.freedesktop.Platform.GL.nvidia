Name:           freedesktop-platform
Version:        1.2
Release:        1%{?dist}
Summary:        Freedesktop platform

License: Various
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

BuildRequires: freedesktop-platform-base

BuildRequires: dbus-libs
BuildRequires: dejavu-fonts
BuildRequires: desktop-file-utils
BuildRequires: glib2
BuildRequires: gnu-free-fonts
BuildRequires: gobject-introspection
BuildRequires: google-crosextra-caladea-fonts
BuildRequires: google-crosextra-carlito-fonts
BuildRequires: gstreamer1
BuildRequires: gstreamer1-plugins-base
BuildRequires: hicolor-icon-theme
BuildRequires: libICE-dev
BuildRequires: libXpm
BuildRequires: libXv
BuildRequires: libXxf86vm-dev
BuildRequires: libepoxy-dev
BuildRequires: liberation-fonts
BuildRequires: libproxy
BuildRequires: mesa-libGL
BuildRequires: pulseaudio-libs-dev
BuildRequires: xkeyboard-config-dev
BuildRequires: SDL2
BuildRequires: SDL2_image
BuildRequires: SDL2_net
BuildRequires: SDL2_ttf
BuildRequires: SDL2_mixer
BuildRequires: hunspell
BuildRequires: hunspell-en
BuildRequires: harfbuzz

Requires: freedesktop-platform-base

Requires: cairo
Requires: cairo-gobject
Requires: dbus
Requires: dbus-libs
Requires: dejavu-fonts
Requires: desktop-file-utils
Requires: fontconfig
Requires: glib2
Requires: gnu-free-fonts
Requires: gobject-introspection
Requires: google-crosextra-caladea-fonts
Requires: google-crosextra-carlito-fonts
Requires: graphite2
Requires: gstreamer1
Requires: gstreamer1-plugins-base
Requires: harfbuzz
Requires: harfbuzz-icu
Requires: hicolor-icon-theme
Requires: hunspell
Requires: hunspell-en
Requires: libICE
Requires: libSM
Requires: libX11
Requires: libXScrnSaver
Requires: libXau
Requires: libXcomposite
Requires: libXcursor
Requires: libXdamage
Requires: libXext
Requires: libXfixes
Requires: libXft
Requires: libXi
Requires: libXinerama
Requires: libXpm
Requires: libXrandr
Requires: libXrender
Requires: libXt
Requires: libXtst
Requires: libXv
Requires: libXxf86vm
Requires: libepoxy
Requires: liberation-fonts
Requires: libproxy
Requires: libwayland-client
Requires: libwayland-cursor
Requires: libwayland-server
Requires: libxcb
Requires: libxkbcommon
Requires: libxkbcommon-x11
Requires: libxshmfence
Requires: mesa-dri-drivers
Requires: mesa-libEGL
Requires: mesa-libGL
Requires: mesa-libwayland-egl
Requires: orc-dev
Requires: pulseaudio-libs
Requires: pulseaudio-libs-glib2
Requires: shared-mime-info
Requires: xkeyboard-config
Requires: SDL2
Requires: SDL2_image
Requires: SDL2_net
Requires: SDL2_ttf
Requires: SDL2_mixer

%description
Meta package for Freedesktop platform dependencies

%prep


%build

%install
# Need empty machine-id to bind mount over
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/
touch $RPM_BUILD_ROOT%{_sysconfdir}/machine-id

%files
%doc
%{_sysconfdir}/machine-id

%changelog
* Fri Nov  7 2014 Alexander Larsson <alexl@redhat.com>
- Initial version
