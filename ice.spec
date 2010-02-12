%define	build_java 0

Name:		ice
Version:	3.3.1
Summary:	Files common to all Ice packages 
Release:	%mkrel 1%
License:	GPL
Group:		System Environment/Libraries
URL:		http://www.zeroc.com/
Source0:	Ice-%{version}.tar.gz
Source1:	Ice-rpmbuild-%{version}.tar.gz
%if %{build_java} == 0
Patch0:		Ice-no-java.patch
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%define	soversion 33
%define dotnetversion 3.3.1
%define dotnetpolicyversion 3.3

%define formsversion 1.2.0
%define looksversion 2.1.4
%define dbversion 4.6.21

BuildRequires:	openssl-devel >= 0.9.7a
BuildRequires:	db4.6-devel >= 4.6.21
BuildRequires:	jpackage-utils
BuildRequires:	mcpp-devel >= 2.7.2
BuildRequires:	bzip2-devel
BuildRequires:	libexpat-devel >= 1.95.7
BuildRequires:	python-devel >= 2.4.3
BuildRequires:	php-devel >= 5.1.6
BuildRequires:	ruby-devel
BuildRequires:	mono >= 1.2.6, mono-devel >= 1.2.6

%description
Ice is a modern alternative to object middleware such as CORBA or
COM/DCOM/COM+.  It is easy to learn, yet provides a powerful network
infrastructure for demanding technical applications. It features an
object-oriented specification language, easy to use C++, .NET, Java,
Python, Ruby, and PHP mappings, a highly efficient protocol, 
asynchronous method invocation and dispatch, dynamic transport 
plug-ins, TCP/IP and UDP/IP support, SSL-based security, a firewall
solution, and much more.

%package	mono
Summary:	The Ice runtime for .NET (mono)
Group:		System Environment/Libraries
Requires:	ice = %{version}-%{release}, mono-core >= 1.2.2

%description mono
The Ice runtime for .NET (mono).

%if %{build_java}
%package java
Summary:	The Ice runtime for Java
Group:		System Environment/Libraries
Requires:	ice = %{version}-%{release}, db46-java,

%description java
The Ice runtime for Java.

%package java-devel
Summary:	Tools for developing Ice applications in Java
Group:		Development/Tools
Requires:	ice-java = %{version}-%{release}, ice-libs = %{version}-%{release}

%description java-devel
Tools for developing Ice applications in Java.
%endif

%package libs
Summary:	The Ice runtime for C++
Group:		System Environment/Libraries
Requires:	ice = %{version}-%{release}, db46

%description libs
The Ice runtime for C++

%package utils
Summary:	Ice utilities and admin tools.
Group:		Applications/System
Requires:	ice-libs = %{version}-%{release}

%description utils
Admin tools to manage Ice servers (IceGrid, IceStorm, IceBox etc.),
plus various Ice-related utilities.

%package servers
Summary:	Ice servers and related files.
Group:		System Environment/Daemons
Requires:	ice-utils = %{version}-%{release}
Requires:	ice-mono = %{version}-%{release}

%description servers
Ice servers: glacier2router, icebox, icegridnode, icegridregistry, 
icebox, iceboxnet, icepatch2server and related files.

%package c++-devel
Summary:	Tools, libraries and headers for developing Ice applications in C++
Group:		Development/Tools
Requires:	ice-libs = %{version}-%{release}

%description c++-devel
Tools, libraries and headers for developing Ice applications in C++.

%package mono-devel
Summary:	Tools for developing Ice applications in C#
Group:		Development/Tools
Requires:	ice-mono = %{version}-%{release}, ice-libs = %{version}-%{release}, pkgconfig

%description mono-devel
Tools for developing Ice applications in C#.

%package ruby
Summary:	The Ice runtime for Ruby
Group:		System Environment/Libraries
Requires:	ice-libs = %{version}-%{release}, ruby

%description ruby
The Ice runtime for Ruby.

