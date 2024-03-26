
def foo(**kwargs):
    for key, value in kwargs.items():
        print("%s == %s" % (key, value))

def test_foo():
    foo(test="id")
