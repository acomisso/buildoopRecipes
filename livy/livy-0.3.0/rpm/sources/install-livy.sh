#!/bin/sh
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

set -ex

usage() {
  echo "
usage: $0 <options>
  Required not-so-options:
     --build-dir=DIR             path to flumedist.dir
     --prefix=PREFIX             path to install into

  Optional options:
     --doc-dir=DIR               path to install docs into [/usr/share/doc/flume]
     --lib-dir=DIR               path to install flume home [/usr/lib/flume]
     --bin-dir=DIR               path to install bins [/usr/bin]
     --examples-dir=DIR          path to install examples [doc-dir/examples]
     ... [ see source for more similar options ]
  "
  exit 1
}

OPTS=$(getopt \
  -n $0 \
  -o '' \
  -l 'prefix:' \
  -l 'doc-dir:' \
  -l 'lib-dir:' \
  -l 'bin-dir:' \
  -l 'examples-dir:' \
  -l 'build-dir:' -- "$@")

if [ $? != 0 ] ; then
    usage
fi

eval set -- "$OPTS"

while true ; do
    case "$1" in
        --prefix)
        PREFIX=$2 ; shift 2
        ;;
        --build-dir)
        BUILD_DIR=$2 ; shift 2
        ;;
        --doc-dir)
        DOC_DIR=$2 ; shift 2
        ;;
        --lib-dir)
        LIB_DIR=$2 ; shift 2
        ;;
        --bin-dir)
        BIN_DIR=$2 ; shift 2
        ;;
        --examples-dir)
        EXAMPLES_DIR=$2 ; shift 2
        ;;
        --)
        shift ; break
        ;;
        *)
        echo "Unknown option: $1"
        usage
        exit 1
        ;;
    esac
done

for var in PREFIX BUILD_DIR ; do
  if [ -z "$(eval "echo \$$var")" ]; then
    echo Missing param: $var
    usage
  fi
done

if [ -z "${JAVA_HOME}" ]; then
    echo Missing env. var JAVA_HOME
    usage
fi

LIVY_HOME=/usr/lib/livy
PLUGIN_LIB_DIR=${PLUGIN_DIR}/lib
PLUGIN_LIBEXT_DIR=${PLUGIN_DIR}/libext
FLUME_CONF=/etc/flume/conf

pwd
install -d -m 0755 ${PREFIX}/${LIVY_HOME}
install -d -m 0755 ${PREFIX}/var/log/livy
install -d -m 0755 ${PREFIX}/var/run/livy
install -d -m 0755 ${PREFIX}/etc/livy
install -d -m 0755 ${PREFIX}/etc/systemd/system
cp -Rpd ${BUILD_DIR}/* ${PREFIX}/${LIVY_HOME}/
mv  ${PREFIX}/${LIVY_HOME}/conf   ${PREFIX}/etc/livy/conf.dist
ln -s /etc/livy/conf.dist ${PREFIX}/etc/livy/conf
ln -s /etc/livy/conf  ${PREFIX}/${LIVY_HOME}/conf
cp ${RPM_SOURCE_DIR}/livy.service ${PREFIX}/etc/systemd/system/livy.service
cp ${RPM_SOURCE_DIR}/livy-env.sh ${PREFIX}/etc/livy/conf.dist/livy-env.sh

