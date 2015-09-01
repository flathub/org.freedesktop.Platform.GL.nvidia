%global fontname google-crosextra-carlito
%global fontconf62 62-%{fontname}
%global fontconf30 30-0-%{fontname}
%global _fontdir %{_datadir}/fonts/%{fontname}
%global _fontconfig_templatedir %{_datadir}/fontconfig/conf.avail
%global _fontconfig_confdir %{_sysconfdir}/fonts/conf.d

%global archivename crosextrafonts-carlito-20130920

Name:           %{fontname}-fonts
Version:        1.103
Release:        0.3.20130920%{?dist}
Summary:        Sans-serif font metric-compatible with Calibri font

License:        OFL
URL:            http://code.google.com/p/chromium/issues/detail?id=280557
Source0:        http://gsdview.appspot.com/chromeos-localmirror/distfiles/%{archivename}.tar.gz
Source1:        30-0-%{fontname}-fontconfig.conf
Source2:        62-%{fontname}-fontconfig.conf

BuildArch:      noarch
BuildRequires:  freedesktop-sdk-base

%description
Carlito is metric-compatible with Calibri font. Carlito comes in regular, bold,
italic, and bold italic. The family covers Latin-Greek-Cyrillic (not a 
complete set, though) with about 2,000 glyphs. It has the same character 
coverage as Calibri. This font is sans-serif typeface family based on Lato.

%prep
%setup -q -n %{archivename}

%build

%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p *.ttf %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf30}-fontconfig.conf
install -m 0644 -p %{SOURCE2} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf62}-fontconfig.conf

ln -s %{_fontconfig_templatedir}/%{fontconf30}-fontconfig.conf \
      %{buildroot}%{_fontconfig_confdir}/%{fontconf30}-fontconfig.conf
ln -s %{_fontconfig_templatedir}/%{fontconf62}-fontconfig.conf \
      %{buildroot}%{_fontconfig_confdir}/%{fontconf62}-fontconfig.conf

%files
%dir %{_fontdir}
%{_fontdir}
%{_fontconfig_templatedir}/*
%{_fontconfig_confdir}/*

%changelog
* Mon Mar  9 2015 Alexander Larsson <alexl@redhat.com> - 1.103-0.3.20130920
- Initial version
