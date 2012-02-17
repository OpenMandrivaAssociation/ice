%define major 34
%define libname %mklibname %{name} %{major}

Name:		ice
Version:	3.4.2
Release:	1
Summary:	The Ice base runtime and services

Group:		Networking/WWW
License:	GPLv2 with exceptions
URL:		http://www.zeroc.com/
Source0:	http://www.zeroc.com/download/Ice/3.3/Ice-%{version}.tar.gz
# Man pages courtesy of Francisco Moya's Debian packages
Source1:	ice-3.4.2-man-pages.tar.gz
Source2:	icegridgui
Source3:	IceGridAdmin.desktop
Source4:	Ice-README.Fedora
Source5:	glacier2router.conf
Source6:	glacier2router.service
Source7:	icegridnode.conf
Source8:	icegridnode.service
Source9:	icegridregistry.conf
Source10:	icegridregistry.service
Source11:	ice.ini
Source12:	ice.pth
Source108:	icegridgui
Source109:	IceGridAdmin.desktop
Source110:	Ice-README.Mandriva
# Remove reference to Windows L&F
Patch0:		ice-3.4.2-jgoodies.patch
# fix gcc46 issue
Patch1:		ice-3.4.2-gcc46.patch
# Add support for the s390/s390x architecture
Patch2:		Ice-3.4.0-s390.patch
# don't build demo/test
# TODO: should we keep it or not ?
# significantly reduce compile time but shipping demos could be useful
Patch3:		Ice-3.3-dont-build-demo-test.patch
# disable the CSharp interface
Patch4:		ice-3.4.1-no-mono.patch
# fix java 7 compilation
Patch5:		ice-3.4.2-java7.patch
# fix php 5.4 compilation (from upstream)
Patch6:		ice-3.4.2-php54.patch
Patch7:		ice-3.4.2-gcc47.patch

# Fix redhat initscripts for mdv and change user in server scripts 
# from "ice" to "iceuser" to match the config
Patch8:		Ice-rpmbuild-3.3.1-fix-initscripts-for-mdv.patch

Patch9:		ice-3.3.1-fix-db-include.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

# Ice doesn't officially support ppc64 at all
# sparc64 doesnt have mono
ExcludeArch:	ppc64 sparc64

BuildRequires:	db-devel
BuildRequires:	expat-devel
BuildRequires:	openssl-devel
BuildRequires:	bzip2-devel
BuildRequires:	ant
BuildRequires:	ant-nodeps
BuildRequires:	jpackage-utils
BuildRequires:	php
BuildRequires:	php-devel
BuildRequires:	ruby-devel
BuildRequires:	python-devel
BuildRequires:	mono
BuildRequires:	mono-devel
BuildRequires:	mcpp-devel >= 2.7.1
BuildRequires:	dos2unix

BuildRequires:	java-rpmbuild

BuildRequires:	jgoodies-common
BuildRequires:	jgoodies-forms
BuildRequires:	jgoodies-looks
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils

Requires:	%{libname} = %{version}-%{release}

%description
Ice is a modern alternative to object middleware such as CORBA or
COM/DCOM/COM+.  It is easy to learn, yet provides a powerful network
infrastructure for demanding technical applications. It features an
object-oriented specification language, easy to use C++, C#, Java,
Python, Ruby, PHP, and Visual Basic mappings, a highly efficient
protocol, asynchronous method invocation and dispatch, dynamic
transport plug-ins, TCP/IP and UDP/IP support, SSL-based security, a
firewall solution, and much more.

# All of the other Ice packages also get built by this SRPM.

%package -n	%{libname}
Summary:	Ice shared libraries
Group:		System/Libraries

%description -n	%{libname}
This package contains Ice shared libraries.

%package	servers
Summary:	Ice services to run through /etc/rc.d/init.d
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}
# Requirements for the users
Requires(pre):	shadow-utils
# Requirements for the init.d services
%if %mdkversion < 201010
Requires(post):	rpm-helper
Requires(preun):rpm-helper
%endif

%description	servers
Ice services to run through /etc/rc.d/init.d

%package	devel
Summary:	Tools for developing Ice applications in C++
Group:		Development/C++
Provides:	ice-c++-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description	devel
Tools for developing Ice applications in C++.

