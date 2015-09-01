Name:		SDL2_ttf
Version:	2.0.12
Release:	1%{?dist}
Summary:	TrueType font rendering library for SDL2
Group:		System Environment/Libraries
License:	zlib
URL:		http://www.libsdl.org/projects/SDL_ttf/
Source0:	http://www.libsdl.org/projects/SDL_ttf/release/%{name}-%{version}.tar.gz
BuildRequires:	freedesktop-sdk-base
BuildRequires:	SDL2-dev
BuildRequires:	freetype-dev

%description
This library allows you to use TrueType fonts to render text in SDL2
applications.

%package dev
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	SDL2-dev%{?_isa}

%description dev
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
rm -rf external
# Fix end-of-line encoding
sed -i 's/\r//' README.txt CHANGES.txt COPYING.txt

%build
%configure --disable-dependency-tracking --disable-static
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README.txt CHANGES.txt COPYING.txt
%{_libdir}/lib*.so.*

%files dev
%{_libdir}/lib*.so
%{_includedir}/SDL2/*
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Fri Feb 13 2015 Alexander Larsson <alexl@redhat.com> - 2.0.12-1
- Initial version
