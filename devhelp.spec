#
# Conditional build:
%bcond_without	mozilla_firefox # build with mozilla instead of mozilla-firefox
#
%define		minmozver	5:1.7
Summary:	DevHelp is a developer's help program for GNOME
Summary(pl):	Program pomocy dla programistów GNOME
Name:		devhelp
Version:	0.12
Release:	3
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/devhelp/0.12/%{name}-%{version}.tar.gz
# Source0-md5:	e211ec1a75dba00d8e71a66e2ab2aec3
Patch0:		%{name}-bookdir.patch
Patch1:		%{name}-mozilla_includes.patch
Patch2:		%{name}-desktop.patch
URL:		http://www.imendio.com/projects/devhelp/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-common >= 2.8.0
BuildRequires:	gnome-vfs2-devel >= 2.10.0-2
BuildRequires:	gtk+2-devel >= 2:2.6.4
BuildRequires:	libglade2-devel >= 1:2.5.1
BuildRequires:	libtool
%if %{with mozilla_firefox}
BuildRequires:	mozilla-firefox-devel
%else
BuildRequires:	mozilla-devel >= %{minmozver}
%endif
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	zlib-devel
Requires(post,preun):	GConf2
Requires:	%{name}-libs = %{version}-%{release}
%if %{with mozilla_firefox}
%requires_eq	mozilla-firefox
%else
Requires:	mozilla = %(rpm -q --qf '%{EPOCH}:%{VERSION}' --whatprovides mozilla)
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# can be provided by mozilla or mozilla-embedded
%define		_noautoreqdep	libgtkembedmoz.so libxpcom.so

%description
DevHelp is a developer's help program for GNOME.

%description -l pl
Program pomocy dla programistów GNOME.

%package libs
Summary:	Library to embed Devhelp in other applications
Summary(pl):	Biblioteka do osadzania Devhelp w innych aplikacjach
Group:		Libraries

%description libs
Library of Devhelp for embedding into other applications..

%description libs -l pl
Biblioteka Devhelp do osadzania w innych aplikacjach..

%package devel
Summary:	Headers for Devhelp library
Summary(pl):	Pliki nag³ówkowe biblioteki Devhelp
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Headers for Devhelp library.

%description devel -l pl
Pliki nag³ówkowe biblioteki Devhelp.

%package static
Summary:	Static Devhelp library
Summary(pl):	Statyczna biblioteka Devhelp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of Devhelp library.

%description static -l pl
Statyczna biblioteka Devhelp.

%package -n gedit2-plugin-devhelp
Summary:	Devhelp plugin for Gedit editor
Summary(pl):	Wtyczka devhelpa dle edytora Gedit
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	gedit2

%description -n gedit2-plugin-devhelp
This plugin enables GTK+ documentation browser using devhelp
libraries.

%description -n gedit2-plugin-devhelp -l pl
Wtyczka umo¿liwiaj±ca przegl±danie dokumentacji GTK+ przy pomocy
bibliotek devhelpa.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-install-schemas
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/gconf \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/{books,specs}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_datadir}/mime-info

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install devhelp.schemas

%preun
%gconf_schema_uninstall devhelp.schemas

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/devhelp*
%{_datadir}/%{name}
%{_desktopdir}/*.desktop
%{_iconsdir}/*
%{_sysconfdir}/gconf/schemas/*

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
%{_libdir}/gedit-2/plugins/%{name}.gedit-plugin
%dir %{_libdir}/gedit-2/plugins/%{name}
%{_libdir}/gedit-2/plugins/%{name}/*.py[oc]
