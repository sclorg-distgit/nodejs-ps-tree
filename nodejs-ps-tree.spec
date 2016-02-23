%{?scl:%scl_package nodejs-%{npm_name}}
%{!?scl:%global pkg_name %{name}}

%{?nodejs_find_provides_and_requires}
%global npm_name ps-tree

# Disable until dependencies are met
%global enable_tests 0

Summary:       Get all children of a pid.
Name:          %{?scl_prefix}nodejs-%{npm_name}
Version:       1.0.1
Release:       5%{?dist}
License:       MIT
URL:           https://github.com/indexzero/ps-tree
Source0:       http://registry.npmjs.org/%{npm_name}/-/%{npm_name}-%{version}.tgz
BuildRequires: %{?scl_prefix}runtime
ExclusiveArch: %{nodejs_arches} noarch
BuildArch:     noarch
Provides:      %{?scl_prefix}nodejs-%{npm_name} = %{version}

%if 0%{?enable_tests}
BuildRequires:  %{?scl_prefix}npm(chalk)
BuildRequires:  %{?scl_prefix}npm(istanbul)
BuildRequires:  %{?scl_prefix}npm(tape)
%endif

%description
Get all children of a pid.

%prep
%setup -q -n package

%nodejs_fixdep event-stream '>= 3.2.0'

%build

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pr bin index.js package.json %{buildroot}%{nodejs_sitelib}/%{npm_name}

mkdir -p %{buildroot}%{_bindir}
ln -sf %{nodejs_sitelib}/%{npm_name}/bin/ps-tree.js %{buildroot}%{_bindir}/ps-tree.js

%nodejs_symlink_deps

%if 0%{?enable_tests}

%check
%nodejs_symlink_deps --check
istanbul cover ./node_modules/.bin/tape ./test/test.js ./test/direct.js
%endif

%files
%doc README.md LICENSE
%{nodejs_sitelib}/%{npm_name}
%{_bindir}/ps-tree.js

%changelog
* Tue Feb 16 2016 Zuzana Svetlikova <zsvetlik@redhat.com> - 1.0.1-5
- Use macro in -runtime dependency

* Sun Feb 14 2016 Zuzana Svetlikova <zsvetlik@redhat.com> - 1.0.1-4
- Rebuilt with updated metapackage

* Wed Jan 06 2016 Tomas Hrcka <thrcka@redhat.com> - 1.0.1-3
- Enable scl macros

* Wed Dec 16 2015 Troy Dawson <tdawson@redhat.com> -1.0.1-1
- Initial package
