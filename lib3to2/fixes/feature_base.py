pattern_unformatted = "{0}={1}"
warning_unformatted = """
feature {0} is not supported in Python 2.5.  A minimum version of Python {1} is
required to use this feature.  If your program will only be using that version
of the interpreter or higher, then you may ignore this warning.  Otherwise, you
will need to refactor your code not to use that feature."""

class Feature(object):

    def __init__(self, name, PATTERN, version):
        self.name = name
        self._pattern = PATTERN
        self.version = version

    def warning_text(self):
        return warning_unformatted.format(self.name, self.version)

class Features(set):

    mapping = {}

    def update_mapping(self):
        self.mapping = dict((f.name, f) for f in iter(self))
    
    @property
    def PATTERN(self):
        self.update_mapping()
        return " |\n".join(pattern_unformatted.format(f.name, f._pattern) for f in iter(self))

    def __getitem__(self, key):
        return self.mapping[key]
        