%package ruby-devel
Summary:	Tools for developing Ice applications in Ruby
Group:		Development/Tools
Requires:	ice-ruby = %{version}-%{release}

%description ruby-devel
Tools for developing Ice applications in Ruby.

%package python
Summary:	The Ice runtime for Python
Group:		System Environment/Libraries
Requires:	ice-libs = %{version}-%{release}

%description python
The Ice runtime for Python.

%package python-devel
Summary:	Tools for developing Ice applications in Python
Group:		Development/Tools
Requires:	ice-python = %{version}-%{release}

%description python-devel
Tools for developing Ice applications in Python.

%package php
Summary:	The Ice runtime for PHP
Group:		System Environment/Libraries
Requires:	ice = %{version}-%{release}

%description php
The Ice runtime for PHP.

%prep

%setup -q -n Ice-%{version}
%setup -q -n Ice-%{version} -T -D -b 1
%patch0 -p1 -b .no-java

%build

%make
#pushd cpp/src
#%make OPTIMIZE=yes embedded_runpath_prefix=""
#popd

#pushd py
#%make OPTIMIZE=yes embedded_runpath_prefix=""
#popd
#
#pushd php
#%make OPTIMIZE=yes embedded_runpath_prefix=""
#popd

#if %{ruby}
#pushd rb
#%make OPTIMIZE=yes embedded_runpath_prefix=""
#popd

#pushd java
#export CLASSPATH=`build-classpath db-%{dbversion} jgoodies-forms-%{formsversion} jgoodies-looks-%{looksversion} proguard`
#JGOODIES_FORMS=`find-jar jgoodies-forms-%{formsversion}`
#JGOODIES_LOOKS=`find-jar jgoodies-looks-%{looksversion}`

#ant -Dice.mapping=java5 -Dbuild.suffix=java5 -Djgoodies.forms=$JGOODIES_FORMS -Djgoodies.looks=$JGOODIES_LOOKS jar

#ant -Dice.mapping=java2 -Dbuild.suffix=java2 jar

#popd 

#%if %{mono}
#pushd cs/src
#%make OPTIMIZE=yes
#popd
#%endif

%install

rm -rf %{buildroot}

#mkdir -p %{buildroot}/lib
%makeinstall_std
#popd cpp
#%makeinstall_std embedded_runpath_prefix=""
#pushd

#pushd py
#%makeinstall embedded_runpath_prefix=""
#popd

#pushd php
#%makeinstall
#popd

mkdir -p %{buildroot}%{_sysconfdir}/php.d
cat << EOF > %{buildroot}%{_sysconfdir}/php.d/ice.ini
extension=IcePHP.so
EOF

%if %{build_java}
#
# IceGridGUI
#
mkdir -p %{buildroot}%{_javadir}
cp -p $RPM_BUILD_DIR/Ice-%{version}/java/libjava5/IceGridGUI.jar %{buildroot}%{_javadir}/IceGridGUI-%{version}.jar
ln -s IceGridGUI-%{version}.jar %{buildroot}%{_javadir}/IceGridGUI.jar 
cp -p $RPM_BUILD_DIR/Ice-%{version}/java/bin/icegridgui.rpm %{buildroot}%{_bindir}/icegridgui
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}/help
cp -Rp $RPM_BUILD_DIR/Ice-%{version}/java/resources/IceGridAdmin %{buildroot}%{_docdir}/%{name}-%{version}/help

cp -p $RPM_BUILD_DIR/Ice-%{version}/java/libjava5/ant-ice.jar %{buildroot}%{_javadir}/ant-ice-%{version}.jar
ln -s ant-ice-%{version}.jar %{buildroot}%{_javadir}/ant-ice.jar 
%endif
#
# Mono: for iceboxnet.exe and GAC symlinks
#
#pushd cs
#%makeinstall GACINSTALL=yes GAC_ROOT=%{buildroot}%{_prefix}/lib
#popd

