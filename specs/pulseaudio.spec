%global pa_major   6.0
#global pa_minor   0

Name:           pulseaudio
Summary:        Improved Linux Sound Server
Version:        %{pa_major}%{?pa_minor:.%{pa_minor}}
Release:        1%{?dist}
License:        LGPLv2+
URL:            http://www.freedesktop.org/wiki/Software/PulseAudio
Source0:        http://freedesktop.org/software/pulseaudio/releases/pulseaudio-%{version}.tar.xz

Requires: freedesktop-platform-base
BuildRequires:  glib2-dev
BuildRequires:  gtk2-dev
BuildRequires:  xorg-x11-proto-dev
BuildRequires:  libXtst-dev
BuildRequires:  libXi-dev
BuildRequires:  libSM-dev
BuildRequires:  libX11-dev
BuildRequires:  libICE-dev
BuildRequires:  dbus-dev

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
PulseAudio is a sound server for Linux and other Unix like operating
systems. It is intended to be an improved drop-in replacement for the
Enlightened Sound Daemon (ESOUND).

%package libs
Summary:        Libraries for PulseAudio clients
License:        LGPLv2+
Obsoletes:      pulseaudio-libs-zeroconf < 1.1

%description libs
This package contains the runtime libraries for any application that wishes
to interface with a PulseAudio sound server.

%package libs-glib2
Summary:        GLIB 2.x bindings for PulseAudio clients
License:        LGPLv2+
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description libs-glib2
This package contains bindings to integrate the PulseAudio client library with
a GLIB 2.x based application.

%package libs-dev
Summary:        Headers and libraries for PulseAudio client development
License:        LGPLv2+
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs-glib2%{?_isa} = %{version}-%{release}
%description libs-dev
Headers and libraries for developing applications that can communicate with
a PulseAudio sound server.

%package esound-compat
Summary:        PulseAudio EsounD daemon compatibility script
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description esound-compat
A compatibility script that allows applications to call /usr/bin/esd
and start PulseAudio with EsounD protocol modules.

%package module-x11
Summary:        X11 support for the PulseAudio sound server
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-utils

%description module-x11
X11 bell and security modules for the PulseAudio sound server.

%package utils
Summary:        PulseAudio sound server utilities
License:        LGPLv2+
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
# when made non-multilib'd, https://bugzilla.redhat.com/891425
Obsoletes:      pulseaudio-utils < 3.0-3

%description utils
This package contains command line utilities for the PulseAudio sound server.


%prep
%setup -q -n %{name}-%{version}

NOCONFIGURE=1 ./bootstrap.sh

%build

%configure \
  --disable-static \
  --disable-rpath \
  --with-system-user=pulse \
  --with-system-group=pulse \
  --with-access-group=pulse-access \
  --disable-oss-output \
  --disable-jack \
  --disable-lirc \
  --disable-bluez4 \
  --disable-bluez5 \
  --disable-systemd

# we really should preopen here --preopen-mods=module-udev-detect.la, --force-preopen
make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

