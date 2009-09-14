"""
Main program for 3to2.
"""

import sys
import os
import difflib
import logging
import shutil
import optparse

from lib2to3 import refactor
from lib2to3 import pygram

def diff_texts(a, b, filename):
    """Return a unified diff of two strings."""
    a = a.splitlines()
    b = b.splitlines()
    return difflib.unified_diff(a, b, filename, filename,
                                "(original)", "(refactored)",
                                lineterm="")


class StdoutRefactoringTool(refactor.MultiprocessRefactoringTool):
    """
    Prints output to stdout.
    """

    def __init__(self, fixers, options, explicit, nobackups, show_diffs):
        self.nobackups = nobackups
        self.show_diffs = show_diffs
        super(StdoutRefactoringTool, self).__init__(fixers, options, explicit)
        self.driver.grammar = pygram.python_grammar_no_print_statement

    def refactor_string(self, data, name):
        """Override to keep print statements out of the grammar"""
        try:
            tree = self.driver.parse_string(data)
        except Exception, err:
            self.log_error("Can't parse %s: %s: %s",
                           name, err.__class__.__name__, err)
            return
        self.log_debug("Refactoring %s", name)
        self.refactor_tree(tree, name)
        return tree

    def log_error(self, msg, *args, **kwargs):
        self.errors.append((msg, args, kwargs))
        self.logger.error(msg, *args, **kwargs)

    def write_file(self, new_text, filename, old_text, encoding):
        if not self.nobackups:
            # Make backup
            backup = filename + ".bak"
            if os.path.lexists(backup):
                try:
                    os.remove(backup)
                except os.error as err:
                    self.log_message("Can't remove backup %s", backup)
            try:
                os.rename(filename, backup)
            except os.error as err:
                self.log_message("Can't rename %s to %s", filename, backup)
        # Actually write the new file
        write = super(StdoutRefactoringTool, self).write_file
        write(new_text, filename, old_text, encoding)
        if not self.nobackups:
            shutil.copymode(backup, filename)

    def print_output(self, old, new, filename, equal):
        if equal:
            self.log_message("No changes to %s", filename)
        else:
            self.log_message("Refactored %s", filename)
            if self.show_diffs:
                for line in diff_texts(old, new, filename):
                    print line


def warn(msg):
    print >> sys.stderr, "WARNING: %s" % (msg,)


def main(fixer_pkg, args=None):
    """Main program.

    Args:
        fixer_pkg: the name of a package where the fixers are located.
        args: optional; a list of command line arguments. If omitted,
              sys.argv[1:] is used.

    Returns a suggested exit status (0, 1, 2).
    """
    # Set up option parser
    parser = optparse.OptionParser(usage="3to2 [options] file|dir ...")
    parser.add_option("-d", "--doctests_only", action="store_true",
                      help="Fix up doctests only")
    parser.add_option("-f", "--fix", action="append", default=[],
                      help="Each FIX specifies a transformation; default: all")
    parser.add_option("-j", "--processes", action="store", default=1,
                      type="int", help="Run 3to2 concurrently")
    parser.add_option("-x", "--nofix", action="append", default=[],
                      help="Prevent a fixer from being run.")
    parser.add_option("-l", "--list-fixes", action="store_true",
                      help="List available transformations (fixes/fix_*.py)")
    parser.add_option("-v", "--verbose", action="store_true",
                      help="More verbose logging")
    parser.add_option("-w", "--write", action="store_true",
                      help="Write back modified files")
    parser.add_option("-n", "--nobackups", action="store_true", default=False,
                      help="Don't write backups for modified files.")
    parser.add_option("--no-diffs", action="store_true",
                      help="Don't show diffs of the refactoring")

    # Parse command line arguments
    refactor_stdin = False
    options, args = parser.parse_args(args)
    if not options.write and options.no_diffs:
        warn("not writing files and not printing diffs; that's not very useful")
    if not options.write and options.nobackups:
        parser.error("Can't use -n without -w")
    if options.list_fixes:
        print "Available transformations for the -f/--fix option:"
        for fixname in refactor.get_all_fix_names(fixer_pkg):
            print fixname
        if not args:
            return 0
    if not args:
        print >>sys.stderr, "At least one file or directory argument required."
        print >>sys.stderr, "Use --help to show usage."
        return 2
    if "-" in args:
        refactor_stdin = True
        if options.write:
            print >>sys.stderr, "Can't write to stdin."
            return 2

    # Set up logging handler
    level = logging.DEBUG if options.verbose else logging.INFO
    logging.basicConfig(format='%(name)s: %(message)s', level=level)

    # Initialize the refactoring tool
    avail_fixes = set(refactor.get_fixers_from_package(fixer_pkg))
    unwanted_fixes = set(fixer_pkg + ".fix_" + fix for fix in options.nofix)
    explicit = set()
    if options.fix:
        all_present = False
        for fix in options.fix:
            if fix == "all":
                all_present = True
            else:
                explicit.add(fixer_pkg + ".fix_" + fix)
        requested = avail_fixes.union(explicit) if all_present else explicit
    else:
        requested = avail_fixes.union(explicit)
    fixer_names = requested.difference(unwanted_fixes)
    rt = StdoutRefactoringTool(sorted(fixer_names), None, sorted(explicit),
                               options.nobackups, not options.no_diffs)

    # Refactor all files and directories passed as arguments
    if not rt.errors:
        if refactor_stdin:
            rt.refactor_stdin()
        else:
            try:
                rt.refactor(args, options.write, options.doctests_only,
                            options.processes)
            except refactor.MultiprocessingUnsupported:
                assert options.processes > 1
                print >>sys.stderr, \
                      "Sorry, -j isn't supported on this platform."
                return 1
        rt.summarize()

    # Return error status (0 if rt.errors is zero)
    return int(bool(rt.errors))