#
# .NET spec files (for mono-devel)
#
if test ! -d %{buildroot}%{_libdir}/pkgconfig
then
    mv %{buildroot}/lib/pkgconfig %{buildroot}%{_libdir}
fi

#
# initrd files (for servers)
#
mkdir -p %{buildroot}/%{_sysconfdir}
cp ../Ice-rpmbuild-%{version}/*.conf %{buildroot}/%{_sysconfdir}
mkdir -p %{buildroot}/%{_initrddir}
for i in icegridregistry icegridnode glacier2router ; do
    cp ../Ice-rpmbuild-%{version}/$i.redhat %{buildroot}/%{_initrddir}/$i
done

install ../ice.pth %{buildroot}/%{python_sitearch}/ice.pth

#
# Cleanup extra files
#
rm -fr %{buildroot}/doc/reference
rm -fr %{buildroot}/slice
rm -f %{buildroot}%{_libdir}/libIceStormService.so

%if %{build_java}
pushd java
ant -Dice.mapping=java5 -Dbuild.suffix=java5 -Dprefix=%{buildroot} install
ant -Dice.mapping=java2 -Dbuild.suffix=java2 -Dprefix=%{buildroot} install

mkdir -p %{buildroot}%{_javadir}
mv %{buildroot}/lib/Ice.jar %{buildroot}%{_javadir}/Ice-%{version}.jar
ln -s  Ice-%{version}.jar %{buildroot}%{_javadir}/Ice.jar 
mv %{buildroot}/lib/java2/Ice.jar %{buildroot}%{_javadir}/Ice-java2-%{version}.jar
ln -s Ice-java2-%{version}.jar %{buildroot}%{_javadir}/Ice-java2.jar
popd
%endif

#
# Mono
#
cd $RPM_BUILD_DIR/Ice-%{version}/cs
make prefix=%{buildroot} GACINSTALL=yes GAC_ROOT=%{buildroot}%{_prefix}/lib install

#
# Slice  files
#
mkdir -p %{buildroot}%{_datadir}/Ice-%{version}
mv %{buildroot}/slice %{buildroot}%{_datadir}/Ice-%{version}

#
# Cleanup extra files
#
rm -fr %{buildroot}/help
rm -f %{buildroot}/lib/IceGridGUI.jar %{buildroot}/lib/ant-ice.jar
rm -f %{buildroot}/bin/iceboxnet.exe

for f in Ice Glacier2 IceBox IceGrid IcePatch2 IceStorm
do 
     rm -r %{buildroot}%{_prefix}/lib/mono/$f
done

rm -r %{buildroot}/lib/pkgconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%dir %{_datadir}/Ice-%{version}
%{_datadir}/Ice-%{version}/slice

%files mono
%defattr(-, root, root, -)
%dir %{_libdir}/mono/gac/Glacier2
%{_libdir}/mono/gac/Glacier2/%{dotnetversion}.*/
%dir %{_libdir}/mono/gac/Ice
%{_libdir}/mono/gac/Ice/%{dotnetversion}.*/
%dir %{_libdir}/mono/gac/IceBox
%{_libdir}/mono/gac/IceBox/%{dotnetversion}.*/
%dir %{_libdir}/mono/gac/IceGrid
%{_libdir}/mono/gac/IceGrid/%{dotnetversion}.*/
%dir %{_libdir}/mono/gac/IcePatch2
%{_libdir}/mono/gac/IcePatch2/%{dotnetversion}.*/
%dir %{_libdir}/mono/gac/IceStorm
%{_libdir}/mono/gac/IceStorm/%{dotnetversion}.*/
%dir %{_libdir}/mono/gac/policy.%{dotnetpolicyversion}.Glacier2
%{_libdir}/mono/gac/policy.%{dotnetpolicyversion}.Glacier2/0.*/
%dir %{_libdir}/mono/gac/policy.%{dotnetpolicyversion}.Ice
%{_libdir}/mono/gac/policy.%{dotnetpolicyversion}.Ice/0.*/
%dir %{_libdir}/mono/gac/policy.%{dotnetpolicyversion}.IceBox
%{_libdir}/mono/gac/policy.%{dotnetpolicyversion}.IceBox/0.*/
%dir %{_libdir}/mono/gac/policy.%{dotnetpolicyversion}.IceGrid
%{_libdir}/mono/gac/policy.%{dotnetpolicyversion}.IceGrid/0.*/
%dir %{_libdir}/mono/gac/policy.%{dotnetpolicyversion}.IcePatch2
%{_libdir}/mono/gac/policy.%{dotnetpolicyversion}.IcePatch2/0.*/
%dir %{_libdir}/mono/gac/policy.%{dotnetpolicyversion}.IceStorm
%{_libdir}/mono/gac/policy.%{dotnetpolicyversion}.IceStorm/0.*/

