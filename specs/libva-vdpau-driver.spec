Name:           libva-vdpau-driver
Version:        0.7.4
Release:        1%{?dist}
Summary:        HW video decode support for VDPAU platforms
License:        GPLv2+
URL:            http://cgit.freedesktop.org/vaapi/vdpau-driver
Source0:        http://www.freedesktop.org/software/vaapi/releases/%{name}/%{name}-%{version}.tar.bz2

Patch0:         %{name}-0.7.4-glext-85.patch
Patch1:         %{name}-0.7.4-drop-h264-api.patch
Patch2:         %{name}-0.7.4-fix_type.patch

BuildRequires: freedesktop-sdk-base
BuildRequires: libva-dev
BuildRequires: libvdpau-dev
BuildRequires: mesa-libGL-dev

%description
VDPAU Backend for Video Acceleration (VA) API.

%prep
%setup -q

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure \
  --disable-silent-rules \
  --enable-glx

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -delete

%files
%doc AUTHORS COPYING NEWS README
%{_libdir}/dri/*.so

%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Oct 25 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-10
- Fix build with newer libva

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 13 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-7
- Drop conditional source inclusion
- Adjust patch for RHEL >= 7

* Wed Jul 31 2013 Simone Caronni <negativo17@gmail.com> - 0.7.4-6
- Drop H.264 specific VA buffer types only on Fedora 20+.

* Wed Jul 31 2013 Simone Caronni <negativo17@gmail.com> - 0.7.4-5
- Add patch to drop H.264 specific VA buffer types.
- Clean up spec file a bit.

* Thu Jun 27 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-4
- Rebuilt for vaapi 0.34

* Mon Feb 18 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-3
- Add --disable-silent-rules
- Clean-up spec

* Fri Jan 11 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-2
- Fix build with recent mesa

* Sun Oct 07 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-1
- Update to 0.7.4

* Mon Jan 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.7.3-2
- Rename to libva-vdpau-driver

* Wed Mar 02 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.7.3-1
- Update to 0.7.3

* Sun Jan 09 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.7.3-0.2.pre4
- Update to 0.7.3 pre4

* Wed Dec 15 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.7.3-0.1.pre2
- Update to 0.7.3.pre2
- Switch to vdpau-video-freeworld

* Mon Mar 15 2010 Adam Williamson <adamwill AT shaw.ca> - 0.6.5-1
- new release

* Thu Jan 21 2010 Adam Williamson <adamwill AT shaw.ca> - 0.6.2-1
- new release

* Thu Jan 14 2010 Adam Williamson <adamwill AT shaw.ca> - 0.6.1-1
- new release

* Thu Dec 3 2009 Adam Williamson <adamwill AT shaw.ca> - 0.6.0-1
- new release

* Tue Nov 17 2009 Adam Williamson <adamwill AT shaw.ca> - 0.5.2-1
- new release

* Wed Oct 7 2009 Adam Williamson <adamwill AT shaw.ca> - 0.5.0-1
- new release

* Thu Sep 10 2009 Adam Williamson <adamwill AT shaw.ca> - 0.4.1-1
- new release

* Thu Sep 3 2009 Adam Williamson <adamwill AT shaw.ca> - 0.4.0-1
- initial package
