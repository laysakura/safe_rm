#!/usr/bin/env python

import sys
import os
from optparse import OptionParser

def parse_args():
    usage = "usage: %prog [OPTION]... FILE..."
    parser = OptionParser(usage)
    parser.add_option("-v", "--verbose", dest="verbose",
                      action="store_true", default=False,
                      help="Same as `-v' of mv")
    parser.add_option("-f", "--force", dest="force",
                      action="store_true", default=False,
                      help="Same as `-f' of mv")
    parser.add_option("-r", "-R", "--recursive", dest="recursive",
                      action="store_true", default=False,
                      help="You need this option when you `remove' directories")
    (options, args) = parser.parse_args()
    return (args, options)

def gen_opt_for_mv(is_force, is_verbose):
    ret = ""
    if is_force:
        ret += " -f"
    if is_verbose:
        ret += " -v"
    return ret

def check_if_directory_is_in_list(l):
    for p in l:
        if os.path.isdir(os.path.expanduser(p)):
            return True
    return False

def check_and_create_trash_dir(trash_dir):
    if not os.path.exists(os.path.expanduser(trash_dir)):
        print("Creating " + trash_dir + " first...")
        os.system("mkdir -p " + trash_dir)

def srcs_list2srcs_str(srcs_list):
    ret = ""
    for src in srcs_list:
        ret += src + " "
    return ret

def exec_mv(srcs, destdir, option, is_recursive):
    has_src_directory = check_if_directory_is_in_list(srcs)
    srcs_str = srcs_list2srcs_str(srcs)

    if (not is_recursive) and has_src_directory:
        sys.stderr.write("You need to use `-r' when SOURCE has directories\n")
        exit(1)

    os.system("mv" + option + " " + srcs_str + " " + destdir)

def main():
    trash_dir = "~/.Trash"

    args, options = parse_args()
    opt_for_mv = gen_opt_for_mv(options.force, options.verbose)

    check_and_create_trash_dir(trash_dir)

    exec_mv(srcs=args, destdir=trash_dir,
            option=opt_for_mv, is_recursive=options.recursive)

if __name__ == '__main__':
    main()
