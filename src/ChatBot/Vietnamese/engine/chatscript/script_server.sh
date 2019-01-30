#!/usr/bin/env bash
DIR="`dirname \"$0\"`/BINARIES"
SCRIPT=$DIR/LinuxChatScript64
if [ "$(uname)" == "Darwin" ]; then
  SCRIPT=$DIR/MacChatScript
fi
$SCRIPT port=1024 language=VIETNAMESE login=anhv