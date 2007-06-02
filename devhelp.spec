Summary:	API documentation browser for GNOME
Summary(pl.UTF-8):	Przeglądarka dokumentacji API dla GNOME
Name:		devhelp
Version:	0.14
Release:	2
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/devhelp/0.14/%{name}-%{version}.tar.bz2
# Source0-md5:	56dd99412ae3df14a0daf293a9cd398c
Patch0:		%{name}-bookdir.patch
Patch1:		%{name}-mozilla_includes.patch
URL:		http://www.imendio.com/projects/devhelp/
BuildRequires:	GConf2-devel >= 2.18.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-common >= 2.18.0
BuildRequires:	gnome-vfs2-devel >= 2.18.1
BuildRequires:	gtk+2-devel >= 2:2.10.11
BuildRequires:	libglade2-devel >= 1:2.6.0
BuildRequires:	libtool
BuildRequires:	libwnck-devel >= 2.18.0
BuildRequires:	xulrunner-devel >= 1.8.0.4
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	zlib-devel
Requires(post,preun):	GConf2 >= 2.18.0
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires:	%{name}-libs = %{version}-%{release}
%requires_eq_to	xulrunner xulrunner-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# can be provided by mozilla or mozilla-embedded
%define		_noautoreqdep	libgtkembedmoz.so libxpcom.so
# we have strict deps for it
%define		_noautoreq	libxpcom.so

%description
API documentation browser for GNOME.

%description -l pl.UTF-8
Przeglądarka dokumentacji API dla GNOME.

%package libs
Summary:	Library to embed Devhelp in other applications
Summary(pl.UTF-8):	Biblioteka do osadzania Devhelp w innych aplikacjach
Group:		Libraries

%description libs
Library of Devhelp for embedding into other applications.

%description libs -l pl.UTF-8
Biblioteka Devhelp do osadzania w innych aplikacjach.

%package devel
Summary:	Headers for Devhelp library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Devhelp
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Headers for Devhelp library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Devhelp.

%package static
Summary:	Static Devhelp library
Summary(pl.UTF-8):	Statyczna biblioteka Devhelp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of Devhelp library.

%description static -l pl.UTF-8
Statyczna biblioteka Devhelp.

%package -n gedit2-plugin-devhelp
Summary:	Devhelp plugin for Gedit editor
Summary(pl.UTF-8):	Wtyczka devhelpa dla edytora Gedit
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	gedit2

%description -n gedit2-plugin-devhelp
Allows to browse API documentation in Gedit.

%description -n gedit2-plugin-devhelp -l pl.UTF-8
Umożliwia przeglądanie dokumentacji API w Gedit.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-static \
	--disable-install-schemas
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/gconf \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/{books,specs}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_datadir}/mime-info
rm -f $RPM_BUILD_ROOT%{_libdir}/gedit-2/plugins/%{name}/*.py

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install devhelp.schemas
%update_desktop_database_post
%update_icon_cache hicolor

%preun
%gconf_schema_uninstall devhelp.schemas

%postun
%update_desktop_database_postun
%update_icon_cache hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/devhelp*
%{_datadir}/%{name}
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/*
%{_sysconfdir}/gconf/schemas/devhelp.schemas

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_pkgconfigdir}/*.pc
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files -n gedit2-plugin-devhelp
%defattr(644,root,root,755)
%dir %{_libdir}/gedit-2/plugins/%{name}
%{_libdir}/gedit-2/plugins/%{name}.gedit-plugin
%{_libdir}/gedit-2/plugins/%{name}/*.py[oc]
