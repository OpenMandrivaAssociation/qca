%define qtdir   %{_prefix}/lib/qt3
%define plugindir %{qtdir}/plugins/%_lib
%define libname %mklibname %name 1
%define develname %mklibname %name -d

Name:	 	qca
Version:	1.0
Release:	%mkrel 12
License:	LGPLv2.1
Summary:	Straightforward and cross-platform crypto API for Qt
Group:		Development/KDE and Qt
URL:		http://delta.affinix.com/qca
########################################################################################
#it is now part of kde : You can find it here:  http://webcvs.kde.org//kdesupport/qca/ #
#######################################################################################
Source0:	%name-%version.tar.bz2
Source1:	%name-tls-%version.tar.bz2
Source2:	%name-sasl-%version.tar.bz2
Patch0:		qca-1.0-configure-libdir.patch
Patch1:		qca-1.0-lib64.patch
Patch2:		qca-1.0-fix-gcc-4.0.patch
Requires:	%libname = %version
BuildRoot:	%_tmppath/%name-buildroot
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	qt3-devel >= 3.3.5-7mdk


%description
Taking a hint from the similarly-named Java Cryptography Architecture, QCA aims
to provide a straightforward and cross-platform crypto API, using Qt datatypes
and conventions. QCA separates the API from the implementation, using plugins
known as Providers. The advantage of this model is to allow applications to
avoid linking to or explicitly depending on any particular cryptographic
library. This allows one to easily change or upgrade crypto implementations
without even needing to recompile the application! QCA should work everywhere
Qt does, including Windows/Unix/MacOSX.

%package	-n %libname
Summary:	Libraries for QCA
Group:		Development/KDE and Qt
Requires:	%name

%description	-n %libname
Libraries for QCA

%package	-n %develname
Summary:	Development files from QCA
Group:		Development/KDE and Qt
Provides:	lib%name-devel = %version-%release
Provides:	%name-devel = %version-release
Requires:	%libname = %version
Obsoletes:	%mklibname qca 1 -d

%description	-n %develname
Development files from QCA

%package	-n %libname-tls
Summary:	TLS plugin for QCA
Group:		Development/KDE and Qt
Requires:	%libname = %version
Provides:	psi-qca-tls
Obsoletes:	psi-qca-tls

%description	-n %libname-tls
This is a plugin to provide SSL/TLS capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%package	-n %libname-sasl
Summary:	SASL plugin for QCA
Group:		Development/KDE and Qt
Requires:	%libname = %version
BuildRequires:	libsasl-devel

%description	-n %libname-sasl
This is a plugin to provide SASL capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%prep
%setup -q
%setup -q -T -D -a 1
%setup -q -T -D -a 2
%patch0 -p1 -b .libraries
%if "%_lib" != "lib"
%patch1 -p1 -b .lib64
%endif
%patch2 -p1 -b .fix_compile_gcc

%build
export QTDIR=%qtdir

export LD_LIBRARY_PATH=%{qtdir}/%_lib:$LD_LIBRARY_PATH
export PATH=%{qtdir}/bin:$PATH

# main qca
./configure \
	--prefix=%qtdir \
	--libdir=%qtdir/%_lib \
	--qtdir=%qtdir

%make

# Plugins
for plugin in tls sasl; do
   pushd %{name}-${plugin}-%{version}
      ./configure --qtdir=%{qtdir}; %make
   popd
done

%install
rm -rf %{buildroot}
make install INSTALL_ROOT=%{buildroot}

# Plugins
for plugin in tls sasl; do
   pushd %{name}-${plugin}-%{version}
      %makeinstall INSTALL_ROOT=%{buildroot}
   popd
done
mkdir -p %{buildroot}/%{plugindir}/crypto
mv  %{buildroot}/%{qtdir}/plugins/crypto/* %{buildroot}/%{plugindir}/crypto

%clean
rm -rf %{buildroot}

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files
%defattr(0644,root,root,0755)
%dir %{plugindir}/crypto

%files	-n %libname
%defattr(0644,root,root,0755)
%qtdir/%_lib/libqca.so.*

%files	-n %develname
%defattr(0644,root,root,0755)
%doc README TODO
%qtdir/include/%{name}.h
%qtdir/%_lib/libqca.so

%files	-n %libname-tls
%defattr(0644,root,root,0755)
%doc %{name}-tls-%{version}/{README,COPYING}
%{plugindir}/crypto/libqca-tls.so

%files	-n %libname-sasl
%defattr(0644,root,root,0755)
%doc %{name}-sasl-%{version}/{README,COPYING}
%{plugindir}/crypto/libqca-sasl.so



