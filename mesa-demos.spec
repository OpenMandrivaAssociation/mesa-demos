Name:		mesa-demos
Version: 	8.0.1
Release: 	%mkrel 5
Summary:	Demos for Mesa (OpenGL compatible 3D lib)
Group:		Graphics

BuildRequires: libmesagl-devel
BuildRequires: libglew-devel
BuildRequires: libmesaglu-devel

# Not essential, but builds more demos:
BuildRequires: libmesaglut-devel

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.mesa3d.org
Source0:	ftp://ftp://ftp.freedesktop.org/pub/mesa/demos/%version/%name-%{version}.tar.bz2
Source4:	Mesa-icons.tar.bz2

Patch0:		0001-es1_info-convert-indentString-into-a-literal-string.patch

License:	MIT

Provides:	hackMesa-demos = %{version}
Obsoletes:	hackMesa-demos <= %{version}
Obsoletes: 	Mesa-demos < 6.4
Provides:	Mesa-demos = %{version}-%{release}
Requires:	glxinfo = %{version}

%package -n	glxinfo
Summary:	Commandline GLX information tool
Group:		Graphics
Conflicts:	mesa-demos < 7.7-4

%description
Mesa is an OpenGL 2.1 compatible 3D graphics library.

This package contains some demo programs for the Mesa library.

%description -n	glxinfo
Mesa is an OpenGL 2.1 compatible 3D graphics library.

This package contains the glinfo & glxinfo GLX information utility.

%prep
%setup -q -n %{name}-%{version}
%apply_patches

perl -pi -e "s|\.\./images/|%{_libdir}/mesa-demos-data/|" src/*/*.c
perl -pi -e "s,\"(.*?)\.(dat|vert|geom|frag)\",\"%{_libdir}/mesa-demos-data/\$1.\$2\",g" src/*/*.c
perl -pi -e "s|isosurf.dat|%{_libdir}/mesa-demos-data/isosurf.dat|" src/*/isosurf.c


%build
LIB_DIR=%{_lib}
INCLUDE_DIR=%{buildroot}/%{_includedir}
export LIB_DIR INCLUDE_DIR DRI_DRIVER_DIR

%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

# (fg) So that demos at least work :)
mkdir -p %{buildroot}/%{_libdir}/mesa-demos-data
cp -v src/images/*rgb{a,} src/demos/*.dat %{buildroot}/%{_libdir}/mesa-demos-data
cp -a src/glsl/CH0* src/*/*.{frag,vert,geom} %{buildroot}/%{_libdir}/mesa-demos-data

# (tv) fix conflict with ncurses:
mv %{buildroot}/%{_bindir}/clear{,-gl}

# (tv) fix conflict with bitmap:
mv %{buildroot}/%{_bindir}/bitmap{,-gl}

# icons for three demos examples [we lack a frontend
# to launch the demos obviously]
install -m 755 -d %{buildroot}/%{_miconsdir}
install -m 755 -d %{buildroot}/%{_iconsdir}
install -m 755 -d %{buildroot}/%{_liconsdir}
tar jxvf %{SOURCE4} -C %{buildroot}/%{_iconsdir}

%clean
rm -fr %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/*
%exclude %{_bindir}/glxinfo
%exclude %{_bindir}/glinfo
%dir %{_libdir}/mesa-demos-data
%{_libdir}/mesa-demos-data/*
%{_miconsdir}/*demos*.png
%{_iconsdir}/*demos*.png
%{_liconsdir}/*demos*.png

%files -n glxinfo
%defattr(-,root,root)
%{_bindir}/glxinfo
%{_bindir}/glinfo

