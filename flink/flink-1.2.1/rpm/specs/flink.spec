# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
%define flink_name flink
%define lib_flink /usr/lib/%{flink_name}
%define etc_flink /etc/%{flink_name}
%define etc_rcd /etc/rc.d
%define config_flink %{etc_flink}/conf
%define log_flink /var/log/%{flink_name}
%define run_flink /var/run/%{flink_name}
%define man_dir /usr/share/man
%define flink_user_home /var/lib/flink
%define rc_dir /etc/init.d

%define flink_version 1.2.1
%define hadoop_version 2.7.3
%define flink_base_version 1.2.1
%define flink_release 2.0.0%{?dist}

# Disable post hooks (brp-repack-jars, etc) that just take forever and sometimes cause issues
%define __os_install_post \
    %{!?__debug_package:/usr/lib/rpm/brp-strip %{__strip}} \
%{nil}
%define __jar_repack %{nil}
%define __prelink_undo_cmd %{nil}

# Disable debuginfo package, since we never need to gdb
# our own .sos anyway
%define debug_package %{nil}

%if  %{?suse_version:1}0
%define doc_flink %{_docdir}/flink
%define alternatives_cmd update-alternatives
%define alternatives_dep update-alternatives
%global initd_dir %{_sysconfdir}/rc.d
%else
%define doc_flink %{_docdir}/flink-%{flink_version}
%define alternatives_cmd alternatives
%define alternatives_dep chkconfig
%global initd_dir %{_sysconfdir}/rc.d/init.d
%endif

# disable repacking jars
%define __os_install_post %{nil}

Name: flink
Version: %{flink_version}
Release: %{flink_release}
Summary: Apache Flink is a fast and general engine for big data processing
URL: http://flink.apache.org
Vendor: Keedio
Packager: Alessio Comisso <acomisso@keedio.com>
Group: Development/Libraries
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
License: APL2
Source0: %{name}-%{version}-src.tgz
Source1: rpm-build-stage
Source2: install_%{name}.sh
BuildArch: noarch
BuildRequires: autoconf, automake
Requires(pre): coreutils, /usr/sbin/groupadd, /usr/sbin/useradd
Requires: redhat-lsb, hadoop-client, hadoop-yarn
%if  %{?suse_version:1}0
# Required for init scripts
Requires: insserv
%endif

%if  0%{?mgaversion}
# Required for init scripts
Requires: initscripts
%endif

%if %{!?suse_version:1}0 && %{!?mgaversion:1}0
# Required for init scripts
Requires: redhat-lsb
%endif

%description 
Apache Flink™ is an open source platform for distributed stream and batch data processing. 
    
%prep
%setup  %{name}-%{flink_base_version}.tgz 
#cd $RPM_SOURCE_DIR

%build
bash $RPM_SOURCE_DIR/rpm-build-stage
ls .

%install
%__rm -rf $RPM_BUILD_ROOT
sh $RPM_SOURCE_DIR/install_flink.sh \
          --build-dir=`pwd`         \
          --prefix=$RPM_BUILD_ROOT
%__install -d -m 0755 $RPM_BUILD_ROOT/%{initd_dir}/


%post
%{alternatives_cmd} --install /usr/lib/flink/default flink  /usr/lib/flink/%{name}-%{flink_base_version} 32

%preun
if [ "$1" = 0 ]; then
        %{alternatives_cmd} --remove flink  /usr/lib/flink/%{name}-%{flink_base_version}  || :
fi

#######################
#### FILES SECTION ####
#######################
%files 
%defattr(-,flink,hadoop,755)
/usr/lib/%{name}/*
%config(noreplace) /etc/%{name}/*
/var/log/%{name}
