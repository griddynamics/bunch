%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}


Summary: 	Bunch test organizer for Lettuce
Name:	 	python-lettuce-bunch
Version: 	0.2.0
Release: 	1
Source0: 	%{name}-%{version}.tar.gz
License: 	GNU GPL v3+
Group: 		Development/Languages/Python
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: 	%{_prefix}
BuildArch: 	noarch
Url: 		http://github.com/TODO
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-lettuce > 0.1.34-b2167
BuildRequires:  python-jinja2
BuildRequires:  PyYAML
BuildRequires:  python-nose
Requires: 	python-lettuce > 0.1.34-b2167
Requires:       python-jinja2
Requires:       PyYAML
Requires:       python-nose
Requires:       python-anyjson
Requires:       python-lxml
Obsoletes:      python-bunch < 0.0.1-1

%description
Bunch is tool for grouping, managing and running Lettuce scenarios. It offers explicit separation of test fixtures from test scenarios by dividing it into setup, teardown and test scripts. Bunch encourages writing clean, self-sufficient and multi-environment tests, which can be executed in parallel. It also provides more flexibility for test parameterization - test scenarios are treated as templates, which get parameterized upon execution.

Authors:
---------
    Sergey Kosyrev <kosyrevss@gmail.com>

    Alexander Petrovich <apetrovich@griddynamics.com>



%prep
%setup -q -n %{name}-%{version}

%build
cd docs
make man
cd ../

%{__python} setup.py build

%check
make check

%install
mkdir -p %{buildroot}/%{_mandir}/man1
cp -p docs/_build/man/* %{buildroot}/%{_mandir}/man1
ln -sf %{_mandir}/man1/lettuce_bunch.1.gz %{buildroot}/%{_mandir}/man1/bunch.1.gz

%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot} --single-version-externally-managed -O1  --record=INSTALLED_FILES

%clean
rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc %{_mandir}/man1/bunch.1.gz
%doc %{_mandir}/man1/lettuce_bunch.1.gz

%changelog
* Tue Apr 17 2012 skosyrev@griddynamics.com
- Increased version to 0.2.0
- Added HTML reports and output plugin infrastructure
- Some minor bugfixes
* Thu Mar 1 2012 skosyrev@griddynamics.com
- Renamed package to lettuce_bunch. Increased version to 0.1.0
* Thu Feb 16 2012 skosyrev@griddynamics.com
- Increased version to 0.0.2
- Changed default fixture logic. Now they are executed along with test. Common dependency fixtures are executed before and after all tests
* Fri Dec 16 2011 skosyrev@griddynamics.com
- First package at version 0.0.1
