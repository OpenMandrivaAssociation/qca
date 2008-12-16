%define build_debug 0
%{?_with_debug: %{expand: %%global build_debug 1}}

%define build_sys_rootcerts 1
%{?_without_sys_rootcerts: %{expand: %%global build_sys_rootcerts 0}}

%define qtcryptodir	%{qt4plugins}/crypto
%define lib_major	2
%define lib_name	%mklibname %{name} %{lib_major}
%define develname	%mklibname %{name} -d
%define source_ver	%{version}

Name: qca
Version: 2.0.1
Release: %mkrel 4
License: LGPLv2+
Summary: Straightforward and cross-platform crypto API for Qt
Group: System/Libraries
URL: http://delta.affinix.com/qca
# Warning: Code coming from kdesupport to match kde development
Source0: http://delta.affinix.com/download/%{name}/2.0/%{name}-%{version}.tar.bz2
Patch0: qca-2.0.1-mandir.patch
# From upstream SVN: drop use of whirlpool, no longer available in
# openssl - AdamW 2008/12
Patch1: qca-2.0.1-whirlpool.patch
# Fix underlinking in the openssl plugin - AdamW 2008/12
Patch2: qca-2.0.1-underlink.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: qt4-devel >= 2:4.2
%if %{build_sys_rootcerts}
BuildRequires: rootcerts
%endif
BuildRequires: cmake
BuildRequires: libgcrypt-devel
BuildRequires: libsasl-devel
BuildRequires: nss-devel
Obsoletes: qca2 < 2.0.1-3
Provides: qca2 = %{version}-%{release}
Requires: qt4-common >= 4.3

%description
The QCA library provides an easy API for a range of cryptographic
features, including SSL/TLS, X.509 certificates, SASL, symmetric
ciphers, public key ciphers, hashes and much more.

Functionality is supplied via plugins. This is useful for avoiding
dependence on a particular crypto library and makes upgrading easier,
as there is no need to recompile your application when adding or
upgrading a crypto plugin. Also, by pushing crypto functionality into
plugins, applications are free of legal issues, such as export
regulation.

