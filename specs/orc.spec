Name:		orc
Version:	0.4.23
Release:	1%{?dist}
Summary:	The Oil Run-time Compiler

Group:		System Environment/Libraries
License:	BSD
URL:		http://cgit.freedesktop.org/gstreamer/orc/

Source0:	http://gstreamer.freedesktop.org/src/orc/orc-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base

%description
Orc is a library and set of tools for compiling and executing
very simple programs that operate on arrays of data.  The "language"
is a generic assembly language that represents many of the features
available in SIMD architectures, including saturated addition and
subtraction, and many arithmetic operations.

%package doc
Summary:	Documentation for Orc
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for Orc.

%package dev
Summary:	Development files and libraries for Orc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-compiler

%description dev
This package contains the files needed to build packages that depend
on orc.

%package compiler
Summary:	Orc compiler
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description compiler
The Orc compiler, to produce optimized code.


%prep
%setup -q
NOCONFIGURE=1 autoreconf -vif

%build
%configure --disable-static --disable-gtk-doc --enable-user-codemem

make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

# Remove unneeded files.
find %{buildroot}/%{_libdir} -name \*.a -or -name \*.la -delete
rm -rf %{buildroot}/%{_libdir}/orc

touch -r stamp-h1 %{buildroot}%{_includedir}/%{name}-0.4/orc/orc-stdint.h   


%check
%ifnarch s390 s390x ppc %{power64} %{arm} i686 aarch64
# Disable for now, as memcpy_speed fails
#make check
%endif


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc COPYING README
%{_libdir}/liborc-*.so.*
%{_bindir}/orc-bugreport

%files doc
%doc %{_datadir}/gtk-doc/html/orc/

%files dev
%doc examples/*.c
%{_includedir}/%{name}-0.4/
%{_libdir}/liborc-*.so
%{_libdir}/pkgconfig/orc-0.4.pc
%{_datadir}/aclocal/orc.m4

%files compiler
%{_bindir}/orcc


%changelog
* Thu Mar 19 2015 Alexander Larsson <alexl@redhat.com> - 0.4.22-1
- Initial version
