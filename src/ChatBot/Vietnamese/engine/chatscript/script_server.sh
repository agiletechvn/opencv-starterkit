#!/usr/bin/env bash
SCRIPT=./BINARIES/LinuxChatScript64
if [ "$(uname)" == "Darwin" ]; then
  SCRIPT=./BINARIES/MacChatScript
fi
$SCRIPT port=1024 language=VIETNAMESE login=anhv