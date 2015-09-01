Name:           libproxy
Version:        0.4.11
Release:        1%{?dist}
Summary:        A library handling all the details of proxy configuration

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://code.google.com/p/libproxy/

Source0:        http://libproxy.googlecode.com/files/libproxy-%{version}%{?svn}.tar.gz
Patch3:         libproxy-0.4.11-fdleak.patch
Patch4:         libproxy-0.4.11-crash.patch

BuildRequires: freedesktop-sdk-base

%description
libproxy offers the following features:

    * extremely small core footprint (< 35K)
    * no external dependencies within libproxy core
      (libproxy plugins may have dependencies)
    * only 3 functions in the stable external API
    * dynamic adjustment to changing network topology
    * a standard way of dealing with proxy settings across all scenarios
    * a sublime sense of joy and accomplishment 


%package        bin
Summary:        Binary to test %{name}
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}

%description    bin
The %{name}-bin package contains the proxy binary for %{name}

%package        python
Summary:        Binding for %{name} and python
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description    python
The %{name}-python package contains the python binding for %{name}

%package        dev
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    dev
The %{name}-dev package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch3 -p1 -b .fdleak
%patch4 -p1 -b .crash

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
%{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;} \
/usr/bin/cmake \
        -DCMAKE_C_FLAGS_RELEASE:STRING="-DNDEBUG" \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="-DNDEBUG" \
        -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
        -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
        -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
        -DLIB_INSTALL_DIR:PATH=%{_libdir} \
        -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
        -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
        -DBUILD_SHARED_LIBS:BOOL=ON \
        -DMODULE_INSTALL_DIR=%{_libdir}/%{name}/%{version}/modules \
        -DWITH_PERL=OFF \
        -DWITH_GNOME3=OFF \
        .

make VERBOSE=1 %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

#In case all modules are disabled
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}/%{version}/modules

