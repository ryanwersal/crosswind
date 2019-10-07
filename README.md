# crosswind

## About

Crosswind is a library that attempts to allow arbitrary source traversal from either
Python 2 to 3 or Python 3 to 2. The intention is to enable teams to write modern Python
3 even if they have to support older versions of their software still using Python 2.

Crosswind is a fork of the [lib3to2 project that can be found on Bitbucket](http://bitbucket.org/amentajo/crosswind)
and [PyPi](https://pypi.python.org/pypi/crosswind). The source history has been ported from Mercurial to Git
using [hg-fast-export](https://github.com/frej/fast-export).

## Objectives/Goals

The following are the overarching objectives of crosswind. They are subject to change as
the a game plan is established. For now, they are tentatively:

- Support Python 2.7+ and Python 3.5+
- Tooling runs only in Python 3 interpreters
- Both conversion directions are supported equally
- Support latest versions of lib2to3

## Technical Objectives/Goals

- Use pipenv or poetry for project management
- Switch testing infrastructure to pytest instead of unittest
- Combine lib2to3 and/or [fissix](https://github.com/jreese/fissix)
- Get build automation running (Azure Pipelines or GitHub Actions)

## Usage

Run "./crosswind" to convert stdin ("-"), files or directories given as
arguments.  By default, the tool outputs a unified diff-formatted patch on
standard output and a "what was changed" summary on standard error, but the
"-w" option can be given to write back converted files, creating
".bak"-named backup files.

If you are root, you can also install with "./setup.py build" and
"./setup.py install" ("make install" does this for you).

This branch of crosswind must be run with Python 3.

To install locally (used for running tests as a non-privileged user), the
scripts assume you are using python3.1.  Modify accordingly if you are not.

## Thanks/Inspiration

Thanks to Joseph Amenta for developing lib3to2 and making it open source. This effort
wouldn't be possible without it!