## unpackaged files
# extraneous libtool crud
rm -fv $RPM_BUILD_ROOT%{_libdir}/*.la $RPM_BUILD_ROOT%{_libdir}/pulse-%{pa_major}/modules/*.la

%find_lang %{name}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README LICENSE GPL LGPL
%dir %{_sysconfdir}/pulse/
%config(noreplace) %{_sysconfdir}/pulse/daemon.conf
%config(noreplace) %{_sysconfdir}/pulse/default.pa
%config(noreplace) %{_sysconfdir}/pulse/system.pa
%{_sysconfdir}/dbus-1/system.d/pulseaudio-system.conf
%dir %{_sysconfdir}/bash_completion.d/
%{_sysconfdir}/bash_completion.d/pa*
%{_sysconfdir}/bash_completion.d/pulseaudio
%{_datadir}/zsh/site-functions/_pulseaudio
%{_bindir}/pulseaudio
%{_libdir}/libpulsecore-%{pa_major}.so
%dir %{_libdir}/pulse-%{pa_major}/
%dir %{_libdir}/pulse-%{pa_major}/modules/
%{_libdir}/pulse-%{pa_major}/modules/libcli.so
%{_libdir}/pulse-%{pa_major}/modules/libprotocol-cli.so
%{_libdir}/pulse-%{pa_major}/modules/libprotocol-esound.so
%{_libdir}/pulse-%{pa_major}/modules/libprotocol-http.so
%{_libdir}/pulse-%{pa_major}/modules/libprotocol-native.so
%{_libdir}/pulse-%{pa_major}/modules/libprotocol-simple.so
%{_libdir}/pulse-%{pa_major}/modules/librtp.so
%if 0%{?with_webrtc}
%{_libdir}/pulse-%{pa_major}/modules/libwebrtc-util.so
%endif
%{_libdir}/pulse-%{pa_major}/modules/module-cli-protocol-tcp.so
%{_libdir}/pulse-%{pa_major}/modules/module-cli-protocol-unix.so
%{_libdir}/pulse-%{pa_major}/modules/module-cli.so
%{_libdir}/pulse-%{pa_major}/modules/module-combine.so
%{_libdir}/pulse-%{pa_major}/modules/module-combine-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-dbus-protocol.so
%{_libdir}/pulse-%{pa_major}/modules/module-filter-apply.so
%{_libdir}/pulse-%{pa_major}/modules/module-filter-heuristics.so
%{_libdir}/pulse-%{pa_major}/modules/module-device-manager.so
%{_libdir}/pulse-%{pa_major}/modules/module-loopback.so
%{_libdir}/pulse-%{pa_major}/modules/module-esound-compat-spawnfd.so
%{_libdir}/pulse-%{pa_major}/modules/module-esound-compat-spawnpid.so
%{_libdir}/pulse-%{pa_major}/modules/module-esound-protocol-tcp.so
%{_libdir}/pulse-%{pa_major}/modules/module-esound-protocol-unix.so
%{_libdir}/pulse-%{pa_major}/modules/module-esound-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-http-protocol-tcp.so
%{_libdir}/pulse-%{pa_major}/modules/module-http-protocol-unix.so
%{_libdir}/pulse-%{pa_major}/modules/module-match.so
%{_libdir}/pulse-%{pa_major}/modules/module-mmkbd-evdev.so
%{_libdir}/pulse-%{pa_major}/modules/module-native-protocol-fd.so
%{_libdir}/pulse-%{pa_major}/modules/module-native-protocol-tcp.so
%{_libdir}/pulse-%{pa_major}/modules/module-native-protocol-unix.so
%{_libdir}/pulse-%{pa_major}/modules/module-null-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-null-source.so
%{_libdir}/pulse-%{pa_major}/modules/module-pipe-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-pipe-source.so
%{_libdir}/pulse-%{pa_major}/modules/module-remap-source.so
%{_libdir}/pulse-%{pa_major}/modules/module-rescue-streams.so
%{_libdir}/pulse-%{pa_major}/modules/module-role-ducking.so
%{_libdir}/pulse-%{pa_major}/modules/module-rtp-recv.so
%{_libdir}/pulse-%{pa_major}/modules/module-rtp-send.so
%{_libdir}/pulse-%{pa_major}/modules/module-simple-protocol-tcp.so
%{_libdir}/pulse-%{pa_major}/modules/module-simple-protocol-unix.so
%{_libdir}/pulse-%{pa_major}/modules/module-sine.so
%{_libdir}/pulse-%{pa_major}/modules/module-switch-on-port-available.so
%{_libdir}/pulse-%{pa_major}/modules/module-tunnel-sink-new.so
%{_libdir}/pulse-%{pa_major}/modules/module-tunnel-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-tunnel-source-new.so
%{_libdir}/pulse-%{pa_major}/modules/module-tunnel-source.so
%{_libdir}/pulse-%{pa_major}/modules/module-volume-restore.so
%{_libdir}/pulse-%{pa_major}/modules/module-suspend-on-idle.so
%{_libdir}/pulse-%{pa_major}/modules/module-default-device-restore.so
%{_libdir}/pulse-%{pa_major}/modules/module-device-restore.so
%{_libdir}/pulse-%{pa_major}/modules/module-stream-restore.so
%{_libdir}/pulse-%{pa_major}/modules/module-card-restore.so
%{_libdir}/pulse-%{pa_major}/modules/module-ladspa-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-remap-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-always-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-console-kit.so
%{_libdir}/pulse-%{pa_major}/modules/module-position-event-sounds.so
%{_libdir}/pulse-%{pa_major}/modules/module-augment-properties.so
%{_libdir}/pulse-%{pa_major}/modules/module-role-cork.so
%{_libdir}/pulse-%{pa_major}/modules/module-sine-source.so
%{_libdir}/pulse-%{pa_major}/modules/module-intended-roles.so
%{_libdir}/pulse-%{pa_major}/modules/module-rygel-media-server.so
%{_libdir}/pulse-%{pa_major}/modules/module-echo-cancel.so
%{_libdir}/pulse-%{pa_major}/modules/module-switch-on-connect.so
%{_libdir}/pulse-%{pa_major}/modules/module-virtual-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-virtual-source.so
%{_libdir}/pulse-%{pa_major}/modules/module-virtual-surround-sink.so
%{_libdir}/pulse-%{pa_major}/modules/libraop.so
%{_libdir}/pulse-%{pa_major}/modules/module-detect.so
%{_libdir}/pulse-%{pa_major}/modules/module-raop-sink.so

%{_mandir}/man1/pulseaudio.1*
%{_mandir}/man5/default.pa.5*
%{_mandir}/man5/pulse-cli-syntax.5*
%{_mandir}/man5/pulse-client.conf.5*
%{_mandir}/man5/pulse-daemon.conf.5*

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs -f %{name}.lang
%doc README LICENSE GPL LGPL
%dir %{_sysconfdir}/pulse/
%config(noreplace) %{_sysconfdir}/pulse/client.conf
%{_libdir}/libpulse.so.0*
%{_libdir}/libpulse-simple.so.0*
%dir %{_libdir}/pulseaudio/
%{_libdir}/pulseaudio/libpulsecommon-%{pa_major}.*
%{_libdir}/pulseaudio/libpulsedsp.*

%post libs-glib2 -p /sbin/ldconfig
%postun libs-glib2 -p /sbin/ldconfig

%files libs-glib2
%{_libdir}/libpulse-mainloop-glib.so.0*

%files libs-dev
%{_includedir}/pulse/
%{_libdir}/libpulse.so
%{_libdir}/libpulse-mainloop-glib.so
%{_libdir}/libpulse-simple.so
%{_libdir}/pkgconfig/libpulse*.pc
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/libpulse.vapi
%{_datadir}/vala/vapi/libpulse.deps
%{_datadir}/vala/vapi/libpulse-simple.vapi
%{_datadir}/vala/vapi/libpulse-simple.deps
%{_datadir}/vala/vapi/libpulse-mainloop-glib.vapi
%{_datadir}/vala/vapi/libpulse-mainloop-glib.deps
%dir %{_libdir}/cmake
%{_libdir}/cmake/PulseAudio/

%files esound-compat
%{_bindir}/esdcompat
%{_mandir}/man1/esdcompat.1.gz

%files module-x11
%{_sysconfdir}/xdg/autostart/pulseaudio.desktop
%{_bindir}/start-pulseaudio-x11
%{_libdir}/pulse-%{pa_major}/modules/module-x11-bell.so
%{_libdir}/pulse-%{pa_major}/modules/module-x11-publish.so
%{_libdir}/pulse-%{pa_major}/modules/module-x11-xsmp.so
%{_libdir}/pulse-%{pa_major}/modules/module-x11-cork-request.so
%{_mandir}/man1/start-pulseaudio-x11.1.gz

%files utils
%{_bindir}/pacat
%{_bindir}/pacmd
%{_bindir}/pactl
%{_bindir}/paplay
%{_bindir}/parec
%{_bindir}/pamon
%{_bindir}/parecord
%{_bindir}/pax11publish
%{_bindir}/padsp
%ifarch %{multilib_archs}
%{_bindir}/padsp-32
%endif
%{_bindir}/pasuspender
%{_mandir}/man1/pacat.1.gz
%{_mandir}/man1/pacmd.1.gz
%{_mandir}/man1/pactl.1.gz
%{_mandir}/man1/paplay.1.gz
%{_mandir}/man1/pasuspender.1.gz
%{_mandir}/man1/padsp.1.gz
%{_mandir}/man1/pax11publish.1.gz

%changelog
* Thu Dec 11 2014 Alexander Larsson <alexl@redhat.com> - 5.0-1
- Initial version
