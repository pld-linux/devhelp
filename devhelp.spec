#
# Conditional build:
%bcond_without  apidocs         # disable gtk-doc
%bcond_without  static_libs     # static library

Summary:	API documentation browser for GNOME
Summary(pl.UTF-8):	Przeglądarka dokumentacji API dla GNOME
Name:		devhelp
Version:	3.36.2
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/devhelp/3.36/%{name}-%{version}.tar.xz
# Source0-md5:	18c2cb689da880eb2c8936335bd7c1cd
Patch0:		%{name}-bookdir.patch
URL:		https://wiki.gnome.org/Apps/Devhelp
BuildRequires:	amtk-devel >= 5.0
BuildRequires:	gettext-tools >= 0.19.7
BuildRequires:	glib2-devel >= 1:2.60
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+3-devel >= 3.22.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.25}
BuildRequires:	gtk-webkit4-devel >= 2.24
BuildRequires:	meson >= 0.50
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 1:3.3
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	glib2 >= 1:2.60
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name}-libs = %{version}-%{release}
Requires:	amtk >= 5.0
Requires:	gsettings-desktop-schemas
Requires:	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
API documentation browser for GNOME.

%description -l pl.UTF-8
Przeglądarka dokumentacji API dla GNOME.

%package libs
Summary:	Library to embed Devhelp in other applications
Summary(pl.UTF-8):	Biblioteka do osadzania Devhelp w innych aplikacjach
Group:		X11/Libraries
Requires:	glib2 >= 1:2.60
Requires:	gtk+3 >= 3.22.0
Requires:	gtk-webkit4 >= 2.24

%description libs
Library of Devhelp for embedding into other applications.

%description libs -l pl.UTF-8
Biblioteka Devhelp do osadzania w innych aplikacjach.

%package devel
Summary:	Headers for Devhelp library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Devhelp
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.60
Requires:	gtk+3-devel >= 3.22.0
Requires:	gtk-webkit4-devel >= 2.24

%description devel
Headers for Devhelp library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Devhelp.

%package static
Summary:	Static Devhelp library
Summary(pl.UTF-8):	Statyczna biblioteka Devhelp
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of Devhelp library.

%description static -l pl.UTF-8
Statyczna biblioteka Devhelp.

%package apidocs
Summary:	Devhelp API documetation
Summary(pl.UTF-8):	Dokumentacja API Devhelp
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
Devhelp API documetation.

%description apidocs -l pl.UTF-8
Dokumentacja API Devhelp.

%package -n gedit-plugin-devhelp
Summary:	Devhelp plugin for Gedit editor
Summary(pl.UTF-8):	Wtyczka devhelpa dla edytora Gedit
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
# python3 based gedit
Requires:	gedit >= 3.8
Requires:	libpeas-loader-python3
Requires:	python3 >= 1:3.3
Requires:	python3-pygobject3 >= 3
Obsoletes:	gedit2-plugin-devhelp

%description -n gedit-plugin-devhelp
Plugin that allows to browse API documentation in Gedit.

%description -n gedit-plugin-devhelp -l pl.UTF-8
Wtyczka umożliwiająca przeglądanie dokumentacji API w edytorze Gedit.

%prep
%setup -q
%patch0 -p1

%if %{with static_libs}
%{__sed} -i '/libdevhelp = / s/shared_library/library/' devhelp/meson.build
%endif

%build
%meson build \
	%{?with_apidocs:-Dgtk_doc=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/{books,references,specs}

%ninja_install -C build

%py3_comp $RPM_BUILD_ROOT%{_libdir}/gedit/plugins
%py3_ocomp $RPM_BUILD_ROOT%{_libdir}/gedit/plugins

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%update_icon_cache hicolor

%postun
%glib_compile_schemas
%update_icon_cache hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO
%attr(755,root,root) %{_bindir}/devhelp
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/assistant
# 3 following are data dirs
%dir %{_datadir}/%{name}/books
%dir %{_datadir}/%{name}/references
%dir %{_datadir}/%{name}/specs
%{_datadir}/dbus-1/services/org.gnome.Devhelp.service
%{_datadir}/glib-2.0/schemas/org.gnome.devhelp.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.libdevhelp-3.gschema.xml
%{_datadir}/metainfo/org.gnome.Devhelp.appdata.xml
%{_desktopdir}/org.gnome.Devhelp.desktop
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Devhelp.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Devhelp-symbolic.svg
%{_mandir}/man1/devhelp.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdevhelp-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdevhelp-3.so.6
%{_libdir}/girepository-1.0/Devhelp-3.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdevhelp-3.so
%{_datadir}/gir-1.0/Devhelp-3.0.gir
%{_pkgconfigdir}/libdevhelp-3.0.pc
%{_includedir}/devhelp-3

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdevhelp-3.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/devhelp-3
%endif

%files -n gedit-plugin-devhelp
%defattr(644,root,root,755)
%{_libdir}/gedit/plugins/devhelp.plugin
%{_libdir}/gedit/plugins/devhelp.py
%{_libdir}/gedit/plugins/__pycache__/devhelp.cpython-*.py[co]
