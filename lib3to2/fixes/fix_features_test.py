from feature_base import Feature, Features
from lib2to3 import fixer_base

FEATURES = [
   #(FeatureName,
   #    FeaturePattern,
   # FeatureMinVersion,
   #),
    ("memoryview",
        "power < 'memoryview' trailer < '(' any* ')' > any* >",
     "2.7",
    ),
    ("python",
        "power < 'python' trailer < '(' ')' > >",
     "3.8",
    ),
    ("numbers",
        """import_from< 'from' 'numbers' 'import' any* > |
           import_name< 'import' ('numbers' dotted_as_names< any* 'numbers' any* >) >""",
     "2.6",
    ),
    ("abc",
        """import_name< 'import' ('abc' dotted_as_names< any* 'abc' any* >) > |
           import_from< 'from' 'abc' 'import' any* >""",
     "2.6",
    ),
    ("io",
        """import_name< 'import' ('io' dotted_as_names< any* 'io' any* >) > |
           import_from< 'from' 'io' 'import' any* >""",
     "2.6",
    ),
    ("bin",
        "power< 'bin' trailer< '(' any* ')' > any* >",
     "2.6",
    ),
    ("formatting",
        "power< any trailer< '.' 'format' > trailer< '(' any* ')' > >",
     "2.6",
    ),
]

class FixFeaturesTest(fixer_base.BaseFix):

    features_warned = set()

    features = Features(Feature(name, pattern, version) for name, pattern, version in FEATURES)

    PATTERN = features.PATTERN

    def match(self, node):
        to_ret = super(FixFeaturesTest, self).match(node)
        try:
            del to_ret['node']
        except Exception:
            pass
        return to_ret
    
    def transform(self, node, results):
        for feature_name in results:
            if feature_name in self.features_warned:
                continue
            else:
                self.warning(node, reason=self.features[feature_name].warning_text())
                self.features_warned.add(feature_name)
