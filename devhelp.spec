Summary:	DevHelp is a developer's help program for GNOME
Summary(pl):	Program pomocy dla programist�w GNOME
Name:		devhelp
Version:	0.7
Release:	3
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/0.7/%{name}-%{version}.tar.bz2
# Source0-md5:	7391578353368d9db3ed6a74f4128754
Patch0:		%{name}-bookdir.patch
URL:		http://www.imendio.com/projects/devhelp/
BuildRequires:	automake
BuildRequires:	gnome-vfs2-devel
BuildRequires:	libgnomeui-devel >= 2.3.3.1-2
BuildRequires:	libgtkhtml-devel >= 2.2.1
BuildRequires:	zlib-devel
Requires:	libgtkhtml >= 2.2.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DevHelp is a developer's help program for GNOME.

%description -l pl
Program pomocy dla programist�w GNOME.

%prep
%setup -q
%patch0 -p1

%build
cp /usr/share/automake/config.sub .
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

# shut up check-files
rm -f $RPM_BUILD_ROOT%{_libdir}/devhelp/*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/devhelp
%dir %{_libdir}/devhelp
%attr(755,root,root) %{_libdir}/devhelp/*.so
%{_datadir}/%{name}
%{_datadir}/mime-info/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
