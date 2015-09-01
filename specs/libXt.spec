%global tarball libXt

Summary: X.Org X11 libXt runtime library
Name: libXt
Version: 1.1.4
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2

Requires: libX11%{?_isa}

BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-dev
BuildRequires: libSM-dev
BuildRequires: libX11-dev
BuildRequires: libICE-dev

%description
X.Org X11 libXt runtime library

%package dev
Summary: X.Org X11 libXt development package
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description dev
X.Org X11 libXt development package

%prep
%setup -q -n %{tarball}-%{version}

%build
autoreconf -v --install --force
# FIXME: Work around pointer aliasing warnings from compiler for now
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure --disable-static \
  --with-xfile-search-path="%{_sysconfdir}/X11/%%L/%%T/%%N%%C%%S:%{_sysconfdir}/X11/%%l/%%T/\%%N%%C%%S:%{_sysconfdir}/X11/%%T/%%N%%C%%S:%{_sysconfdir}/X11/%%L/%%T/%%N%%S:%{_sysconfdir}/X\11/%%l/%%T/%%N%%S:%{_sysconfdir}/X11/%%T/%%N%%S:%{_datadir}/X11/%%L/%%T/%%N%%C%%S:%{_datadir}/X1\1/%%l/%%T/%%N%%C%%S:%{_datadir}/X11/%%T/%%N%%C%%S:%{_datadir}/X11/%%L/%%T/%%N%%S:%{_datadir}/X11/%%\l/%%T/%%N%%S:%{_datadir}/X11/%%T/%%N%%S"

V=1 make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p -m 0755 $RPM_BUILD_ROOT%{_datadir}/X11/app-defaults
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# adding to installed docs in order to avoid using %%doc magic
cp -p COPYING ${RPM_BUILD_ROOT}%{_datadir}/doc/%{name}/COPYING

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/libXt.so.6
%{_libdir}/libXt.so.6.0.0
%dir %{_datadir}/X11/app-defaults
# not using %%doc because of side-effect (#1001246)
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/COPYING

%files dev
%{_docdir}/%{name}/*.xml
%{_includedir}/X11/CallbackI.h
%{_includedir}/X11/Composite.h
%{_includedir}/X11/CompositeP.h
%{_includedir}/X11/ConstrainP.h
%{_includedir}/X11/Constraint.h
%{_includedir}/X11/ConvertI.h
%{_includedir}/X11/Core.h
%{_includedir}/X11/CoreP.h
%{_includedir}/X11/CreateI.h
%{_includedir}/X11/EventI.h
%{_includedir}/X11/HookObjI.h
%{_includedir}/X11/InitialI.h
%{_includedir}/X11/Intrinsic.h
%{_includedir}/X11/IntrinsicI.h
%{_includedir}/X11/IntrinsicP.h
%{_includedir}/X11/Object.h
%{_includedir}/X11/ObjectP.h
%{_includedir}/X11/PassivGraI.h
%{_includedir}/X11/RectObj.h
%{_includedir}/X11/RectObjP.h
%{_includedir}/X11/ResConfigP.h
%{_includedir}/X11/ResourceI.h
%{_includedir}/X11/SelectionI.h
%{_includedir}/X11/Shell.h
%{_includedir}/X11/ShellI.h
%{_includedir}/X11/ShellP.h
%{_includedir}/X11/StringDefs.h
%{_includedir}/X11/ThreadsI.h
%{_includedir}/X11/TranslateI.h
%{_includedir}/X11/VarargsI.h
%{_includedir}/X11/Vendor.h
%{_includedir}/X11/VendorP.h
%{_includedir}/X11/Xtos.h
%{_libdir}/libXt.so
%{_libdir}/pkgconfig/xt.pc
%{_mandir}/man3/*.3*

%changelog
* Thu Jan  8 2015 Alexander Larsson <alexl@redhat.com> - 1.1.4-1
- Initial version
