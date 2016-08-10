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
#
# Hadoop RPM spec file
#

# FIXME: we need to disable a more strict checks on native files for now,
# since Hadoop build system makes it difficult to pass the kind of flags
# that would make newer RPM debuginfo generation scripts happy.
%undefine _missing_build_ids_terminate_build

%define hadoop_name hadoop
%define etc_hadoop /etc/%{name}
%define etc_yarn /etc/yarn
%define etc_httpfs /etc/%{name}-httpfs
%define config_hadoop %{etc_hadoop}/conf
%define config_yarn %{etc_yarn}/conf
%define config_httpfs %{etc_httpfs}/conf
%define config_kms /etc/hadoop-kms/conf
%define config_dist_kms /etc/hadoop-kms/conf.dist
%define lib_hadoop_dirname /usr/lib
%define lib_hadoop %{lib_hadoop_dirname}/%{name}
%define lib_httpfs %{lib_hadoop_dirname}/%{name}-httpfs
%define lib_kms %{lib_hadoop_dirname}/%{name}-kms
%define lib_hdfs %{lib_hadoop_dirname}/%{name}-hdfs
%define lib_yarn %{lib_hadoop_dirname}/%{name}-yarn
%define lib_mapreduce %{lib_hadoop_dirname}/%{name}-mapreduce
%define log_hadoop_dirname /var/log
%define log_hadoop %{log_hadoop_dirname}/%{name}
%define log_yarn %{log_hadoop_dirname}/%{name}-yarn
%define log_hdfs %{log_hadoop_dirname}/%{name}-hdfs
%define log_httpfs %{log_hadoop_dirname}/%{name}-httpfs
%define log_mapreduce %{log_hadoop_dirname}/%{name}-mapreduce
%define run_hadoop_dirname /var/run
%define run_hadoop %{run_hadoop_dirname}/hadoop
%define run_yarn %{run_hadoop_dirname}/%{name}-yarn
%define run_hdfs %{run_hadoop_dirname}/%{name}-hdfs
%define run_httpfs %{run_hadoop_dirname}/%{name}-httpfs
%define run_mapreduce %{run_hadoop_dirname}/%{name}-mapreduce
%define state_hadoop_dirname /var/lib
%define state_hadoop %{state_hadoop_dirname}/hadoop
%define state_yarn %{state_hadoop_dirname}/%{name}-yarn
%define state_hdfs %{state_hadoop_dirname}/%{name}-hdfs
%define state_mapreduce %{state_hadoop_dirname}/%{name}-mapreduce
%define state_nfs %{state_hadoop_dirname}/%{name}-nfs3
%define bin_hadoop %{_bindir}
%define man_hadoop %{_mandir}
%define src_hadoop /usr/src/%{name}
%define doc_hadoop %{_docdir}/%{name}-%{hadoop_version}
%define httpfs_services httpfs
%define mapreduce_services mapreduce-historyserver
%define hdfs_services hdfs-namenode hdfs-secondarynamenode hdfs-datanode hdfs-zkfc hdfs-journalnode 
%define yarn_services yarn-resourcemanager yarn-nodemanager yarn-proxyserver yarn-timelineserver
%define hadoop_services %{hdfs_services} %{mapreduce_services} %{yarn_services} %{httpfs_services}
# Hadoop outputs built binaries into %{hadoop_build}
%define hadoop_build_path build
%define static_images_dir src/webapps/static/images

%define hadoop_base_version 2.7.2
%define hadoop_release 1.4.0%{?dist}

%ifarch i386
%global hadoop_arch Linux-i386-32
%endif
%ifarch amd64 x86_64
%global hadoop_arch Linux-amd64-64
%endif

# CentOS 5 does not have any dist macro
# So I will suppose anything that is not Mageia or a SUSE will be a RHEL/CentOS/Fedora
%if %{!?suse_version:1}0 && %{!?mgaversion:1}0

# FIXME: brp-repack-jars uses unzip to expand jar files
# Unfortunately aspectjtools-1.6.5.jar pulled by ivy contains some files and directories without any read permission
# and make whole process to fail.
# So for now brp-repack-jars is being deactivated until this is fixed.
# See BIGTOP-294
%define __os_install_post \
    /usr/lib/rpm/redhat/brp-compress ; \
    /usr/lib/rpm/redhat/brp-strip-static-archive %{__strip} ; \
    /usr/lib/rpm/redhat/brp-strip-comment-note %{__strip} %{__objdump} ; \
    /usr/lib/rpm/brp-python-bytecompile ; \
    %{nil}

