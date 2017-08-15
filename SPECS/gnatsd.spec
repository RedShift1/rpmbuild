%define debug_package %{nil}


Name:		gnatsd
Version:	1.0.2
Release:	1%{?dist}
Summary:	A High Performance NATS Server written in Go

License:	MIT
URL:		https://github.com/nats-io/gnatsd
Source0:	https://github.com/nats-io/gnatsd/archive/v1.0.2.tar.gz
Source1:	gnatsd.service
Source2:    gnatsd.conf


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
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/

install -d %{buildroot}%{_sysconfdir}
install -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/


%pre
/bin/getent group gnatsd > /dev/null || /sbin/groupadd -r gnatsd
/bin/getent passwd gnatsd > /dev/null || /sbin/useradd -r -d / -s /sbin/nologin -g gnatsd gnatsd


%files
%{_sbindir}/gnatsd
%{_unitdir}/gnatsd.service
%config(noreplace) %{_sysconfdir}/gnatsd.conf



%changelog

