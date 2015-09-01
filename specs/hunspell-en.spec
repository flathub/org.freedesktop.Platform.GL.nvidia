Name: hunspell-en
Summary: English hunspell dictionaries
%define upstreamid 20121024
Version: 0.%{upstreamid}
Release: 1%{?dist}
#svn export https://wordlist.svn.sourceforge.net/svnroot/wordlist/trunk wordlist
Source0: http://pkgs.fedoraproject.org/repo/pkgs/hunspell-en/wordlist-%{upstreamid}.tar.xz/10a7ff0b2209af7d22b14b219b98c9b5/wordlist-%{upstreamid}.tar.xz
Source1: http://pkgs.fedoraproject.org/repo/pkgs/hunspell-en/en_GB.zip/218909136738f4564b81ecd145ade6ee/en_GB.zip
#See http://mxr.mozilla.org/mozilla/source/extensions/spellcheck/locales/en-US/hunspell/mozilla_words.diff?raw=1
Patch0: mozilla_words.patch
Patch1: en_GB-singleletters.patch
Patch2: en_GB.two_initial_caps.patch
#See http://sourceforge.net/tracker/?func=detail&aid=2355344&group_id=10079&atid=1014602
#filter removes words with "." in them
Patch3: en_US-strippedabbrevs.patch
#See https://sourceforge.net/tracker/?func=detail&aid=2987192&group_id=143754&atid=756397
#to allow "didn't" instead of suggesting change to typographical apostrophe
Patch4: hunspell-en-allow-non-typographical.marks.patch
#See https://sourceforge.net/tracker/?func=detail&aid=3012183&group_id=10079&atid=1014602
#See https://bugzilla.redhat.com/show_bug.cgi?id=619577 add SI and IEC prefixes
Patch5: hunspell-en-SI_and_IEC.patch
#See https://sourceforge.net/tracker/?func=detail&aid=3175662&group_id=10079&atid=1014602 obscure Calender hides misspelling of Calendar
Patch6: hunspell-en-calender.patch
#valid English words that are archaic or rare in en-GB but not in en-IE
Patch7: en_IE.supplemental.patch
Group: Applications/Text
URL: http://wordlist.sourceforge.net/
License: LGPLv2+ and LGPLv2 and BSD
BuildArch: noarch
BuildRequires: freedesktop-sdk-base
BuildRequires: aspell
Requires: hunspell
Requires: hunspell-en-US = %{version}-%{release}
Requires: hunspell-en-GB = %{version}-%{release}

%description
English (US, UK, etc.) hunspell dictionaries

%package US
Requires: hunspell
Summary: US English hunspell dictionaries
Group: Applications/Text

%description US
US English hunspell dictionaries

%package GB
Requires: hunspell
Summary: UK English hunspell dictionaries
Group: Applications/Text

%description GB
UK English hunspell dictionaries

%prep
%setup -q -n wordlist
%setup -q -T -D -a 1 -n wordlist
%patch0 -p1 -b .mozilla
%patch1 -p1 -b .singleletters
%patch2 -p1 -b .two_initial_cap
%patch3 -p1 -b .strippedabbrevs
%patch4 -p1 -b .allow-non-typographical
%patch5 -p1 -b .SI_and_IEC
%patch6 -p1 -b .calender
%patch7 -p1 -b .en_IE

%build
make
cd scowl/speller
make hunspell
for i in README_en_CA.txt README_en_US.txt; do
  if ! iconv -f utf-8 -t utf-8 -o /dev/null $i > /dev/null 2>&1; then
    iconv -f ISO-8859-1 -t UTF-8 $i > $i.new
    touch -r $i $i.new
    mv -f $i.new $i
  fi
  tr -d '\r' < $i > $i.new
  touch -r $i $i.new
  mv -f $i.new $i
done

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p en_*.dic en_*.aff $RPM_BUILD_ROOT/%{_datadir}/myspell
cd scowl/speller
cp -p en_*.dic en_*.aff $RPM_BUILD_ROOT/%{_datadir}/myspell

pushd $RPM_BUILD_ROOT/%{_datadir}/myspell/
en_GB_aliases="en_AG en_AU en_BS en_BW en_BZ en_DK en_GH en_HK en_IE en_IN en_JM en_MW en_NA en_NG en_NZ en_SG en_TT en_ZA en_ZM en_ZW"
for lang in $en_GB_aliases; do
	ln -s en_GB.aff $lang.aff
	ln -s en_GB.dic $lang.dic
done
en_US_aliases="en_PH"
for lang in $en_US_aliases; do
	ln -s en_US.aff $lang.aff
	ln -s en_US.dic $lang.dic
done
popd

%files
%defattr(-,root,root,-)
%doc scowl/speller/README_en_CA.txt
%{_datadir}/myspell/*
%exclude %{_datadir}/myspell/en_GB.*
%exclude %{_datadir}/myspell/en_US.*

%files US
%defattr(-,root,root,-)
%doc scowl/speller/README_en_US.txt
%{_datadir}/myspell/en_US.*

%files GB
%defattr(-,root,root,-)
%doc README_en_GB.txt
%{_datadir}/myspell/en_GB.*

%changelog
* Thu Jan 22 2015 Alexander Larsson <alexl@redhat.com> - 0.20121024-9
- Initial version