%define netcat_package nc
%define libexecdir %{_libexecdir}
%define doc_hadoop %{_docdir}/%{name}-%{hadoop_jar_version}
%define alternatives_cmd alternatives
%global initd_dir %{_sysconfdir}/rc.d/init.d
%endif


%if  %{?suse_version:1}0

# Only tested on openSUSE 11.4. le'ts update it for previous release when confirmed
%if 0%{suse_version} > 1130
%define suse_check \# Define an empty suse_check for compatibility with older sles
%endif

# Deactivating symlinks checks
%define __os_install_post \
    %{suse_check} ; \
    /usr/lib/rpm/brp-compress ; \
    %{nil}

%define netcat_package netcat-openbsd
%define libexecdir /usr/lib
%define doc_hadoop %{_docdir}/%{name}
%define alternatives_cmd update-alternatives
%global initd_dir %{_sysconfdir}/rc.d
%endif

%if  0%{?mgaversion}
%define netcat_package netcat-openbsd
%define libexecdir /usr/libexec/
%define doc_hadoop %{_docdir}/%{name}-%{hadoop_jar_version}
%define alternatives_cmd update-alternatives
%global initd_dir %{_sysconfdir}/rc.d/init.d
%endif


# Even though we split the RPM into arch and noarch, it still will build and install
# the entirety of hadoop. Defining this tells RPM not to fail the build
# when it notices that we didn't package most of the installed files.
%define _unpackaged_files_terminate_build 0

# RPM searches perl files for dependancies and this breaks for non packaged perl lib
# like thrift so disable this
%define _use_internal_dependency_generator 0

Name: hadoop
Version: %{hadoop_base_version}
Release: %{hadoop_release}
Summary: Hadoop is a software platform for processing vast amounts of data
License: Apache License v2.0
URL: http://hadoop.apache.org/core/
Vendor: Keedio 
Packager: Alessio Comisso <acomisso@keedio.org>
Group: Development/Libraries
Source0: %{name}-%{hadoop_base_version}-src.tar.gz 
Source1: rpm-build-stage
Source2: install_%{name}.sh
Source3: hadoop.default
Source4: hadoop-fuse.default
Source5: httpfs.default
Source6: hadoop.1
Source7: hadoop-fuse-dfs.1
Source8: hdfs.conf
Source9: yarn.conf
Source10: mapreduce.conf
Source11: init.d.tmpl 
Source12: hadoop-hdfs-namenode.svc
Source13: hadoop-hdfs-datanode.svc
Source14: hadoop-hdfs-secondarynamenode.svc
Source15: hadoop-mapreduce-historyserver.svc
Source16: hadoop-yarn-resourcemanager.svc
Source17: hadoop-yarn-nodemanager.svc
Source18: hadoop-httpfs.svc
Source19: mapreduce.default
Source20: hdfs.default
Source21: yarn.default
Source22: hadoop-layout.sh
Source23: hadoop-hdfs-zkfc.svc
Source24: hadoop-hdfs-journalnode.svc
Source25: hadoop-hdfs-nfs3.default 
Source26: hadoop-hdfs-nfs3
Source27: hadoop-yarn-timelineserver.svc

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id} -u -n)

BuildRequires: fuse-devel, fuse, cmake
Requires: coreutils, /usr/sbin/useradd, /usr/sbin/usermod, /sbin/chkconfig, /sbin/service, zookeeper >= 3.4.0

Requires: psmisc, %{netcat_package}
# Sadly, Sun/Oracle JDK in RPM form doesn't provide libjvm.so, which means we have
# to set AutoReq to no in order to minimize confusion. Not ideal, but seems to work.
# I wish there was a way to disable just one auto dependency (libjvm.so)
AutoReq: no

%if  %{?suse_version:1}0
BuildRequires: pkg-config, libfuse2, libopenssl-devel, gcc-c++
# Required for init scripts
Requires: sh-utils, insserv
%endif

# CentOS 5 does not have any dist macro
# So I will suppose anything that is not Mageia or a SUSE will be a RHEL/CentOS/Fedora
%if %{!?suse_version:1}0 && %{!?mgaversion:1}0
BuildRequires: pkgconfig, fuse-libs, redhat-rpm-config, lzo-devel, openssl-devel
# Required for init scripts
Requires: sh-utils, redhat-lsb
%endif

%if  0%{?mgaversion}
BuildRequires: pkgconfig, libfuse-devel, libfuse2 , libopenssl-devel, gcc-c++, liblzo-devel, zlib-devel
Requires: chkconfig, xinetd-simple-services, zlib, initscripts
%endif


