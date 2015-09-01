%global fontname    dejavu
%global _fontdir %{_datadir}/fonts/%{fontname}
%global _fontconfig_templatedir %{_datadir}/fontconfig/conf.avail
%global _fontconfig_confdir %{_sysconfdir}/fonts/conf.d

Name:    %{fontname}-fonts
Version: 2.34
Release: 1%{?alphatag}%{?dist}
Summary: DejaVu fonts

Group:     User Interface/X
License:   Bitstream Vera and Public Domain
URL:       http://%{name}.org/
Source0:   http://sourceforge.net/projects/dejavu/files/%{fontname}/%{version}/%{name}-ttf-%{version}.tar.bz2

BuildArch:     noarch

%description
The DejaVu font set is based on the “Bitstream Vera” fonts, release 1.10. Its\
purpose is to provide a wider range of characters, while maintaining the \
original style, using an open collaborative development process.

%prep
%setup -q -n %{name}-ttf-%{version}

%build


%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p ttf/*.ttf %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_confdir} \
                   %{buildroot}%{_fontconfig_templatedir}

cd fontconfig
for fontconf in *conf ; do
  install -m 0644 -p $fontconf %{buildroot}%{_fontconfig_templatedir}
  ln -s %{_fontconfig_templatedir}/$fontconf \
        %{buildroot}%{_fontconfig_confdir}/$fontconf
done

%files
%defattr(0644,root,root,0755)
%doc AUTHORS BUGS LICENSE NEWS README
%{_fontdir}
%{_fontconfig_templatedir}/*
%{_fontconfig_confdir}/*

%changelog
* Thu Nov 13 2014 Alexander Larsson <alexl@redhat.com> - 2.34-1%{?dist}
- Initial version based on F21
