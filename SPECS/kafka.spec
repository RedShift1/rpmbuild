%define __jar_repack 0
%define debug_package %{nil}
%define _prefix      /usr/libexec
%define _conf_dir    %{_sysconfdir}/kafka
%define _log_dir     %{_var}/log/kafka
%define _data_dir    %{_sharedstatedir}/kafka

%{!?version:%global version 0.11.0.1}
%{!?build_number:%global build_number 1}
%{!?scala_version:%global scala_version 2.12}

Summary: Publish-subscribe messaging rethought as a distributed commit log
Name: kafka
Version: %{version}
Release: %{build_number}
License: ASL 2.0
URL: http://kafka.apache.org/
Source0: http://apache.belnet.be/kafka/%{version}/kafka_%{scala_version}-%{version}.tgz
Source1: kafka.service
Source2: kafka.logrotate
Source3: kafka.log4j.properties
Source4: kafka.sysconfig
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
# Prefix: %{_prefix}
Vendor: Apache Software Foundation
Packager: Ivan Dyachkov <ivan.dyachkov@klarna.com>
Provides: kafka-server
BuildRequires: systemd
%systemd_requires

%description
Kafka is designed to allow a single cluster to serve as the central data
backbone for a large organization. It can be elastically and transparently
expanded without downtime. Data streams are partitioned and spread over a
cluster of machines to allow data streams larger than the capability of any
single machine and to allow clusters of co-ordinated consumers. Messages are
persisted on disk and replicated within the cluster to prevent data loss.

%prep
%setup -q -n kafka_%{scala_version}-%{version}

%build
rm -f libs/{*-javadoc.jar,*-scaladoc.jar,*-sources.jar,*-test.jar}

%install
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}%{_prefix}/kafka/{libs,bin,config}
mkdir -p %{buildroot}%{_log_dir}
mkdir -p %{buildroot}%{_data_dir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_conf_dir}/
install -p -D -m 755 bin/*.sh %{buildroot}%{_prefix}/kafka/bin
install -p -D -m 644 config/* %{buildroot}%{_prefix}/kafka/config
install -p -D -m 644 config/server.properties %{buildroot}%{_conf_dir}/
sed -i "s:^log.dirs=.*:log.dirs=%{_data_dir}:" %{buildroot}%{_conf_dir}/server.properties
install -p -D -m 755 %{S:1} %{buildroot}%{_unitdir}/
install -p -D -m 644 %{S:2} %{buildroot}%{_sysconfdir}/logrotate.d/kafka
install -p -D -m 644 %{S:3} %{buildroot}%{_conf_dir}/log4j.properties
install -p -D -m 644 %{S:4} %{buildroot}%{_sysconfdir}/sysconfig/kafka
install -p -D -m 644 libs/* %{buildroot}%{_prefix}/kafka/libs
for b in %{buildroot}%{_prefix}/kafka/bin/{kafka,connect}*.sh
do
    ln -sf %{_prefix}/kafka/bin/$(basename ${b}) %{buildroot}/usr/bin/$(basename ${b})
done


%clean
rm -rf %{buildroot}

%pre
/usr/bin/getent group kafka >/dev/null || /usr/sbin/groupadd -r kafka
/usr/bin/getent passwd kafka >/dev/null || /usr/sbin/useradd -r \
  -g kafka -d %{_prefix}/kafka -s /bin/bash -c "Kafka" kafka
exit 0

%post
%systemd_post kafka.service

%preun
%systemd_preun kafka.service

%postun
%systemd_postun kafka.service

%files
%defattr(-,root,root)
%attr(0644,root,root) %{_unitdir}/kafka.service
%config(noreplace) %{_sysconfdir}/logrotate.d/kafka
%config(noreplace) %{_sysconfdir}/sysconfig/kafka
%config(noreplace) %{_conf_dir}/*
%{_prefix}/kafka
/usr/bin/*.sh
%attr(0755,kafka,kafka) %dir %{_log_dir}
%attr(0700,kafka,kafka) %dir %{_data_dir}
%doc NOTICE
%doc LICENSE


%changelog
* Sun Sep 24 2017 Glenn Matthys <glenn@webmind.be> - 0.11.0.1-1
- Removed plugins (should go in a seperate package)
- Changed prefix to /usr/libexec (packages mustn't touch /opt)
- Set default attributes on kafka.service unit file
- Move version numbers into spec file, lose makefile dependency
- Fix rpmlint warnings with regards to package summary & description
