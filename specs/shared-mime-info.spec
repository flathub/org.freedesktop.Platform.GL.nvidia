Summary: Shared MIME information database
Name: shared-mime-info
Version: 1.3
Release: 1%{?dist}
License: GPLv2+
Group: System Environment/Base
URL: http://freedesktop.org/Software/shared-mime-info
Source0: http://people.freedesktop.org/~hadess/%{name}-%{version}.tar.xz

BuildRequires:  freedesktop-sdk-base
BuildRequires:  glib2-dev

Requires(post): glib2

%description
This is the freedesktop.org shared MIME info database.

Many programs and desktops use the MIME system to represent the types of
files. Frequently, it is necessary to work out the correct MIME type for
a file. This is generally done by examining the file's name or contents,
and looking up the correct MIME type in a database.

%package dev
Summary: Development files for the shared-mime-info
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description dev
This package includes libraries, header files, and developer documentation
needed for shared-mime-info.

%prep
%setup -q

%build
%configure --disable-silent-rules --disable-update-mimedb
# not smp safe, pretty small package anyway
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_datadir}/mime -type d \
| sed -e "s|^$RPM_BUILD_ROOT|%%dir |" > %{name}.files
find $RPM_BUILD_ROOT%{_datadir}/mime -type f -not -path "*/packages/*" \
| sed -e "s|^$RPM_BUILD_ROOT|%%ghost |" >> %{name}.files

## remove bogus translation files
## translations are already in the xml file installed
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/*

%post
/bin/touch --no-create %{_datadir}/mime/packages &>/dev/null ||:

%posttrans
%{_bindir}/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null ||:

%files -f %{name}.files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README NEWS HACKING shared-mime-info-spec.xml
%{_bindir}/*
%{_datadir}/mime/packages/*
%{_mandir}/man*/*

%files dev
%{_datadir}/pkgconfig/shared-mime-info.pc

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 1.3-1
- Initial version based on f21
