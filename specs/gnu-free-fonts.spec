%global fontname gnu-free
%global priority  69
%global fontconf %{priority}-%{fontname}
%global _fontdir %{_datadir}/fonts/%{fontname}
%global _fontconfig_templatedir %{_datadir}/fontconfig/conf.avail
%global _fontconfig_confdir %{_sysconfdir}/fonts/conf.d

Name:      %{fontname}-fonts
Version:   20120503
Release:   1%{?dist}
Summary:   Free UCS Outline Fonts

# Standard font exception
License:   GPLv3+ with exceptions
URL:       http://www.gnu.org/software/freefont/
Source0:   http://ftp.gnu.org/gnu/freefont/freefont-ttf-%{version}.zip
Source2:   %{fontconf}-mono.conf
Source3:   %{fontconf}-sans.conf
Source4:   %{fontconf}-serif.conf

BuildArch: noarch
BuildRequires: freedesktop-sdk-base

%description
Gnu FreeFont is a free family of scalable outline fonts, suitable for general
use on computers and for desktop publishing. It is Unicode-encoded for
compatibility with all modern operating systems.

Besides a full set of characters for writing systems based on the Latin
alphabet, FreeFont contains large selection of characters from other writing
systems some of which are hard to find elsewhere.

FreeFont also contains a large set of symbol characters, both technical and
decorative. We are especially pleased with the Mathematical Operators range,
with which most of the glyphs used in LaTeX can be displayed.

%prep
%setup -qn freefont-%{version}

%build

%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -p -m 644 *.ttf  %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE2} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-mono.conf

install -m 0644 -p %{SOURCE3} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-sans.conf

install -m 0644 -p %{SOURCE4} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-serif.conf

for fconf in %{fontconf}-mono.conf \
                %{fontconf}-sans.conf \
                %{fontconf}-serif.conf ; do
  ln -s %{_fontconfig_templatedir}/$fconf \
        %{buildroot}%{_fontconfig_confdir}/$fconf
done

%files
%doc AUTHORS ChangeLog
%dir %{_fontdir}
%{_fontdir}
%{_fontconfig_templatedir}/*
%{_fontconfig_confdir}/*

%changelog
* Mon Mar  9 2015 Alexander Larsson <alexl@redhat.com> - 20120503-1
- Initial version
