#!/usr/bin/env bash

# Check if user is root
if [[ $EUID -ne 0 ]]; then
	echo "Script must be run as root"
	exit 1
fi
delim='!'

echo 'Enter the new password template:'
read -r passTemp
echo 'Confirm:'
read -r passConfirm

if [[ -z "$passTemp" ]] || [[ "$passTemp" != "$passConfirm" ]]; then
	echo 'Invalid new password'
	exit 2
fi

host=$(hostname)

for userDir in /home/*/; do
	user=$(echo "$userDir" | cut -d/ -f3)
	echo "Changing password for $user"
	newPass="$passTemp$delim$host$delim$user"
	echo -e "$newPass\\n$newPass" | passwd "$user"
done
