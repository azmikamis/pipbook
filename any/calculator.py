#!/usr/bin/env python3
# Copyright © 2012-13 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version. It is provided for
# educational purposes and is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

import collections
import math
import sys


if sys.version_info >= (3, 3):
    import types

    def main():
        quit = "Ctrl+Z,Enter" if sys.platform.startswith("win") else "Ctrl+D"
        prompt = "Enter an expression ({} to quit): ".format(quit)
        current = types.SimpleNamespace(letter="A")
        globalContext = global_context()
        localContext = collections.OrderedDict()
        while True:
            try:
                expression = input(prompt)
                if expression:
                    calculate(expression, globalContext, localContext, current)
            except EOFError:
                print()
                break
else:
    def main():
        quit = "Ctrl+Z,Enter" if sys.platform.startswith("win") else "Ctrl+D"
        prompt = "Enter an expression ({} to quit): ".format(quit)
        current = type("_", (), dict(letter="A"))()
        globalContext = global_context()
        localContext = collections.OrderedDict()
        while True:
            try:
                expression = input(prompt)
                if expression:
                    calculate(expression, globalContext, localContext, current)
            except EOFError:
                print()
                break


def global_context():
    globalContext = globals().copy()
    for name in dir(math):
        if not name.startswith("_"):
            globalContext[name] = getattr(math, name)
    return globalContext


def calculate(expression, globalContext, localContext, current):
    try:
        result = eval(expression, globalContext, localContext)
        update(localContext, result, current)
        print(", ".join(["{}={}".format(variable, value)
                for variable, value in localContext.items()]))
        print("ANS={}".format(result))
    except Exception as err:
        print(err)


def update(localContext, result, current):
    localContext[current.letter] = result
    current.letter = chr(ord(current.letter) + 1)
    if current.letter > "Z": # We only support 26 variables
        current.letter = "A"


if __name__ == "__main__":
    main()