%{?_with_test:
%check
make test
}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/*.so.*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%dir %{_libdir}/%{name}/%{version}/modules

%files bin
%defattr(-,root,root,-)
%{_bindir}/proxy

%files python
%defattr(-,root,root,-)
%{python_sitelib}/*

%files dev
%defattr(-,root,root,-)
%{_includedir}/proxy.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libproxy-1.0.pc
%{_datadir}/cmake/Modules/Findlibproxy.cmake


%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 11 2013 Dan Winship <danw@redhat.com> - 0.4.11-8
- Really fix the JS_AbortIfWrongThread crash (#998232)

* Thu Sep 19 2013 Dan Winship <danw@redhat.com> - 0.4.11-7
- Fix file descriptor leak (#911066)
- Fix crash when pacrunner fails (probably because of EMFILE...) (#998232)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 David Woodhouse <David.Woodhouse@intel.com> - 0.4.11-5
- Add PacRunner module now that Fedora has PacRunner

* Mon Jun 03 2013 Colin Walters <walters@redhat.com> - 0.4.11-4
- Add patch to build with mozjs17, use it by default

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan  3 2013 Dan Winship <danw@redhat.com> - 0.4.11-2
- Minor dependency fixes

* Mon Dec 03 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.4.11-1
- Update to 0.4.11 -  CVE-2012-5580

* Tue Oct 16 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.4.10-1
- Update to 0.4.10
- Fix CVE-2012-4504

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 27 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.4.7-4
- Add upstream patches to use js rather than xulrunner
- Add patch to fix FTBFS on gcc 4.7
- Cleanup spec for latest updates and remove obsolete bits

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.4.7-2
- Rebuild for new libpng

* Tue Jun 07 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.4.7-1
- Update to 0.4.7
- libproxy-1.0.pc is now reliable starting with 0.4.7

* Tue Apr 12 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.4.7-0.1svn20110412
- Update to 0.4.7 svn20110412
- Add support for webkitgtk3
- Add support for xulrunner 2.0
- fix #683015 - libproxy fails with autoconfiguration
- fix #683018 - libproxy needs BR: NetworkManager-glib-dev  (f14)
- Manually fix libproxy-1.0.pc version field - #664781 / #674854

* Wed Nov 24 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.4.6-3
- Fix mozjs/webkit obsoletion - rhbz#656849
- Workaround unreliable Version field in pkg-config - rhbz#656484

* Sun Nov 07 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.4.6-1
- Update to 0.4.6
- Fix python module not arch dependant

* Mon Sep 06 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.4.5-2
- Update to 0.4.5
- Disable mozjs on fedora >= 15
- Disable webkit
- Add libproxy bootstrap option to disable modules.

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.4.4-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jul 13 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.4.4-6
- Fix libproxy-1.0.pc

* Mon Jul 05 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.4.4-5
- Re-enable mozjs and webkit

* Mon Jul 05 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.4.4-4
- Disable mozjs to get around a build error temporarily

* Mon Jul 05 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.4.4-3
- Disable webkit subpackage in order to resolve circular dep

* Sat Jul 03 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.4.4-2
- Fix missing BuildRequires: libmodman-dev

* Sun Jun 13 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.4.4-1
- Update to 0.4.4
- Removed install workarounds (fixed upstream)
- Removed patches (fixed upstream)
- Moved -python to noarch
- Downgrade cmake requirement (upstream change)
- Disabled perl bindings
- Run tests

* Thu Mar 11 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.3.1-4
- Add missing libXmu-dev

* Sun Feb 21 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.3.1-4
- Globalism and update gecko to 1.9.2
- Avoid rpath on _libdir
- Fix BR for kde4 to kdelibs-dev

* Sun Dec 27 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.3.1-1
- Update to 0.3.1
- Avoid dependecies on -python and -bin subpackages
- Create -networkmanager sub-package.

* Thu Sep 24 2009 kwizart < kwizart at gmail.com > - 0.3.0-1
- Update to 0.3.0

* Thu Sep 17 2009 kwizart < kwizart at gmail.com > - 0.2.3-12
- Remove Requirement of %%{name}-pac virtual provides 
  from the main package - #524043

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar  9 2009 kwizart < kwizart at gmail.com > - 0.2.3-10
- Rebuild for webkit
- Raise requirement for xulrunner to 1.9.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 kwizart < kwizart at gmail.com > - 0.2.3-8
- Merge NetworkManager module into the main libproxy package
- Main Requires the -python and -bin subpackage 
 (splitted for multilibs compliance).

* Fri Oct 24 2008 kwizart < kwizart at gmail.com > - 0.2.3-7
- Disable Gnome/KDE default support via builtin modules.
 (it needs to be integrated via Gconf2/neon instead).

* Tue Oct 21 2008 kwizart < kwizart at gmail.com > - 0.2.3-6
- Disable Obsoletes.
- Requires ev instead of evr for optionnals sub-packages.

* Tue Oct 21 2008 kwizart < kwizart at gmail.com > - 0.2.3-5
- Use conditionals build.

* Mon Sep 15 2008 kwizart < kwizart at gmail.com > - 0.2.3-4
- Remove plugin- in the name of the packages

* Mon Aug  4 2008 kwizart < kwizart at gmail.com > - 0.2.3-3
- Move proxy.h to libproxy/proxy.h
  This will prevent it to be included in the default include path
- Split main to libs and util and use libproxy to install all

* Mon Aug  4 2008 kwizart < kwizart at gmail.com > - 0.2.3-2
- Rename binding-python to python
- Add Requires: gecko-libs >= %%{gecko_version}
- Fix some descriptions
- Add plugin-webkit package
 
* Fri Jul 11 2008 kwizart < kwizart at gmail.com > - 0.2.3-1
- Convert to Fedora spec

* Fri Jun 6 2008 - dominique-rpm@leuenberger.net
- Updated to version 0.2.3
* Wed Jun 4 2008 - dominique-rpm@leuenberger.net
- Extended spec file to build all available plugins
* Tue Jun 3 2008 - dominique-rpm@leuenberger.net
- Initial spec file for Version 0.2.2

