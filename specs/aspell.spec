Summary: Spell checker
Name: aspell
Version: 0.60.6.1
Release: 1%{?dist}
# LGPLv2+ .. common/gettext.h
# LGPLv2  .. modules/speller/default/phonet.hpp,
#            modules/speller/default/phonet.cpp,
#            modules/speller/default/affix.cpp
# GPLv2+  .. ltmain.sh, misc/po-filter.c
# BSD     .. myspell/munch.c
License: LGPLv2+ and LGPLv2 and GPLv2+ and BSD
Group: Applications/Text
URL: http://aspell.net/
Source: ftp://ftp.gnu.org/gnu/aspell/aspell-%{version}.tar.gz

BuildRequires: freedesktop-sdk-base

%description
GNU Aspell is a spell checker designed to eventually replace Ispell. It can
either be used as a library or as an independent spell checker. Its main
feature is that it does a much better job of coming up with possible
suggestions than just about any other spell checker out there for the
English language, including Ispell and Microsoft Word. It also has many
other technical enhancements over Ispell such as using shared memory for
dictionaries and intelligently handling personal dictionaries when more
than one Aspell process is open at once.

%package dev
Summary: Libraries and header files for Aspell development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description dev
The aspell-dev package includes libraries
and header files needed for Aspell development.

%prep
%setup -q
iconv -f iso-8859-2 -t utf-8 < manual/aspell.info > manual/aspell.info.aux
mv manual/aspell.info.aux manual/aspell.info

%build
%configure --disable-rpath
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags}
cp scripts/aspell-import examples/aspell-import
chmod 644 examples/aspell-import
cp manual/aspell-import.1 examples/aspell-import.1

%install
# make install DESTDIR=$RPM_BUILD_ROOT doesn't work
%makeinstall

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60

mv ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/ispell ${RPM_BUILD_ROOT}%{_bindir}
mv ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/spell ${RPM_BUILD_ROOT}%{_bindir}

chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//nroff-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//sgml-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//context-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//email-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//tex-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//texinfo-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_bindir}/aspell
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/libpspell.so.*

rm -f ${RPM_BUILD_ROOT}%{_libdir}/libaspell.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libpspell.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/*-filter.la
rm -f ${RPM_BUILD_ROOT}%{_bindir}/aspell-import
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/aspell-import.1

%find_lang %{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc README TODO COPYING examples/aspell-import examples/aspell-import.1
%dir %{_libdir}/aspell-0.60
%{_bindir}/a*
%{_bindir}/ispell
%{_bindir}/pr*
%{_bindir}/run-with-aspell
%{_bindir}/spell
%{_bindir}/word-list-compress
%{_libdir}/lib*.so.*
%{_libdir}/aspell-0.60/*
%{_infodir}/aspell.*
%{_mandir}/man1/aspell.1*
%{_mandir}/man1/run-with-aspell.1*
%{_mandir}/man1/word-list-compress.1*
%{_mandir}/man1/prezip-bin.1*

%files dev
%dir %{_includedir}/pspell
%{_bindir}/pspell-config
%{_includedir}/aspell.h
%{_includedir}/pspell/pspell.h
%{_libdir}/lib*spell.so
%{_infodir}/aspell-dev.*
%{_mandir}/man1/pspell-config.1*

%changelog
* Thu Jan 22 2015 Alexander Larsson <alexl@redhat.com> - 0.60.6.1-1
- Initial version
