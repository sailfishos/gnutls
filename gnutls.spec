Summary: A TLS protocol implementation
Name: gnutls
Version: 3.7.2
Release: 1
# The libgnutls core library is LGPLv2+, MeeGo doesn't ship other
# utilities or remaining libraries
License: LGPLv2+
Group: System/Libraries
BuildRequires: pkgconfig(libtasn1)
BuildRequires: pkgconfig(p11-kit-1)
BuildRequires: pkgconfig(nettle)
BuildRequires: gmp-devel
BuildRequires: libtool, automake, autoconf, gettext-devel texinfo
URL: http://www.gnutls.org/
Source0: %{name}-%{version}.tar.xz

%package devel
Summary: Development files for the %{name} package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS
protocols and technologies around them. It provides a simple C language
application programming interface (API) to access the secure communications
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and
other required structures.

%description devel
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS
protocols and technologies around them. It provides a simple C language
application programming interface (API) to access the secure communications
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and
other required structures.
This package contains files needed for developing applications with
the GnuTLS library.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}

%description doc
%{summary}.

%prep
%setup -q -n %{name}-%{version}

%build
%configure --with-included-unistring --disable-srp-authentication
%make_build

%install
rm -fr $RPM_BUILD_ROOT
%makeinstall
rm -f $RPM_BUILD_ROOT%{_libdir}/libgnutls*.la
rm -f $RPM_BUILD_ROOT%{_docdir}/gnutls/*.png
rm -rf $RPM_BUILD_ROOT%{_bindir}
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -rf $RPM_BUILD_ROOT%{_mandir}

%find_lang gnutls

%clean
rm -fr $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f gnutls.lang
%defattr(-,root,root,-)
%license LICENSE doc/COPYING.LESSER
%{_libdir}/libgnutls*.so.*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/gnutls
%{_includedir}/gnutls/*.h
%{_libdir}/libgnutls*.so
%{_libdir}/pkgconfig/*.pc

%files doc
%defattr(-,root,root,-)
%doc README.md AUTHORS