%description
Hadoop is a software platform that lets one easily write and
run applications that process vast amounts of data.

Here's what makes Hadoop especially useful:
* Scalable: Hadoop can reliably store and process petabytes.
* Economical: It distributes the data and processing across clusters
              of commonly available computers. These clusters can number
              into the thousands of nodes.
* Efficient: By distributing the data, Hadoop can process it in parallel
             on the nodes where the data is located. This makes it
             extremely rapid.
* Reliable: Hadoop automatically maintains multiple copies of data and
            automatically redeploys computing tasks based on failures.

Hadoop implements MapReduce, using the Hadoop Distributed File System (HDFS).
MapReduce divides applications into many small blocks of work. HDFS creates
multiple replicas of data blocks for reliability, placing them on compute
nodes around the cluster. MapReduce can then process the data where it is
located.

%package hdfs
Summary: The Hadoop Distributed File System
Group: System/Daemons
Requires: %{name} = %{version}-%{release}

%description hdfs
Hadoop Distributed File System (HDFS) is the primary storage system used by 
Hadoop applications. HDFS creates multiple replicas of data blocks and distributes 
them on compute nodes throughout a cluster to enable reliable, extremely rapid 
computations.

%package yarn
Summary: The Hadoop NextGen MapReduce (YARN)
Group: System/Daemons
Requires: %{name} = %{version}-%{release}

%description yarn
YARN (Hadoop NextGen MapReduce) is a general purpose data-computation framework.
The fundamental idea of YARN is to split up the two major functionalities of the 
JobTracker, resource management and job scheduling/monitoring, into separate daemons:
ResourceManager and NodeManager.

The ResourceManager is the ultimate authority that arbitrates resources among all 
the applications in the system. The NodeManager is a per-node slave managing allocation
of computational resources on a single node. Both work in support of per-application 
ApplicationMaster (AM).

An ApplicationMaster is, in effect, a framework specific library and is tasked with 
negotiating resources from the ResourceManager and working with the NodeManager(s) to 
execute and monitor the tasks. 


%package mapreduce
Summary: The Hadoop MapReduce (MRv2)
Group: System/Daemons
Requires: %{name}-yarn = %{version}-%{release}

%description mapreduce


%package hdfs-namenode
Summary: The Hadoop namenode manages the block locations of HDFS files
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}

%description hdfs-namenode
The Hadoop Distributed Filesystem (HDFS) requires one unique server, the
namenode, which manages the block locations of files on the filesystem.

%package hdfs-nfs3
Summary: NFS3 gateway for HDFS
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}

%description hdfs-nfs3
The NFS Gateway supports NFSv3 and allows HDFS to be mounted as part of the client's local file system. Currently NFS Gateway supports and enables the following usage patterns:
Users can browse the HDFS file system through their local file system on NFSv3 client compatible operating systems.
Users can download files from the the HDFS file system on to their local file system.
Users can upload files from their local file system directly to the HDFS file system.
Users can stream data directly to HDFS through the mount point. File append is supported but random write is not supported.
The NFS gateway machine needs the same thing to run an HDFS client like Hadoop JAR files, HADOOP_CONF directory. The NFS gateway can be on the same host as DataNode, NameNode, or any HDFS client.


%package hdfs-secondarynamenode
Summary: Hadoop Secondary namenode
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires(pre): %{name}-hdfs = %{version}-%{release} 

%description hdfs-secondarynamenode
The Secondary Name Node periodically compacts the Name Node EditLog
into a checkpoint.  This compaction ensures that Name Node restarts
do not incur unnecessary downtime.

%package hdfs-zkfc
Summary: Hadoop HDFS failover controller
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires(pre): %{name}-hdfs = %{version}-%{release}

%description hdfs-zkfc
The Hadoop HDFS failover controller is a ZooKeeper client which also
monitors and manages the state of the NameNode. Each of the machines
which runs a NameNode also runs a ZKFC, and that ZKFC is responsible
for: Health monitoring, ZooKeeper session management, ZooKeeper-based
election.

%package hdfs-journalnode                                               
Summary: Hadoop HDFS JournalNode
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}

%description hdfs-journalnode
The HDFS JournalNode is responsible for persisting NameNode edit logs.
In a typical deployment the JournalNode daemon runs on at least three
separate machines in the cluster.

%package hdfs-datanode
Summary: Hadoop Data Node
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires(pre): %{name}-hdfs = %{version}-%{release}

%description hdfs-datanode
The Data Nodes in the Hadoop Cluster are responsible for serving up
blocks of data over the network to Hadoop Distributed Filesystem
(HDFS) clients.

