Summary:	The talloc library - a hierarchical pool based memory system
Summary(pl.UTF-8):	Biblioteka talloc - system przydzielania pamięci oparty na hierarchicznej puli
Name:		talloc
Version:	2.0.7
Release:	2
License:	LGPL v3+
Group:		Libraries
Source0:	http://samba.org/ftp/talloc/%{name}-%{version}.tar.gz
# Source0-md5:	dbfb3146f4cc47054e13b8a2988299f9
URL:		http://talloc.samba.org/
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	libxslt-progs
BuildRequires:	python >= 1:2.4.2
BuildRequires:	python-devel >= 1:2.4.2
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
Provides:	libtalloc = 2:%{version}-%{release}
Obsoletes:	libtalloc < 2:2.0.7-1
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
Requires:	%{name} = %{version}-%{release}
Provides:	libtalloc-devel = 2:%{version}-%{release}
Obsoletes:	libtalloc-devel < 2:2.0.7-1
Obsoletes:	libtalloc-static

%description devel
Development files needed to create programs that link against the
talloc library.

%description devel -l pl.UTF-8
Pliki programistyczne potrzebne do tworzenia programów używających
biblioteki talloc.

%package -n python-talloc
Summary:	Python binding for talloc library
Summary(pl.UTF-8):	Wiązanie Pythona do biblioteki talloc
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-libs >= 1:2.4.2

%description -n python-talloc
Python binding for talloc library.

%description -n python-talloc -l pl.UTF-8
Wiązanie Pythona do biblioteki talloc.

%package -n python-talloc-devel
Summary:	Development files for pytalloc-util library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki pytalloc-util
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	python-devel >= 1:2.4.2
Requires:	python-talloc = %{version}-%{release}

%description -n python-talloc-devel
Development files for pytalloc-util library.

%description -n python-talloc-devel -l pl.UTF-8
Pliki programistyczne biblioteki pytalloc-util.

%prep
%setup -q

%build
# note: configure in fact is waf call
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
PYTHONDIR=%{py_sitedir} \
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir}

%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%triggerpostun -p /sbin/postshell -- libtalloc < 2:2.0.1-5
-rm -f %{_libdir}/libtalloc.so.2
/sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtalloc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtalloc.so.2

%files devel
%defattr(644,root,root,755)
%doc talloc_guide.txt
%attr(755,root,root) %{_libdir}/libtalloc.so
%{_includedir}/talloc.h
%{_pkgconfigdir}/talloc.pc
%{_mandir}/man3/talloc.3*

%files -n python-talloc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpytalloc-util.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpytalloc-util.so.2
%attr(755,root,root) %{py_sitedir}/talloc.so

%files -n python-talloc-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpytalloc-util.so
%{_includedir}/pytalloc.h
%{_pkgconfigdir}/pytalloc-util.pc
