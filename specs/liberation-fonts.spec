%global priority  59
%global fontname liberation
%global fontconf %{priority}-%{fontname}
%global archivename %{name}-ttf-%{version}
%global _fontdir %{_datadir}/fonts/%{fontname}
%global _fontconfig_templatedir %{_datadir}/fontconfig/conf.avail
%global _fontconfig_confdir %{_sysconfdir}/fonts/conf.d

Name:             %{fontname}-fonts
Summary:          Fonts to replace commonly used Microsoft Windows fonts
Version:          2.00.1
Release:          1%{?dist}

# The license of the Liberation Fonts is a EULA that contains GPLv2 and two
# exceptions:
# The first exception is the standard FSF font exception.
# The second exception is an anti-lockdown clause somewhat like the one in
# GPLv3. This license is Free, but GPLv2 and GPLv3 incompatible.
License:          Liberation
Group:            User Interface/X
URL:              http://fedorahosted.org/liberation-fonts/
Source0:          https://fedorahosted.org/releases/l/i/liberation-fonts/%{archivename}.tar.gz
Source2:          %{name}-mono.conf
Source3:          %{name}-sans.conf
Source4:          %{name}-serif.conf
Source5:          %{name}-narrow.conf

BuildArch:        noarch
BuildRequires: freedesktop-sdk-base

%description
The Liberation Fonts are intended to be replacements for the three most
commonly used fonts on Microsoft systems: Times New Roman, Arial, and Courier
New.

%files
%doc AUTHORS ChangeLog
%dir %{_fontdir}
%{_fontdir}
%{_fontconfig_templatedir}/*
%{_fontconfig_confdir}/*

%prep
%setup -q -n %{archivename}

%build

%install
# fonts .ttf
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p *.ttf %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

# Repeat for every font family
install -m 0644 -p %{SOURCE2} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-mono.conf
install -m 0644 -p %{SOURCE3} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-sans.conf
install -m 0644 -p %{SOURCE4} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-serif.conf
install -m 0644 -p %{SOURCE5} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-narrow.conf

for fconf in %{fontconf}-mono.conf \
             %{fontconf}-sans.conf \
             %{fontconf}-serif.conf \
             %{fontconf}-narrow.conf; do
  ln -s %{_fontconfig_templatedir}/$fconf \
        %{buildroot}%{_fontconfig_confdir}/$fconf
done

%changelog
* Mon Mar  9 2015 Alexander Larsson <alexl@redhat.com> - 2.00.1-1
- Initial version