%package httpfs
Summary: HTTPFS for Hadoop
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}, tomcat-server
Requires(pre): %{name} = %{version}-%{release}

%description httpfs
The server providing HTTP REST API support for the complete FileSystem/FileContext
interface in HDFS.

%package kms
Summary: Key storage manager 
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}, tomcat-server
Requires(pre): %{name} = %{version}-%{release}

%description kms
Hadoop KMS is a cryptographic key management server based on Hadoop's KeyProvider API. It provides a client which is a KeyProvider implementation that interacts with the KMS using the HTTP REST API. Both the KMS and its client support HTTP SPNEGO Kerberos authentication and SSL-secured communication. The KMS is a Java-based web application which runs using a pre-configured Tomcat server bundled with the Hadoop distribution.


%package kms-server
Summary: Key storage manager init scritps
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}, tomcat-server
Requires(pre): %{name} = %{version}-%{release}
Requires:%{name}-kms = %{version}-%{release}

%description kms-server
Hadoop KMS is a cryptographic key management server based on Hadoop's KeyProvider API. It provides a client which is a KeyProvider implementation that interacts with the KMS using the HTTP REST API. Both the KMS and its client support HTTP SPNEGO Kerberos authentication and SSL-secured communication. The KMS is a Java-based web application which runs using a pre-configured Tomcat server bundled with the Hadoop distribution.

%package yarn-resourcemanager
Summary: YARN Resource Manager
Group: System/Daemons
Requires: %{name}-yarn = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires(pre): %{name}-yarn = %{version}-%{release}

%description yarn-resourcemanager
The resource manager manages the global assignment of compute resources to applications

%package yarn-nodemanager
Summary: YARN Node Manager
Group: System/Daemons
Requires: %{name}-yarn = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires(pre): %{name}-yarn = %{version}-%{release}

%description yarn-nodemanager
The NodeManager is the per-machine framework agent who is responsible for
containers, monitoring their resource usage (cpu, memory, disk, network) and
reporting the same to the ResourceManager/Scheduler.

%package yarn-timelineserver
Summary: YARN Application Timeline Server
Group: System/Daemons
Requires: %{name}-yarn = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires(pre): %{name}-yarn = %{version}-%{release}

%description yarn-timelineserver
The Storage and retrieval of application’s current and historic information in a generic fashion is addressed in YARN through the Timeline Server.


%package yarn-proxyserver
Summary: YARN Web Proxy
Group: System/Daemons
Requires: %{name}-yarn = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires(pre): %{name}-yarn = %{version}-%{release}

%description yarn-proxyserver
The web proxy server sits in front of the YARN application master web UI.

%package mapreduce-historyserver
Summary: MapReduce History Server
Group: System/Daemons
Requires: %{name}-mapreduce = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}

%description mapreduce-historyserver
The History server keeps records of the different activities being performed on a Apache Hadoop cluster

%package client
Summary: Hadoop client side dependencies
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
Requires: %{name}-hdfs = %{version}-%{release}
Requires: %{name}-yarn = %{version}-%{release}
Requires: %{name}-mapreduce = %{version}-%{release}

%description client
Installation of this package will provide you with all the dependencies for Hadoop clients.

%package conf-pseudo
Summary: Pseudo-distributed Hadoop configuration
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
Requires: %{name}-hdfs-namenode = %{version}-%{release}
Requires: %{name}-hdfs-datanode = %{version}-%{release}
Requires: %{name}-hdfs-secondarynamenode = %{version}-%{release}
Requires: %{name}-yarn-resourcemanager = %{version}-%{release}
Requires: %{name}-yarn-nodemanager = %{version}-%{release}
Requires: %{name}-yarn-timelineserver = %{version}-%{release}
Requires: %{name}-mapreduce-historyserver = %{version}-%{release}

%description conf-pseudo
Contains configuration files for a "pseudo-distributed" Hadoop deployment.
In this mode, each of the hadoop components runs as a separate Java process,
but all on the same machine.

%package doc
Summary: Hadoop Documentation
Group: Documentation
%description doc
Documentation for Hadoop

%package source
Summary: Source code for Hadoop
Group: System/Daemons
AutoReq: no

%description source
The Java source code for Hadoop and its contributed packages. This is handy when
trying to debug programs that depend on Hadoop.

%package libhdfs
Summary: Hadoop Filesystem Library
Group: Development/Libraries
Requires: %{name}-hdfs = %{version}-%{release}
# TODO: reconcile libjvm
AutoReq: no

%description libhdfs
Hadoop Filesystem Library

