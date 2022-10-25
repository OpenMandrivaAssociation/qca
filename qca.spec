%define lib_major 2
%define lib_name %mklibname %{name} %{lib_major}
%define develname %mklibname %{name} -d

%global optflags %{optflags} -O3

%define git %nil
%bcond_without botan
%bcond_without openssl

Name: qca
Version: 2.3.5
%if 0%git
Release: 1.%{git}.1
# From git export git://anongit.kde.org/qca.git
Source0: qca-%{version}-%git.tar.xz
%else
Release: 1
Source0: http://download.kde.org/stable/%{name}/%{version}/%{name}-%{version}.tar.xz
%endif
License: LGPLv2+
Summary: Straightforward and cross-platform crypto API for Qt
Group: System/Libraries
URL: http://userbase.kde.org/QCA
Source100: %{name}.rpmlintrc
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5Test)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: qmake5
BuildRequires: rootcerts
BuildRequires: cmake
BuildRequires: pkgconfig(libgcrypt)
BuildRequires: pkgconfig(gpg-error)
BuildRequires: sasl-devel
BuildRequires: pkgconfig(nss)
Obsoletes: qca2 < 2.0.1-3
Provides: qca2 = %{EVRD}

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
%{_bindir}/mozcerts-qt5
%{_bindir}/qcatool-qt5
%doc %{_mandir}/man1/qcatool-qt5.*

#------------------------------------------------------------------------------

%package -n %{lib_name}
Summary: Libraries for QCA
Group: System/Libraries
Requires: %{name} = %{EVRD}
Requires: rootcerts
Obsoletes: %{name}-root-certificates < %{EVRD}
%if %{with openssl}
Recommends: %{lib_name}-plugin-openssl
%endif

%description -n %{lib_name}
Libraries for QCA.

%files -n %{lib_name}
%dir %{_libdir}/qca-qt5
%dir %{_libdir}/qca-qt5/crypto
%defattr(0755,root,root,0755)
%{_libdir}/libqca-qt5.so.*

#------------------------------------------------------------------------------

%package -n %{develname}
Summary: Development files for QCA
Group: Development/KDE and Qt
Requires: %{lib_name} = %{EVRD}
Provides: %{name}-devel = %{EVRD}
Provides: %{name}2-devel = %{EVRD}
Obsoletes: %{mklibname -d qca 1} < 1.0-17
Obsoletes: %{mklibname -d qca 2} < 2.0.1-3
Obsoletes: %{lib_name}-static-devel

%description -n %{develname}
Development files for QCA.

%files -n %{develname}
%doc README COPYING INSTALL TODO
%{_libdir}/pkgconfig/qca2-qt5.pc
%{_libdir}/qt5/mkspecs/features/crypto.prf
%{_libdir}/cmake/Qca-qt5
%{_includedir}/Qca-qt5
%{_libdir}/libqca-qt5.so

#------------------------------------------------------------------------------

%package -n %{lib_name}-plugin-gnupg
Summary: GnuPG plugin for QCA
Group: Development/KDE and Qt
Requires: gnupg
Provides: qca-plugin-gnupg-%{_lib} = %{EVRD}

%description -n %{lib_name}-plugin-gnupg
This is a plugin to provide GnuPG capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-gnupg
%attr(0755,root,root) %{_libdir}/qca-qt5/crypto/libqca-gnupg.*

#------------------------------------------------------------------------------

%if %{with openssl}
%package -n %{lib_name}-plugin-openssl
Summary: OpenSSL plugin for QCA
Group: Development/KDE and Qt
BuildRequires: pkgconfig(openssl)
Provides: qca-plugin-openssl-%{_lib} = %{EVRD}

%description -n %{lib_name}-plugin-openssl
This is a plugin to provide OpenSSL capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-openssl
%attr(0755,root,root) %{_libdir}/qca-qt5/crypto/libqca-ossl.*
%endif

#------------------------------------------------------------------------------

