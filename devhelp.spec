Summary:	DevHelp is a developer's help program for GNOME
Summary(pl):	Program pomocy dla developerów GNOME
Name:		devhelp
Version:	0.3
Release:	1.1
License:	GPL
Group:		X11/Applications
Source0:	http://www.devhelp.net/download/%{name}-%{version}.tar.gz
URL:		http://www.devhelp.net/
BuildRequires:	glib-devel >= 1.2.9
BuildRequires:	gtk+-devel >= 1.2.9
BuildRequires:	libxml-devel >= 1.8.10
BuildRequires:	gnome-vfs-devel >= 1.0.0
BuildRequires:	ORBit-devel >= 0.5.7
BuildRequires:	gnome-libs-devel >= 1.2.8
BuildRequires:	GConf-devel >= 0.12
BuildRequires:	gtkhtml-devel >= 0.10.0
BuildRequires:	gnome-print-devel >= 0.29
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define		_sysconfdir	/etc/X11/GNOME

%description
DevHelp is a developer's help program for GNOME.

%description -l pl
Program pomocy dla developerów GNOME.

%prep
%setup -q

%build
%configure2_13 \
	--disable-install-schemas
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/gconf

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT 

gzip -9nf AUTHORS ChangeLog NEWS README TODO

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/devhelp
%dir %{_libdir}/*
%dir %{_prefix}/share/
%dir %{_prefix}/share/%{name}/glade/*
%dir %{_prefix}/share/gnome/apps/Development/*
%dir %{_prefix}/share/gnome/ui/*
%dir %{_prefix}/share/images/%{name}/*
%dir %{_prefix}/share/oaf/*
%dir %{_prefix}/share/pixmaps/*
%{_sysconfdir}/*/*/*