%package libhdfs-devel                                                  
Summary: Development support for libhdfs
Group: Development/Libraries
Requires: hadoop = %{version}-%{release}, hadoop-libhdfs = %{version}-%{release}

%description libhdfs-devel
Includes examples and header files for accessing HDFS from C

%package hdfs-fuse
Summary: Mountable HDFS
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libhdfs = %{version}-%{release}
Requires: %{name}-client = %{version}-%{release}
Requires: fuse
AutoReq: no

%if %{?suse_version:1}0
Requires: libfuse2
%else
Requires: fuse-libs
%endif


%description hdfs-fuse
These projects (enumerated below) allow HDFS to be mounted (on most flavors of Unix) as a standard file system using


%prep
%setup -q -n %{name}-%{hadoop_base_version}-src 


%build
# This assumes that you installed Java JDK 6 and set JAVA_HOME
# This assumes that you installed Java JDK 5 and set JAVA5_HOME
# This assumes that you installed Forrest and set FORREST_HOME

env HADOOP_VERSION=%{hadoop_base_version} hadoop_jar_version=%{hadoop_jar_version} HADOOP_ARCH=%{hadoop_arch} bash %{SOURCE1}

%clean
%__rm -rf $RPM_BUILD_ROOT

#########################
#### INSTALL SECTION ####
#########################
%install
%__rm -rf $RPM_BUILD_ROOT

%__install -d -m 0755 $RPM_BUILD_ROOT/%{lib_hadoop}

bash %{SOURCE2} \
  --distro-dir=$RPM_SOURCE_DIR \
  --build-dir=$PWD/build \
  --src-dir=$RPM_BUILD_ROOT%{src_hadoop} \
  --httpfs-dir=$RPM_BUILD_ROOT%{lib_httpfs} \
  --system-include-dir=$RPM_BUILD_ROOT%{_includedir} \
  --system-lib-dir=$RPM_BUILD_ROOT%{_libdir} \
  --system-libexec-dir=$RPM_BUILD_ROOT/%{lib_hadoop}/libexec \
  --hadoop-etc-dir=$RPM_BUILD_ROOT%{etc_hadoop} \
  --httpfs-etc-dir=$RPM_BUILD_ROOT%{etc_httpfs} \
  --prefix=$RPM_BUILD_ROOT \
  --doc-dir=$RPM_BUILD_ROOT%{doc_hadoop} \
  --example-dir=$RPM_BUILD_ROOT%{doc_hadoop}/examples \
  --native-build-string=%{hadoop_arch} \
  --installed-lib-dir=%{lib_hadoop} \
  --man-dir=$RPM_BUILD_ROOT%{man_hadoop} \

# Forcing Zookeeper dependency to be on the packaged jar
%__ln_s -f /usr/lib/zookeeper/zookeeper.jar $RPM_BUILD_ROOT/%{lib_hadoop}/lib/zookeeper*.jar
# Workaround for BIGTOP-583
%__rm -f $RPM_BUILD_ROOT/%{lib_hadoop}-*/lib/slf4j-log4j12-*.jar

# Init.d scripts
%__install -d -m 0755 $RPM_BUILD_ROOT/%{initd_dir}/

# Install top level /etc/default files
%__install -d -m 0755 $RPM_BUILD_ROOT/etc/default
%__cp $RPM_SOURCE_DIR/hadoop.default $RPM_BUILD_ROOT/etc/default/hadoop
# FIXME: BIGTOP-463
#echo 'export JSVC_HOME=%{libexecdir}/bigtop-utils' >> $RPM_BUILD_ROOT/etc/default/hadoop
%__cp $RPM_SOURCE_DIR/%{name}-fuse.default $RPM_BUILD_ROOT/etc/default/%{name}-fuse
%__cp $RPM_SOURCE_DIR/%{name}-hdfs-nfs3.default $RPM_BUILD_ROOT/etc/default/%{name}-hdfs-nfs3
%__cp $RPM_SOURCE_DIR/%{name}-hdfs-nfs3 $RPM_BUILD_ROOT/%{initd_dir}/%{name}-hdfs-nfs3
%__cp $RPM_SOURCE_DIR/%{name}-kms.default   $RPM_BUILD_ROOT/etc/default/%{name}-kms
%__cp $RPM_SOURCE_DIR/%{name}-kms-server $RPM_BUILD_ROOT/%{initd_dir}/%{name}-kms-server
# Generate the init.d scripts
for service in %{hadoop_services}
do
       init_file=$RPM_BUILD_ROOT/%{initd_dir}/%{name}-${service}
       # On RedHat, SuSE and Mageia run-level 2 is networkless, hence excluding it
       env CHKCONFIG="345 85 15"       \
           INIT_DEFAULT_START="3 4 5"  \
           INIT_DEFAULT_STOP="0 1 2 6" \
         bash $RPM_SOURCE_DIR/init.d.tmpl $RPM_SOURCE_DIR/%{name}-${service}.svc > $init_file
       chmod 755 $init_file
       cp $RPM_SOURCE_DIR/${service/-*/}.default $RPM_BUILD_ROOT/etc/default/%{name}-${service}
       chmod 644 $RPM_BUILD_ROOT/etc/default/%{name}-${service}
