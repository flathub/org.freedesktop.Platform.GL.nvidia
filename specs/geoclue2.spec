Name:           geoclue2
Version:        2.2.0
Release:        1%{?dist}
Summary:        Geolocation service

License:        GPLv2+
URL:            http://www.freedesktop.org/wiki/Software/GeoClue/
Source0:        http://www.freedesktop.org/software/geoclue/releases/2.2/geoclue-%{version}.tar.xz

BuildRequires:  freedesktop-sdk-base
BuildRequires:  glib2-dev
BuildRequires:  itstool
BuildRequires:  json-glib-dev
BuildRequires:  libsoup-dev

%description
Geoclue is a D-Bus service that provides location information. The primary goal
of the Geoclue project is to make creating location-aware applications as
simple as possible, while the secondary goal is to ensure that no application
can access location information without explicit permission from user.

%package        dev
Summary:        Development files for %{name}

%description    dev
The %{name}-dev package contains files for developing applications that
use %{name}.

%package        demos
Summary:        Demo applications for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    demos
The %{name}-demos package contains demo applications that use %{name}.

%prep
%setup -q -n geoclue-%{version}

%build
%configure --with-dbus-service-user=geoclue --disable-modem-gps-source --disable-3g-source --disable-cdma-source --disable-demo-agent
make %{?_smp_mflags} V=1

%install
%make_install

%files
%doc COPYING NEWS
%config %{_sysconfdir}/geoclue/
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.GeoClue2.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.GeoClue2.Agent.conf
%{_libexecdir}/geoclue
%{_datadir}/dbus-1/system-services/org.freedesktop.GeoClue2.service

%files dev
%{_datadir}/dbus-1/interfaces/org.freedesktop.GeoClue2*.xml
%{_libdir}/pkgconfig/geoclue-2.0.pc

%files demos
%{_libexecdir}/geoclue-2.0/demos/where-am-i
%{_datadir}/applications/geoclue-demo-agent.desktop
%{_datadir}/applications/geoclue-where-am-i.desktop

%changelog
* Mon Sep  7 2015 Alexander Larsson <alexl@redhat.com> - 2.2.0-1
- initial version
