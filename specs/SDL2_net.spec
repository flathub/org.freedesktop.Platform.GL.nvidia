Name:		SDL2_net
Version:	2.0.0
Release:	1%{?dist}
Summary:	SDL portable network library
License:	zlib
URL:		http://www.libsdl.org/projects/SDL_net/
Source0:	http://www.libsdl.org/projects/SDL_net/release/%{name}-%{version}.tar.gz
BuildRequires:	freedesktop-sdk-base
BuildRequires:	SDL2-dev

%description
This is a portable network library for use with SDL.

%package	dev
Summary:	Libraries and includes to develop SDL networked applications
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	SDL2-dev%{?_isa}

%description	dev
This is a portable network library for use with SDL.

This is the libraries and include files you can use to develop SDL
networked applications.

%prep
%setup -q
# Fix end-of-line encoding
sed -i 's/\r//' README.txt CHANGES.txt COPYING.txt

%build
%configure --disable-static --disable-gui
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
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Feb 13 2015 Alexander Larsson <alexl@redhat.com> - 2.0.0-1
- Initial version
