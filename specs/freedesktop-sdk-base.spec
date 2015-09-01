Name:           freedesktop-sdk-base
Version:        0.1
Release:        1%{?dist}
Summary:        Base sdk

License: Various
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

# Yocto builds without the normal find-provides, we supply those provides in the freedesktop-sdk-base package

Provides: freedesktop-sdk-base %(if [ -e /app/packages/base_sdk_provides ]; then cat /app/packages/base_sdk_provides; fi)

%if %{__isa_bits} == 64
%define provides_suffix (64bit)
%endif

# There is a bug in find_prov.sh which missed this provides:
Provides: libsndfile.so.1(libsndfile.so.1.0)%{?provides_suffix}

%description
The base sdk files

%prep


%build


%install

%files
%doc

%changelog
* Fri Nov  7 2014 Alexander Larsson <alexl@redhat.com>
- Initial version
