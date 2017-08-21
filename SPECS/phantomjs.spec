%define debug_package %{nil}


Name:		phantomjs
Version:	2.1.1
Release:	1%{?dist}
Summary:	PhantomJS is a headless WebKit scriptable with a JavaScript API

License:	BSD
URL:		http://phantomjs.org/
Source0:	https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-%{version}-linux-x86_64.tar.bz2
Requires:	fontconfig



%description
PhantomJS is a headless WebKit scriptable with a JavaScript API. It has
fast and native support for various web standards: DOM handling,
CSS selector, JSON, Canvas, and SVG.


%prep
%setup -q -n phantomjs-2.1.1-linux-x86_64


%install

install -d %{buildroot}%{_bindir}
install -p -m 0755 bin/phantomjs %{buildroot}%{_bindir}/phantomjs

install -d %{buildroot}%{_docdir}
install -D -m 0644 README.md %{buildroot}%{_docdir}/README.md


%files
%{_bindir}/phantomjs
%doc %{_docdir}/README.md


%changelog

