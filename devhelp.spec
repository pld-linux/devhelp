Summary:	DevHelp is a developer's help program for GNOME
Summary(pl):	Program pomocy dla developerów GNOME
Name:		devhelp
Version:	0.6.0
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/0.6/%{name}-%{version}.tar.bz2
# Source0-md5:	550483a3717f8bc58d0f3bfdab57413f
Patch0:		%{name}-bookdir.patch
URL:		http://www.devhelp.net/
BuildRequires:	gnome-vfs2-devel
BuildRequires:	libgnomeui-devel
BuildRequires:	libgtkhtml-devel >= 2.2.1
BuildRequires:	zlib-devel
Requires:	libgtkhtml >= 2.2.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DevHelp is a developer's help program for GNOME.

%description -l pl
Program pomocy dla developerów GNOME.

%prep
%setup -q
%patch0 -p1

%build
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

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/devhelp
%dir %{_libdir}/*/*
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}
%{_datadir}/mime-info/*
%{_pixmapsdir}/*
