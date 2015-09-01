Name:           libdatrie
Version:        0.2.8
Release:        1%{?dist}
Summary:        Implementation of Double-Array structure for representing trie
License:        LGPLv2+
URL:            http://linux.thai.net/projects/datrie
Source0:        http://linux.thai.net/pub/thailinux/software/libthai/%{name}-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base

%description
datrie is an implementation of double-array structure for representing trie.

Trie is a kind of digital search tree, an efficient indexing method with O(1) 
time complexity for searching. Comparably as efficient as hashing, trie also 
provides flexibility on incremental matching and key spelling manipulation. 
This makes it ideal for lexical analyzers, as well as spelling dictionaries.

Details of the implementation: http://linux.thai.net/~thep/datrie/datrie.html

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    dev
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
#sed -i '/sys_lib_dlsearch_path_spec/s|/usr/lib |/usr/lib /usr/lib64|' configure
%configure --disable-static \
           --with-html-docdir=%{_pkgdocdir}-dev
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make

%install
%make_install
rm -frv %{buildroot}%{_pkgdocdir}
find %{buildroot} -name '*.*a' -delete -print

%check
LD_LIBRARY_PATH=../datrie/.libs make check %{?_smp_mflags}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_libdir}/libdatrie.so.*

%files dev
%doc AUTHORS ChangeLog NEWS README*
%{_includedir}/datrie/
%{_libdir}/libdatrie.so
%{_libdir}/pkgconfig/datrie-0.2.pc
%{_bindir}/trietool*
%{_mandir}/man1/trietool*.1*
%{_datadir}/doc/libdatrie/README.migration

%changelog
* Wed Nov 12 2014 Alexander Larsson <alexl@redhat.com> - 0.2.8-1
- Initial version based on F21