%package	java
Summary:	The Ice runtime for Java
Group:		System/Libraries
Requires:	java >= 1.5.0
Requires:	%{libname} = %{version}-%{release}
Requires:	db5.3

%description	java
The Ice runtime for Java

%package	java-devel
Summary:	Tools for developing Ice applications in Java
Group:		Development/Java
Requires:	%{name}-java = %{version}-%{release}

%description	java-devel
Tools for developing Ice applications in Java.

%package -n	icegrid-gui
Summary:	IceGrid Admin Tool
Group:		Development/Other
Requires:	java
Requires:	%{name}-java = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	jgoodies-forms
Requires:	jgoodies-looks
Requires:	jpackage-utils

%description -n icegrid-gui
Graphical administration tool for IceGrid

%package	csharp
Summary:	The Ice runtime for C#
Group:		System/Libraries
Provides:	ice-dotnet = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	mono >= 1.2.2

%description	csharp
The Ice runtime for C#

%package	csharp-devel
Summary:	Tools for developing Ice applications in C#
Group:		Development/Other
Requires:	%{name}-csharp = %{version}-%{release}
Requires:	pkgconfig

%description	csharp-devel
Tools for developing Ice applications in C#.

%package	ruby
Summary:	The Ice runtime for Ruby applications
Group:		Development/Ruby
Requires:	%{libname} = %{version}-%{release}

%description	ruby
The Ice runtime for Ruby applications.

%package	ruby-devel
Summary:	Tools for developing Ice applications in Ruby
Group:		Development/Ruby
Requires:	%{name}-ruby = %{version}-%{release}

%description	ruby-devel
Tools for developing Ice applications in Ruby.

%package -n	python-%{name}
Summary:	The Ice runtime for Python applications
Group:		Development/Python
Requires:	%{libname} = %{version}-%{release}
Requires:	python >= 2.3.4

%description -n	python-%{name}
The Ice runtime for Python applications.

%package -n	python-%{name}-devel
Summary:	Tools for developing Ice applications in Python
Group:		Development/Python
Requires:	python-%{name} = %{version}-%{release}

%description -n	python-%{name}-devel
Tools for developing Ice applications in Python.

%package -n	php-%{name}
Summary:	The Ice runtime for PHP applications
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Requires:	php

%description -n	php-%{name}
The Ice runtime for PHP applications.

%prep
%setup -n Ice-%{version} -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1 -b .php54
%patch7 -p1
#patch9 -p1
#patch8 -p1 -b .formdv

%build
# Set the CLASSPATH correctly for the Java compile
export CLASSPATH=`build-classpath db5.3 jgoodies-forms jgoodies-looks`
export CFLAGS="%{optflags} -I%{_includedir}/db53"
# Set JAVA_HOME
export JAVA_HOME=%{java_home}

# Compile the main Ice runtime
cd %{_builddir}/Ice-%{version}

make CFLAGS="$CFLAGS" CXXFLAGS="$CFLAGS" embedded_runpath_prefix=""

# Rebuild the Java ImportKey class
cd %{_builddir}/Ice-%{version}/cpp/src/ca
rm *.class
javac ImportKey.java

# Create the IceGrid icon
cd %{_builddir}/Ice-%{version}/java
cd resources/icons
convert icegrid.ico temp.png
mv temp-8.png icegrid.png
rm temp*.png


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

# Do the basic "make install"
cd %{_builddir}/Ice-%{version}
make prefix=%{buildroot} GACINSTALL=yes GAC_ROOT=%{buildroot}%{_libdir} embedded_runpath_prefix="" install

# Move Java stuff where it should be
mkdir -p %{buildroot}%{_javadir}
mv %{buildroot}/lib/ant-ice.jar %{buildroot}%{_javadir}/ant-ice-%{version}.jar
ln -s ant-ice-%{version}.jar %{buildroot}%{_javadir}/ant-ice.jar
mv %{buildroot}/lib/Ice.jar %{buildroot}%{_javadir}/Ice-%{version}.jar
ln -s Ice-%{version}.jar %{buildroot}%{_javadir}/Ice.jar


