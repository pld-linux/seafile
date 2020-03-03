# NOTE:
# using -server tag because 5.1.2..5.1.2-server differ
# http://manual.seafile.com/build_seafile/server.html
# explanation of the tags:
# http://manual.seafile.com/deploy/#for-those-that-want-to-package-seafile-server
# TODO
# - fix python to install sitescriptdir: %{py_sitedir}/seafile

Summary:	File syncing and sharing software with file encryption and group sharing
Name:		seafile
Version:	7.0.5
Release:	2
License:	GPL v2
Group:		Applications/Networking
Source0:	https://github.com/haiwen/seafile/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9904adcb43b7194a8e89552794f77209
URL:		http://seafile.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	pkgconfig
BuildRequires:	ccnet-devel
BuildRequires:	curl-devel
BuildRequires:	glib2-devel
BuildRequires:	intltool
BuildRequires:	jansson-devel
BuildRequires:	libevent-devel
BuildRequires:	libfuse-devel >= 2.7.3
# for bin/searpc-codegen
BuildRequires:	libsearpc
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	openssl-devel
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	vala
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Seafile is a next-generation open source cloud storage system with
advanced support for file syncing, privacy protection and teamwork.

Seafile allows users to create groups with file syncing, wiki, and
discussion to enable easy collaboration around documents within a
team.

%package devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

# bogus destdir?
%{__sed} -i -e 's/(DESTDIR)//' lib/libseafile.pc.in

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python(\s|$),#!%{__python}\1,' \
      app/seaf-cli \
      scripts/breakpad.py \
      setupwin.py

%build
%{__glib_gettextize}
%{__intltoolize} --automake
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake} --gnu
%{__autoconf}
%configure \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_postclean

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libseafile.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.markdown LICENSE.txt
%attr(755,root,root) %{_libdir}/libseafile.so.*.*.*
%ghost %{_libdir}/libseafile.so.0
%attr(755,root,root) %{_bindir}/seaf-cli
%attr(755,root,root) %{_bindir}/seaf-daemon
%{_mandir}/man1/seaf-cli.1*
%{_mandir}/man1/seaf-daemon.1*
%dir %{py_sitedir}/seafile
%{py_sitedir}/seafile/*.py[co]

%files devel
%defattr(644,root,root,755)
%{_includedir}/seafile
%{_libdir}/libseafile.so
%{_pkgconfigdir}/libseafile.pc
