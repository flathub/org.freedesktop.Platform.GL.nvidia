Summary: stub for gtk-doc
Name: gtk-doc-stub
Version: 0.1
Release: 1%{?dist}
License: GPLv2+ and GFDL
Group: Development/Tools
#VCS: git:git://git.gnome.org/gtk-doc-stub
Source: gtk-doc-stub.tar.gz

BuildRequires: freedesktop-sdk-base

BuildArch: noarch
URL: http://www.gtk.org/gtk-doc

Provides: gtk-doc

%description
gtk-doc-stub can be used to build things without gtk-doc
and its dependencies

%prep
%setup -q -n gtk-doc-stub

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

mkdir -p $RPM_BUILD_ROOT%{_datadir}/gtk-doc/html
# We don't need this
rm -rf  $RPM_BUILD_ROOT/%{_datadir}/gobject-introspection-1.0

%files
%defattr(-, root, root,-)
%doc COPYING
%{_bindir}/*
%{_datadir}/aclocal/*
%{_datadir}/gtk-doc-devel/

%changelog
* Fri Nov  7 2014 Alexander Larsson <alexl@redhat.com> - 0.1-1
- Initial version
