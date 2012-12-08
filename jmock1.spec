# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
%define gcj_support 0
%define section   free
%define maven_name jmock

Name:           jmock1
Version:        1.2.0
Release:        %mkrel 3
Summary:        Test Java code using mock objects

Group:          Development/Java
License:        Open Source
URL:            http://jmock.codehaus.org/
Source0:        jmock-1.2.0.tar.gz
# svn export http://svn.codehaus.org/jmock/tags/1.2.0/ jmock-1.2.0
Source1:        jmock-1.2.0.pom
Source2:        jmock-cglib-1.2.0.pom


Patch0:         jmock-1.2.0-AssertMo.patch
Patch1:         jmock-1.2.0-build_xml.patch
Patch2:		jmock-asm_rename.patch
Patch3:		jmock-1.2.0-cglib2.2-asm3.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRequires:	java-devel 
BuildRequires:  java-rpmbuild 
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit
BuildRequires:  junit >= 0:3.8.1
BuildRequires:  cglib
BuildRequires:  objectweb-asm
BuildRequires:  jaxp_parser_impl
Requires:  cglib
Requires:  objectweb-asm
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%endif
Provides:	jmock = %{version}-%{release}

%description
jMock is a library for testing Java code using mock objects.
Mock objects help you design and test the interactions between the 
objects in your programs.
The jMock package:
* makes it quick and easy to define mock objects, so you don't break 
  the rhythm of programming.
* lets you define flexible constraints over object interactions, 
  reducing the brittleness of your tests.
* is easy to extend.


%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
%{summary}.

%package        demo
Summary:        Examples for %{name}
Group:          Development/Java

%description    demo
%{summary}.

%prep
%setup -q -n jmock-%version
%remove_java_binaries

%patch0 -p0 -b .sav
%patch1 -p0 -b .sav
%patch2 -p1
%patch3 -p1

%build
export OPT_JAR_LIST="ant/ant-junit junit"

export CLASSPATH=$(build-classpath cglib objectweb-asm):build/classes
CLASSPATH=build/classes:$CLASSPATH
%ant -Dbuild.sysclasspath=only package


%install
rm -rf $RPM_BUILD_ROOT

install -Dpm 644 build/jmock-core-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/jmock-%{version}.jar
install -pm 644 build/jmock-cglib-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/jmock-cglib-%{version}.jar
install -pm 644 build/jmock-tests-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/jmock-tests-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

%add_to_maven_depmap %{maven_name} %{maven_name} %{version} JPP %{maven_name}
%add_to_maven_depmap %{maven_name} %{maven_name}-cglib %{version} JPP %{maven_name}-cglib

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 %{SOURCE1} \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{maven_name}.pom
install -pm 644 %{SOURCE2} \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{maven_name}-cglib.pom

#
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/javadoc-%{version}/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} 
#
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
cp -pr examples/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}

%{gcj_compile}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root,-)
%doc LICENSE.txt overview.html
%{_javadir}/*.jar
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}
%{gcj_files}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files demo
%defattr(-,root,root,-)
%doc %{_datadir}/%{name}-%{version}


%changelog
* Wed Apr 11 2012 Andrew Lukoshko <andrew.lukoshko@rosalab.ru> 1.2.0-3
- patched to build with cglib 2.2 and objectweb-asm 3 (ROSA exclusive)

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.0-2.0.6mdv2011.0
+ Revision: 606096
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.0-2.0.5mdv2010.1
+ Revision: 523086
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.2.0-2.0.4mdv2010.0
+ Revision: 425464
- rebuild

* Tue Jun 17 2008 Alexander Kurtakov <akurtakov@mandriva.org> 1.2.0-2.0.3mdv2009.0
+ Revision: 222356
- build with cglib not cglib-nohook
- add gcj_support=0
- fix typo
- fix BRs and disable gcj_compile

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 1.2.0-2.0.3mdv2008.1
+ Revision: 120947
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sun Dec 16 2007 Alexander Kurtakov <akurtakov@mandriva.org> 1.2.0-2.0.2mdv2008.1
+ Revision: 120742
- bumb release

* Sun Dec 16 2007 Alexander Kurtakov <akurtakov@mandriva.org> 1.2.0-2.0.1.1mdv2008.1
+ Revision: 120675
- fix maven depmap

* Fri Nov 30 2007 Alexander Kurtakov <akurtakov@mandriva.org> 1.2.0-2.0.1mdv2008.1
+ Revision: 114185
- fix Require so it can be installed

* Wed Sep 19 2007 Nicolas Vigier <nvigier@mandriva.com> 1.2.0-2mdv2008.0
+ Revision: 90615
- rebuild

* Tue Sep 18 2007 Nicolas Vigier <nvigier@mandriva.com> 1.2.0-1mdv2008.0
+ Revision: 89754
- adapt package to mandriva
- patch sources for net.sf.cglib.asm renamed to org.objectweb.asm
- Import jmock1



* Fri Sep 14 2007 Nicolas Vigier <nvigier@mandriva.com>
- rename package to jmock1
- change buildrequire from cglib to cglib-nohook

* Tue Jul 17 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.2.0-1jpp
- Upgrade to 1.2.0
- Add poms and depmap frags
- Make Vendor, Distribution based on macro

* Fri Feb 23 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.0.1-4jpp
- Patch AssertMo.java to current junit
- Add gcj_support option

* Fri Feb 17 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.0.1-3jpp
- Require cglib-nohook instead of cglib to break circular dependency

* Wed Jan 04 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0.1-2jpp
- First JPP 1.7 build

* Wed Mar 16 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.0.1-1jpp
- Upgrade to 1.0.1
- Patch to adapt to asm-1.5.3
- Built with asm-1.5.3 and cglib-2.1.0

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:1.0.0-3jpp
- Rebuild with ant-1.6.2
- Upgrade to Ant 1.6.X

* Fri Jun 04 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0.0-2jpp
- Graduate to free section for use with qdox-1.4

* Tue Jun 01 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0.0-1jpp
- First JPackage release
