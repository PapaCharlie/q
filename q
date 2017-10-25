#!/bin/bash

if [[ -z $1 ]] ; then
  vi ${Q_SHORTCUTS_FILE-~/.q.yaml}
else
  python -c "import webbrowser; webbrowser.open('http://q/$1')"
fi
