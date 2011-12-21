%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}


Summary: 	Bunch test organizer for Lettuce
Name:	 	python-bunch
Version: 	0.0.1
Release: 	1
Source0: 	%{name}-%{version}.tar.gz
License: 	GNU GPL v3+
Group: 		Development/Languages/Python
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: 	%{_prefix}
BuildArch: 	noarch
Url: 		http://github.com/TODO
BuildRequires:  python-setuptools, python-sphinx
Requires: 	python-lettuce, python-jinja2, PyYAML, python-nose

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

%install
mkdir -p %{buildroot}/%{_mandir}/man1
cp -p docs/_build/man/* %{buildroot}/%{_mandir}/man1

%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot} --single-version-externally-managed -O1  --record=INSTALLED_FILES

%clean
rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc %{_mandir}/man1/bunch.1.gz

%changelog
* Fri Dec 16 2011 skosyrev@griddynamics.com
- First package at version 0.0.1

