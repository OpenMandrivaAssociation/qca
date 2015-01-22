%define build_debug 0
%{?_with_debug: %{expand: %%global build_debug 1}}

%define build_sys_rootcerts 1
%{?_without_sys_rootcerts: %{expand: %%global build_sys_rootcerts 0}}

%define lib_major	2
%define lib_name	%mklibname %{name} %{lib_major}
%define develname	%mklibname %{name} -d
%define source_ver	%{version}

%define git 20150120
%bcond_without qt5

Name: qca
Version: 2.1.0.3
%if 0%git
Release: 0.%git.7
# From git export git://anongit.kde.org/qca.git
Source0: qca-%git.tar.xz
%else
Release: 4
Source0: http://download.kde.org/stable/%{name}-qt5/%{version}/src/%{name}-qt5-%{version}.tar.xz
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
BuildRequires: pkgconfig(Qt5Test)
%endif
%if %{build_sys_rootcerts}
BuildRequires: rootcerts
%endif
BuildRequires: cmake
BuildRequires: pkgconfig(libgcrypt)
BuildRequires: sasl-devel
BuildRequires: pkgconfig(nss)
Obsoletes: qca2 < 2.0.1-3
Provides: qca2 = %{EVRD}
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
%{_bindir}/mozcerts-qt5
%{_bindir}/qcatool-qt5
%endif
%_mandir/man1/*

#------------------------------------------------------------------------------
%package tools-qt4
Summary:	QCA tools for Qt 4.x
Group:		System/Libraries

%description tools-qt4
QCA tools for Qt 4.x

%files tools-qt4
%{_bindir}/mozcerts
%{_bindir}/qcatool

#------------------------------------------------------------------------------

%if ! %{build_sys_rootcerts}
%package -n %{name}-root-certificates
Summary:	Common root CA certificates for QCA
Group:		System/Libraries
Requires:	%{lib_name} = %{EVRD}

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
Obsoletes:	%{name}-root-certificates < %{EVRD}
%else
Requires:	%{name}-root-certificates >= %{EVRD}
%endif
Obsoletes:	%{lib_name}-static-devel 

%description	-n %{lib_name}
Libraries for QCA.

%files -n %{lib_name}
%defattr(0644,root,root,0755)
%doc README COPYING INSTALL TODO
%if %{with qt5}
%dir %{_libdir}/qca-qt5
%dir %{_libdir}/qca-qt5/crypto
%defattr(0755,root,root,0755)
%{_libdir}/libqca-qt5.so.*
%endif

#------------------------------------------------------------------------------

%package	-n %{lib_name}-qt4
Summary:	Libraries for QCA
Group:		System/Libraries
%if %{build_sys_rootcerts}
Requires:	rootcerts
Obsoletes:	%{name}-root-certificates < %{EVRD}
%else
Requires:	%{name}-root-certificates >= %{EVRD}
%endif
Obsoletes:	%{lib_name}-static-devel
Requires:	%{lib_name} = %{EVRD}

%description	-n %{lib_name}-qt4
Libraries for QCA.

%files -n %{lib_name}-qt4
%defattr(0644,root,root,0755)
%doc README COPYING INSTALL TODO
%defattr(0755,root,root,0755)
%{_libdir}/libqca.so.*


#------------------------------------------------------------------------------

%package	-n %{develname}-qt4
Summary:	Development files for QCA
Group:		Development/KDE and Qt
Requires:	%{lib_name}-qt4 = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	%{name}-devel-qt4 = %{EVRD}
Provides:	%{name}2-devel = %{EVRD}
Provides:	%{name}2-devel-qt4 = %{EVRD}
Obsoletes:	%{mklibname -d qca 1} < 1.0-17
Obsoletes:	%{mklibname -d qca 2} < 2.0.1-3

%description	-n %{develname}-qt4
Development files for QCA.

%files	-n %{develname}-qt4
%defattr(0644,root,root,0755)
%{_libdir}/pkgconfig/qca2.pc
%{qt4dir}/mkspecs/features/crypto.prf
%dir %{_includedir}/QtCrypto
%{_includedir}/QtCrypto/*
%{_libdir}/cmake/Qca/QcaConfig*.cmake
%{_libdir}/cmake/Qca/QcaTargets*.cmake
%{_libdir}/libqca.so

#------------------------------------------------------------------------------

%if %{with qt5}
%package	-n %{develname}
Summary:	Development files for QCA
Group:		Development/KDE and Qt
Requires:	%{lib_name} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	%{name}2-devel = %{EVRD}
Obsoletes:	%{mklibname -d qca 1} < 1.0-17
Obsoletes:	%{mklibname -d qca 2} < 2.0.1-3

%description	-n %{develname}
Development files for QCA.

%files	-n %{develname}
%defattr(0644,root,root,0755)
%{_libdir}/pkgconfig/qca2-qt5.pc
%{_prefix}/mkspecs/features/crypto.prf
%{_libdir}/cmake/Qca/Qca-qt5*.cmake
%{_includedir}/Qca-qt5/QtCrypto
%{_libdir}/libqca-qt5.so
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
%attr(0755,root,root) %{_libdir}/qca-qt5/crypto/libqca-gnupg.*
%endif
#------------------------------------------------------------------------------

%package -n %{lib_name}-qt4-plugin-gnupg
Summary: GnuPG plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-gnupg = %version
Provides: qca2-plugin-gnupg-%{_lib} = %{EVRD}
Obsoletes: qca2-plugin-gnupg-%{_lib} < 2.0.0-5

%description -n %{lib_name}-qt4-plugin-gnupg
This is a plugin to provide GnuPG capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-qt4-plugin-gnupg
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_libdir}/qca/crypto/libqca-gnupg.*

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
%attr(0755,root,root) %{_libdir}/qca-qt5/crypto/libqca-ossl.*
%endif

#------------------------------------------------------------------------------

%package -n %{lib_name}-qt4-plugin-openssl
Summary: OpenSSL plugin for QCA
Group: Development/KDE and Qt
BuildRequires: openssl-devel
Provides: qca2-openssl = %version
Provides: qca2-tls = %version
Provides: qca2-plugin-openssl-%{_lib} = %{EVRD}
Obsoletes: qca2-plugin-openssl < 2.1.0
Obsoletes: %{mklibname qca 1}-tls < 1.0-17

%description -n %{lib_name}-qt4-plugin-openssl
This is a plugin to provide OpenSSL capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-qt4-plugin-openssl
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_libdir}/qca/crypto/libqca-ossl.*

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
%attr(0755,root,root) %{_libdir}/qca-qt5/crypto/libqca-pkcs11.*
%endif
#------------------------------------------------------------------------------

%package -n %{lib_name}-qt4-plugin-pkcs11
Summary: PKCS11 plugin for QCA
Group: Development/KDE and Qt
BuildRequires: openssl-devel
BuildRequires: pkcs11-helper-devel
Provides: qca2-pkcs11 = %version
Provides: qca2-plugin-pkcs11-%{_lib} = %{EVRD}
Obsoletes: qca2-plugin-pkcs11-%{_lib} < 2.0.0-5

%description -n %{lib_name}-qt4-plugin-pkcs11
This is a plugin to provide PKCS11 capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-qt4-plugin-pkcs11
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_libdir}/qca/crypto/libqca-pkcs11.*

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
%attr(0755,root,root) %{_libdir}/qca-qt5/crypto/libqca-cyrus-sasl.*
%endif
#------------------------------------------------------------------------------

%package -n %{lib_name}-qt4-plugin-cyrus-sasl
Summary: Cyrus-sasl plugin for QCA
Group: Development/KDE and Qt
BuildRequires: sasl-devel
Provides: qca2-sasl = %version
Provides: qca2-plugin-cyrus-sasl-%{_lib} = %{EVRD}
Obsoletes: qca2-plugin-cyrus-sasl-%{_lib} < 2.0.0-5
Obsoletes: %{mklibname qca 1}-sasl < 1.0-17

%description -n %{lib_name}-qt4-plugin-cyrus-sasl
This is a plugin to provide cyrus-sasl capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-qt4-plugin-cyrus-sasl
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_libdir}/qca/crypto/libqca-cyrus-sasl.*

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
%attr(0755,root,root) %{_libdir}/qca-qt5/crypto/libqca-logger.*
%endif
#------------------------------------------------------------------------------

%package -n %{lib_name}-qt4-plugin-logger
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-logger = %version
Provides: qca2-plugin-logger-%{_lib} = %{EVRD}
Obsoletes: qca2-plugin-logger-%{_lib} < 2.0.0-5

%description -n %{lib_name}-qt4-plugin-logger
This is a plugin to provide logger capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-qt4-plugin-logger
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_libdir}/qca/crypto/libqca-logger.*

#------------------------------------------------------------------------------

%if %{with qt5}
%package -n %{lib_name}-plugin-gcrypt
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca-plugin-gcrypt-%{_lib} = %{EVRD}

%description -n %{lib_name}-plugin-gcrypt
This is a plugin to provide gcrypt capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-gcrypt
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_libdir}/qca-qt5/crypto/libqca-gcrypt.*
%endif
#------------------------------------------------------------------------------

%package -n %{lib_name}-qt4-plugin-gcrypt
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-gcrypt = %version
Provides: qca2-plugin-gcrypt-%{_lib} = %{EVRD}
Obsoletes: qca2-plugin-gcrypt-%{_lib} < 2.0.0-5

%description -n %{lib_name}-qt4-plugin-gcrypt
This is a plugin to provide gcrypt capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-qt4-plugin-gcrypt
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_libdir}/qca/crypto/libqca-gcrypt.*

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
%attr(0755,root,root) %{_libdir}/qca-qt5/crypto/libqca-nss.*
%endif
#------------------------------------------------------------------------------

%package -n %{lib_name}-qt4-plugin-nss
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-nss = %version
Provides: qca2-plugin-nss-%{_lib} = %{EVRD}
Obsoletes: qca2-plugin-nss-%{_lib} < 2.0.0-5

%description -n %{lib_name}-qt4-plugin-nss
This is a plugin to provide nss capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-qt4-plugin-nss
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_libdir}/qca/crypto/libqca-nss.*

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
%attr(0755,root,root) %{_libdir}/qca-qt5/crypto/libqca-softstore.*
%endif
#------------------------------------------------------------------------------

%package -n %{lib_name}-qt4-plugin-softstore
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-softstore = %version
Provides: qca2-plugin-softstore-%{_lib} = %{EVRD}
Obsoletes: qca2-plugin-softstore-%{_lib} < 2.0.0-5

%description -n %{lib_name}-qt4-plugin-softstore
This is a plugin to provide softstore capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-qt4-plugin-softstore
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_libdir}/qca/crypto/libqca-softstore.*

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
%attr(0755,root,root) %{_libdir}/qca-qt5/crypto/libqca-botan.*
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
%attr(0755,root,root) %{_libdir}/qca/crypto/libqca-botan.*


%prep
%if 0%git
%setup -q -n %name-%{git}
%else
%setup -q -n %{name}-%{source_ver}
%endif
%apply_patches

%build
%cmake_qt4 \
	-DQT4_BUILD:BOOL=ON \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DPKGCONFIG_INSTALL_PREFIX=%{_libdir}/pkgconfig \
	-DQCA_MAN_INSTALL_DIR=%{_mandir} \
	-DBOTANCONFIG_EXECUTABLE=%{_bindir}/botan-config-1.10 \
	-DQCA_FEATURE_INSTALL_DIR=%{qt4dir}/mkspecs/features
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
	-DBOTANCONFIG_EXECUTABLE=%{_bindir}/botan-config-1.10 \
    -DQCA_SUFFIX=qt5
%make
%endif

%install
cd build
make DESTDIR=%buildroot install

%if %{with qt5}
cd ../build-qt5
make DESTDIR=%buildroot install
%endif
