# INFO: When doing a bootstrap build on a new architecture, set this to 1 to
# avoid build loops.
%define build_bootstrap 1

%define debug_package %{nil}

Summary: X.Org X11 Protocol headers
Name: xorg-x11-proto-dev
Version: 7.7
Release: 1%{?dist}
License: MIT
Group: Development/System
URL: http://www.x.org
BuildArch: noarch

Source0:  http://xorg.freedesktop.org/archive/individual/proto/bigreqsproto-1.1.2.tar.bz2
Source1:  http://xorg.freedesktop.org/archive/individual/proto/compositeproto-0.4.2.tar.bz2
Source2:  http://xorg.freedesktop.org/archive/individual/proto/damageproto-1.2.1.tar.bz2
Source3:  http://xorg.freedesktop.org/archive/individual/proto/dmxproto-2.3.1.tar.bz2
Source31: http://xorg.freedesktop.org/archive/individual/proto/dri2proto-2.8.tar.bz2
Source33: http://xorg.freedesktop.org/pub/individual/proto/dri3proto-1.0.tar.bz2
Source4:  http://xorg.freedesktop.org/archive/individual/proto/evieext-1.1.1.tar.bz2
Source5:  http://xorg.freedesktop.org/archive/individual/proto/fixesproto-5.0.tar.bz2
Source7:  http://xorg.freedesktop.org/archive/individual/proto/fontsproto-2.1.3.tar.bz2
Source8:  http://xorg.freedesktop.org/archive/individual/proto/glproto-1.4.17.tar.bz2
Source9:  http://xorg.freedesktop.org/archive/individual/proto/inputproto-2.3.1.tar.bz2
Source10: http://xorg.freedesktop.org/archive/individual/proto/kbproto-1.0.6.tar.bz2
Source32: http://xorg.freedesktop.org/archive/individual/proto/presentproto-1.0.tar.bz2
Source13: http://xorg.freedesktop.org/archive/individual/proto/randrproto-1.4.0.tar.bz2
Source14: http://xorg.freedesktop.org/archive/individual/proto/recordproto-1.14.2.tar.bz2
Source15: http://xorg.freedesktop.org/archive/individual/proto/renderproto-0.11.1.tar.bz2
Source16: http://xorg.freedesktop.org/archive/individual/proto/resourceproto-1.2.0.tar.bz2
Source17: http://xorg.freedesktop.org/archive/individual/proto/scrnsaverproto-1.2.2.tar.bz2
Source19: http://xorg.freedesktop.org/archive/individual/proto/videoproto-2.3.2.tar.bz2
Source20: http://xorg.freedesktop.org/archive/individual/proto/xcmiscproto-1.2.2.tar.bz2
Source21: http://xorg.freedesktop.org/archive/individual/proto/xextproto-7.3.0.tar.bz2
Source22: http://xorg.freedesktop.org/archive/individual/proto/xf86bigfontproto-1.2.0.tar.bz2
Source23: http://xorg.freedesktop.org/archive/individual/proto/xf86dgaproto-2.1.tar.bz2
Source24: http://xorg.freedesktop.org/archive/individual/proto/xf86driproto-2.1.1.tar.bz2
Source25: http://xorg.freedesktop.org/archive/individual/proto/xf86miscproto-0.9.3.tar.bz2
Source27: http://xorg.freedesktop.org/archive/individual/proto/xf86vidmodeproto-2.3.1.tar.bz2
Source28: http://xorg.freedesktop.org/archive/individual/proto/xineramaproto-1.2.1.tar.bz2
Source29: http://xorg.freedesktop.org/archive/individual/proto/xproto-7.0.26.tar.bz2
Source30: http://xorg.freedesktop.org/archive/individual/proto/xproxymanagementprotocol-1.0.3.tar.bz2

Patch1: presentproto-0001-Force-Window-and-Pixmap-to-be-CARD32-on-the-wire.patch
Patch2: randrproto-0001-Add-a-GUID-property.patch

BuildRequires: freedesktop-sdk-base
BuildRequires: xorg-x11-util-macros

%if ! %{build_bootstrap}
Requires: mesa-libGL-dev
Requires: libXau-dev
%endif

%description
X.Org X11 Protocol headers


%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4 -a5 -a7 -a8 -a9 -a10 -a13 -a14 -a15 -a16 -a17 -a19 -a20 -a21 -a22 -a23 -a24 -a25 -a27 -a28 -a29 -a30 -a31 -a32 -a33

pushd presentproto-*
%patch1 -p1
popd

pushd randrproto-*
%patch2 -p1
popd


%build

# Proceed through each proto package directory, building them all
for dir in $(ls -1) ; do
	pushd $dir
        [ -e configure ] || ./autogen.sh
	# HdG: AFAIK this is not necessary, remove ?
	autoreconf -vif
	# yes, this looks horrible, but it's to get the .pc files in datadir
	%configure --libdir=%{_datadir} --without-xmlto
	make %{?_smp_mflags}
	# XXX presentproto, dri3proto missing this initially
	[ -e COPYING ] || touch COPYING
	mv COPYING COPYING-${dir%%-*}
	popd
