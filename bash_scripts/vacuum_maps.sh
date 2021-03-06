#!/bin/bash

HADIR="/config"

### You shouldn't touch anything below ###

LOCKFILE="/var/tmp/ha-rockrobo.lock"

# Exit if already locked
if [ -f ${LOCKFILE} ]; then
    [ -z "${2}" ] || logger -t map_to_ha "${1} process locked, exiting."
    exit 0
fi

NAVMAP="$(ls -t ${HADIR}/vacuum/navmap*.ppm | head -1)"
NAVMAP_SIZE="$(du ${NAVMAP} | cut -d$'\t' -f 1)"

# Exit if NAVMAP not yet completed (3076 bytes)
if ! [[ "$NAVMAP_SIZE" == 3076 ]]; then
    [ -z "${2}" ] || logger -t map_to_ha "${1} not yet completed, exiting."
    exit 0
fi

# Acquire lock
if ! [ -f ${LOCKFILE} ]; then
    [ -z "${2}" ] || logger -t map_to_ha "*** ${1} acquiring lock."
    touch ${LOCKFILE}
fi

# Process image
[ -z "${2}" ] || logger -t map_to_ha "${1} starting to render map."
python ${HADIR}/scripts/build_maps.py -map ${NAVMAP} -slam ${HADIR}/vacuum/SLAM_fprintf.log -out /images/vacuum_maps/latest.png
RES=$?

# Release lock
[ -z "${2}" ] || logger -t map_to_ha "*** ${1} release lock. (RESULT=${RES})"
rm -f ${LOCKFILE}
exit 0
