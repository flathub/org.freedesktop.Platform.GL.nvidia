%global fontname google-crosextra-caladea
%global fontconf62 62-%{fontname}
%global fontconf30 30-0-%{fontname}
%global _fontdir %{_datadir}/fonts/%{fontname}
%global _fontconfig_templatedir %{_datadir}/fontconfig/conf.avail
%global _fontconfig_confdir %{_sysconfdir}/fonts/conf.d

%global archivename crosextrafonts-20130214

Name:           %{fontname}-fonts
Version:        1.002
Release:        0.5.20130214%{?dist}
Summary:        Serif font metric-compatible with Cambria font

# License added in font as "otfinfo -i Caladea-Regular.ttf | grep License"
# also from http://code.google.com/p/chromium/issues/detail?id=280557
License:        ASL 2.0
URL:            http://code.google.com/p/chromium/issues/detail?id=168879
Source0:        http://gsdview.appspot.com/chromeos-localmirror/distfiles/%{archivename}.tar.gz
Source1:        30-0-%{fontname}-fontconfig.conf
Source2:        62-%{fontname}-fontconfig.conf

BuildArch:      noarch
BuildRequires:  freedesktop-sdk-base

%description
Caladea is metric-compatible with Cambria font. This font is a serif
typeface family based on Lato.

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
* Mon Mar  9 2015 Alexander Larsson <alexl@redhat.com> - 1.002-0.5.20130214
- Initial version
