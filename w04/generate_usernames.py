#!/usr/bin/env python3
# Copyright (c) 2008-11 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version. It is provided for educational
# purposes and is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

import collections
import sys


ID, FORENAME, MIDDLENAME, SURNAME, DEPARTMENT = range(5)

User = collections.namedtuple("User",
            "username forename middlename surname id")


def main():
    if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
        print("usage: {0} file1 [file2 [... fileN]]".format(
              sys.argv[0]))
        sys.exit()

    usernames = set()
    users = {}
    for filename in sys.argv[1:]:
        for line in open(filename, encoding="utf8"):
            line = line.rstrip()
            if line:
                user = process_line(line, usernames)
                users[(user.surname.lower(), user.forename.lower(),
                       user.id)] = user
    print_users(users)


def process_line(line, usernames):
    fields = line.split(":")
    username = generate_username(fields, usernames)
    user = User(username, fields[FORENAME], fields[MIDDLENAME],
                fields[SURNAME], fields[ID])
    return user


def generate_username(fields, usernames):
    username = ((fields[FORENAME][0] + fields[MIDDLENAME][:1] +
                 fields[SURNAME]).replace("-", "").replace("'", ""))
    username = original_name = username[:8].lower()
    count = 1
    while username in usernames:
        username = "{0}{1}".format(original_name, count)
        count += 1
    usernames.add(username)
    return username


def print_users(users):
    namewidth = 24
    usernamewidth = 17

    # print("{0:<{nw}} {1:^6} {2:{uw}}".format(
    #       "Name", "ID", "Username", nw=namewidth, uw=usernamewidth))
    # print("{0:-<{nw}} {0:-<6} {0:-<{uw}}".format(
    #       "", nw=namewidth, uw=usernamewidth))

    print("{0:<{nw}} {1:^6} {2:{uw}}".format(
          "Name", "ID", "Username", nw=namewidth, uw=usernamewidth))
    print("{0:-<{nw}} {0:-<6} {0:-<{uw}}".format(
          "", nw=namewidth, uw=usernamewidth))

    count = 0;
    for key in sorted(users):
        count+=1
        user = users[key]
        initial = ""
        if count % 2 == 0:
            ender = "\n"
        else:
            ender = ""
        if user.middlename:
            initial = " " + user.middlename[0]
        name = "{u.forename}{i}, {u.surname}".format(u=user, i=initial)
        print("{u.username:<{uw}} ({u.id:4}) {n:>{nw}} ".format(
              n=name, u=user, nw=namewidth, uw=usernamewidth), end=ender)
        if count % 64 == 0:
            print("\n{0:<{uw}} {1:^6} {2:{nw}} {0:<{uw}} {1:^6} {2:{nw}}".format(
                "Username", "ID", "Name", nw=namewidth, uw=usernamewidth))
            print("{0:-<{uw}} {0:-<6} {0:-<{nw}} {0:-<{uw}} {0:-<6} {0:-<{nw}}".format(
                "", nw=namewidth, uw=usernamewidth))



main()