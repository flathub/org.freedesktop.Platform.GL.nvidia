Name:           SDL2_mixer
Version:        2.0.0
Release:        1%{?dist}
Summary:        Simple DirectMedia Layer - Sample Mixer Library

Group:          System Environment/Libraries
License:        zlib
URL:            http://www.libsdl.org/projects/SDL_mixer/
Source0:        http://www.libsdl.org/projects/SDL_mixer/release/%{name}-%{version}.tar.gz

BuildRequires:	freedesktop-sdk-base
BuildRequires:  SDL2-dev

%description
SDL_mixer is a sample multi-channel audio mixer library.
It supports any number of simultaneously playing channels of 16 bit stereo
audio, plus a single channel of music, mixed by the popular FLAC,
MikMod MOD, Timidity MIDI, Ogg Vorbis, and SMPEG MP3 libraries. 

%package dev
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       SDL2-dev

%description dev
The %{name}-dev package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
sed -i -e 's/\r//g' README.txt CHANGES.txt COPYING.txt
rm -rf external/

%build
%configure --disable-dependency-tracking \
           --disable-static
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags}

%install
%make_install install-bin

find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc CHANGES.txt COPYING.txt
%{_libdir}/lib*.so.*

%files dev
%doc README.txt
%{_bindir}/playmus
%{_bindir}/playwave
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/SDL2/*

%changelog
* Fri Feb 13 2015 Alexander Larsson <alexl@redhat.com> - 2.0.0-1
- Initial version
