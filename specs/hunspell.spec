Name:      hunspell
Summary:   A spell checker and morphological analyzer library
Version:   1.3.3
Release:   1%{?dist}
Source:    http://downloads.sourceforge.net/%{name}/hunspell-%{version}.tar.gz
Group:     System Environment/Libraries
URL:       http://hunspell.sourceforge.net/
License:   LGPLv2+ or GPLv2+ or MPLv1.1

BuildRequires: freedesktop-sdk-base
Requires:  hunspell-en-US

%description
Hunspell is a spell checker and morphological analyzer library and program 
designed for languages with rich morphology and complex word compounding or 
character encoding. Hunspell interfaces: Ispell-like terminal interface using 
Curses library, Ispell pipe interface, OpenOffice.org UNO module.

%package dev
Requires: hunspell = %{version}-%{release}, pkgconfig
Summary: Files for developing with hunspell
Group: Development/Libraries

%description dev
Includes and definitions for developing with hunspell

%prep
%setup -q

%build
configureflags="--disable-rpath --disable-static --with-ui --with-readline"

%configure $configureflags
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
mkdir $RPM_BUILD_ROOT/%{_datadir}/myspell
%find_lang %{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README README.myspell COPYING COPYING.LGPL COPYING.MPL AUTHORS AUTHORS.myspell license.hunspell license.myspell THANKS
%{_libdir}/*.so.*
%{_datadir}/myspell
%{_bindir}/hunspell
%{_mandir}/man1/hunspell.1*
%lang(hu) %{_mandir}/hu/man1/hunspell.1*

%files dev
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_libdir}/*.so
%{_bindir}/affixcompress
%{_bindir}/makealias
%{_bindir}/munch
%{_bindir}/unmunch
%{_bindir}/analyze
%{_bindir}/chmorph
%{_bindir}/hzip
%{_bindir}/hunzip
%{_bindir}/ispellaff2myspell
%{_bindir}/wordlist2hunspell
%{_bindir}/wordforms
%{_libdir}/pkgconfig/hunspell.pc
%{_mandir}/man1/hunzip.1*
%{_mandir}/man1/hzip.1*
%{_mandir}/man3/hunspell.3*
%{_mandir}/man5/hunspell.5*

%changelog
* Thu Jan 22 2015 Alexander Larsson <alexl@redhat.com> - 1.3.3-1
- Initial version

