%define		minmozver	5:1.7
Summary:	DevHelp is a developer's help program for GNOME
Summary(pl):	Program pomocy dla programistów GNOME
Name:		devhelp
Version:	0.9.1
Release:	3
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/0.9/%{name}-%{version}.tar.bz2
# Source0-md5:	2d6358178bbb4e74cf564b7c608d46fa
Patch0:		%{name}-bookdir.patch
Patch1:		%{name}-locale-names.patch
Patch2:		%{name}-mozilla_home.patch
URL:		http://www.imendio.com/projects/devhelp/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-common >= 2.8.0
BuildRequires:	gnome-vfs2-devel >= 2.4.0
BuildRequires:	gtk+2-devel >= 2:2.4.4
BuildRequires:	libglade2-devel >= 2.0.0
BuildRequires:	libgnomeui-devel >= 2.4.0
BuildRequires:	libtool
BuildRequires:	mozilla-devel >= %{minmozver}
BuildRequires:	zlib-devel
Requires(post,postun):	GConf2
Requires:	%{name}-libs = %{version}-%{release}
Requires:	mozilla =  %(rpm -q --qf '%{EPOCH}:%{VERSION}' --whatprovides mozilla)
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

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

mv po/{no,nb}.po

%build
%{__libtoolize}
%{__aclocal}
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

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install

%postun
%gconf_schema_install

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/devhelp*
%{_datadir}/%{name}
%{_datadir}/mime-info/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
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
