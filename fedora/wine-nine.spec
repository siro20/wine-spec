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

%define patchlevel 2

Name:             wine-nine
Version:          3.0
Release:          %{?dist}
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
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libd3d-devel
BuildRequires:  libXext-devel
BuildRequires:  libxcb-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  libdrm-devel
BuildRequires:  llvm-devel

Requires:       wine-common >= %{version}
Enhances:       wine

%ifarch %{ix86}
Requires:       mesa-dri-drivers(x86-32)
Requires:       mesa-libd3d(x86-32)
Requires:       libxcb(x86-32)
Requires:       libX11(x86-32)
Requires:       libXext(x86-32)
Provides:       wine-nine(x86-32) = %{version}-%{release}
Obsoletes:      wine-nine(x86-32) < %{version}-%{release}

Provides: ninewinecfg.exe.so(x86-32) = %{version}
Provides: d3d9-nine.dll.so(x86-32) = %{version}
%endif

%ifarch x86_64
Requires:       mesa-dri-drivers(x86-64)
Requires:       mesa-libd3d(x86-64)
Requires:       libxcb(x86-64)
Requires:       libX11(x86-64)
Requires:       libXext(x86-64)
Provides:       wine-nine(x86-64) = %{version}-%{release}
Obsoletes:      wine-nine(x86-64) < %{version}-%{release}
Requires:       wine-nine(x86-32) = %{version}-%{release}

Provides: ninewinecfg.exe.so(x86-64) = %{version}
Provides: d3d9-nine.dll.so(x86-64) = %{version}
%endif

%define desc Wine sub package that contains the D3D9 library as well as the tool to configure it. \
Installs d3d9-nine.dll that interfaces Mesa's gallium nine statetracker. \
Installs ninewinecfg.exe that allows to configure nine and to provide debugging information. \
Offical bugtracker is at: https://github.com/iXit/Mesa-3D/issues

%description
%desc


%prep
%autosetup -n wine-%{name}-%{version}-%{patchlevel}

%build

export PKG_CONFIG_PATH=%{_libdir}/pkgconfig

./configure \
  --with-x \
  --without-freetype \
  --without-fontconfig \
  --without-curses \
  --without-cms \
  --without-gstreamer \
  --without-alsa \
  --without-capi \
  --without-opencl \
  --without-openal \
  --without-netapi  \
  --without-mpg123 \
  --without-ldap \
  --without-krb5 \
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

make include
make __builddeps__
make d3d9-nine.dll.so -C dlls/d3d9-nine
make d3d9-nine.dll.fake -C dlls/d3d9-nine
make programs/ninewinecfg

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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog
* Sun Oct 8 2017 Patrick Rudolph <siro@das-labor.org> Patchlevel 3:
- Implement some Adapter*Ex methods.

* Sun Oct 8 2017 Patrick Rudolph <siro@das-labor.org> Patchlevel 2:
- Add support for Wine using symlinks (remove the dependency to wine-staging).

* Mon Sep 11 2017 Patrick Rudolph <siro@das-labor.org> Patchlevel 1:
- Initial release for Wine 2.0.
