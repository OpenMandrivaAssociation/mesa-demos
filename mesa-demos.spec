Name:		mesa-demos
Version: 	8.0.1
Release: 	8
Summary:	Demos for Mesa (OpenGL compatible 3D lib)
Group:		Graphics
License:	MIT
URL:		http://www.mesa3d.org
Source0:	ftp://ftp://ftp.freedesktop.org/pub/mesa/demos/%{version}/%{name}-%{version}.tar.bz2
Source4:	Mesa-icons.tar.bz2

Patch0:		0001-es1_info-convert-indentString-into-a-literal-string.patch

BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glew)
# Not essential, but builds more demos:
BuildRequires:	pkgconfig(glut)

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
%setup -q
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
%makeinstall_std

# (fg) So that demos at least work :)
mkdir -p %{buildroot}%{_libdir}/mesa-demos-data
cp -v src/images/*rgb{a,} src/demos/*.dat %{buildroot}%{_libdir}/mesa-demos-data
cp -a src/glsl/CH0* src/*/*.{frag,vert,geom} %{buildroot}%{_libdir}/mesa-demos-data

# (tv) fix conflict with ncurses:
mv %{buildroot}%{_bindir}/clear{,-gl}

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
%dir %{_libdir}/mesa-demos-data
%{_libdir}/mesa-demos-data/*
%{_miconsdir}/*demos*.png
%{_iconsdir}/*demos*.png
%{_liconsdir}/*demos*.png

%files -n glxinfo
%{_bindir}/glxinfo
%{_bindir}/glinfo



%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 8.0.1-6mdv2011.0
+ Revision: 666418
- mass rebuild

* Thu Jan 06 2011 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 8.0.1-5mdv2011.0
+ Revision: 629150
- Re-enable Werror_cflags and add patch to fix errors (submitted upstream)
- Remove disable_ld_no_undefined since it was not for the demos
- Don't define src_type since it's only used once
- Remove useless makedepend macro

* Wed Oct 06 2010 Thierry Vignaud <tv@mandriva.org> 8.0.1-4mdv2011.0
+ Revision: 583892
- fix conflict with bitmap (#61211)
- cleanup now that we have proper BR for glinfo & the like
- fix even more paths in demos and do it faster

* Wed Oct 06 2010 Thierry Vignaud <tv@mandriva.org> 8.0.1-3mdv2011.0
+ Revision: 583353
- fix more paths in demos and do it faster
  (but 8.0.1 still lacks some files)
- package more data files
- relax require on glxinfo
- parallel build is OK

* Wed Oct 06 2010 Thierry Vignaud <tv@mandriva.org> 8.0.1-2mdv2011.0
+ Revision: 583243
- package more data files for demos

* Wed Oct 06 2010 Thierry Vignaud <tv@mandriva.org> 8.0.1-1mdv2011.0
+ Revision: 583191
- BuildRequires mesaglut-devel for glinfo
- build fix
- import mesa-demos

