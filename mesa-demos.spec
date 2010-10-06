# (cg) Cheater...
%define Werror_cflags %nil

# (aco) Needed for the dri drivers
%define _disable_ld_no_undefined 1

%define src_type tar.bz2

%define makedepend		%{_bindir}/gccmakedep

Name:		mesa-demos
Version: 	8.0.1
Release: 	%mkrel 4
Summary:	Demos for Mesa (OpenGL compatible 3D lib)
Group:		Graphics

# (tv) BR probably need to be shrinked:
BuildRequires:	tcl
BuildRequires:	texinfo
BuildRequires:	libxfixes-devel		>= 4.0.3
BuildRequires:	libxt-devel		>= 1.0.5
BuildRequires:	libxmu-devel		>= 1.0.3
BuildRequires:	libx11-devel		>= 1.3.3
BuildRequires:	libxdamage-devel	>= 1.1.1
BuildRequires:	libexpat-devel		>= 2.0.1
BuildRequires:	gccmakedep
BuildRequires:	x11-proto-devel		>= 7.3
BuildRequires:	libdrm-devel		>= 2.4.19-3

BuildRequires:	libxext-devel		>= 1.1.1
BuildRequires:	libxxf86vm-devel	>= 1.1.0
BuildRequires:	libxi-devel		>= 1.3

BuildRequires:	libglew-devel

# (tv) for glinfo:
BuildRequires:	mesaglut-devel

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.mesa3d.org
Source0:	ftp://ftp://ftp.freedesktop.org/pub/mesa/demos/%version/%name-%{version}.%{src_type}
Source4:	Mesa-icons.tar.bz2

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

perl -pi -e "s|\.\./images/|%{_libdir}/mesa-demos-data/|" src/*/*.c
perl -pi -e "s,\"(.*?)\.(dat|vert|geom|frag)\",\"%{_libdir}/mesa-demos-data/\$1.\$2\",g" src/*/*.c
perl -pi -e "s|isosurf.dat|%{_libdir}/mesa-demos-data/isosurf.dat|" src/*/isosurf.c 


%build
LIB_DIR=%{_lib}
INCLUDE_DIR=$RPM_BUILD_ROOT%{_includedir}
export LIB_DIR INCLUDE_DIR DRI_DRIVER_DIR

%configure2_5x	
%make

%install
rm -rf %{buildroot}
make DESTDIR=$RPM_BUILD_ROOT install
%makeinstall

# (fg) So that demos at least work :)
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mesa-demos-data
cp -v src/images/*rgb{a,} src/demos/*.dat %{buildroot}/%{_libdir}/mesa-demos-data
cp -a src/glsl/CH0* src/*/*.{frag,vert,geom} %{buildroot}/%{_libdir}/mesa-demos-data

# (tv) fix conflict with ncurses:
mv %{buildroot}/%{_bindir}/clear{,-gl}

# (tv) fix conflict with bitmap:
mv %{buildroot}/%{_bindir}/bitmap{,-gl}

# icons for three demos examples [we lack a frontend
# to launch the demos obviously]
install -m 755 -d $RPM_BUILD_ROOT%{_miconsdir}
install -m 755 -d $RPM_BUILD_ROOT%{_iconsdir}
install -m 755 -d $RPM_BUILD_ROOT%{_liconsdir}
tar jxvf %{SOURCE4} -C $RPM_BUILD_ROOT%{_iconsdir}

%clean
rm -fr $RPM_BUILD_ROOT


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



