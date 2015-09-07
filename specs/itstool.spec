Name:           itstool
Version:        2.0.2
Release:        1%{?dist}
Summary:        ITS-based XML translation tool

Group:          Development/Tools
License:        GPLv3+
URL:            http://itstool.org/
Source0:        http://files.itstool.org/itstool/%{name}-%{version}.tar.bz2

BuildArch:      noarch

BuildRequires: freedesktop-sdk-base

%description
ITS Tool allows you to translate XML documents with PO files, using rules from
the W3C Internationalization Tag Set (ITS) to determine what to translate and
how to separate it into PO file messages.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%doc COPYING COPYING.GPL3 NEWS
%{_bindir}/itstool
%{_datadir}/itstool
%doc %{_mandir}/man1/itstool.1.gz

%changelog
* Wed Nov 12 2014 Alexander Larsson <alexl@redhat.com> - 2.0.2-1
- Initial version based on F21
