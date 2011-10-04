Summary: A TLS protocol implementation
Name: gnutls
Version: 2.10.4
Release: 1
# The libgnutls core library is LGPLv2+, MeeGo doesn't ship other
# utilities or remaining libraries
License: LGPLv2+
Group: System/Libraries
BuildRequires: libgcrypt-devel >= 1.2.2, gettext
BuildRequires: zlib-devel, readline-devel, libtasn1-devel
BuildRequires: lzo-devel, libtool, automake, autoconf
URL: http://www.gnutls.org/
#Source0: ftp://ftp.gnutls.org/pub/gnutls/%{name}-%{version}.tar.gz
#Source1: ftp://ftp.gnutls.org/pub/gnutls/%{name}-%{version}.tar.gz.sig
# XXX patent tainted SRP code removed.
Source0: %{name}-%{version}.tar.bz2
Source1: libgnutls-config

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: libgcrypt >= 1.2.2

%package devel
Summary: Development files for the %{name} package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libgcrypt-devel
Requires: pkgconfig
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

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

%prep
%setup -q

# Remove other utils files
rm -rf maint.mk libextra doc gl lib/gl/test \
  build-aux/vc-list-files \
  build-aux/useless-if-before-free \
  build-aux/pmccabe2html

for i in auth_srp_rsa.c auth_srp_sb64.c auth_srp_passwd.c auth_srp.c gnutls_srp.c ext_srp.c; do
    touch lib/$i
done

%build
# On MeeGo we build core lib only
pushd lib
%configure --with-libtasn1-prefix=%{_prefix} \
           --disable-srp-authentication
make
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
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/srptool.1
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/*srp*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
%find_lang libgnutls

%clean
rm -fr $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
if [ -f %{_infodir}/gnutls.info.gz ]; then
    /sbin/install-info %{_infodir}/gnutls.info.gz %{_infodir}/dir || :
fi

%preun devel
if [ $1 = 0 -a -f %{_infodir}/gnutls.info.gz ]; then
   /sbin/install-info --delete %{_infodir}/gnutls.info.gz %{_infodir}/dir || :
fi


%files -f libgnutls.lang
%defattr(-,root,root,-)
%{_libdir}/libgnutls*.so.*
%doc lib/COPYING.LIB README AUTHORS

%files devel
%defattr(-,root,root,-)
%{_bindir}/libgnutls*-config
%{_includedir}/*
%{_libdir}/libgnutls*.a
%{_libdir}/libgnutls*.so
%{_libdir}/pkgconfig/*.pc
#%{_mandir}/man3/*
#%{_infodir}/gnutls*