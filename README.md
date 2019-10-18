# crosswind

## About

Crosswind is a library that attempts to allow arbitrary source traversal from either
Python 2 to 3 or Python 3 to 2. The intention is to enable teams to write modern Python
3 even if they have to support older versions of their software still using Python 2.

Crosswind is a fork of the [lib3to2 project that can be found on Bitbucket](http://bitbucket.org/amentajo/lib3to2)
and [PyPi](https://pypi.python.org/pypi/crosswind). The source history has been ported from Mercurial to Git
using [hg-fast-export](https://github.com/frej/fast-export).

## Objectives/Goals

The following are the overarching objectives of crosswind. They are subject to change as
the a game plan is established. For now, they are tentatively:

- Support Python 2.7+ and Python 3.6+
- Tooling runs only in Python 3 interpreters
- Both conversion directions are supported equally
- Support latest versions of lib2to3

## Technical Objectives/Goals

- Use pipenv or poetry for project management
- Switch testing infrastructure to pytest instead of unittest
- Integrate lib2to3 from latest CPython and/or [fissix](https://github.com/jreese/fissix)
- Get build automation running (Azure Pipelines or GitHub Actions)
- Investigate/resolve [open issues on lib3to2](https://bitbucket.org/amentajo/lib3to2/issues?status=new&status=open)

## Development

Development uses the Poetry tool for managing dependencies and virtual environments. Common
development tasks have aliases that have been collected in a Makefile at the root of the
project.

To get started with crosswind development, run `make install`. This will use Poetry to create
the virtualenv and install the dependencies (both runtime and dev-time).

Then you can lint the code and run the tests with `make lint` and `make tests` or combine them
(since they're separate targets and make allows specifying many targets in a single invocation)
with `make lint tests` and so on.

Currently, running crosswind requires a manual invocation of poetry such as:

```shell
poetry run python crosswind/crosswind --help
```

This will show the help output containing the currently supported options. It should be noted that
the current state of the crosswind tool is that it only has access to the 2to3 fixers. Further efforts
are needed to allow it to combine arbitrary fixers and fixer suites.

## Thanks/Inspiration

Thanks to Joseph Amenta for developing lib3to2 and making it open source. This effort
wouldn't be possible without it!
