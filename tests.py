
# ------------------------------------
class Foo:
    def __call__(self):
        print('Just called')

F = Foo()

# this calls the __call__ method
F() 
# ------------------------------------

class Value(object):
    def __init__(self) -> None:
        self._value = 0

    def __iadd__(self, v):
        self._value += v
        return self._value

    def __isub__(self, v):
        self._value -= v
        return self._value

V = Value()
V += 5
V -= 2

print(V) # prints 3
# ------------------------------------

def Add(a, b):
    return a + b

def Del(a, b): 
    return a - b

def NumberOperation(a, b, Func):
    return Func(a, b)

x = NumberOperation(5, 4, Add)
print(x)

x = NumberOperation(3, 2, Del)
print(x)

# ------------------------------------
def Test(v: int) -> int:
    return v + v

print(Test('Python'))
