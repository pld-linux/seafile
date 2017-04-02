# NOTE:
# using -server tag because 5.1.2..5.1.2-server differ
# http://manual.seafile.com/build_seafile/server.html
# explanation of the tags:
# http://manual.seafile.com/deploy/#for-those-that-want-to-package-seafile-server
# TODO
# - fix python to install sitescriptdir: %{py_sitedir}/seafile

Summary:	File syncing and sharing software with file encryption and group sharing
Name:		seafile
Version:	5.1.2
Release:	2
License:	GPL v2
Group:		Applications/Networking
Source0:	https://github.com/haiwen/seafile/archive/v%{version}-server/%{name}-%{version}.tar.gz
# Source0-md5:	5fa7f0403aa168088c42498018f72422
Patch0:		codegen.patch
URL:		http://seafile.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	pkgconfig
BuildRequires:	ccnet-devel = %{version}
BuildRequires:	curl-devel
BuildRequires:	glib2-devel
BuildRequires:	intltool
BuildRequires:	jansson-devel
BuildRequires:	libevent-devel
BuildRequires:	libfuse-devel >= 2.7.3
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
%setup -qn %{name}-%{version}-server
%patch0 -p1

# bogus destdir?
sed -i -e 's/(DESTDIR)//' lib/libseafile.pc.in

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
%dir %{py_sitedir}/seaserv
%{py_sitedir}/seaserv/*.py[co]

%files devel
%defattr(644,root,root,755)
%{_includedir}/seafile
%{_libdir}/libseafile.so
%{_pkgconfigdir}/libseafile.pc
