#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#2017-05-22
"""
Windows style:

applic.exe /f:12 /b:now yes, indeed  /G: 40 /M:light /1:"yes/no" /2 /poink:XX

...and fill it in a convenient dictionary which is returned
"""

# params - the command line itself, in full, without the app .exe name
# switch - the key character that 'starts' the switch
# param - the delimiter between the switch name and its value, if given
#         (if value is not given, have None in the value)
# escaper - which character to use for enclosing literals
# capswitches - whether to capitalize switch names on output

## Fish: straightforward and simple, but works for what I need


def parsecl(params, switch='/', paramdel=':', escaper='"', capswitches=True):

    result = {'': ''}
    newparam = False
    literal = False
    paramname = ''
    # Fill input string into "canisters"
    for order, char in enumerate(params):

        # Beginning a switch
        if char == switch and not literal:
            if newparam:
                result[paramname.strip()] = ''
                paramname = ''
            else:
                newparam = True
                paramname = ''

        # Switch value delimiter
        elif char == paramdel and not literal:
            newparam = False
            result[paramname] = ''

        # Check if literal
        elif char == escaper:
            literal = not literal

        # Nothing of the above, add to the current sequence
        else:
            if newparam:
                paramname += char
                if order == len(params) - 1:
                    result[paramname.strip()] = ''
            else:
                result[paramname.strip()] += char

    # Clean up
    for key in result.keys():
        result[key] = result[key].strip()
        if capswitches:
            result[key.upper()] = result.pop(key)

    return result
