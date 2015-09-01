%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')
%global bin_version 2.10.0

Summary: The GIMP ToolKit (GTK+), a library for creating GUIs for X
Name: gtk2
Version: 2.24.28
Release: 1%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
URL: http://www.gtk.org
#VCS: git:git://git.gnome.org/gtk+#gtk-2-24
Source: http://download.gnome.org/sources/gtk+/%{release_version}/gtk+-%{version}.tar.xz
Source3: im-cedilla.conf

BuildRequires: freedesktop-sdk-base
BuildRequires: atk-dev
BuildRequires: glib2-dev
BuildRequires: cairo-dev
BuildRequires: gdk-pixbuf2-dev
BuildRequires: pango-dev
BuildRequires: libXi-dev
#BuildRequires: cups-dev
BuildRequires: libXrandr-dev
BuildRequires: libXrender-dev
BuildRequires: libXcursor-dev
BuildRequires: libXfixes-dev
BuildRequires: libXinerama-dev
BuildRequires: libXcomposite-dev
BuildRequires: libXdamage-dev
BuildRequires: gobject-introspection-dev
BuildRequires: gtk-doc-stub

# required for icon theme apis to work
Requires: hicolor-icon-theme

# We need to prereq these so we can run gtk-query-immodules-2.0
Requires(post): glib2 >= %{glib2_version}
Requires(post): atk >= %{atk_version}
Requires(post): pango >= %{pango_version}
# and these for gdk-pixbuf-query-loaders
Requires: libXrandr >= %{xrandr_version}

%description
GTK+ is a multi-platform toolkit for creating graphical user
interfaces. Offering a complete set of widgets, GTK+ is suitable for
projects ranging from small one-off tools to complete application
suites.

%package immodules
Summary: Input methods for GTK+
Group: System Environment/Libraries
Requires: gtk2 = %{version}-%{release}

%description immodules
The gtk2-immodules package contains standalone input methods that are shipped
as part of GTK+.

%package immodule-xim
Summary: XIM support for GTK+
Group: System Environment/Libraries
Requires: gtk2 = %{version}-%{release}

%description immodule-xim
The gtk2-immodule-xim package contains XIM support for GTK+.

%package dev
Summary: Development files for GTK+
Group: Development/Libraries
Requires: gtk2 = %{version}-%{release}
Requires: pango-dev
Requires: atk-dev
Requires: glib2-dev
Requires: gdk-pixbuf2-dev
Requires: cairo-dev
Requires: libX11-dev, libXcursor-dev, libXinerama-dev
Requires: libXext-dev, libXi-dev, libXrandr-dev
Requires: libXfixes-dev, libXcomposite-dev
Requires: pkgconfig

%description dev
This package contains the libraries and header files that are needed
for writing applications with the GTK+ widget toolkit. If you plan
to develop applications with GTK+, consider installing the gtk2-dev-docs
package.

%package dev-docs
Summary: Developer documentation for GTK+
Group: Development/Libraries
Requires: gtk2 = %{version}-%{release}
#BuildArch: noarch

%description dev-docs
This package contains developer documentation for the GTK+ widget toolkit.

%prep
%setup -q -n gtk+-%{version}


%build
%configure \
        --disable-gtk-doc \
        --disable-man            \
	--with-xinput=xfree	\
	--enable-debug

# fight unused direct deps
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool

make %{?_smp_mflags}

# truncate NEWS
awk '/^Overview of Changes/ { seen+=1 }
{ if (seen < 2) print }
{ if (seen == 2) { print "For older news, see http://git.gnome.org/cgit/gtk+/plain/NEWS"; exit } }' NEWS > tmp; mv tmp NEWS

%install
make install DESTDIR=$RPM_BUILD_ROOT        \
             RUN_QUERY_IMMODULES_TEST=false

%find_lang gtk20
%find_lang gtk20-properties

# Input method frameworks want this
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinput.d
cp %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinput.d

# Remove unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/%{bin_version}/*/*.la

touch $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/%{bin_version}/immodules.cache

mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/immodules
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/%{bin_version}/filesystems

# We use the gtk3 version of this:
rm $RPM_BUILD_ROOT%{_bindir}/gtk-update-icon-cache

%post
/sbin/ldconfig
gtk-query-immodules-2.0 --update-cache

%post immodules
gtk-query-immodules-2.0 --update-cache

%post immodule-xim
gtk-query-immodules-2.0 --update-cache

%postun
/sbin/ldconfig
if [ $1 -gt 0 ]; then
  gtk-query-immodules-2.0 --update-cache
fi

%postun immodules
gtk-query-immodules-2.0 --update-cache

%postun immodule-xim
gtk-query-immodules-2.0 --update-cache

%files -f gtk20.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/gtk-query-immodules-2.0
%{_libdir}/libgtk-x11-2.0.so.*
%{_libdir}/libgdk-x11-2.0.so.*
%{_libdir}/libgailutil.so.*
%dir %{_libdir}/gtk-2.0
%dir %{_libdir}/gtk-2.0/%{bin_version}
%{_libdir}/gtk-2.0/%{bin_version}/engines
%{_libdir}/gtk-2.0/%{bin_version}/filesystems
%dir %{_libdir}/gtk-2.0/%{bin_version}/immodules
%{_libdir}/gtk-2.0/%{bin_version}/printbackends
%{_libdir}/gtk-2.0/modules
%{_libdir}/gtk-2.0/immodules
%dir %{_datadir}/gtk-2.0
%{_datadir}/themes/Default
%{_datadir}/themes/Emacs
%{_datadir}/themes/Raleigh
%ghost %{_libdir}/gtk-2.0/%{bin_version}/immodules.cache
%{_libdir}/girepository-1.0

%files immodules
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-am-et.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-cedilla.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-cyrillic-translit.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-inuktitut.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-ipa.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-multipress.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-thai.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-ti-er.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-ti-et.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-viqr.so
%{_sysconfdir}/X11/xinit/xinput.d/im-cedilla.conf
%dir %{_sysconfdir}/gtk-2.0
%config(noreplace) %{_sysconfdir}/gtk-2.0/im-multipress.conf

%files immodule-xim
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-xim.so

%files dev -f gtk20-properties.lang
%{_libdir}/lib*.so
%{_libdir}/gtk-2.0/include
%{_includedir}/*
%{_datadir}/aclocal/*
%{_bindir}/gtk-builder-convert
%{_libdir}/pkgconfig/*
%{_bindir}/gtk-demo
%{_datadir}/gtk-2.0/demo
%{_datadir}/gir-1.0

%files dev-docs
%{_datadir}/gtk-doc

%changelog
* Fri Nov 21 2014 Alexander Larsson <alexl@redhat.com> - 2.24.25-1
- Initial version, based on F21
