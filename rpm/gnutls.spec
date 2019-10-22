Summary: A TLS protocol implementation
Name: gnutls
Version: 2.12.24
Release: 1
# The libgnutls core library is LGPLv2+, MeeGo doesn't ship other
# utilities or remaining libraries
License: LGPLv2+
Group: System/Libraries
BuildRequires: pkgconfig(libgcrypt) >= 1.4.0
BuildRequires: pkgconfig(libtasn1)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(p11-kit-1)
BuildRequires: libtool, automake, autoconf, gettext-devel
URL: http://www.gnutls.org/
Source0: %{name}-%{version}.tar.bz2
Source1: libgnutls-config

%package devel
Summary: Development files for the %{name} package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libgcrypt-devel
Requires: pkgconfig

%description
GnuTLS is a project that aims to develop a library which provides a secure 
layer, over a reliable transport layer. Currently the GnuTLS library implements
the proposed standards by the IETF's TLS working group.

%description devel
GnuTLS is a project that aims to develop a library which provides a secure
layer, over a reliable transport layer. Currently the GnuTLS library implements
the proposed standards by the IETF's TLS working group.
This package contains files needed for developing applications with
the GnuTLS library.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}

%description doc
%{summary}.

%prep
%setup -q -n %{name}-%{version}/gnutls

%build
make autoreconf
pushd lib
%configure --disable-srp-authentication \
           --with-libgcrypt
make %{_smp_mflags}
cp COPYING COPYING.LIB
popd

%install
rm -fr $RPM_BUILD_ROOT
pushd lib
%makeinstall
popd
rm -f $RPM_BUILD_ROOT%{_bindir}/srptool
rm -f $RPM_BUILD_ROOT%{_bindir}/gnutls-srpcrypt
install -d $RPM_BUILD_ROOT%{_bindir}
install -m755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/libgnutls-config
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m0644 -t $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} \
        README AUTHORS

%find_lang libgnutls

%clean
rm -fr $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f libgnutls.lang
%defattr(-,root,root,-)
%license lib/COPYING.LIB
%{_libdir}/libgnutls*.so.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/libgnutls*-config
%dir %{_includedir}/gnutls
%{_includedir}/gnutls/*.h
%{_libdir}/libgnutls*.a
%{_libdir}/libgnutls*.so
%{_libdir}/pkgconfig/*.pc

%files doc
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}
