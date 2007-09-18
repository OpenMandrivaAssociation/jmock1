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

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

%define section   free

Name:           jmock1
Version:        1.2.0
Release:        %mkrel 1
Summary:        Test Java code using mock objects

Group:          Development/Libraries/Java
License:        Open Source
URL:            http://jmock.codehaus.org/
Source0:        jmock-1.2.0.tar.gz
# svn export http://svn.codehaus.org/jmock/tags/1.2.0/ jmock-1.2.0
Source1:        jmock-1.2.0.pom
Source2:        jmock-cglib-1.2.0.pom


Patch0:         jmock-1.2.0-AssertMo.patch
Patch1:         jmock-1.2.0-build_xml.patch
Patch2:		jmock-asm_rename.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit
BuildRequires:  junit >= 0:3.8.1
BuildRequires:  cglib-nohook >= 0:2.1.3
BuildRequires:  asm >= 0:1.5.3
Requires:  cglib >= 0:2.1.3
Requires:  asm >= 0:1.5.3
%if %{gcj_support}
BuildRequires:    gnu-crypto
BuildRequires:    java-gcj-compat-devel
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
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
Group:          Development/Documentation
Requires(post):   /bin/rm,/bin/ln
Requires(postun): /bin/rm

%description    javadoc
%{summary}.

%package        demo
Summary:        Examples for %{name}
Group:          Development/Documentation

%description    demo
%{summary}.

%prep
%setup -q -n jmock-%version
for j in $(find . -name "*.jar"); do
    mv $j $j.no
done

%patch0 -b .sav
%patch1 -b .sav
%patch2 -p1

%build
export OPT_JAR_LIST="ant/ant-junit junit"

export CLASSPATH=$(build-classpath \
asm \
cglib-nohook)

CLASSPATH=build/classes:$CLASSPATH
ant -Dbuild.sysclasspath=only package


%install
rm -rf $RPM_BUILD_ROOT

install -Dpm 644 build/jmock-core-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/jmock-%{version}.jar
install -pm 644 build/jmock-cglib-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/jmock-cglib-%{version}.jar
install -pm 644 build/jmock-tests-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/jmock-tests-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

%add_to_maven_depmap %{name} %{name} %{version} JPP %{name}
%add_to_maven_depmap %{name} %{name}-cglib %{version} JPP %{name}-cglib

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 %{SOURCE1} \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}.pom
install -pm 644 %{SOURCE2} \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-cglib.pom

#
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/javadoc-%{version}/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
#
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
cp -pr examples/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}

%if %{gcj_support}
export CLASSPATH=$(build-classpath gnu-crypto)
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%post
%update_maven_depmap
%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(-,root,root,-)
%doc LICENSE.txt overview.html
%{_javadir}/*.jar
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}
%if %{gcj_support}
%dir %attr(-,root,root) %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}*%{version}.jar.*
%endif

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files demo
%defattr(-,root,root,-)
%doc %{_datadir}/%{name}-%{version}
