Name:		mesa-demos
Version:	8.4.0
Release:	3
Summary:	Demos for Mesa (OpenGL compatible 3D lib)
Group:		Graphics
License:	MIT
URL:		http://www.mesa3d.org
Source0:	ftp://ftp.freedesktop.org/pub/mesa/demos/%{name}-%{version}.tar.bz2
Source4:	Mesa-icons.tar.bz2
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(osmesa)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glew)
# Not essential, but builds more demos:
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(wayland-server)
BuildRequires:	pkgconfig(glesv2)
BuildRequires:	openvg-devel
Requires:	glxinfo = %{version}

%description
Mesa is an OpenGL 2.1 compatible 3D graphics library.

This package contains some demo programs for the Mesa library.

%package -n glxinfo
Summary:	Commandline GLX information tool
Group:		Graphics
Conflicts:	mesa-demos < 7.7-4

%description -n glxinfo
Mesa is an OpenGL 2.1 compatible 3D graphics library.

This package contains the glinfo & glxinfo GLX information utility.

%prep
%autosetup -p1

perl -pi -e "s|\.\./images/|%{_libdir}/mesa-demos-data/|" src/*/*.c
perl -pi -e "s,\"(.*?)\.(dat|vert|geom|frag)\",\"%{_libdir}/mesa-demos-data/\$1.\$2\",g" src/*/*.c
perl -pi -e "s|isosurf.dat|%{_libdir}/mesa-demos-data/isosurf.dat|" src/*/isosurf.c

%build
LIB_DIR=%{_lib}
INCLUDE_DIR=%{buildroot}/%{_includedir}
export LIB_DIR INCLUDE_DIR DRI_DRIVER_DIR

%configure \
    --with-system-data-files \
    --disable-gles1

%make_build -j1 V=1

%install
%make_install

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
