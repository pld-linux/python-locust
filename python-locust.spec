# Conditional build:
%bcond_with	doc		# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module  (no python3-gevent)

%define 	module	locust
Summary:	Easy-to-use, distributed, user load www servers testing tool
Summary(pl.UTF-8):	Łatwe do użycia, rozproszone narzędzie do testowania obciążeniem serwerów www
Name:		python-%{module}
Version:	0.8
Release:	4
License:	MIT
Group:		Libraries/Python
Source0:	https://github.com/locustio/locust/archive/v%{version}.tar.gz
# Source0-md5:	7b821f11ebdd0e1bf70396d4571e887b
Patch0:		loose-ver.patch
URL:		http://locust.io/
BuildRequires:	rpm-pythonprov
# if py_postclean is used
BuildRequires:	rpmbuild(macros) >= 1.710
# when using /usr/bin/env or other in-place substitutions
#BuildRequires:	sed >= 4.0
%if %{with python2}
BuildRequires:	python-distribute
BuildRequires:	python-gevent >= 1.0.1
BuildRequires:	python-msgpack
%endif
%if %{with python3}
BuildRequires:	python3-gevent >= 1.0.1
BuildRequires:	python3-modules
BuildRequires:	python3-msgpack
%endif
# Below Rs only work for main package (python2)
#Requires:		python-libs
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Allows to define user behaviour with Python code, and swarm your
system with millions of simultaneous users.

%description -l pl.UTF-8
Pozwala na zdefiniowanie zachowań użytkowników w Pythonie i testować
wydajnościowo serwer www milionami równoczesnych użytkowników.

%package -n python3-%{module}
Summary:	Easy-to-use, distributed, user load www servers testing tool
Summary(pl.UTF-8):	Łatwe do użycia, rozproszone narzędzie do testowania obciążeniem serwerów www
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
Allows to define user behaviour with Python code, and swarm your
system with millions of simultaneous users.

%description -n python3-%{module} -l pl.UTF-8
Pozwala na zdefiniowanie zachowań użytkowników w Pythonie i testować
wydajnościowo serwer www milionami równoczesnych użytkowników.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
%if %{with python2}
## %py_build %{?with_tests:test}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
# 	build --build-base build-2 \
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

# in case there are examples provided
%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/locust
%doc README
%dir %{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}/*.py[co]
%dir %{py_sitescriptdir}/%{module}/rpc
%{py_sitescriptdir}/%{module}/rpc/*.py[co]
%{py_sitescriptdir}/%{module}/static
%{py_sitescriptdir}/%{module}/templates
%dir %{py_sitescriptdir}/%{module}/test
%{py_sitescriptdir}/%{module}/test/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/locustio-%{version}-py*.egg-info
%endif
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
