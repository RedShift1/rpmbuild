%define debug_package %{nil}


Name:		gnatsd
Version:	1.0.4
Release:	1%{?dist}
Summary:	A High Performance NATS Server written in Go

License:	MIT
URL:		https://github.com/nats-io/gnatsd
Source0:	https://github.com/nats-io/gnatsd/archive/v%{version}.tar.gz
Source2:    gnatsd.conf
Source3:	gnatsd.8


BuildRequires:	golang

Requires(pre):		/sbin/useradd, /bin/getent
Requires(postun):	/sbin/userdel


%description
NATS Server is a simple, high performance open source messaging system for
cloud native applications, IoT messaging, and microservices architectures.

%prep
%setup -q -n gnatsd-%{version}

%build
mkdir -p ./_build/src/github.com/nats-io
ln -s $(pwd) ./_build/src/github.com/nats-io/gnatsd

export GOPATH=$(pwd)/_build:%{gopath}
go build -ldflags="-s -w" -o gnatsd .


%install

install -d %{buildroot}%{_sbindir}
install -p -m 0755 ./gnatsd %{buildroot}%{_sbindir}/gnatsd

install -d %{buildroot}%{_unitdir}
install -D -m 0644 util/gnatsd.service %{buildroot}%{_unitdir}/

install -d %{buildroot}%{_sysconfdir}
install -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/

install -d %{buildroot}%{_docdir}
install -D -m 0644 README.md %{buildroot}%{_docdir}/gnatsd/README.md

install -d %{buildroot}%{_mandir}/man8
install -D -m 0644 %{SOURCE3} %{buildroot}%{_mandir}/man8/gnatsd.8


%pre
/bin/getent group gnatsd > /dev/null || /sbin/groupadd -r gnatsd
/bin/getent passwd gnatsd > /dev/null || /sbin/useradd -r -d / -s /sbin/nologin -g gnatsd gnatsd

%preun
if [[ $1 -eq 0 ]]
then
    service gnatsd stop
fi

%files
%{_sbindir}/gnatsd
%{_unitdir}/gnatsd.service
%{_mandir}/man8/gnatsd.8*
%config(noreplace) %{_sysconfdir}/gnatsd.conf
%doc %{_docdir}/gnatsd/README.md


%changelog