done

# Install security limits
%__install -d -m 0755 $RPM_BUILD_ROOT/etc/security/limits.d
%__install -m 0644 %{SOURCE8} $RPM_BUILD_ROOT/etc/security/limits.d/hdfs.conf
%__install -m 0644 %{SOURCE9} $RPM_BUILD_ROOT/etc/security/limits.d/yarn.conf
%__install -m 0644 %{SOURCE10} $RPM_BUILD_ROOT/etc/security/limits.d/mapreduce.conf

# Install fuse default file
%__install -d -m 0755 $RPM_BUILD_ROOT/etc/default
%__cp %{SOURCE4} $RPM_BUILD_ROOT/etc/default/hadoop-fuse

# /var/lib/*/cache
%__install -d -m 1777 $RPM_BUILD_ROOT/%{state_yarn}/cache
%__install -d -m 1777 $RPM_BUILD_ROOT/%{state_hdfs}/cache
%__install -d -m 1777 $RPM_BUILD_ROOT/%{state_mapreduce}/cache
# /var/log/*
%__install -d -m 0775 $RPM_BUILD_ROOT/%{log_yarn}
%__install -d -m 0775 $RPM_BUILD_ROOT/%{log_hdfs}
%__install -d -m 0775 $RPM_BUILD_ROOT/%{log_mapreduce}
%__install -d -m 0775 $RPM_BUILD_ROOT/%{log_httpfs}
# /var/run/*
%__install -d -m 0775 $RPM_BUILD_ROOT/%{run_yarn}
%__install -d -m 0775 $RPM_BUILD_ROOT/%{run_hdfs}
%__install -d -m 0775 $RPM_BUILD_ROOT/%{run_mapreduce}
%__install -d -m 0775 $RPM_BUILD_ROOT/%{run_httpfs}

%pre
getent group hadoop >/dev/null || groupadd -r hadoop

%pre hdfs
getent group hdfs >/dev/null   || groupadd -r hdfs
getent passwd hdfs >/dev/null || /usr/sbin/useradd --comment "Hadoop HDFS" --shell /bin/bash -M -r -g hdfs -G hadoop --home %{state_hdfs} hdfs

%pre hdfs-nfs3

getent passwd nfsserver >/dev/null || /usr/sbin/useradd --comment "Hadoop HDFS NFS" --shell /bin/bash -M -r -g hdfs -G hadoop --home %{state_hdfs} nfsserver

%pre kms
getent group kms >/dev/null   || groupadd -r kms
getent passwd kms >/dev/null || /usr/sbin/useradd --comment "Hadoop KMS" --shell /bin/bash -M -r -g kms -G kms --home /var/lib/hadoop-kms kms


%pre httpfs 
getent group httpfs >/dev/null   || groupadd -r httpfs
getent passwd httpfs >/dev/null || /usr/sbin/useradd --comment "Hadoop HTTPFS" --shell /bin/bash -M -r -g httpfs -G hadoop --home %{run_httpfs} httpfs

%pre yarn
getent passwd yarn >/dev/null || /usr/sbin/useradd --comment "Hadoop Yarn" --shell /bin/bash -M -r -G hadoop --home %{state_yarn} yarn

%pre mapreduce
getent passwd mapred >/dev/null || /usr/sbin/useradd --comment "Hadoop MapReduce" --shell /bin/bash -M -r -G hadoop --home %{state_mapreduce} mapred

%post
/sbin/ldconfig
%{alternatives_cmd} --install %{config_hadoop} %{name}-conf %{etc_hadoop}/conf.empty 10

%post httpfs
%{alternatives_cmd} --install %{config_httpfs} %{name}-httpfs-conf %{etc_httpfs}/conf.empty 10
chkconfig --add %{name}-httpfs

%post kms 
alternatives --install /etc/hadoop-kms/conf hadoop-kms-conf /etc/hadoop-kms/conf.dist 10

%post kms-server
chkconfig --add %{name}-kms-server

