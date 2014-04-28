#! /usr/bin/env python
# vim: set fileencoding=utf-8:

import re


def tdecode(byti):
    try:
        text = byti.decode('utf-8')
    except UnicodeDecodeError:
        try:
            text = byti.decode('iso-8859-1')
        except UnicodeDecodeError:
            text = byti.decode('cp1252')
    return text


def tencode(byti):
    try:
        text = byti.encode('utf-8')
    except UnicodeEncodeError:
        try:
            text = byti.encode('iso-8859-1')
        except UnicodeEncodeError:
            text = byti.encode('cp1252')
    return text


class BambaRosaNasaBuffer(object):  # decoda a naso. VIVA!
    line_sep_exp = re.compile(b'\r?\n')

    def __init__(self):
        self.buffer = b''

    def feed(self, bytes):
        self.buffer += bytes

    def __iter__(self):
        return self.lines()

    def __len__(self):
        return len(self.buffer)

    def lines(self):
        lines = self.line_sep_exp.split(self.buffer)
        # save the last, unfinished, possibly empty line
        self.buffer = lines.pop()
        for line in iter(lines):
            for encodi in [('utf-8', 'strict'),
                           ('latin-1', 'strict'),
                           ('utf-8', 'replace'),
                           ('utf-8', 'ignore')]: #tipo a tentativi ma peggio
                try:
                    l = line.decode(encodi[0], encodi[1])
                    break
                except:
                    l = ""
            yield l

