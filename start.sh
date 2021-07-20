#!/usr/bin/env bash
set -e

# SE GIRI CON ROOT SEI UN GRAN FARABOOT
grep "${RUNAS_GID}" /etc/group > /dev/null || addgroup -g "${RUNAS_GID}" "${RUNAS_GROUP}"
grep "${RUNAS_UID}" /etc/passwd > /dev/null || adduser -h /opt/arnaldo -S -u "${RUNAS_UID}" "${RUNAS_USER}"

# CHI NON CLONA È COMPLICE
chown -R "${RUNAS_USER}:${RUNAS_GROUP}" .
if [ ! -d ./.git ] ; then
    runuser -g $RUNAS_GROUP -m -u $RUNAS_USER -- git clone https://github.com/informateci/arnaldo.git .
    runuser -g $RUNAS_GROUP -m -u $RUNAS_USER -- git checkout python3
fi

exec runuser -g $RUNAS_GROUP -m -u $RUNAS_USER -- "$@"
