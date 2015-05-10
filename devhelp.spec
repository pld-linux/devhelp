Summary:	API documentation browser for GNOME
Summary(pl.UTF-8):	Przeglądarka dokumentacji API dla GNOME
Name:		devhelp
Version:	3.16.1
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/devhelp/3.16/%{name}-%{version}.tar.xz
# Source0-md5:	ee158fdb4cd29f7bde0026d69e3f333f
Patch0:		%{name}-bookdir.patch
Patch1:		%{name}-use-python3.patch
URL:		http://www.imendio.com/projects/devhelp/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	glib2-devel >= 1:2.38.0
BuildRequires:	gnome-common >= 2.24.0
BuildRequires:	gtk+3-devel >= 3.14.0
BuildRequires:	gtk-webkit4-devel >= 2.0.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.3
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires(post,postun):	glib2 >= 1:2.32.0
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gtk-webkit4 >= 2.0.0
Requires:	hicolor-icon-theme
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
API documentation browser for GNOME.

%description -l pl.UTF-8
Przeglądarka dokumentacji API dla GNOME.

%package libs
Summary:	Library to embed Devhelp in other applications
Summary(pl.UTF-8):	Biblioteka do osadzania Devhelp w innych aplikacjach
Group:		X11/Libraries

%description libs
Library of Devhelp for embedding into other applications.

%description libs -l pl.UTF-8
Biblioteka Devhelp do osadzania w innych aplikacjach.

%package devel
Summary:	Headers for Devhelp library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Devhelp
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.38.0
Requires:	gtk+3-devel >= 3.14.0

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

%package -n gedit-plugin-devhelp
Summary:	Devhelp plugin for Gedit editor
Summary(pl.UTF-8):	Wtyczka devhelpa dla edytora Gedit
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	gedit
Requires:	libpeas-loader-python3
Requires:	python3-pygobject3
Obsoletes:	gedit2-plugin-devhelp

%description -n gedit-plugin-devhelp
Plugin that allows to browse API documentation in Gedit.

%description -n gedit-plugin-devhelp -l pl.UTF-8
Wtyczka umożliwiająca przeglądanie dokumentacji API w edytorze Gedit.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-static \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/{books,references,specs}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name}

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
%{_datadir}/%{name}
%{_desktopdir}/devhelp.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%{_iconsdir}/hicolor/*/apps/*.svg
%{_datadir}/GConf/gsettings/devhelp.convert
%{_datadir}/glib-2.0/schemas/org.gnome.devhelp.gschema.xml
%{_datadir}/appdata/devhelp.appdata.xml

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdevhelp-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdevhelp-3.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdevhelp-3.so
%{_pkgconfigdir}/libdevhelp-3.0.pc
%{_includedir}/devhelp-3.0

%files static
%defattr(644,root,root,755)
%{_libdir}/libdevhelp-3.a

%files -n gedit-plugin-devhelp
%defattr(644,root,root,755)
%{_libdir}/gedit/plugins/__pycache__
%{_libdir}/gedit/plugins/devhelp.plugin
%{_libdir}/gedit/plugins/devhelp.py
