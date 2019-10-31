def class_decorator(cls):
    cls.added_by_decorator = True
    return cls

@class_decorator
class A(object):
    pass

def test_class_decorator_does_not_explode():
    a_instance = A()
    assert a_instance.added_by_decorator # pylint: disable=no-member
