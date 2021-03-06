#!/bin/bash

# Wrapper script for calling the post-flash steps for Pluto factory testing
# Called with:  sudo ./postflash_pluto.sh
# Requires `sudo`
# Mostly used for testing

SCRIPT_DIR="$(readlink -f $(dirname $0))"

source $SCRIPT_DIR/config/pluto/postflash.sh

post_flash $@
