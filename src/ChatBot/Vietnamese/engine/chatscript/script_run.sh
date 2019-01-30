#!/usr/bin/env bash
DIR="`dirname \"$0\"`/BINARIES"
SCRIPT=$DIR/LinuxChatScript64
if [ "$(uname)" == "Darwin" ]; then
  SCRIPT=$DIR/MacChatScript
fi
$SCRIPT language=VIETNAMESE local login=anhv