Summary:	DevHelp is a developer's help program for GNOME
Summary(pl):	Program pomocy dla developerów GNOME
Name:		devhelp
Version:	0.3
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://www.devhelp.net/download/%{name}-%{version}.tar.gz
URL:		http://www.devhelp.net/
BuildRequires:	GConf-devel >= 0.12
BuildRequires:	ORBit-devel >= 0.5.7
BuildRequires:	autoconf
BuildRequires:	gdk-pixbuf-gnome-devel >= 0.18.0
BuildRequires:	glib-devel >= 1.2.9
BuildRequires:	gnome-libs-devel >= 1.2.8
BuildRequires:	gnome-print-devel >= 0.29
BuildRequires:	gnome-vfs-devel >= 1.0.0
BuildRequires:	gtkhtml-devel >= 0.10.0
BuildRequires:	gtk+-devel >= 1.2.9
BuildRequires:	libxml-devel >= 1.8.10
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
%{__autoconf}
%configure \
	--disable-install-schemas
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/gconf \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/{books,specs}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT 

mv -f $RPM_BUILD_ROOT%{_datadir}/gnome/apps $RPM_BUILD_ROOT%{_applnkdir}

gzip -9nf AUTHORS ChangeLog NEWS README TODO

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/devhelp
%dir %{_libdir}/*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/books
%dir %{_datadir}/%{name}/specs
%{_datadir}/%{name}/glade
%{_applnkdir}/Development/*
%{_datadir}/gnome/ui/*
%{_datadir}/images/%{name}
%{_datadir}/oaf/*
%{_pixmapsdir}/*
%{_sysconfdir}/*/*/*
