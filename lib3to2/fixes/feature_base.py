"""
Base classes for features that are backwards-incompatible.

Usage:
features = Features()
features.add(Feature("py3k_feature", "power< 'py3k' any* >", "2.7"))
PATTERN = features.PATTERN
"""

pattern_unformatted = "{0}={1}" # name=pattern, for dict lookups
warning_unformatted = """
feature {0} is not supported in Python 2.5.  A minimum version of Python {1} is
required to use this feature.  If your program will only be using that version
of the interpreter or higher, then you may ignore this warning.  Otherwise, you
will need to refactor your code not to use that feature."""

class Feature(object):
    """
    A feature has a name, a pattern, and a minimum version of Python 2.x
    required to use the feature (or 3.x if there is no backwards-compatible
    version of 2.x)
    """
    def __init__(self, name, PATTERN, version):
        self.name = name
        self._pattern = PATTERN
        self.version = version

    def warning_text(self):
        """
        Format the above text with the name and minimum version required.
        """
        return warning_unformatted.format(self.name, self.version)

class Features(set):
    """
    A set of features that generates a pattern for the features it contains.
    This set will act like a mapping in that we map names to patterns.
    """
    mapping = {}

    def update_mapping(self):
        """
        Called every time we care about the mapping of names to features.
        """
        self.mapping = dict((f.name, f) for f in iter(self))
    
    @property
    def PATTERN(self):
        """
        Uses the mapping of names to features to return a PATTERN suitable
        for using the lib2to3 patcomp.
        """
        self.update_mapping()
        return " |\n".join(pattern_unformatted.format(f.name, f._pattern) for f in iter(self))

    def __getitem__(self, key):
        """
        Implement a simple mapping to get patterns from names.
        """
        return self.mapping[key]
        
