Summary:	The talloc library - a hierarchical pool based memory system
Summary(pl.UTF-8):	Biblioteka talloc - system przydzielania pamięci oparty na hierarchicznej puli
Name:		talloc
Version:	2.3.1
Release:	1
Epoch:		2
License:	LGPL v3+
Group:		Libraries
Source0:	https://www.samba.org/ftp/talloc/%{name}-%{version}.tar.gz
# Source0-md5:	ce40593428c0de6b85946189dcc37b5e
URL:		https://talloc.samba.org/
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	libxslt-progs
BuildRequires:	python3 >= 1:3.2
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	rpm-pythonprov
Provides:	libtalloc = 2:%{version}-%{release}
Obsoletes:	libtalloc < 2:2.0.7-2
# talloc 2.2+ dropped python2 support
Obsoletes:	python-talloc
Obsoletes:	python-talloc-devel
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
Provides:	libtalloc-devel = 2:%{version}-%{release}
Obsoletes:	libtalloc-devel < 2:2.0.7-2
Obsoletes:	libtalloc-static

%description devel
Development files needed to create programs that link against the
talloc library.

%description devel -l pl.UTF-8
Pliki programistyczne potrzebne do tworzenia programów używających
biblioteki talloc.

%package -n python3-talloc
Summary:	Python 3 binding for talloc library
Summary(pl.UTF-8):	Wiązanie Pythona 3 do biblioteki talloc
Group:		Libraries/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	python3-libs >= 1:3.2

%description -n python3-talloc
Python 2 binding for talloc library.

%description -n python3-talloc -l pl.UTF-8
Wiązanie Pythona 3 do biblioteki talloc.

%package -n python3-talloc-devel
Summary:	Development files for Python 3 pytalloc-util library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki pytalloc-util dla Pythona 3
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Requires:	python3-devel >= 1:3.2
Requires:	python3-talloc = %{epoch}:%{version}-%{release}

%description -n python3-talloc-devel
Development files for Python 3 pytalloc-util library.

%description -n python3-talloc-devel -l pl.UTF-8
Pliki programistyczne biblioteki pytalloc-util dla Pythona 3.

%prep
%setup -q

%build
# threading breaks waf
export JOBS=1

CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python3} buildtools/bin/waf configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--disable-rpath

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

%post	-n python3-talloc -p /sbin/ldconfig
%postun	-n python3-talloc -p /sbin/ldconfig

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

%files -n python3-talloc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpytalloc-util.cpython-3*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpytalloc-util.cpython-3*.so.2
%attr(755,root,root) %{py3_sitedir}/talloc.cpython-3*.so

%files -n python3-talloc-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpytalloc-util.cpython-3*.so
%{_includedir}/pytalloc.h
%{_pkgconfigdir}/pytalloc-util.cpython-3*.pc
