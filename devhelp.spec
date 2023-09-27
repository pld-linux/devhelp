#
# Conditional build:
%bcond_without  apidocs         # gtk-doc based API documentation
%bcond_without  static_libs     # static library

Summary:	API documentation browser for GNOME
Summary(pl.UTF-8):	Przeglądarka dokumentacji API dla GNOME
Name:		devhelp
Version:	43.0
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/devhelp/43/%{name}-%{version}.tar.xz
# Source0-md5:	14b56884ae13c4ad7d87036a65b9eaed
Patch0:		%{name}-bookdir.patch
URL:		https://wiki.gnome.org/Apps/Devhelp
BuildRequires:	gettext-tools >= 0.19.7
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.6}
BuildRequires:	glib2-devel >= 1:2.64
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+3-devel >= 3.22.0
# gtk-webkit4-devel >= 2.26 possible as fallback
BuildRequires:	gtk-webkit4.1-devel >= 2.34
BuildRequires:	meson >= 0.57
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 1:3.3
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.029
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2 >= 1:2.64
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
Requires:	glib2 >= 1:2.64
Requires:	gtk+3 >= 3.22.0
Requires:	gtk-webkit4.1 >= 2.34

%description libs
Library of Devhelp for embedding into other applications.

%description libs -l pl.UTF-8
Biblioteka Devhelp do osadzania w innych aplikacjach.

%package devel
Summary:	Headers for Devhelp library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Devhelp
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.64
Requires:	gtk+3-devel >= 3.22.0
Requires:	gtk-webkit4.1-devel >= 2.34

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
BuildArch:	noarch

%description apidocs
Devhelp API documetation.

%description apidocs -l pl.UTF-8
Dokumentacja API Devhelp.

%package -n emacs-devhelp
Summary:	Emacs integration for Devhelp
Summary(pl.UTF-8):	Integracja Emacsa z Devhelpem
Group:		Applications/Editors
Requires:	%{name} = %{version}-%{release}
Requires:	emacs-common
BuildArch:	noarch

%description -n emacs-devhelp
Emacs integration for Devhelp.

%description -n emacs-devhelp -l pl.UTF-8
Integracja Emacsa z Devhelpem.

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
Obsoletes:	gedit2-plugin-devhelp < 3.4.1-2

%description -n gedit-plugin-devhelp
Plugin that allows to browse API documentation in Gedit.

%description -n gedit-plugin-devhelp -l pl.UTF-8
Wtyczka umożliwiająca przeglądanie dokumentacji API w edytorze Gedit.

%package -n vim-plugin-devhelp
Summary:	Vim integration for Devhelp
Summary(pl.UTF-8):	Integracja Vima z Devhelpem
Group:		Applications/Editors
Requires:	%{name} = %{version}-%{release}
Requires:	vim-rt
BuildArch:	noarch

%description -n vim-plugin-devhelp
Vim integration for Devhelp.

%description -n vim-plugin-devhelp -l pl.UTF-8
Integracja Vima z Devhelpem.

%prep
%setup -q
%patch0 -p1

%if %{with static_libs}
%{__sed} -i '/libdevhelp_shared_lib = / s/shared_library/library/' devhelp/meson.build
%endif

%build
%meson build \
	%{?with_apidocs:-Dgtk_doc=true} \
	-Dplugin_emacs=true \
	-Dplugin_gedit=true \
	-Dplugin_vim=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/{books,references,specs}

%ninja_install -C build

%py3_comp $RPM_BUILD_ROOT%{_libdir}/gedit/plugins
%py3_ocomp $RPM_BUILD_ROOT%{_libdir}/gedit/plugins

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/devhelp-3 $RPM_BUILD_ROOT%{_gidocdir}
%endif

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
%doc NEWS README.md
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
%{_gidocdir}/devhelp-3
%endif

%files -n emacs-devhelp
%defattr(644,root,root,755)
%{_datadir}/emacs/site-lisp/devhelp.el

%files -n gedit-plugin-devhelp
%defattr(644,root,root,755)
%{_libdir}/gedit/plugins/devhelp.plugin
%{_libdir}/gedit/plugins/devhelp.py
%{_libdir}/gedit/plugins/__pycache__/devhelp.cpython-*.py[co]

%files -n vim-plugin-devhelp
%defattr(644,root,root,755)
%{_datadir}/vim/vimfiles/plugin/devhelp.vim
