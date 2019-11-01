# crosswind

## About

Crosswind is a tool and library that is looking to enable easy conversion of a codebase from Python 2
to 3 and back. The intention is to enable teams to write modern Python 3 even if they have to support
older versions of their software still using Python 2. Crosswind also aims to provide a means to write
arbitrary large-scale refactoring that can be applied to a codebase in much the same way as the 2to3
or 3to2 migration.

Crosswind is a fork of the [lib3to2 project that can be found on Bitbucket](http://bitbucket.org/amentajo/lib3to2)
and [PyPi](https://pypi.python.org/pypi/crosswind). The source history has been ported from Mercurial to Git
using [hg-fast-export](https://github.com/frej/fast-export).

lib2to3 was also ported over from [the Python project](https://github.com/python/cpython/).

## Objectives/Goals

The following are the overarching objectives of crosswind. They are subject to change as
a game plan is established. For now, they are:

- Support _only_ Python 2.7 for backporting 3 to 2
- Support upgrading to 3.6 and above whem migrating 2 to 3
- Running all tooling is only supported on 3.6 and up
- Reach and maintain parity between the `two_to_three` and `three_to_two` fixer suites
- Consistently pull in upstream updates for both `lib2to3` and `lib3to2` when it aligns with the above goals
- Investigate/resolve [open issues on lib3to2](https://bitbucket.org/amentajo/lib3to2/issues?status=new&status=open)

## Contributing

If you're looking for ways to contribute there are a few options to choose from:

- Helping write wiki pages with more knowledge of all facets of writing fixers or tests or understanding the pgen/lib2to3 libraries/APIs
- Try out Crosswind on your codebase and open issues for things you suspect aren't coming out quite right (please include code samples!)
- Submit a pull request with a fix or enhancement (it would be ideal to open an issue first for discussion)

You can start by taking a look at the [Writing a Fixer](https://github.com/ryanwersal/crosswind/wiki/Writing-a-Fixer) wiki
page to learn about what goes into the fixer and its tests.

## Development

Crosswind uses the Poetry tool for managing dependencies and virtual environments. Common
development tasks have aliases that have been collected in a Makefile at the root of the
project.

To get started with crosswind development, run `make install`. This will use Poetry to create
the virtualenv and install the dependencies (both runtime and dev-time). Note that you need your
currently active python to be compatible with the versions in the `pyproject.toml` file. If that
isn't the case, you'll have to manage the virtualenv creation yourself. For example, by executing
the following in your checkout of Crosswind:

```bash
python3 -m virtualenv .venv
```

If you don't yet have virtualenv available you can get it via pip: `python3 -m pip install virtualenv`.
Once you have the virtualenv created you will need to activate it before continuing.

WIth the virtualenv created you can then proceed to `make install` to have Poetry download and install
dependencies into your activated venv.

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

## Configuration

In addition to passing flags at the command line (issue `--help` to crosswind for available flags) you can
configure crosswind by defining such configuration in `pyproject.toml` under a `tool.crosswind` heading such
as:

```toml
[tool.croswind]
output_dir = "path/to/output"
```

Additionally, presets can be defined by adding `.preset.<name>` as an additional heading like:

```toml
[tool.crosswind.preset.foo]
output_dir = "foo/specific/path"
```

If a preset is specified it will exclusively use that preset's configuration and _will not_ merge it with the default
configuration. Command line flags are still merged into the preset configuration however.

## Thanks/Inspiration

Thanks to Joseph Amenta for developing lib3to2 and making it open source. This effort
wouldn't be possible without it!

Also a huge thank you to everyone who has contribued to Python, pgen, and lib2to3. Having such a foundation to start
from has made things immeasurably easier and far more productive!

And finally a shoutout to contributors of both [futurize](https://github.com/PythonCharmers/python-future/) and
[drop2](https://github.com/purplediane/drop2) which together served as the basis of the defuturize fixer suite.