%package -n %{lib_name}-plugin-pkcs11
Summary: PKCS11 plugin for QCA
Group: Development/KDE and Qt
BuildRequires: pkgconfig(openssl)
BuildRequires: pkcs11-helper-devel
Provides: qca-plugin-pkcs11-%{_lib} = %{EVRD}

%description -n %{lib_name}-plugin-pkcs11
This is a plugin to provide PKCS11 capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-pkcs11
%attr(0755,root,root) %{_libdir}/qca-qt5/crypto/libqca-pkcs11.*
#------------------------------------------------------------------------------

%package -n %{lib_name}-plugin-cyrus-sasl
Summary: Cyrus-sasl plugin for QCA
Group: Development/KDE and Qt
BuildRequires: sasl-devel
Provides: qca-plugin-cyrus-sasl-%{_lib} = %{EVRD}

%description -n %{lib_name}-plugin-cyrus-sasl
This is a plugin to provide cyrus-sasl capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-cyrus-sasl
%attr(0755,root,root) %{_libdir}/qca-qt5/crypto/libqca-cyrus-sasl.*

#------------------------------------------------------------------------------

%package -n %{lib_name}-plugin-logger
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca-plugin-logger-%{_lib} = %{EVRD}

%description -n %{lib_name}-plugin-logger
This is a plugin to provide logger capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-logger
%attr(0755,root,root) %{_libdir}/qca-qt5/crypto/libqca-logger.*

#------------------------------------------------------------------------------

%package -n %{lib_name}-plugin-gcrypt
Summary: GCrypt plugin for QCA
Group: Development/KDE and Qt
Provides: qca-plugin-gcrypt-%{_lib} = %{EVRD}

%description -n %{lib_name}-plugin-gcrypt
This is a plugin to provide gcrypt capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-gcrypt
%attr(0755,root,root) %{_libdir}/qca-qt5/crypto/libqca-gcrypt.*

#------------------------------------------------------------------------------

%package -n %{lib_name}-plugin-nss
Summary: NSS plugin for QCA
Group: Development/KDE and Qt
Provides: qca-plugin-nss-%{_lib} = %{EVRD}

%description -n %{lib_name}-plugin-nss
This is a plugin to provide nss capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-nss
%attr(0755,root,root) %{_libdir}/qca-qt5/crypto/libqca-nss.*

#------------------------------------------------------------------------------

%package -n %{lib_name}-plugin-softstore
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca-plugin-softstore-%{_lib} = %{EVRD}

%description -n %{lib_name}-plugin-softstore
This is a plugin to provide softstore capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-softstore
%attr(0755,root,root) %{_libdir}/qca-qt5/crypto/libqca-softstore.*

#------------------------------------------------------------------------------

%if %{with botan}
%package -n %{lib_name}-plugin-botan
Summary:        Botan plugin for QCA
Group:          Development/KDE and Qt
BuildRequires:  pkgconfig(botan-2)

%description -n %{lib_name}-plugin-botan
This is a plugin to allow the Qt Cryptographic Architecture (QCA) to
use the Botan cryptography library as its backend.

%files -n %{lib_name}-plugin-botan
%attr(0755,root,root) %{_libdir}/qca-qt5/crypto/libqca-botan.*
%endif

#------------------------------------------------------------------------------

%prep
%if 0%git
%autosetup -n %{name}-%{version}-%{git} -p1
%else
%autosetup -p1
%endif

%build
%cmake_qt5 \
	-DQT4_BUILD:BOOL=OFF \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DPKGCONFIG_INSTALL_PREFIX=%{_libdir}/pkgconfig \
	-DQCA_FEATURE_INSTALL_DIR:PATH=%{_qt5_libdir}/qt5/mkspecs/features \
	-DQCA_MAN_INSTALL_DIR=%{_mandir} \
%if %{with botan}
	-DBOTANCONFIG_EXECUTABLE=%{_bindir}/botan \
%endif
%if ! %{with openssl}
	-DWITH_ossl_PLUGIN:BOOL=OFF \
%endif
	-DQCA_SUFFIX=qt5

%make_build

%install
%make_install DESTDIR=%{buildroot} -C build
