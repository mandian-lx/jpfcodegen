%{?_javapackages_macros:%_javapackages_macros}

Summary:	Code generator for JabRef's plugins 
Name:		jpfcodegen
Version:	0.4
Release:	1
License:	LGPLv3
Group:		Development/Java
URL:		http://jabref.sourceforge.net/
# svn export https://jabref.svn.sourceforge.net/svnroot/jabref/tags/jpfcodegen-0.4
# tar cvJf jpfcodegen-0.4.tar.xz jpfcodegen-0.4
Source0:	%{name}-%{version}.tar.xz
# Fix the build to use system jars
Patch0:	 %{name}-0.4-build.patch
BuildArch:	noarch

BuildRequires:	ant
BuildRequires:	jpackage-utils
BuildRequires:	mvn(commons-logging:commons-logging)
BuildRequires:	mvn(net.sf.jpf:jpf)
BuildRequires:	mvn(net.sf.jpf:jpf-boot)
BuildRequires:	mvn(org.apache.velocity:velocity)

Requires:	java-headless
Requires:	jpackage-utils
Requires:	mvn(net.sf.jpf:jpf)
Requires:	mvn(net.sf.jpf:jpf-boot)

%description
JPF Code Generator is a handy little tool that generates classes for
accessing the attributes and extensions of JPF plug-ins from plugin.xml
files. This has the advantage of providing a strongly typed access to the
plug-in and simplifies working with plug-ins.

%files
%{_javadir}/*.jar
%doc index.html
%doc resources/
%doc tutorials/
%doc lgpl-3.0.txt

#----------------------------------------------------------------------------

%package	javadoc
Summary:	Javadoc for %{name}

%description javadoc
API documentation for JPF Code Generator.

%files javadoc
%{_javadocdir}/%{name}
%doc lgpl-3.0.txt

#----------------------------------------------------------------------------

%prep
%setup -q

# Delete all pre-built binaries
find . -name "*.jar" -delete
find . -name "*.class" -delete

# apply the patch
%patch0 -p1 -b .orig

# fix jar-not-indexed warning
sed -i -e 's|<jar |<jar index="true" |g' build.xml

%build
export CLASSPATH=`build-classpath jpf jpf-boot commons-logging velocity`
%ant jars

# javadoc
%javadoc -d doc src/net/sf/jabref/plugin/util/*.java

%install
# jars
install -dm 0755 %{buildroot}%{_javadir}/
install -pm 0644 JPFCodeGenerator-0.4.jar %{buildroot}%{_javadir}/%{name}.jar
install -pm 0644 JPFCodeGenerator-0.4-rt.jar %{buildroot}%{_javadir}/%{name}-rt.jar

# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}/
cp -pr doc/* %{buildroot}%{_javadocdir}/%{name}/

