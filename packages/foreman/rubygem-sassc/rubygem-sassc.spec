# template: scl
%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}
%{!?_root_libdir:%global _root_libdir %{_libdir}}

%global gem_name sassc
%global gem_require_name %{gem_name}
%define debug_package %{nil}

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 2.2.1
Release: 2%{?dist}
Summary: Use libsass with Ruby!
Group: Development/Languages
License: MIT
URL: https://github.com/sass/sassc-ruby
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

# start specfile generated dependencies
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby >= 2.0.0
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(ffi) >= 1.9
Requires: %{?scl_prefix}rubygem(ffi) < 2
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}ruby-devel >= 2.0.0
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix}rubygem(ffi) >= 1.9
BuildRequires: %{?scl_prefix}rubygem(ffi) < 2
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}
# end specfile generated dependencies

BuildRequires: libsass
Requires: libsass

%description
Use libsass with Ruby!


%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

# disable building bundled libsass
sed -i "/s\.extensions/d" %{gem_name}.gemspec

%build
# use libsass.so.0 from host
sed -i "s/libsass\.\#{dl_ext}/libsass\.\#{dl_ext}\.0/" lib/sassc/native.rb
sed -i "/LoadError/,+1d" lib/sassc/native.rb
sed -i "s!__dir__!\"%{_root_libdir}\"!" lib/sassc/native.rb

# Create the gem as gem install only works on a gem file
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%{?scl:EOF}

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%{?scl:scl enable %{scl} - << \EOF}
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
%{?scl:scl enable %{scl} - << \EOF}
ruby -I "%{buildroot}%{gem_libdir}" -e "require '%{gem_require_name}'"
%{?scl:EOF}

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.gitmodules
%exclude %{gem_instdir}/.travis.yml
%license %{gem_instdir}/LICENSE.txt
%{gem_libdir}
%exclude %{gem_instdir}/ext
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CODE_OF_CONDUCT.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/sassc.gemspec
%{gem_instdir}/test

%changelog
* Fri Mar 27 2020 Ewoud Kohl van Wijngaarden <ewoud@kohlvanwijngaarden.nl> - 2.2.1-2
- Add check section to test native library

* Tue Jan 28 2020 Ondřej Ezr <oezr@redhat.com> 2.2.1-1
- Add rubygem-sassc generated by gem2rpm using the scl template

