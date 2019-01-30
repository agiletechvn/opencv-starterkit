#!/usr/bin/env bash
SCRIPT=BINARIES/LinuxChatScript64
if [ "$(uname)" == "Darwin" ]; then
  SCRIPT=BINARIES/MacChatScript
fi
$SCRIPT language=VIETNAMESE local login=anhv