Summary:	DevHelp is a developer's help program for GNOME
Summary(pl):	Program pomocy dla programistów GNOME
Name:		devhelp
Version:	0.8
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/0.8/%{name}-%{version}.tar.bz2
# Source0-md5:	83e2521ac66288996d3907d51be413a4
Patch0:		%{name}-bookdir.patch
Patch1:		%{name}-enable-deprecated.patch
URL:		http://www.imendio.com/projects/devhelp/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-vfs2-devel
BuildRequires:	libgnomeui-devel >= 2.3.3.1-2
BuildRequires:	libgtkhtml-devel >= 2.2.1
BuildRequires:	libtool
BuildRequires:	zlib-devel
Requires:	libgtkhtml >= 2.2.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DevHelp is a developer's help program for GNOME.

%description -l pl
Program pomocy dla programistów GNOME.

%package devel
Summary:        Library to embed Devhelp in other applications
Summary(pl):    Biblioteka do osadzania Devhelp w innych aplikacjach
Group:          X11/Development/Libraries
Requires:       %{name} = %{version}

%description devel
Library of Devhelp for embedding into other applications.

%description devel -l pl
Biblioteka Devhelp do osadzania w innych aplikacjach.

%package static
Summary:        Static library of Devhelp
Summary(pl):    Biblioteka statyczna Devhelp
Group:          X11/Development/Libraries
Requires:       %{name}-devel = %{version}

%description static
Static library of Devhelp.

%description static -l pl
Biblioteka statyczna Devhelp.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cp /usr/share/automake/config.sub .
%{__libtoolize}
%{__aclocal} -I %{_aclocaldir}/gnome2-macros
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

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/devhelp
%attr(755,root,root) %{_libdir}/*.so.*.*.*
%{_datadir}/%{name}
%{_datadir}/mime-info/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/devhelp*
%{_libdir}/*.so
%{_libdir}/*.la
%{_pkgconfigdir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
