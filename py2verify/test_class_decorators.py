def foo(cls):
    return cls

@foo
class A(object):
    pass

def test_class_decorator_does_not_explode():
    x = A()
