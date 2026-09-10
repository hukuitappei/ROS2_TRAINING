#!/usr/bin/env bash

# Load the ROS 2 underlay and this workspace overlay when it exists.
if [[ ! -f /opt/ros/jazzy/setup.bash ]]; then
  echo "ROS 2 Jazzy is not installed: /opt/ros/jazzy/setup.bash was not found." >&2
  return 1 2>/dev/null || exit 1
fi

source /opt/ros/jazzy/setup.bash

if [[ -f "${BASH_SOURCE[0]%/*}/install/setup.bash" ]]; then
  source "${BASH_SOURCE[0]%/*}/install/setup.bash"
fi