%files
%defattr(0644,root,root,0755)
%doc README COPYING INSTALL TODO
%defattr(0755,root,root,0755)
%{qt4dir}/bin/qcatool2
%_mandir/man1/*

#------------------------------------------------------------------------------

%if ! %{build_sys_rootcerts}
%package -n %{name}-root-certificates
Summary:	Common root CA certificates for QCA
Group:		System/Libraries
Requires:	%{lib_name} = %{version}-%{release}

%description	-n %{name}-root-certificates
Provides root Certificate Authority certificates for the QCA library.
These certificates are the same ones that are included in Mozilla.

%files -n %{name}-root-certificates
%defattr(0644,root,root,0755)
%dir %{qt4dir}/share/qca
%dir %{qt4dir}/share/qca/certs
%doc %{qt4dir}/share/qca/certs/README
%{qt4dir}/share/qca/certs/rootcerts.pem
%endif

#------------------------------------------------------------------------------

%package	-n %{lib_name}
Summary:	Libraries for QCA
Group:		System/Libraries
%if %{build_sys_rootcerts}
Requires:	rootcerts
Obsoletes:	%{name}-root-certificates
%else
Requires:	%{name}-root-certificates >= %{version}
%endif
Obsoletes:	%{lib_name}-static-devel 

%description	-n %{lib_name}
Libraries for QCA.

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%files -n %{lib_name}
%defattr(0644,root,root,0755)
%doc README COPYING INSTALL TODO
%dir %{qtcryptodir}
%defattr(0755,root,root,0755)
%{qt4lib}/libqca.so.*

#------------------------------------------------------------------------------

%package	-n %{develname}
Summary:	Development files for QCA
Group:		Development/KDE and Qt
Requires:	%{lib_name} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{name}2-devel = %{version}-%{release}
Obsoletes:	%{mklibname -d qca 1} < 1.0-17
Obsoletes:	%{mklibname -d qca 2} < 2.0.1-3

%description	-n %{develname}
Development files for QCA.

%files	-n %{develname}
%defattr(0644,root,root,0755)
%{_libdir}/pkgconfig/qca2.pc
%{qt4dir}/mkspecs/features/crypto.prf
%dir %{qt4include}/QtCrypto
%{qt4include}/QtCrypto/*
%{qt4lib}/libqca.so

#------------------------------------------------------------------------------

%package -n %{lib_name}-plugin-gnupg
Summary: GnuPG plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-gnupg = %version
Provides: qca2-plugin-gnupg-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-gnupg-%{_lib} < 2.0.0-5

%description -n %{lib_name}-plugin-gnupg
This is a plugin to provide GnuPG capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-gnupg
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-gnupg.*

#------------------------------------------------------------------------------

%package -n %{lib_name}-plugin-openssl
Summary: OpenSSL plugin for QCA
Group: Development/KDE and Qt
BuildRequires: openssl-devel
Provides: qca2-openssl = %version
Provides: qca2-tls = %version
Provides: qca2-plugin-openssl-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-openssl-%{_lib} < 2.0.0-5
Obsoletes: %{mklibname qca 1}-tls < 1.0-17

%description -n %{lib_name}-plugin-openssl
This is a plugin to provide OpenSSL capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-openssl
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-ossl.*

#------------------------------------------------------------------------------

%package -n %{lib_name}-plugin-pkcs11
Summary: PKCS11 plugin for QCA
Group: Development/KDE and Qt
BuildRequires: openssl-devel
BuildRequires: pkcs11-helper-devel
Provides: qca2-pkcs11 = %version
Provides: qca2-plugin-pkcs11-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-pkcs11-%{_lib} < 2.0.0-5

%description -n %{lib_name}-plugin-pkcs11
This is a plugin to provide PKCS11 capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-pkcs11
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-pkcs11.*

#------------------------------------------------------------------------------

%package -n %{lib_name}-plugin-cyrus-sasl
Summary: Cyrus-sasl plugin for QCA
Group: Development/KDE and Qt
BuildRequires: libsasl2-devel
Provides: qca2-sasl = %version
Provides: qca2-plugin-cyrus-sasl-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-cyrus-sasl-%{_lib} < 2.0.0-5
Obsoletes: %{mklibname qca 1}-sasl < 1.0-17

%description -n %{lib_name}-plugin-cyrus-sasl
This is a plugin to provide cyrus-sasl capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-cyrus-sasl
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-cyrus-sasl.*

#------------------------------------------------------------------------------

%package -n %{lib_name}-plugin-logger
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-logger = %version
Provides: qca2-plugin-logger-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-logger-%{_lib} < 2.0.0-5

%description -n %{lib_name}-plugin-logger
This is a plugin to provide logger capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-logger
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-logger.*

#------------------------------------------------------------------------------

%package -n %{lib_name}-plugin-gcrypt
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-gcrypt = %version
Provides: qca2-plugin-gcrypt-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-gcrypt-%{_lib} < 2.0.0-5

%description -n %{lib_name}-plugin-gcrypt
This is a plugin to provide gcrypt capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-gcrypt
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-gcrypt.*

#------------------------------------------------------------------------------

%package -n %{lib_name}-plugin-nss
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-nss = %version
Provides: qca2-plugin-nss-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-nss-%{_lib} < 2.0.0-5

%description -n %{lib_name}-plugin-nss
This is a plugin to provide nss capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-nss
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-nss.*

#------------------------------------------------------------------------------

%package -n %{lib_name}-plugin-softstore
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-softstore = %version
Provides: qca2-plugin-softstore-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-softstore-%{_lib} < 2.0.0-5

%description -n %{lib_name}-plugin-softstore
This is a plugin to provide softstore capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-softstore
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-softstore.*

#------------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{source_ver}
%patch0 -p1 -b .mandir
%patch1 -p1 -b .whirlpool
%patch2 -p1 -b .underlink

%build
%cmake_qt4 \
	-DCMAKE_INSTALL_PREFIX=%{qt4dir} \
	-DLIB_INSTALL_DIR=%_libdir \
	-DPKGCONFIG_INSTALL_PREFIX=%_libdir/pkgconfig

%make


%install
rm -rf %{buildroot}
cd build

make DESTDIR=%buildroot install

# Make directory for plugins
install -d -m 755 %{buildroot}/%{qtcryptodir}

%clean
rm -rf %buildroot



