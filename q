#!/bin/bash

if [[ -z $1 ]] ; then
  vi ${Q_SHORTCUTS_FILE-~/.q.yaml}
elif [[ $1 = "-c" || $1 = "--curl" ]] ; then
  shift && curl "http://q/$@"
else
  python -c "import webbrowser; webbrowser.open('http://q/$1')"
fi
