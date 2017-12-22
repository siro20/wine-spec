#
# spec file for package wine-nine
#
# Copyright (c) 2017 siro@das-labor.org
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Depends on stable Wine API. No need to rebuild with every minor release
# Official nine bugtracker https://github.com/iXit/Mesa-3D/issues
# Depends on libdl to install redirects to d3d9-nine.dll
# define WINE_STAGING 1 to use Wine staging's DllRedirects feature instead of symlinks in WINEPREFIX

%define patchlevel 3

Name:             wine-nine
Version:          2.0
Release:          %{patchlevel}%{?dist}
Summary:          Wine D3D9 interface library for Mesa's Gallium Nine statetracker
License:          LGPL-2.0
URL:              https://github.com/iXit/wine
Source0:          https://github.com/iXit/wine/archive/%{name}-%{version}-%{patchlevel}.tar.gz
Group:            Applications/Emulators
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

ExclusiveArch:  %{ix86} x86_64


BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  autoconf
BuildRequires:  libX11-devel
BuildRequires:  Mesa-devel
BuildRequires:  Mesa-libGL-devel
BuildRequires:  Mesa-libEGL-devel
BuildRequires:  Mesa-libd3d-devel
BuildRequires:  libXext-devel
BuildRequires:  libxcb-devel
BuildRequires:  xorg-x11-devel
BuildRequires:  libdrm-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  dri2proto-devel
BuildRequires:  dri3proto-devel
BuildRequires:  libOSMesa-devel


Requires:       wine >= %{version}
Enhances:       wine

%ifarch %{ix86}
Requires:       Mesa-dri-nouveau(x86-32)
Requires:       Mesa-libd3d(x86-32)
Provides:       wine-nine(x86-32) = %{version}-%{release}
Obsoletes:      wine-nine(x86-32) < %{version}-%{release}

Provides: ninewinecfg.exe.so(x86-32) = %{version}
Provides: d3d9-nine.dll.so(x86-32) = %{version}
%endif

%ifarch x86_64
Requires:       Mesa-dri-nouveau(x86-64)
Requires:       Mesa-libd3d(x86-64)
Provides:       wine-nine(x86-64) = %{version}-%{release}
Obsoletes:      wine-nine(x86-64) < %{version}-%{release}

Provides: ninewinecfg.exe.so(x86-64) = %{version}
Provides: d3d9-nine.dll.so(x86-64) = %{version}

Requires:       wine-nine-32bit = %{version}-%{release}
%endif

%define desc Wine sub package that contains the D3D9 library as well as the tool to configure it. \
Installs d3d9-nine.dll that interfaces Mesa's gallium nine statetracker. \
Installs ninewinecfg.exe that allows to configure nine and to provide debugging information. \
Offical bugtracker is at: https://github.com/iXit/Mesa-3D/issues

%description
%desc

%ifarch x86_64
%package 32bit-build-deps
Summary:        Wine build dependencies for 32bit builds on x86_64 systems
Group:          Development/Libraries/C and C++
BuildRequires:  libX11-devel-32bit
BuildRequires:  Mesa-devel-32bit
BuildRequires:  Mesa-libGL-devel-32bit
BuildRequires:  Mesa-libEGL-devel-32bit
BuildRequires:  Mesa-libd3d-devel-32bit
BuildRequires:  libXext-devel-32bit
BuildRequires:  libxcb-devel-32bit
BuildRequires:  xorg-x11-devel-32bit
BuildRequires:  libdrm-devel-32bit
BuildRequires:  xorg-x11-proto-devel-32bit
BuildRequires:  dri2proto-devel-32bit
BuildRequires:  dri3proto-devel-32bit
BuildRequires:  libOSMesa-devel-32bit

# TODO: remove obsolete packages
Requires:       dbus-1-devel-32bit
Requires:       fontconfig-devel-32bit
Requires:       freeglut-devel-32bit
Requires:       glibc-devel-32bit
Requires:       glu-devel-32bit
Requires:       libXcomposite-devel-32bit
Requires:       libXcursor-devel-32bit
Requires:       libXi-devel-32bit
Requires:       libXinerama-devel-32bit
Requires:       libXrandr-devel-32bit
Requires:       libXrender-devel-32bit
Requires:       libXxf86vm-devel-32bit
Requires:       liblcms2-devel-32bit
#Requires:	gcc-32bit

%description 32bit-build-deps
This virtual package provides the 32bit development build dependencies for use on x86_64.
%endif


%prep
%autosetup -n wine-%{name}-%{version}-%{patchlevel}

%build

export PKG_CONFIG_PATH=%{_libdir}/pkgconfig

./configure \
  --with-x \
  --without-freetype \
  --without-gstreamer \
  --without-alsa \
  --without-opencl \
  --without-openal \
  --without-netapi  \
  --without-mpg123 \
  --without-ldap \
  --without-jpeg \
  --without-gnutls \
  --without-coreaudio \
  --without-dbus \
  --without-cups \
  --without-gsm \
  --without-osmesa \
  --without-oss  \
  --without-pcap \
  --without-png \
  --without-pulse \
  --without-sane \
  --without-tiff \
  --without-udev \
  --without-v4l \
  --without-xinput \
  --without-xinput2 \
  --without-xml \
  --without-xslt \
  --without-zlib \
  --with-d3d9-nine \
%ifarch x86_64
  --enable-win64 \
%endif
  --disable-tests

make include %{?_smp_mflags}
make __builddeps__ %{?_smp_mflags}
make d3d9-nine.dll.so -C dlls/d3d9-nine %{?_smp_mflags}
make d3d9-nine.dll.fake -C dlls/d3d9-nine %{?_smp_mflags}
make programs/ninewinecfg %{?_smp_mflags}

%install
install -m 755 -d %{buildroot}/%{_libdir}/wine
install -m 755 -d %{buildroot}/%{_libdir}/wine/fakedlls

install -m 755 programs/ninewinecfg/ninewinecfg.exe.so %{buildroot}/%{_libdir}/wine/ninewinecfg.exe.so
install -m 755 programs/ninewinecfg/ninewinecfg.exe.fake %{buildroot}/%{_libdir}/wine/fakedlls/ninewinecfg.exe

install -m 755 dlls/d3d9-nine/d3d9-nine.dll.so %{buildroot}/%{_libdir}/wine/d3d9-nine.dll.so
install -m 755 dlls/d3d9-nine/d3d9-nine.dll.fake %{buildroot}/%{_libdir}/wine/fakedlls/d3d9-nine.dll

%files
%dir %{_libdir}/wine
%dir %{_libdir}/wine/fakedlls
%{_libdir}/wine/*.so
%{_libdir}/wine/fakedlls/*

%ifarch x86_64
%files 32bit-build-deps
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog
* Sun Oct 8 2017 Patrick Rudolph <siro@das-labor.org> Patchlevel 3:
- Implement some Adapter*Ex methods.

* Sun Oct 8 2017 Patrick Rudolph <siro@das-labor.org> Patchlevel 2:
- Add support for Wine using symlinks (remove the dependency to wine-staging).

* Mon Sep 11 2017 Patrick Rudolph <siro@das-labor.org> Patchlevel 1:
- Initial release for Wine 2.0.