%if %build_java
%files java
%defattr(-, root, root, -)
%{_javadir}/Ice-%{version}.jar
%{_javadir}/Ice.jar
%{_javadir}/Ice-java2-%{version}.jar
%{_javadir}/Ice-java2.jar

%files java-devel
%defattr(-, root, root, -)
%{_bindir}/slice2java
%{_bindir}/slice2freezej
%{_javadir}/ant-ice-%{version}.jar
%{_javadir}/ant-ice.jar
%endif

%files libs
%defattr(-, root, root, -)
%{_libdir}/libFreeze.so.%{version}
%{_libdir}/libFreeze.so.%{soversion}
%{_libdir}/libGlacier2.so.%{version}
%{_libdir}/libGlacier2.so.%{soversion}
%{_libdir}/libIceBox.so.%{version}
%{_libdir}/libIceBox.so.%{soversion}
%{_libdir}/libIcePatch2.so.%{version}
%{_libdir}/libIcePatch2.so.%{soversion}
%{_libdir}/libIce.so.%{version}
%{_libdir}/libIce.so.%{soversion}
%{_libdir}/libIceSSL.so.%{version}
%{_libdir}/libIceSSL.so.%{soversion}
%{_libdir}/libIceStorm.so.%{version}
%{_libdir}/libIceStorm.so.%{soversion}
%{_libdir}/libIceUtil.so.%{version}
%{_libdir}/libIceUtil.so.%{soversion}
%{_libdir}/libSlice.so.%{version}
%{_libdir}/libSlice.so.%{soversion}
%{_libdir}/libIceGrid.so.%{version}
%{_libdir}/libIceGrid.so.%{soversion}

%files utils
%defattr(-, root, root, -)
%{_libdir}/libIceXML.so.%{version}
%{_libdir}/libIceXML.so.%{soversion}
%{_bindir}/dumpdb
%{_bindir}/transformdb
%{_bindir}/iceboxadmin
%{_bindir}/icepatch2calc
%{_bindir}/icepatch2client
%{_bindir}/icestormadmin
%{_bindir}/slice2docbook
%{_bindir}/slice2html
%{_bindir}/icegridadmin
%{_bindir}/icegridgui
%{_bindir}/iceca
%{_javadir}/IceGridGUI-%{version}.jar
%{_javadir}/IceGridGUI.jar
%{doc} %{name}-%{version}/help
%dir %{_datadir}/Ice-%{version}
%{_datadir}/Ice-%{version}/ImportKey.class
%attr(755,root,root) %{_datadir}/Ice-%{version}/convertssl.py*

