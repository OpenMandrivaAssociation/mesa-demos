%ifarch %{x86_64}
# 32-bit compat glxinfo can be very useful for debugging
# graphics issues with 32-bit applications...
%bcond_without compat32
%endif

Name:		mesa-demos
Version:	9.0.0
Release:	2
Summary:	Demos for Mesa (OpenGL compatible 3D lib)
Group:		Graphics
License:	MIT
URL:		https://www.mesa3d.org
Source0:	https://gitlab.freedesktop.org/mesa/demos/-/archive/mesa-demos-%{version}/demos-mesa-demos-%{version}.tar.bz2
Source4:	Mesa-icons.tar.bz2
BuildRequires:	meson
BuildRequires:	glslang
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(libdrm)
#BuildRequires:	pkgconfig(osmesa)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glew)
# Not essential, but builds more demos:
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(wayland-server)
BuildRequires:	pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:	pkgconfig(glesv2)
BuildRequires:	pkgconfig(libdecor-0)
BuildRequires:	pkgconfig(xkbcommon-x11)
BuildRequires:	openvg-devel
Requires:	glxinfo = %{version}
Requires:	eglinfo = %{version}
%if %{with compat32}
BuildRequires:	devel(libX11)
BuildRequires:	devel(libXext)
BuildRequires:	devel(libdrm)
BuildRequires:	devel(libGL)
BuildRequires:	devel(libGLU)
BuildRequires:	devel(libGLdispatch)
BuildRequires:	devel(libGLX)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libxkbcommon)
BuildRequires:	devel(libxkbcommon-x11)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
BuildRequires:	devel(libbsd)
BuildRequires:	devel(libGLEW)
BuildRequires:	devel(libglut)
#BuildRequires:	devel(libOSMesa)
BuildRequires:	devel(libwayland-server)
BuildRequires:	devel(libffi)
BuildRequires:  devel(libvulkan)
%endif

%description
Mesa is an OpenGL 2.1 compatible 3D graphics library.

This package contains some demo programs for the Mesa library.

%package 32
Summary:	32-bit versions of Mesa demos
Group:		Graphics

%description 32
Mesa is an OpenGL 2.1 compatible 3D graphics library.

This package contains 32-bit versions of some demo programs
for the Mesa library.

%package -n glxinfo
Summary:	Commandline GLX information tool
Group:		Graphics
Conflicts:	mesa-demos < 7.7-4

%description -n glxinfo
Mesa is an OpenGL 2.1 compatible 3D graphics library.

This package contains the glinfo & glxinfo GLX information utility.

%package -n glxinfo32
Summary:	Commandline GLX information tool (32-bit)
Group:		Graphics
Conflicts:	mesa-demos < 7.7-4

%description -n glxinfo32
Mesa is an OpenGL 2.1 compatible 3D graphics library.

This package contains 32-bit versions of the glinfo & glxinfo GLX
information utility.

%package -n eglinfo
Summary:	Commandline EGL information tool
Group:		Graphics
Conflicts:	mesa-demos < 8.4.0-5

%description -n eglinfo
Mesa is an OpenGL 2.1 compatible 3D graphics library.

This package contains the eglinfo information utility.

%package -n eglinfo32
Summary:	Commandline EGL information tool (32-bit)
Group:		Graphics
Conflicts:	mesa-demos < 8.4.0-5

%description -n eglinfo32
Mesa is an OpenGL 2.1 compatible 3D graphics library.

This package contains 32-bit version of eglinfo information utility.

%prep
%autosetup -p1 -n demos-mesa-demos-%{version}

perl -pi -e "s|\.\./images/|%{_libdir}/mesa-demos-data/|" src/*/*.c
perl -pi -e "s,\"(.*?)\.(dat|vert|geom|frag)\",\"%{_libdir}/mesa-demos-data/\$1.\$2\",g" src/*/*.c
perl -pi -e "s|isosurf.dat|%{_libdir}/mesa-demos-data/isosurf.dat|" src/*/isosurf.c

%if %{with compat32}
%meson32 \
	-Dgles1=disabled \
	-Dwith-system-data-files=true \
	-Dwayland=disabled
%endif

%meson \
	-Dgles1=disabled \
	-Dwith-system-data-files=true

%build
%if %{with compat32}
%ninja_build -C build32
%endif
%meson_build

%install
%if %{with compat32}
%ninja_install -C build32
for i in $(ls -1 %{buildroot}%{_bindir}); do
    mv %{buildroot}%{_bindir}/"$i" %{buildroot}%{_bindir}/"$i"32
done
%endif
%meson_install

install -m 0755 build/src/egl/opengl/{eglgears_wayland,eglgears_x11,eglkms,egltri_wayland,egltri_x11,peglgears,xeglgears,xeglthreads} %{buildroot}%{_bindir}

# (fg) So that demos at least work :)
mkdir -p %{buildroot}%{_libdir}/mesa-demos-data
cp -v src/data/*rgb{a,} src/data/*.dat %{buildroot}%{_libdir}/mesa-demos-data
cp -a src/glsl/CH0* src/*/*.{frag,vert,geom} %{buildroot}%{_libdir}/mesa-demos-data

# (tv) fix conflict with bitmap:
mv %{buildroot}%{_bindir}/bitmap{,-gl}

# icons for three demos examples [we lack a frontend
# to launch the demos obviously]
install -m 755 -d %{buildroot}%{_miconsdir}
install -m 755 -d %{buildroot}%{_iconsdir}
install -m 755 -d %{buildroot}%{_liconsdir}
tar jxvf %{SOURCE4} -C %{buildroot}%{_iconsdir}

%files
%{_bindir}/*
%if %{with compat32}
%exclude %{_bindir}/*32
%endif
%exclude %{_bindir}/glxinfo
%exclude %{_bindir}/glinfo
%dir %{_datadir}/mesa-demos
%{_datadir}/mesa-demos/*
%dir %{_libdir}/mesa-demos-data
%{_libdir}/mesa-demos-data/*
%{_miconsdir}/*demos*.png
%{_iconsdir}/*demos*.png
%{_liconsdir}/*demos*.png

%files -n glxinfo
%{_bindir}/glxinfo
%{_bindir}/glinfo

%files -n eglinfo
%{_bindir}/eglinfo

%if %{with compat32}
%files 32
%exclude %{_bindir}/glxinfo32
%exclude %{_bindir}/glinfo32
%{_bindir}/*32

%files -n glxinfo32
%{_bindir}/glxinfo32
%{_bindir}/glinfo32

%files -n eglinfo32
%{_bindir}/eglinfo32
%endif
