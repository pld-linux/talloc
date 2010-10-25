Summary:	The talloc library - a hierarchical pool based memory system
Summary(pl.UTF-8):	Biblioteka talloc - system przydzielania pamięci oparty na hierarchicznej puli
Name:		libtalloc
Version:	2.0.1
Release:	5
Epoch:		2
License:	LGPL v3+
Group:		Daemons
Source0:	http://samba.org/ftp/talloc/talloc-%{version}.tar.gz
# Source0-md5:	c6e736540145ca58cb3dcb42f91cf57b
URL:		http://talloc.samba.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	docbook-style-xsl
BuildRequires:	libxslt-progs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The talloc library implements a hierarchical allocator with
destructors.

%description -l pl.UTF-8
Biblioteka talloc jest implementacją systemu zarządzania pamięcią
opartego na hierarchicznej puli wraz z destruktorami.

%package devel
Summary:	Development files for the talloc library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki talloc
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Development files needed to create programs that link against the
talloc library.

%description devel -l pl.UTF-8
Pliki programistyczne potrzebne do tworzenia programów używających
biblioteki talloc.

%package static
Summary:	Static talloc library
Summary(pl.UTF-8):	Statyczna biblioteka talloc
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static talloc library.

%description static -l pl.UTF-8
Statyczna biblioteka talloc.

%prep
%setup -q -n talloc-%{version}

%build
%{__autoconf} -I libreplace
%{__autoheader} -I libreplace
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

ln -sf libtalloc.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libtalloc.so
ln -sf libtalloc.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libtalloc.so.2

%{__rm} $RPM_BUILD_ROOT%{_datadir}/swig/*/talloc.i

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%triggerpostun -p /sbin/postshell -- %{name} < 2:2.0.1-5
-rm -f %{_libdir}/libtalloc.so.2
/sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtalloc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtalloc.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtalloc.so
%{_includedir}/talloc.h
%{_pkgconfigdir}/talloc.pc
%{_mandir}/man3/talloc.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libtalloc.a