%preun
if [ "$1" = 0 ]; then
  # Stop any services that might be running
  for service in %{hadoop_services}
  do
     service hadoop-$service stop 1>/dev/null 2>/dev/null || :
  done
  %{alternatives_cmd} --remove %{name}-conf %{etc_hadoop}/conf.empty || :
fi

%preun httpfs
if [ $1 = 0 ]; then
  service %{name}-httpfs stop > /dev/null 2>&1
  chkconfig --del %{name}-httpfs
  %{alternatives_cmd} --remove %{name}-httpfs-conf %{etc_httpfs}/conf.empty || :
fi

%preun kms 
if [ $1 = 0 ]; then
  alternatives --remove hadoop-kms-conf /etc/hadoop-kms/conf.dist || :
fi

%preun kms-server
if [ $1 = 0 ]; then
  service %{name}-kms-server stop > /dev/null 2>&1
  chkconfig --del {name}-kms-server
fi

%postun httpfs
if [ $1 -ge 1 ]; then
  service %{name}-httpfs condrestart >/dev/null 2>&1
fi

%postun kms-server 
if [ $1 -ge 1 ]; then
  service %{name}-kms-server condrestart >/dev/null 2>&1
fi


%files yarn
%defattr(-,root,root)
%config(noreplace) %{etc_hadoop}/conf.empty/yarn-env.sh
%config(noreplace) %{etc_hadoop}/conf.empty/yarn-site.xml
%config(noreplace) /etc/security/limits.d/yarn.conf
%{lib_hadoop}/libexec/yarn-config.sh
%{lib_yarn}
%attr(6050,root,yarn) %{lib_yarn}/bin/container-executor
%{bin_hadoop}/yarn
%attr(0775,yarn,hadoop) %{run_yarn}
%attr(0775,yarn,hadoop) %{log_yarn}
%attr(0755,yarn,hadoop) %{state_yarn}
%attr(1777,yarn,hadoop) %{state_yarn}/cache

%files hdfs
%defattr(-,root,root)
%config(noreplace) %{etc_hadoop}/conf.empty/hdfs-site.xml
%config(noreplace) /etc/default/hadoop-fuse
%config(noreplace) /etc/security/limits.d/hdfs.conf
%{lib_hdfs}
%{lib_hadoop}/libexec/hdfs-config.sh
%{bin_hadoop}/hdfs
%attr(0775,hdfs,hadoop) %{run_hdfs}
%attr(0775,hdfs,hadoop) %{log_hdfs}
%attr(0755,hdfs,hadoop) %{state_hdfs}
%attr(1777,hdfs,hadoop) %{state_hdfs}/cache

%files mapreduce
%defattr(-,root,root)
%config(noreplace) %{etc_hadoop}/conf.empty/mapred-site.xml
%config(noreplace) /etc/security/limits.d/mapreduce.conf
%{lib_mapreduce}
%{lib_hadoop}/libexec/mapred-config.sh
%{bin_hadoop}/mapred
%attr(0775,mapred,hadoop) %{run_mapreduce}
%attr(0775,mapred,hadoop) %{log_mapreduce}
%attr(0775,mapred,hadoop) %{state_mapreduce}
%attr(1777,mapred,hadoop) %{state_mapreduce}/cache


