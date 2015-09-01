Summary:	Font configuration and customization library
Name:		fontconfig
Version:	2.11.93
Release:	1%{?dist}
# src/ftglue.[ch] is in Public Domain
# src/fccache.c contains Public Domain code
# fc-case/CaseFolding.txt is in the UCD
# otherwise MIT
License:	MIT and Public Domain and UCD
Group:		System Environment/Libraries
Source:		http://fontconfig.org/release/%{name}-%{version}.tar.bz2
Source2:	fontconfig-xdg-app.conf
URL:		http://fontconfig.org

# https://bugzilla.redhat.com/show_bug.cgi?id=140335
Patch0:		%{name}-sleep-less.patch

BuildRequires:  freedesktop-sdk-base
BuildRequires:	freetype-dev

Requires(pre):	freetype

%description
Fontconfig is designed to locate fonts within the
system and select them according to requirements specified by
applications.

%package	dev
Summary:	Font configuration and customization library
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	freetype-dev >= %{freetype_version}

%description	dev
The fontconfig-dev package includes the header files,
and developer docs for the fontconfig package.

Install fontconfig-dev if you want to develop programs which
will use fontconfig.

%package	dev-doc
Summary:	Development Documentation files for fontconfig library
Group:		Documentation
BuildArch:	noarch
Requires:	%{name}-dev = %{version}-%{release}

%description	dev-doc
The fontconfig-dev-doc package contains the documentation files
which is useful for developing applications that uses fontconfig.

%prep
%setup -q
%patch0 -p1 -b .sleep-less

%build
# We don't want to rebuild the docs, but we want to install the included ones.
export HASDOCBOOK=no

%configure	--disable-static

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# move installed doc files back to build directory to package themm
# in the right place
mv $RPM_BUILD_ROOT%{_docdir}/fontconfig/* .
rmdir $RPM_BUILD_ROOT%{_docdir}/fontconfig/

rm -f $RPM_BUILD_ROOT/etc/fonts/fonts.conf.bak

install -m 0644 -p -T %{SOURCE2} $RPM_BUILD_ROOT/etc/fonts/conf.d/50-xdg-app.conf

%check
make check

%post
/sbin/ldconfig

umask 0022

mkdir -p %{_localstatedir}/cache/fontconfig

# Force regeneration of all fontconfig cache files
# The check for existance is needed on dual-arch installs (the second
#  copy of fontconfig might install the binary instead of the first)
# The HOME setting is to avoid problems if HOME hasn't been reset
if [ -x /usr/bin/fc-cache ] && /usr/bin/fc-cache --version 2>&1 | grep -q %{version} ; then
  HOME=/root /usr/bin/fc-cache -f
fi

%postun -p /sbin/ldconfig

%files
%doc README AUTHORS COPYING
%doc fontconfig-user.txt fontconfig-user.html
%{_libdir}/libfontconfig.so.*
%{_bindir}/fc-cache
%{_bindir}/fc-cat
%{_bindir}/fc-list
%{_bindir}/fc-match
%{_bindir}/fc-pattern
%{_bindir}/fc-query
%{_bindir}/fc-scan
%{_bindir}/fc-validate
%{_datadir}/fontconfig/*/*.conf
%{_datadir}/xml/fontconfig
# fonts.conf is not supposed to be modified.
# If you want to do so, you should use local.conf instead.
%config /etc/fonts/fonts.conf
/etc/fonts/conf.d/README
%config(noreplace) /etc/fonts/conf.d/*.conf
%dir %{_localstatedir}/cache/fontconfig
%{_mandir}/man1/*
%{_mandir}/man5/*

%files dev
%{_libdir}/libfontconfig.so
%{_libdir}/pkgconfig/*
%{_includedir}/fontconfig
%{_mandir}/man3/*

%files dev-doc
%doc fontconfig-devel.txt fontconfig-devel

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 2.11.1-1
- Initial version based on f21

