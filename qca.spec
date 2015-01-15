%define build_debug 0
%{?_with_debug: %{expand: %%global build_debug 1}}

%define build_sys_rootcerts 1
%{?_without_sys_rootcerts: %{expand: %%global build_sys_rootcerts 0}}

%define qtcryptodir	%{qt4plugins}/crypto
%define lib_major	2
%define lib_name	%mklibname %{name} %{lib_major}
%define develname	%mklibname %{name} -d
%define source_ver	%{version}

# Override to make sure Qt4 and Qt5 versions don't end up in the
# same directory
%define qt4lib %{_libdir}/qt4

%define git 20140616
%bcond_without qt5

Name: qca
Version: 2.1.0
%if 0%git
Release: 0.%git.5
# From git export git://anongit.kde.org/qca.git
Source0: qca-%git.tar.xz
%else
Release: 4
# Warning: Code coming from kdesupport to match kde development
Source0: http://delta.affinix.com/download/%{name}/2.0/%{name}-%{version}.tar.bz2
%endif
Source100: %{name}.rpmlintrc
License: LGPLv2+
Summary: Straightforward and cross-platform crypto API for Qt
Group: System/Libraries
URL: http://delta.affinix.com/qca
# Fix underlinking in the openssl plugin - AdamW 2008/12
Patch2: qca-2.0.1-underlink.patch
BuildRequires: qt4-devel >= 2:4.2
%if %{with qt5}
BuildRequires: qt5-devel
%endif
%if %{build_sys_rootcerts}
BuildRequires: rootcerts
%endif
BuildRequires: cmake
BuildRequires: pkgconfig(libgcrypt)
BuildRequires: sasl-devel
BuildRequires: pkgconfig(nss)
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
%if %{with qt5}
%{_bindir}/mozcerts
%{_bindir}/qcatool
%endif
%_mandir/man1/*

#------------------------------------------------------------------------------
%package tools-qt4
Summary:	QCA tools for Qt 4.x
Group:		System/Libraries

%description tools-qt4
QCA tools for Qt 4.x

%files tools-qt4
%{qt4dir}/bin/mozcerts
%{qt4dir}/bin/qcatool

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

%files -n %{lib_name}
%defattr(0644,root,root,0755)
%doc README COPYING INSTALL TODO
%if %{with qt5}
%dir %{_libdir}/qca
%dir %{_libdir}/qca/crypto
%defattr(0755,root,root,0755)
%{_libdir}/libqca.so.*
%endif

#------------------------------------------------------------------------------

%package	-n %{lib_name}-qt4
Summary:	Libraries for QCA
Group:		System/Libraries
%if %{build_sys_rootcerts}
Requires:	rootcerts
Obsoletes:	%{name}-root-certificates
%else
Requires:	%{name}-root-certificates >= %{version}
%endif
Obsoletes:	%{lib_name}-static-devel 

%description	-n %{lib_name}-qt4
Libraries for QCA.

%files -n %{lib_name}-qt4
%defattr(0644,root,root,0755)
%doc README COPYING INSTALL TODO
%dir %{qtcryptodir}
%defattr(0755,root,root,0755)
%{qt4lib}/libqca.so.*


#------------------------------------------------------------------------------

%package	-n %{develname}-qt4
Summary:	Development files for QCA
Group:		Development/KDE and Qt
Requires:	%{lib_name}-qt4 = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel-qt4 = %{version}-%{release}
Provides:	%{name}2-devel = %{version}-%{release}
Provides:       %{name}2-devel-qt4 = %{version}-%{release}
Obsoletes:	%{mklibname -d qca 1} < 1.0-17
Obsoletes:	%{mklibname -d qca 2} < 2.0.1-3

%description	-n %{develname}-qt4
Development files for QCA.

%files	-n %{develname}-qt4
%defattr(0644,root,root,0755)
%if %{with qt5}
%{qt4lib}/pkgconfig/qca2.pc
%else
%{_libdir}/pkgconfig/qca2.pc
%endif
%{qt4dir}/mkspecs/features/crypto.prf
%dir %{qt4include}/QtCrypto
%{qt4include}/QtCrypto/*
%{qt4lib}/libqca.so

#------------------------------------------------------------------------------

%if %{with qt5}
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
%{_prefix}/mkspecs/features/crypto.prf
%{_includedir}/QtCrypto
%{_libdir}/libqca.so
%endif
#------------------------------------------------------------------------------

%if %{with qt5}
%package -n %{lib_name}-plugin-gnupg
Summary: GnuPG plugin for QCA
Group: Development/KDE and Qt
Provides: qca-plugin-gnupg-%{_lib} = %{EVRD}

%description -n %{lib_name}-plugin-gnupg
This is a plugin to provide GnuPG capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-gnupg
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_libdir}/qca/crypto/libqca-gnupg.*
%endif
#------------------------------------------------------------------------------

%package -n %{lib_name}-qt4-plugin-gnupg
Summary: GnuPG plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-gnupg = %version
Provides: qca2-plugin-gnupg-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-gnupg-%{_lib} < 2.0.0-5

%description -n %{lib_name}-qt4-plugin-gnupg
This is a plugin to provide GnuPG capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-qt4-plugin-gnupg
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-gnupg.*

#------------------------------------------------------------------------------

%if %{with qt5}
%package -n %{lib_name}-plugin-openssl
Summary: OpenSSL plugin for QCA
Group: Development/KDE and Qt
BuildRequires: openssl-devel
Provides: qca-plugin-openssl-%{_lib} = %{EVRD}

%description -n %{lib_name}-plugin-openssl
This is a plugin to provide OpenSSL capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-openssl
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_libdir}/qca/crypto/libqca-ossl.*
%endif

#------------------------------------------------------------------------------

%package -n %{lib_name}-qt4-plugin-openssl
Summary: OpenSSL plugin for QCA
Group: Development/KDE and Qt
BuildRequires: openssl-devel
Provides: qca2-openssl = %version
Provides: qca2-tls = %version
Provides: qca2-plugin-openssl-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-openssl < 2.1.0
Obsoletes: %{mklibname qca 1}-tls < 1.0-17

%description -n %{lib_name}-qt4-plugin-openssl
This is a plugin to provide OpenSSL capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-qt4-plugin-openssl
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-ossl.*

#------------------------------------------------------------------------------

%if %{with qt5}
%package -n %{lib_name}-plugin-pkcs11
Summary: PKCS11 plugin for QCA
Group: Development/KDE and Qt
BuildRequires: openssl-devel
BuildRequires: pkcs11-helper-devel
Provides: qca-plugin-pkcs11-%{_lib} = %{EVRD}

%description -n %{lib_name}-plugin-pkcs11
This is a plugin to provide PKCS11 capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-pkcs11
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_libdir}/qca/crypto/libqca-pkcs11.*
%endif
#------------------------------------------------------------------------------

%package -n %{lib_name}-qt4-plugin-pkcs11
Summary: PKCS11 plugin for QCA
Group: Development/KDE and Qt
BuildRequires: openssl-devel
BuildRequires: pkcs11-helper-devel
Provides: qca2-pkcs11 = %version
Provides: qca2-plugin-pkcs11-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-pkcs11-%{_lib} < 2.0.0-5

%description -n %{lib_name}-qt4-plugin-pkcs11
This is a plugin to provide PKCS11 capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-qt4-plugin-pkcs11
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-pkcs11.*

#------------------------------------------------------------------------------

%if %{with qt5}
%package -n %{lib_name}-plugin-cyrus-sasl
Summary: Cyrus-sasl plugin for QCA
Group: Development/KDE and Qt
BuildRequires: sasl-devel
Provides: qca-plugin-cyrus-sasl-%{_lib} = %{EVRD}

%description -n %{lib_name}-plugin-cyrus-sasl
This is a plugin to provide cyrus-sasl capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-cyrus-sasl
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_libdir}/qca/crypto/libqca-cyrus-sasl.*
%endif
#------------------------------------------------------------------------------

%package -n %{lib_name}-qt4-plugin-cyrus-sasl
Summary: Cyrus-sasl plugin for QCA
Group: Development/KDE and Qt
BuildRequires: sasl-devel
Provides: qca2-sasl = %version
Provides: qca2-plugin-cyrus-sasl-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-cyrus-sasl-%{_lib} < 2.0.0-5
Obsoletes: %{mklibname qca 1}-sasl < 1.0-17

%description -n %{lib_name}-qt4-plugin-cyrus-sasl
This is a plugin to provide cyrus-sasl capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-qt4-plugin-cyrus-sasl
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-cyrus-sasl.*

#------------------------------------------------------------------------------

%if %{with qt5}
%package -n %{lib_name}-plugin-logger
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca-plugin-logger-%{_lib} = %{EVRD}

%description -n %{lib_name}-plugin-logger
This is a plugin to provide logger capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-logger
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_libdir}/qca/crypto/libqca-logger.*
%endif
#------------------------------------------------------------------------------

%package -n %{lib_name}-qt4-plugin-logger
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-logger = %version
Provides: qca2-plugin-logger-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-logger-%{_lib} < 2.0.0-5

%description -n %{lib_name}-qt4-plugin-logger
This is a plugin to provide logger capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-qt4-plugin-logger
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-logger.*

#------------------------------------------------------------------------------

%if %{with qt5}
%package -n %{lib_name}-plugin-gcrypt
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca-plugin-gcrypt-%{_lib} = %{version}-%{release}

%description -n %{lib_name}-plugin-gcrypt
This is a plugin to provide gcrypt capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-gcrypt
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_libdir}/qca/crypto/libqca-gcrypt.*
%endif
#------------------------------------------------------------------------------

%package -n %{lib_name}-qt4-plugin-gcrypt
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-gcrypt = %version
Provides: qca2-plugin-gcrypt-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-gcrypt-%{_lib} < 2.0.0-5

%description -n %{lib_name}-qt4-plugin-gcrypt
This is a plugin to provide gcrypt capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-qt4-plugin-gcrypt
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-gcrypt.*

#------------------------------------------------------------------------------

%if %{with qt5}
%package -n %{lib_name}-plugin-nss
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca-plugin-nss-%{_lib} = %{EVRD}

%description -n %{lib_name}-plugin-nss
This is a plugin to provide nss capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-nss
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_libdir}/qca/crypto/libqca-nss.*
%endif
#------------------------------------------------------------------------------

%package -n %{lib_name}-qt4-plugin-nss
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-nss = %version
Provides: qca2-plugin-nss-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-nss-%{_lib} < 2.0.0-5

%description -n %{lib_name}-qt4-plugin-nss
This is a plugin to provide nss capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-qt4-plugin-nss
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-nss.*

#------------------------------------------------------------------------------

%if %{with qt5}
%package -n %{lib_name}-plugin-softstore
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca-plugin-softstore-%{_lib} = %{EVRD}

%description -n %{lib_name}-plugin-softstore
This is a plugin to provide softstore capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-softstore
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_libdir}/qca/crypto/libqca-softstore.*
%endif
#------------------------------------------------------------------------------

%package -n %{lib_name}-qt4-plugin-softstore
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-softstore = %version
Provides: qca2-plugin-softstore-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-softstore-%{_lib} < 2.0.0-5

%description -n %{lib_name}-qt4-plugin-softstore
This is a plugin to provide softstore capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-qt4-plugin-softstore
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-softstore.*

#------------------------------------------------------------------------------

%if %{with qt5}
%package -n %{lib_name}-plugin-botan
Summary:        Botan plugin for QCA
Group:          Development/KDE and Qt
BuildRequires:  pkgconfig(botan-1.10)

%description -n %{lib_name}-plugin-botan
This is a plugin to allow the Qt Cryptographic Architecture (QCA) to
use the Botan cryptography library as its backend.

%files -n %{lib_name}-plugin-botan
%attr(0755,root,root) %{_libdir}/qca/crypto/libqca-botan.*
%endif
#------------------------------------------------------------------------------

%package -n %{lib_name}-qt4-plugin-botan
Summary:        Botan plugin for QCA
Group:          Development/KDE and Qt
BuildRequires:  pkgconfig(botan-1.10)

%description -n %{lib_name}-qt4-plugin-botan
This is a plugin to allow the Qt Cryptographic Architecture (QCA) to
use the Botan cryptography library as its backend.

%files -n %{lib_name}-qt4-plugin-botan
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-botan.*


%prep
%if 0%git
%setup -q -n %name
%else
%setup -q -n %{name}-%{source_ver}
%endif
%apply_patches

%build
%cmake_qt4 \
	-DQT4_BUILD:BOOL=ON \
	-DCMAKE_INSTALL_PREFIX=%{qt4dir} \
	-DLIB_INSTALL_DIR=%{qt4lib} \
%if %{with qt5}
	-DPKGCONFIG_INSTALL_PREFIX=%{qt4lib}/pkgconfig \
%else
	-DPKGCONFIG_INSTALL_PREFIX=%{_libdir}/pkgconfig \
%endif
	-DQCA_MAN_INSTALL_DIR=%{_mandir} \
	-DQCA_PLUGINS_INSTALL_DIR=%{qtcryptodir} \
	-DBOTANCONFIG_EXECUTABLE=%{_bindir}/botan-config-1.10
%make

%if %{with qt5}
cd ..
mkdir build-qt5
cd build-qt5
cmake .. \
	-DQT4_BUILD:BOOL=OFF \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DPKGCONFIG_INSTALL_PREFIX=%_libdir/pkgconfig \
	-DQCA_MAN_INSTALL_DIR=%{_mandir} \
	-DBOTANCONFIG_EXECUTABLE=%{_bindir}/botan-config-1.10
%make
%endif

%install
cd build
make DESTDIR=%buildroot install

# Make directory for plugins
install -d -m 755 %{buildroot}/%{qtcryptodir}

%if %{with qt5}
cd ../build-qt5
make DESTDIR=%buildroot install
%endif