%files
%defattr(-,root,root)
/etc/profile.d/hadoop-env.sh
/etc/ld.so.conf.d/hadoop.sh
%config(noreplace) %{etc_hadoop}/conf.empty/core-site.xml
%config(noreplace) %{etc_hadoop}/conf.empty/hadoop-metrics.properties
%config(noreplace) %{etc_hadoop}/conf.empty/hadoop-metrics2.properties
%config(noreplace) %{etc_hadoop}/conf.empty/log4j.properties
%config(noreplace) %{etc_hadoop}/conf.empty/slaves
%config(noreplace) %{etc_hadoop}/conf.empty/ssl-client.xml.example
%config(noreplace) %{etc_hadoop}/conf.empty/ssl-server.xml.example
%config(noreplace) %{etc_hadoop}/conf.empty/capacity-scheduler.xml
%config(noreplace) %{etc_hadoop}/conf.empty/configuration.xsl
%config(noreplace) %{etc_hadoop}/conf.empty/container-executor.cfg
%config(noreplace) %{etc_hadoop}/conf.empty/hadoop-env.cmd
%config(noreplace) %{etc_hadoop}/conf.empty/hadoop-env.sh
%config(noreplace) %{etc_hadoop}/conf.empty/hadoop-policy.xml
%config(noreplace) %{etc_hadoop}/conf.empty/mapred-env.cmd
%config(noreplace) %{etc_hadoop}/conf.empty/mapred-env.sh
%config(noreplace) %{etc_hadoop}/conf.empty/mapred-queues.xml.template
%config(noreplace) %{etc_hadoop}/conf.empty/mapred-site.xml.template
%config(noreplace) %{etc_hadoop}/conf.empty/yarn-env.cmd
%config(noreplace) /etc/default/hadoop
/etc/bash_completion.d/hadoop
%{lib_hadoop}/*.jar
%{lib_hadoop}/lib
%{lib_hadoop}/sbin
%{lib_hadoop}/bin
%exclude %{lib_hadoop}/bin/fuse_dfs
%{lib_hadoop}/etc
%{lib_hadoop}/libexec/hadoop-config.sh
%{lib_hadoop}/libexec/hadoop-layout.sh
%{lib_hadoop}/libexec/hadoop-config.cmd
%{lib_hadoop}/libexec/hdfs-config.cmd
%{lib_hadoop}/libexec/mapred-config.cmd
%{lib_hadoop}/libexec/yarn-config.cmd
%{bin_hadoop}/hadoop
%{man_hadoop}/man1/hadoop.1.*

%files doc
%defattr(-,root,root)
%doc %{doc_hadoop}

%files source
%defattr(-,root,root)
%{src_hadoop}

%files httpfs
%defattr(-,root,root)
%config(noreplace) %{etc_httpfs}/conf.empty
%config(noreplace) /etc/default/%{name}-httpfs
%{lib_hadoop}/libexec/httpfs-config.sh
%{initd_dir}/%{name}-httpfs
%{lib_httpfs}
%attr(0775,httpfs,httpfs) %{run_httpfs}
%attr(0775,httpfs,httpfs) %{log_httpfs}

%files kms 
%defattr(-,root,root)
%config(noreplace) %{config_dist_kms}
%config(noreplace) /etc/default/%{name}-kms 
%{lib_hadoop}/libexec/kms-config.sh
%{lib_kms}
%{lib_kms}/sbin
%attr(0775,kms,kms) /var/lib/hadoop-kms 
%attr(0775,kms,kms) /var/log/hadoop-kms
%attr(0775,kms,kms) /var/run/hadoop-kms
%attr(0775,kms,kms) /var/run/hadoop-https

%files kms-server
%defattr(-,root,root)
%{initd_dir}/%{name}-kms-server

# Service file management RPMs
%define service_macro() \
%files %1 \
%defattr(-,root,root) \
%{initd_dir}/%{name}-%1 \
%config(noreplace) /etc/default/%{name}-%1 \
%post %1 \
chkconfig --add %{name}-%1 \
\
%preun %1 \
if [ $1 = 0 ]; then \
  service %{name}-%1 stop > /dev/null 2>&1 \
  chkconfig --del %{name}-%1 \
fi \
%postun %1 \
if [ $1 -ge 1 ]; then \
  service %{name}-%1 condrestart >/dev/null 2>&1 \
fi

%service_macro hdfs-namenode
%service_macro hdfs-secondarynamenode
%service_macro hdfs-zkfc
%service_macro hdfs-journalnode
%service_macro hdfs-datanode
%service_macro hdfs-nfs3
%service_macro yarn-resourcemanager
%service_macro yarn-nodemanager
%service_macro yarn-timelineserver
%service_macro yarn-proxyserver
%service_macro mapreduce-historyserver

# Pseudo-distributed Hadoop installation
%post conf-pseudo
%{alternatives_cmd} --install %{config_hadoop} %{name}-conf %{etc_hadoop}/conf.pseudo 30

%preun conf-pseudo
if [ "$1" = 0 ]; then
        %{alternatives_cmd} --remove %{name}-conf %{etc_hadoop}/conf.pseudo
        rm -f %{etc_hadoop}/conf
fi

%files conf-pseudo
%defattr(-,root,root)
%config(noreplace) %attr(755,root,root) %{etc_hadoop}/conf.pseudo

%files client
%defattr(-,root,root)
%{lib_hadoop}/client

%files libhdfs
%defattr(-,root,root)
%{_libdir}/libhdfs*

%files libhdfs-devel
%{_includedir}/hdfs.h
%{_includedir}/*.hh
# -devel should be its own package
#%doc %{_docdir}/libhdfs-%{hadoop_version}

%files hdfs-fuse
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) /etc/default/hadoop-fuse
%attr(0755,root,root) %{lib_hadoop}/bin/fuse_dfs
%attr(0755,root,root) %{bin_hadoop}/hadoop-fuse-dfs