# Install the IceGrid GUI
mkdir -p %{buildroot}%{_datadir}/%{name}
mv %{buildroot}/lib/IceGridGUI.jar %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/
cp -p %{_builddir}/Ice-%{version}/java/resources/icons/icegrid.png \
        %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/
mkdir -p %{buildroot}%{_bindir}
cp -p %{SOURCE108} %{buildroot}%{_bindir}
sed -i -e "s#DIR#%{_datadir}/%{name}#" %{buildroot}%{_bindir}/icegridgui
desktop-file-install \
        --dir=%{buildroot}%{_datadir}/applications \
        %{SOURCE109}

# Move other rpm-specific files into the right place (README, service stuff)
mkdir -p %{buildroot}%{_defaultdocdir}/%{name}
cp -p %{SOURCE110} %{buildroot}/%{_defaultdocdir}/%{name}/README.Mandriva
cp -p %{_builddir}/Ice-rpmbuild-%{version}/ice.ini %{buildroot}/ice.ini

# Install the servers
mkdir -p %{buildroot}%{_sysconfdir}
cp -p %{_builddir}/Ice-rpmbuild-%{version}/*.conf %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_initrddir}
for i in icegridregistry icegridnode glacier2router
do
    cp -p %{_builddir}/Ice-rpmbuild-%{version}/$i.redhat %{buildroot}%{_initrddir}/$i
done
mkdir -p %{buildroot}%{_localstatedir}/lib/icegrid

# "make install" assumes it's going into a directory under /opt.
# Move things to where they should be in an RPM setting (adapted from
# the original ZeroC srpm).
mkdir -p %{buildroot}%{_bindir}
mv %{buildroot}/bin/* %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}
mv %{buildroot}/include/* %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
# There are a couple of files that end up installed in /lib, not %{_libdir},
# so we try this move too.
mv %{buildroot}/%{_lib}/* %{buildroot}%{_libdir}
mv %{buildroot}/lib/* %{buildroot}%{_libdir} || true
mkdir -p %{buildroot}%{_defaultdocdir}/icegrid-gui
mv %{buildroot}/help/IceGridAdmin %{buildroot}%{_defaultdocdir}/icegrid-gui

# Copy the man pages into the correct directory
mkdir -p %{buildroot}%{_mandir}/man1
cp -p %{_builddir}/Ice-3.3.0-man-pages/*.1 %{buildroot}%{_mandir}/man1

# Fix the encoding and line-endings of all the IceGridAdmin documentation files
cd %{buildroot}%{_defaultdocdir}/icegrid-gui/IceGridAdmin
chmod a-x *
for f in *.js *.css;
do
    dos2unix $f
done
for f in helpman_topicinit.js icegridadmin_navigation.js \
    IceGridAdmin_popup_html.js zoom_pageinfo.js;
do
    iconv -f ISO88591 -t UTF8 $f -o $f.tmp
    mv $f.tmp $f
done

# .NET spec files (for csharp-devel) -- convert the paths
for f in IceGrid Glacier2 IceBox Ice IceStorm IcePatch2;
do 
    sed -i -e "s#/lib/#%{_libdir}/#" %{buildroot}%{_libdir}/pkgconfig/$f.pc
    sed -i -e "s#mono_root}/usr#mono_root}#" %{buildroot}%{_libdir}/pkgconfig/$f.pc
done

# Put the PHP stuff into the right place
mkdir -p %{buildroot}%{_sysconfdir}/php.d
mv %{buildroot}/ice.ini %{buildroot}%{_sysconfdir}/php.d
mkdir -p %{buildroot}%{_libdir}/php/extensions/
mv %{buildroot}%{_libdir}/IcePHP.so %{buildroot}%{_libdir}/php/extensions/

# Also Ruby and Python -- remove all shebang lines while we're at it
for f in %{buildroot}/python/Ice.py %{buildroot}/ruby/*.rb;
do
    grep -v '/usr/bin/env' $f > $f.tmp
    mv $f.tmp $f
done
mkdir -p %{buildroot}%{ruby_sitearchdir}
mv %{buildroot}/ruby/* %{buildroot}%{ruby_sitearchdir}
mkdir -p %{buildroot}%{python_sitearch}/Ice
mv %{buildroot}/python/* %{buildroot}%{python_sitearch}/Ice
cp -p %{_builddir}/Ice-rpmbuild-%{version}/ice.pth %{buildroot}%{python_sitearch}

mkdir -p %{buildroot}%{_datadir}/%{name}
mv %{buildroot}/config/* %{buildroot}%{_datadir}/%{name}
mv %{buildroot}/slice %{buildroot}%{_datadir}/%{name}
# Somehow, some files under "slice" end up with executable permissions -- ??
find %{buildroot}%{_datadir}/%{name} -name "*.ice" | xargs chmod a-x

# Move the ImportKey.class file -- it'll be in %{_libdir} because of the moves earlier
mkdir -p %{buildroot}%{_datadir}/%{name}
mv %{buildroot}%{_libdir}/ImportKey.class %{buildroot}%{_datadir}/%{name}

# Put the license files in as documentation
mkdir -p %{buildroot}%{_defaultdocdir}/%{name}
mv %{buildroot}/ICE_LICENSE %{buildroot}%{_defaultdocdir}/%{name}/ICE_LICENSE
mv %{buildroot}/LICENSE %{buildroot}%{_defaultdocdir}/%{name}/LICENSE


%clean
rm -rf %{buildroot}

%pre servers
%_pre_useradd iceuser %{_localstatedir}/lib/icegrid /bin/sh

%post servers
%_post_service icegridregistry
%_post_service icegridnode
%_post_service glacier2router

%preun servers
if [ $1 = 0 ]; then
        %_preun_service icegridregistry
        %_preun_service icegridnode
        %_preun_service glacier2router
fi

%postun servers
if [ "$1" -ge "1" ]; then
        /sbin/service icegridregistry condrestart >/dev/null 2>&1 || :
        /sbin/service icegridnode condrestart >/dev/null 2>&1 || :
        /sbin/service glacier2router condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%{_defaultdocdir}/%{name}
%{_bindir}/dumpdb
%{_bindir}/glacier2router
%{_bindir}/icebox
%{_bindir}/iceboxadmin
%{_bindir}/iceca
%{_bindir}/icegridadmin
%{_bindir}/icegridnode
%{_bindir}/icegridregistry
%{_bindir}/icepatch2calc
%{_bindir}/icepatch2client
%{_bindir}/icepatch2server
%{_bindir}/icestormadmin
%{_bindir}/icestormmigrate
%{_bindir}/slice2docbook
%{_bindir}/slice2html
%{_bindir}/transformdb
%{_datadir}/%{name}
# Exclude the stuff that's in IceGrid
%exclude %{_datadir}/%{name}/IceGridGUI.jar
%{_mandir}/man1/dumpdb.1.*
%{_mandir}/man1/glacier2router.1.*
%{_mandir}/man1/icebox.1.*
%{_mandir}/man1/iceboxadmin.1.*
%{_mandir}/man1/icegridadmin.1.*
%{_mandir}/man1/icegridnode.1.*
%{_mandir}/man1/icegridregistry.1.*
%{_mandir}/man1/icepatch2calc.1.*
%{_mandir}/man1/icepatch2client.1.*
%{_mandir}/man1/icepatch2server.1.*
%{_mandir}/man1/icestormadmin.1.*
%{_mandir}/man1/slice2docbook.1.*
%{_mandir}/man1/slice2html.1.*
%{_mandir}/man1/transformdb.1.*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libFreeze.so.%{version}
%{_libdir}/libFreeze.so.%{major}
%{_libdir}/libGlacier2.so.%{version}
%{_libdir}/libGlacier2.so.%{major}
%{_libdir}/libIceBox.so.%{version}
%{_libdir}/libIceBox.so.%{major}
%{_libdir}/libIcePatch2.so.%{version}
%{_libdir}/libIcePatch2.so.%{major}
%{_libdir}/libIce.so.%{version}
%{_libdir}/libIce.so.%{major}
%{_libdir}/libIceSSL.so.%{version}
%{_libdir}/libIceSSL.so.%{major}
%{_libdir}/libIceStormService.so.%{version}
%{_libdir}/libIceStormService.so.%{major}
%{_libdir}/libIceStorm.so.%{version}
%{_libdir}/libIceStorm.so.%{major}
%{_libdir}/libIceUtil.so.%{version}
%{_libdir}/libIceUtil.so.%{major}
%{_libdir}/libIceXML.so.%{version}
%{_libdir}/libIceXML.so.%{major}
%{_libdir}/libSlice.so.%{version}
%{_libdir}/libSlice.so.%{major}
%{_libdir}/libIceGrid.so.%{version}
%{_libdir}/libIceGrid.so.%{major}

%files servers
%defattr(-,root,root,-)
%{_initrddir}/icegridregistry
%{_initrddir}/icegridnode
%{_initrddir}/glacier2router
%config(noreplace) %{_sysconfdir}/icegridregistry.conf
%config(noreplace) %{_sysconfdir}/icegridnode.conf
%config(noreplace) %{_sysconfdir}/glacier2router.conf
%dir %{_localstatedir}/lib/icegrid

%files devel
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
%{_libdir}/libIceStormService.so
%{_libdir}/libIceStorm.so
%{_libdir}/libIceUtil.so
%{_libdir}/libIceXML.so
%{_libdir}/libSlice.so
%{_mandir}/man1/slice2cpp.1.*
%{_mandir}/man1/slice2freeze.1.*

%files java
%defattr(-,root,root,-)
%{_javadir}/Ice-%{version}.jar
%{_javadir}/Ice.jar

%files -n icegrid-gui
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/icegridgui
%{_datadir}/%{name}/IceGridGUI.jar
%{_datadir}/applications/IceGridAdmin.desktop
%{_datadir}/icons/hicolor/48x48/apps/icegrid.png
%{_defaultdocdir}/icegrid-gui
%{_mandir}/man1/icegridgui.1.*

%files java-devel
%defattr(-,root,root,-)
%{_bindir}/slice2java
%{_bindir}/slice2freezej
%{_javadir}/ant-ice-%{version}.jar
%{_javadir}/ant-ice.jar
%{_mandir}/man1/slice2java.1.*
%{_mandir}/man1/slice2freezej.1.*

%files csharp
%defattr(-,root,root,-)
%{_libdir}/mono/Glacier2/
%{_libdir}/mono/Ice/
%{_libdir}/mono/IceBox/
%{_libdir}/mono/IceGrid/
%{_libdir}/mono/IcePatch2/
%{_libdir}/mono/IceStorm/

%{_libdir}/mono/gac/Glacier2
%{_libdir}/mono/gac/Ice
%{_libdir}/mono/gac/IceBox
%{_libdir}/mono/gac/IceGrid
%{_libdir}/mono/gac/IcePatch2
%{_libdir}/mono/gac/IceStorm

%{_libdir}/mono/gac/policy*

%{_bindir}/iceboxnet.exe
%{_mandir}/man1/iceboxnet.exe.1.*

%files csharp-devel
%defattr(-,root,root,-)
%{_bindir}/slice2cs
%{_libdir}/pkgconfig/Glacier2.pc
%{_libdir}/pkgconfig/Ice.pc
%{_libdir}/pkgconfig/IceBox.pc
%{_libdir}/pkgconfig/IceGrid.pc
%{_libdir}/pkgconfig/IcePatch2.pc
%{_libdir}/pkgconfig/IceStorm.pc
%{_mandir}/man1/slice2cs.1.*

%files -n python-%{name}
%defattr(644,root,root,755)
%{python_sitearch}/Ice/
%{python_sitearch}/%{name}.pth

%files -n python-%{name}-devel
%defattr(-,root,root,-)
%{_bindir}/slice2py
%{_mandir}/man1/slice2py.1.*

%files ruby
%defattr(644,root,root,755)
%{ruby_sitearchdir}/*

%files ruby-devel
%defattr(-,root,root,-)
%{_bindir}/slice2rb
%{_mandir}/man1/slice2rb.1.*

%files -n php-%{name}
%defattr(-,root,root,-)
%{_libdir}/php/extensions/IcePHP.so
%config(noreplace) %{_sysconfdir}/php.d/ice.ini
