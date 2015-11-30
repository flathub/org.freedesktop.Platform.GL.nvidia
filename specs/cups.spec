Summary: CUPS printing system
Name: cups
Version: 2.1.0
Release: 1%{?dist}
License: GPLv2
Url: http://www.cups.org/
Source0: http://www.cups.org/software/%{version}/cups-%{version}-source.tar.bz2

BuildRequires: freedesktop-sdk-base
BuildRequires: dbus-dev

%package dev
Summary: CUPS printing system - development environment
License: LGPLv2
Requires: %{name}%{?_isa} = %{version}-%{release}

%package ipptool
Summary: CUPS printing system - tool for performing IPP requests
Requires: %{name}%{?_isa} = %{version}-%{release}

%description
CUPS printing system provides a portable printing layer for
UNIX® operating systems. It has been developed by Apple Inc.
to promote a standard printing solution for all UNIX vendors and users.
CUPS provides the System V and Berkeley command-line interfaces.

%description dev
CUPS printing system provides a portable printing layer for
UNIX® operating systems. This is the development package for creating
additional printer drivers, and other CUPS services.

%description ipptool
Sends IPP requests to the specified URI and tests and/or displays the results.

%prep
%setup -q -n cups-%{version}

f=CREDITS.txt
mv "$f" "$f"~
iconv -f MACINTOSH -t UTF-8 "$f"~ > "$f"
rm -f "$f"~

aclocal -I config-scripts
autoconf -I config-scripts

%build
%configure \
           --disable-static \
           --with-docdir=%{_datadir}/%{name}/www \
           --enable-debug \
           --with-components=core \
           --with-dbusdir=%{_sysconfdir}/dbus-1 \
           --enable-avahi \
           --disable-systemd \
           --enable-threads \
           --enable-gnutls \
           localedir=%{_datadir}/locale

# If we got this far, all prerequisite libraries must be here.
make %{?_smp_mflags}

%install
make BUILDROOT=%{buildroot} install

find %{buildroot} -type f -o -type l | sed '
s:.*\('%{_datadir}'/\)\([^/_]\+\)\(.*\.po$\):%lang(\2) \1\2\3:
/^%lang(C)/d
/^\([^%].*\)/d
' > %{name}.lang

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc README.txt CREDITS.txt CHANGES.txt
%doc LICENSE.txt
%{_libdir}/*.so.*

%files dev
%{_bindir}/cups-config
%{_libdir}/*.so
%{_includedir}/cups
%{_datadir}/cups/ppdc/*.defs
%{_datadir}/cups/ppdc/*.h

%files ipptool
%{_bindir}/ipptool
%dir %{_datadir}/cups/ipptool
%{_datadir}/cups/ipptool/*

%changelog
* Mon Nov 30 2015 Alexander Larsson <alexl@redhat.com> - 2.1.0-1
- Initial version

