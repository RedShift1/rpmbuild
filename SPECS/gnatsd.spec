Name:		gnatsd
Version:	1.0.2
Release:	1%{?dist}
Summary:	A High Performance NATS Server written in Go.

Group:		Messaging Server Support
License:	MIT
URL:		https://github.com/nats-io/gnatsd
Source0:	https://github.com/nats-io/gnatsd/releases/download/v1.0.2/gnatsd-v1.0.2-linux-amd64.zip
Source1:	gnatsd.service
Source2:    gnatsd.conf


BuildRequires:	zip

%description


%prep
unzip %{SOURCE0} > /dev/null
%setup -D -T -n gnatsd-v1.0.2-linux-amd64


%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sbindir}
install -D -m 0755 gnatsd %{buildroot}%{_sbindir}/gnatsd

mkdir -p %{buildroot}%{_unitdir}
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/

mkdir -p %{buildroot}%{_sysconfdir}
install -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/


%files
%{_sbindir}/gnatsd
%{_unitdir}/gnatsd.service
%{_sysconfdir}/gnatsd.conf


%clean
rm -rf %{buildroot}

%changelog