%files servers
%defattr(-, root, root, -)
%{_bindir}/glacier2router
%{_bindir}/icebox
%{_bindir}/iceboxnet.exe
%{_bindir}/icegridnode
%{_bindir}/icegridregistry
%{_bindir}/icepatch2server
%{_bindir}/icestormmigrate
%{_libdir}/libIceStormService.so.%{version}
%{_libdir}/libIceStormService.so.%{soversion}
%dir %{_datadir}/Ice-%{version}
%{_datadir}/Ice-%{version}/templates.xml
%attr(755,root,root) %{_datadir}/Ice-%{version}/upgradeicegrid.py*
%{_datadir}/Ice-%{version}/icegrid-slice.3.1.ice.gz
%{_datadir}/Ice-%{version}/icegrid-slice.3.2.ice.gz
%{_datadir}/Ice-%{version}/icegrid-slice.3.3.ice.gz
%attr(755,root,root) %{_initrddir}/icegridregistry
%attr(755,root,root) %{_initrddir}/icegridnode
%attr(755,root,root) %{_initrddir}/glacier2router
%config(noreplace) %{_sysconfdir}/icegridregistry.conf
%config(noreplace) %{_sysconfdir}/icegridnode.conf
%config(noreplace) %{_sysconfdir}/glacier2router.conf

%pre servers
%_pre_groupadd ice
%_pre_useradd %{_localstatedir}/lib/ice /sbin/nologin ice
test -d %{_localstatedir}/lib/ice/icegrid/registry || \
       mkdir -p %{_localstatedir}/lib/ice/icegrid/registry; chown -R ice.ice %{_localstatedir}/lib/ice
test -d %{_localstatedir}/lib/ice/icegrid/node1 || \
       mkdir -p %{_localstatedir}/lib/ice/icegrid/node1; chown -R ice.ice %{_localstatedir}/lib/ice

%post servers
%_post_service icegridregistry
%_post_service icegridnode
%_post_service glacier2router

%preun servers
%_preun_service icegridnode
%_preun_service icegridregistry
%_preun_service glacier2router

%postun servers
%_postun_groupdel  ice
%_postun_userdel

%files c++-devel
%defattr(-, root, root, -)
%{_bindir}/slice2cpp
%{_bindir}/slice2freeze
%{_includedir}/Freeze
%{_includedir}/Glacier2
%{_includedir}/Ice
%{_includedir}/IceBox
%{_includedir}/IceGrid
%{_includedir}/IcePatch2
%{_includedir}/IceSSL
%{_includedir}/IceStorm
%{_includedir}/IceUtil
%{_includedir}/IceXML
%{_includedir}/Slice
%{_libdir}/libFreeze.so
%{_libdir}/libGlacier2.so
%{_libdir}/libIceBox.so
%{_libdir}/libIceGrid.so
%{_libdir}/libIcePatch2.so
%{_libdir}/libIce.so
%{_libdir}/libIceSSL.so
%{_libdir}/libIceStorm.so
%{_libdir}/libIceUtil.so
%{_libdir}/libIceXML.so
%{_libdir}/libSlice.so

%files mono-devel
%defattr(-, root, root, -)
%{_bindir}/slice2cs
%{_libdir}/pkgconfig/Ice.pc
%{_libdir}/pkgconfig/Glacier2.pc
%{_libdir}/pkgconfig/IceBox.pc
%{_libdir}/pkgconfig/IceGrid.pc
%{_libdir}/pkgconfig/IcePatch2.pc
%{_libdir}/pkgconfig/IceStorm.pc
%{_prefix}/lib/mono/Glacier2/
%{_prefix}/lib/mono/Ice/
%{_prefix}/lib/mono/IceBox/
%{_prefix}/lib/mono/IceGrid/
%{_prefix}/lib/mono/IcePatch2/
%{_prefix}/lib/mono/IceStorm/

%files python
%defattr(-, root, root, -)
%{python_sitearch}/Ice
%{python_sitearch}/ice.pth

%files python-devel
%defattr(-, root, root, -)
%{_bindir}/slice2py

%files ruby
%defattr(-, root, root, -)
%{ruby_sitearch}/*

%files ruby-devel
%defattr(-, root, root, -)
%{_bindir}/slice2rb

%files php
%defattr(-, root, root, -)
%{_libdir}/php/modules/IcePHP.so
%config(noreplace) %{_sysconfdir}/php.d/ice.ini

