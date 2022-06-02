#!/bin/bash

# THIS IS A REPLICA OF THE FILE ON TYRELL, THIS FILE IS FOR REFERENCE.
if [ $# -lt 1 ]; then
    echo "Syntax: $_ USER[ USER[ ...]]" >&2
    exit 1
fi

exit_code=0

for user in "$@"; do
    home="/nfshome/$user"

    # Check whether user account exists first
    USEREXISTS=$(getent passwd | grep ^$user:)
    if [ ! "$USEREXISTS" ]; then
	echo $'\e[31m'"User does not exist: $user"$'\e[m'
    elif [ -d "$home" ]; then
	echo $'\e[31m'"Home drive already exists: $home"$'\e[m'
    else
	group="students"
        cp -R /etc/skel "$home" && echo $'\e[32m'"Copied skeleton to: $home"$'\e[m' || ( exit_code=$?; echo $'\e[31m'"Failed to create: $home"$'\e[m' ) >&2
        chown -R "$user:$group" "$home" && echo $'\e[32m'"Set owner on: $home"$'\e[m' || ( exit_code=$?; echo $'\e[31m'"Failed to set owner on: $home"$'\e[m' ) >&2
    fi
done

exit $exit_code