done


%install
for dir in $(ls -1) ; do
	pushd $dir
	%make_install
	install -m 444 COPYING-${dir%%-*} $OLDPWD
	popd
done

mv $RPM_BUILD_ROOT%{_docdir}/*/*.{txt,xml} .

#for i in composite damage fixes randr render ; do
#    mv $RPM_BUILD_ROOT%{_docdir}/${i}proto/${i}proto.txt .
#done
mv $RPM_BUILD_ROOT%{_docdir}/xproxymanagementprotocol/PM_spec .

# keep things building even if you have the html doc tools for xmlto installed
rm -f $RPM_BUILD_ROOT%{_docdir}/*/*.{html,svg}


%files
%doc COPYING-*
%doc *.txt
%doc PM_spec
%dir %{_includedir}/GL
%{_includedir}/GL/glxint.h
%{_includedir}/GL/glxmd.h
%{_includedir}/GL/glxproto.h
%{_includedir}/GL/glxtokens.h
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/glcore.h
%dir %{_includedir}/X11
%{_includedir}/X11/DECkeysym.h
%{_includedir}/X11/HPkeysym.h
%dir %{_includedir}/X11/PM
%{_includedir}/X11/PM/PM.h
%{_includedir}/X11/PM/PMproto.h
%{_includedir}/X11/Sunkeysym.h
%{_includedir}/X11/X.h
%{_includedir}/X11/XF86keysym.h
%{_includedir}/X11/XWDFile.h
%{_includedir}/X11/Xalloca.h
%{_includedir}/X11/Xarch.h
%{_includedir}/X11/Xatom.h
%{_includedir}/X11/Xdefs.h
%{_includedir}/X11/Xfuncproto.h
%{_includedir}/X11/Xfuncs.h
%{_includedir}/X11/Xmd.h
%{_includedir}/X11/Xos.h
%{_includedir}/X11/Xos_r.h
%{_includedir}/X11/Xosdefs.h
%{_includedir}/X11/Xpoll.h
%{_includedir}/X11/Xproto.h
%{_includedir}/X11/Xprotostr.h
%{_includedir}/X11/Xthreads.h
%{_includedir}/X11/Xw32defs.h
%{_includedir}/X11/Xwindows.h
%{_includedir}/X11/Xwinsock.h
%{_includedir}/X11/ap_keysym.h
%dir %{_includedir}/X11/dri
%{_includedir}/X11/dri/xf86dri.h
%{_includedir}/X11/dri/xf86driproto.h
%{_includedir}/X11/dri/xf86dristr.h
%dir %{_includedir}/X11/extensions
%{_includedir}/X11/extensions/EVI.h
%{_includedir}/X11/extensions/EVIproto.h
%{_includedir}/X11/extensions/XI.h
%{_includedir}/X11/extensions/XI2.h
%{_includedir}/X11/extensions/XI2proto.h
%{_includedir}/X11/extensions/XIproto.h
%{_includedir}/X11/extensions/XKB.h
%{_includedir}/X11/extensions/XKBgeom.h
%{_includedir}/X11/extensions/XKBproto.h
%{_includedir}/X11/extensions/XKBsrv.h
%{_includedir}/X11/extensions/XKBstr.h
%{_includedir}/X11/extensions/XResproto.h
%{_includedir}/X11/extensions/Xeviestr.h
%{_includedir}/X11/extensions/Xv.h
%{_includedir}/X11/extensions/XvMC.h
%{_includedir}/X11/extensions/XvMCproto.h
%{_includedir}/X11/extensions/Xvproto.h
%{_includedir}/X11/extensions/ag.h
%{_includedir}/X11/extensions/agproto.h
%{_includedir}/X11/extensions/bigreqsproto.h
%{_includedir}/X11/extensions/bigreqstr.h
%{_includedir}/X11/extensions/composite.h
%{_includedir}/X11/extensions/compositeproto.h
%{_includedir}/X11/extensions/cup.h
%{_includedir}/X11/extensions/cupproto.h
%{_includedir}/X11/extensions/damageproto.h
%{_includedir}/X11/extensions/damagewire.h
%{_includedir}/X11/extensions/dbe.h
%{_includedir}/X11/extensions/dbeproto.h
%{_includedir}/X11/extensions/dmx.h
%{_includedir}/X11/extensions/dmxproto.h
%{_includedir}/X11/extensions/dpmsconst.h
%{_includedir}/X11/extensions/dpmsproto.h
%{_includedir}/X11/extensions/dri2proto.h
%{_includedir}/X11/extensions/dri2tokens.h
%{_includedir}/X11/extensions/dri3proto.h
%{_includedir}/X11/extensions/evieproto.h
%{_includedir}/X11/extensions/ge.h
%{_includedir}/X11/extensions/geproto.h
%{_includedir}/X11/extensions/lbx.h
%{_includedir}/X11/extensions/lbxproto.h
%{_includedir}/X11/extensions/mitmiscconst.h
%{_includedir}/X11/extensions/mitmiscproto.h
%{_includedir}/X11/extensions/multibufconst.h
%{_includedir}/X11/extensions/multibufproto.h
%{_includedir}/X11/extensions/panoramiXproto.h
%{_includedir}/X11/extensions/presentproto.h
%{_includedir}/X11/extensions/presenttokens.h
%{_includedir}/X11/extensions/randr.h
%{_includedir}/X11/extensions/randrproto.h
%{_includedir}/X11/extensions/recordconst.h
%{_includedir}/X11/extensions/recordproto.h
%{_includedir}/X11/extensions/recordstr.h
%{_includedir}/X11/extensions/render.h
%{_includedir}/X11/extensions/renderproto.h
%{_includedir}/X11/extensions/saver.h
%{_includedir}/X11/extensions/saverproto.h
%{_includedir}/X11/extensions/secur.h
%{_includedir}/X11/extensions/securproto.h
%{_includedir}/X11/extensions/shapeconst.h
%{_includedir}/X11/extensions/shapeproto.h
%{_includedir}/X11/extensions/shapestr.h
%{_includedir}/X11/extensions/shm.h
%{_includedir}/X11/extensions/shmproto.h
%{_includedir}/X11/extensions/shmstr.h
%{_includedir}/X11/extensions/syncconst.h
%{_includedir}/X11/extensions/syncproto.h
%{_includedir}/X11/extensions/syncstr.h
%{_includedir}/X11/extensions/vldXvMC.h
%{_includedir}/X11/extensions/xcmiscproto.h
%{_includedir}/X11/extensions/xcmiscstr.h
%{_includedir}/X11/extensions/xf86bigfont.h
%{_includedir}/X11/extensions/xf86bigfproto.h
%{_includedir}/X11/extensions/xf86bigfstr.h
%{_includedir}/X11/extensions/xf86dga.h
%{_includedir}/X11/extensions/xf86dga1const.h
%{_includedir}/X11/extensions/xf86dga1proto.h
%{_includedir}/X11/extensions/xf86dga1str.h
%{_includedir}/X11/extensions/xf86dgaconst.h
%{_includedir}/X11/extensions/xf86dgaproto.h
%{_includedir}/X11/extensions/xf86dgastr.h
%{_includedir}/X11/extensions/xf86misc.h
%{_includedir}/X11/extensions/xf86mscstr.h
%{_includedir}/X11/extensions/xf86vm.h
%{_includedir}/X11/extensions/xf86vmproto.h
%{_includedir}/X11/extensions/xf86vmstr.h
%{_includedir}/X11/extensions/xfixesproto.h
%{_includedir}/X11/extensions/xfixeswire.h
%{_includedir}/X11/extensions/xtestconst.h
%{_includedir}/X11/extensions/xtestext1const.h
%{_includedir}/X11/extensions/xtestext1proto.h
%{_includedir}/X11/extensions/xtestproto.h
%dir %{_includedir}/X11/fonts
%{_includedir}/X11/fonts/FS.h
%{_includedir}/X11/fonts/FSproto.h
%{_includedir}/X11/fonts/font.h
%{_includedir}/X11/fonts/fontproto.h
%{_includedir}/X11/fonts/fontstruct.h
%{_includedir}/X11/fonts/fsmasks.h
%{_includedir}/X11/keysym.h
%{_includedir}/X11/keysymdef.h
%{_datadir}/pkgconfig/bigreqsproto.pc
%{_datadir}/pkgconfig/compositeproto.pc
%{_datadir}/pkgconfig/damageproto.pc
%{_datadir}/pkgconfig/dmxproto.pc
%{_datadir}/pkgconfig/dri2proto.pc
%{_datadir}/pkgconfig/dri3proto.pc
%{_datadir}/pkgconfig/evieproto.pc
%{_datadir}/pkgconfig/fixesproto.pc
%{_datadir}/pkgconfig/fontsproto.pc
%{_datadir}/pkgconfig/glproto.pc
%{_datadir}/pkgconfig/inputproto.pc
%{_datadir}/pkgconfig/kbproto.pc
%{_datadir}/pkgconfig/presentproto.pc
%{_datadir}/pkgconfig/randrproto.pc
%{_datadir}/pkgconfig/recordproto.pc
%{_datadir}/pkgconfig/renderproto.pc
%{_datadir}/pkgconfig/resourceproto.pc
%{_datadir}/pkgconfig/scrnsaverproto.pc
%{_datadir}/pkgconfig/videoproto.pc
%{_datadir}/pkgconfig/xcmiscproto.pc
%{_datadir}/pkgconfig/xextproto.pc
%{_datadir}/pkgconfig/xf86bigfontproto.pc
%{_datadir}/pkgconfig/xf86dgaproto.pc
%{_datadir}/pkgconfig/xf86driproto.pc
%{_datadir}/pkgconfig/xf86miscproto.pc
%{_datadir}/pkgconfig/xf86vidmodeproto.pc
%{_datadir}/pkgconfig/xineramaproto.pc
%{_datadir}/pkgconfig/xproto.pc
%{_datadir}/pkgconfig/xproxymngproto.pc

%changelog
* Tue Nov 11 2014 Alexander Larsson <alexl@redhat.com> - 7.7-1
- Initial version based on f21
