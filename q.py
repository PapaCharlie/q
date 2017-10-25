#!/usr/bin/python

import filelock
import os

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

SHORTCUTS_LOCK = filelock.FileLock(os.environ["SHORTCUTS_LOCK"])

class ShortcutFile(file):
    def __init__(self, mode='r', lock=SHORTCUTS_LOCK):
        super(ShortcutFile, self).__init__(os.environ["SHORTCUTS"], mode)
        self.__lock = lock

    def __enter__(self, *args, **kwargs):
        self.__lock.__enter__(*args, **kwargs)
        super(ShortcutFile, self).__enter__(*args, **kwargs)
        return self

    def __exit__(self, *args, **kwargs):
        super(ShortcutFile, self).__exit__(*args, **kwargs)
        self.__lock.__exit__(*args, **kwargs)


def not_found(start_response, message="Not Found"):
    start_response("404 Not Found", [])
    return iter([message])


def find_link(segments):
    with ShortcutFile() as f:
        last = load(f, Loader=Loader)
    for seg in segments:
        if seg in last:
            last = last[seg]
        else:
            return None
    if isinstance(last, dict):
        if '*' in last:
            return last['*']
        else:
            return None
    return last


def save_shortcut(segments, link):
    with ShortcutFile() as f:
        shortcuts = load(f, Loader=Loader)
    last = shortcuts
    for seg in segments[:-1]:
        if seg not in last:
            last[seg] = dict()
        last = last[seg]
    last[segments[-1]] = link
    with ShortcutFile('w') as f:
        dump(shortcuts, f, Dumper=Dumper, default_flow_style=False)


def read(environ, start_response):
    path = environ["PATH_INFO"]

    if "favicon" in path.lower():
        return not_found(start_response)

    if len(path.replace("/","")) == 0:
        with ShortcutFile() as f:
            return iter([f.read()])

    if path.startswith("/ "):
        query = path.split(" ")
        if len(query) != 3:
            raise Exception("asdasd")
        shortcut, link = query[1:]
        segments = [seg for seg in shortcut.split('/') if len(seg) > 0]
        save_shortcut(segments, link)
        return iter(["Added %s as `%s`"%(link, shortcut)])
    else:
        segments = [seg for seg in path.split('/') if len(seg) > 0]
        print segments
        res = find_link(segments)
        if res is None:
            return not_found(start_response, message="%s is not a known shortcut"%path)
        else:
            if not res.startswith("http"):
                res = "http://" + res
            start_response("307 Temporary Redirect", [("Content-type", "text/html"), ("Location", res)])
            return iter([res])
