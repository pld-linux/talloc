Summary:	The talloc library
Name:		libtalloc
Version:	2.0.1
DIE FOR NOW (we use libtalloc from samba)
Release:	0.1
License:	LGPL v3+
Group:		Daemons
URL:		http://talloc.samba.org/
Source0:	http://samba.org/ftp/talloc/talloc-%{version}.tar.gz
# Source0-md5:	c6e736540145ca58cb3dcb42f91cf57b
BuildRequires:	autoconf
BuildRequires:	docbook-style-xsl
BuildRequires:	libxslt

%description
A library that implements a hierarchical allocator with destructors.

%package devel
Summary:	Developer tools for the Talloc library
Group:		Development/Libraries
Requires:	libtalloc = %{version}-%{release}

%description devel
Header files needed to develop programs that link against the Talloc
library.

%prep
%setup -q -n talloc-%{version}

%build
./autogen.sh
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

ln -s libtalloc.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libtalloc.so.2
ln -s libtalloc.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libtalloc.so

rm -f $RPM_BUILD_ROOT%{_libdir}/libtalloc.a
rm -f $RPM_BUILD_ROOT%{_datadir}/swig/*/talloc.i


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtalloc.so.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/talloc.h
%attr(755,root,root) %{_libdir}/libtalloc.so
%{_pkgconfigdir}/talloc.pc
%{_mandir}/man3/talloc.3*

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
