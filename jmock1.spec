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

Summary:	Test Java code using mock objects
Name:		jmock1
Version:	1.2.0
Release:	7
Group:		Development/Java
License:	Open Source
Url:		http://jmock.codehaus.org/
Source0:	jmock-1.2.0.tar.gz
# svn export http://svn.codehaus.org/jmock/tags/1.2.0/ jmock-1.2.0
Source1:	jmock-1.2.0.pom
Source2:	jmock-cglib-1.2.0.pom
Patch0:		jmock-1.2.0-AssertMo.patch
Patch1:		jmock-1.2.0-build_xml.patch
Patch2:		jmock-asm_rename.patch
Patch3:		jmock-1.2.0-cglib2.2-asm3.patch
%if ! %{gcj_support}
BuildArch:	noarch
%endif
BuildRequires:	java-devel 
BuildRequires:	java-rpmbuild 
BuildRequires:	ant >= 0:1.6
BuildRequires:	ant-junit
BuildRequires:	junit >= 0:3.8.1
BuildRequires:	cglib
BuildRequires:	objectweb-asm
BuildRequires:	jaxp_parser_impl
Requires:	cglib
Requires:	objectweb-asm
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
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
Summary:	Javadoc for %{name}
Group:		Development/Java

%description    javadoc
%{summary}.

%package        demo
Summary:	Examples for %{name}
Group:		Development/Java

%description    demo
%{summary}.

%prep
%setup -qn jmock-%{version}
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
install -Dpm 644 build/jmock-core-%{version}.jar \
	%{buildroot}%{_javadir}/jmock-%{version}.jar
install -pm 644 build/jmock-cglib-%{version}.jar \
	%{buildroot}%{_javadir}/jmock-cglib-%{version}.jar
install -pm 644 build/jmock-tests-%{version}.jar \
	%{buildroot}%{_javadir}/jmock-tests-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

%add_to_maven_depmap %{maven_name} %{maven_name} %{version} JPP %{maven_name}
%add_to_maven_depmap %{maven_name} %{maven_name}-cglib %{version} JPP %{maven_name}-cglib

# poms
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -pm 644 %{SOURCE1} \
	%{buildroot}%{_datadir}/maven2/poms/JPP.%{maven_name}.pom
install -pm 644 %{SOURCE2} \
	%{buildroot}%{_datadir}/maven2/poms/JPP.%{maven_name}-cglib.pom

#
install -dm 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr build/javadoc-%{version}/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} 
#
install -dm 755 %{buildroot}%{_datadir}/%{name}-%{version}
cp -pr examples/* %{buildroot}%{_datadir}/%{name}-%{version}

%gcj_compile

%post
%update_maven_depmap
%if %{gcj_support}
%update_gcjdb
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%clean_gcjdb
%endif

%files
%doc LICENSE.txt overview.html
%{_javadir}/*.jar
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}
%{gcj_files}

%files javadoc
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files demo
%doc %{_datadir}/%{name}-%{version}

