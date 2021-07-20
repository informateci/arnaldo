#!/usr/bin/env bash
set -e

# SE GIRI CON ROOT SEI UN GRAN FARABOOT
grep "${RUNAS_GID}" /etc/group > /dev/null || addgroup -g "${RUNAS_GID}" "${RUNAS_GROUP}"
grep "${RUNAS_UID}" /etc/passwd > /dev/null || adduser -S -u "${RUNAS_UID}" "${RUNAS_USER}"

# CHI NON CLONA È COMPLICE
if [ ! -d ./.git ] ; then
    chown -R "${RUNAS_USER}:${RUNAS_GROUP}" .
    git clone https://github.com/informateci/arnaldo.git .
    git checkout python3
fi

exec runuser -g $RUNAS_GROUP -m -u $RUNAS_USER -- "$@"
