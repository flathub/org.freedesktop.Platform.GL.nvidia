Name:           freedesktop-platform-base
Version:        0.1
Release:        1%{?dist}
Summary:        Base platform

License: Various
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

# Yocto builds without the normal find-provides, we supply those provides in the freedesktop-platform-base package
Provides: freedesktop-platform-base %(if [ -e /app/packages/base_provides ]; then cat /app/packages/base_provides; fi)

%if %{__isa_bits} == 64
%define provides_suffix (64bit)
%endif

# There is a bug in /usr/lib/rpm/find-provides which missed this provides:
Provides: libsndfile.so.1(libsndfile.so.1.0)%{?provides_suffix}

%description
The base platform files

%prep


%build


%install

%files

%changelog
* Fri Nov  7 2014 Alexander Larsson <alexl@redhat.com>
- Initial version
