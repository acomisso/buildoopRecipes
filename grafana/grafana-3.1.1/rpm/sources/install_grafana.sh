#!/bin/bash -x
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

# Check Usage
usage() {
  echo "
usage: $0 <options>
  Required not-so-options:
     --prefix=PREFIX             path to install into
  "
  exit 1
}

#check opts
OPTS=$(getopt \
  -n $0 \
  -o '' \
  -l 'prefix:' \
  -l 'build-dir:' \
  -- "$@")

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

for var in PREFIX BUILD_DIR; do
  if [ -z "$(eval "echo \$$var")" ]; then
    echo Missing param: $var
    usage
  fi
done

GRAFANA_HOME=${PREFIX}/usr/lib/grafana

install -d -m 755 ${GRAFANA_HOME}
install -d -m 755 ${PREFIX}/etc/init.d
install -d -m 755 ${PREFIX}/etc/sysconfig
install -d -m 755 ${PREFIX}/etc/grafana
install -d -m 755 ${PREFIX}/var/lib/grafana
install -d -m 755 ${PREFIX}/var/log/grafana

cp -Rpd ${BUILD_DIR}/grafana/src/github.com/grafana/grafana/bin ${GRAFANA_HOME}
cp -Rpd ${BUILD_DIR}/grafana/src/github.com/grafana/grafana/conf ${GRAFANA_HOME}
cp -Rpd ${BUILD_DIR}/grafana/src/github.com/grafana/grafana/vendor ${GRAFANA_HOME}
cp -Rpd ${BUILD_DIR}/grafana/src/github.com/grafana/grafana/public ${GRAFANA_HOME}
cp -Rpd ${BUILD_DIR}/grafana/src/github.com/grafana/grafana/public_gen ${GRAFANA_HOME}
f2qfg3	gtf
ln -s /etc/grfana/conf.dist ${PREFIX}/etc/grafana/conf
ln -s /usr/lib/grafana/conf  ${PREFIX}/etc/grafana/conf.dist
