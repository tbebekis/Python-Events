# Python Events

Source code can be found at [Github](https://github.com/tbebekis/Python-Events).

## Introduction

Event is "something that happens".

An Event in computer programming is a code construction. 

An object, known as **Publisher**, informs other objects, known as **Subscribers** or **Listeners**, that something special is about to happen to it or has happened to it.

The actual cause of broadcasting such an information to Subscribers could be a state change, say the Publisher's `Name` property changes, or any occurence of some importance, say the Publisher's mouse is clicked.

Subscribers are objects interested in such state changes or important moments in the life of a certain Publisher object.

The Publisher object publishes the name of the event and provides the means to Subscriber objects to attach a proper function, called `event handler` to that event.

Then when the event takes place in the Publisher, the Publisher `invokes` the Subscriber's `event handler` function.

## Events in Programming Languages

Events are directly or indirectly supported by a number of Programming Languages.

[Java](https://docs.oracle.com/javase/tutorial/uiswing/events/intro.html) supports events using, the so called, `Listener` classes.

[Javascript DOM objects](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Building_blocks/Events) support events in a, more or less, similar way.

[Object Pascal](https://docwiki.embarcadero.com/RADStudio/Sydney/en/Events_(Delphi)) and .Net languages, such as [C#](https://learn.microsoft.com/en-us/dotnet/standard/events/), support events too.

In [Python](https://www.python.org/) the developer has to invent a way to create, publish, subscribe to and invoke events.

The rest of this text describes such a solution.

## What is an event actually

An event handler is actually a **callback function**.

From [Wikipedia](https://en.wikipedia.org/wiki/Callback_(computer_programming)): *In computer programming, a callback or callback function is any reference to executable code that is passed as an argument to another piece of code*.

In computer programming every code element resides in a memory address. Everything has a memory address. 

If a code knows the memory address of a function (has a reference to that function, i.e. in a variable) it can call the function.

Consider the following.

```
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
```

The `Func` parameter maybe `Add` or `Del`, effectively passing a reference to the corresponding function.

Note that when passing the `Add` or `Del` argument the **call operator**, which is the `()` is ommited. Thus the function is **not** called. Just its address is passed.

The `Event` class stores event handler function references in its internal `_Handlers` list.

## The source code

Following are the source code files used in this exercise.<!--more-->

### The `Event.py` file

This file contains the `Event` class and the `EventArgs` class.

Those two classes is all that is needed in order to implement events in Python the same way other languages do. They are described later.

```
from typing import TypeVar

class EventArgs():
	""" 
	Event Arguments class.
	To be used as a base class for event argument classes.
	"""	
	def __init__(self, Sender: object):
		self.Sender = Sender
		self.EventParams = dict()

Args = TypeVar('Args', bound=EventArgs)

class Event(object): 	
	def __init__(self):
		self._Handers = [] 
	
	def __iadd__(self, handler):
		""" SEE: https://docs.python.org/3/reference/datamodel.html#object.__iadd__ """
		self._Handers.append(handler)
		return self
	
	def __isub__(self, handler):
		""" Subtraction, see above  """
		self._Handers.remove(handler)
		return self 	 
	
	def __call__(self, Args: Args):	
		""" SEE: https://docs.python.org/3/reference/datamodel.html#object.__call__ """
		for Hander in self._Handers:
			Hander(Args) 
```

### The `Classes.py` file

This file contains the `Publisher` class which demonstrates how to publish events.

It also contains the `Subscriber` class which contains event handler functions that can be attached to `Publisher` events. 

Will see how later.

```
from Event import Event, EventArgs

class Publisher():
	def __init__(self):
		self.StartEvent = Event()
		self.StopEvent = Event()		 
	
	def OnStart(self):
		Args = EventArgs(self)
		self.StartEvent(Args)

	def OnStop(self):	
		Args = EventArgs(self)
		self.StopEvent(Args)	

	def Start(self):
		self.OnStart()

	def Stop(self):
		self.OnStop()

class Subscriber():
	def StartedHandler(self, Args: EventArgs):
		print("Started")

	def StoppedHandler(self, Args: EventArgs):
		print("Stopped")
```
 
### The `main.py` file

This file is just a sample on how to 
- create an instance of the `Publisher` class, 
- create an instance of the `Subscriber` class, 
- attach event handler functions to `Publisher` events, 
- and then trigger the events 
- that invoke the event handler functions

```
from Classes import Publisher, Subscriber

Pub = Publisher() 

Sub = Subscriber()
Pub.StartEvent += Sub.StartedHandler
Pub.StopEvent += Sub.StoppedHandler	

Pub.Start()
```

## Discussion

This code takes advantage of a number of Python features.

### Emulating numeric types
By defining an `__iadd__` and an `__isub__` method the `Event` class emulates [addition and subtraction](https://docs.python.org/3/reference/datamodel.html#object.__iadd__). 

The documentation states: *if `x` is an instance of a class with an `__iadd__()` method, `x += y` is equivalent to `x = x.__iadd__(y)`*. 

This is useful when having classes for numeric operations.

Here is an example.

```
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
```
The `Event` class uses this feature in order to add or remove event handlers, provided by Subscriders, to its internal `_Handlers` list.

This is exactly what happens when the followin line of the `main.py` is called. A reference to the `StartedHandler()` method of the `Subscriber` object is added to the internal `Event`'s internal `_Handlers` list.

```
Pub.StartEvent += Sub.StartedHandler
```

### Callable classes
The `Event` class is a **callable** class. A class is callable when defines a [`__call__` function](https://docs.python.org/3/reference/datamodel.html#object.__call__).

Here is an example.

```
class Foo:
    def __call__(self):
        print('Just called')

F = Foo()

# this calls the __call__ method
F() 
```

This feature is useful when it comes to trigger the event and invoke the event handlers.

The `main.py` calls.

```
Pub.Start()
```

The `Publisher.Start()` method is called.

```
	def Start(self):
		self.OnStart()
```

Which in turn calls the `Publisher.OnStart()` method.

```
	def OnStart(self):
		Args = EventArgs(self)
		self.StartEvent(Args)
```

The `Publisher.OnStart()` method prepares an object of the `EventArgs` class and then calls the `StartEvent`.

The `StartEvent` is just a field. Its type is `Event`. And `Event` is a callable class. As a consequence the `__call__()` method of the `Event` class is called.

```
	def __call__(self, Args: Args):	
		for Hander in self._Handers:
			Hander(Args)
```

### Generics

Python is an interpreter, a script. Not a strictly typed language. So even the following code is executed without errors, although it uses [Type Annotations](https://docs.python.org/3/library/typing.html).

```
def Test(v: int) -> int:
    return v + v

print(Test('Python'))
```

So [Generics](https://en.wikipedia.org/wiki/Generic_programming) have little meaning in that context.

Nevertheless the `Event` class is a generic class in that it uses a `TypeVar` [type variable](https://docs.python.org/3/library/typing.html#typing.TypeVar) in order to define a generic type argument.

This is how a type variable is defined.

```
Args = TypeVar('Args', bound=EventArgs)
```
The above defines a type argument, an argument for generic classes or functions, under the name `Args`. Everything that is `EventArgs` or inherits from `EventArgs` can be used. That's the meaning of the `bound=`.

The `Event` class involves `Args` in its `def __call__(self, Args: Args)` method.

An application may subclass the `EventArgs` class and define its own event argument classes, proper for its own needs.

## Events in Python the easy way

If all of the above look too fancy or cryptic here is the easy way to have events in Python.

Following is a new version of the `Event` and `EventArgs` classes along with a new version of the sample classes without the cryptic `__xxx()__` calls.

### The `Event2.py` file

```
from typing import TypeVar

class EventArgs2():
	def __init__(self, Sender: object):
		self.Sender = Sender
		self.EventParams = dict()

Args = TypeVar('Args', bound=EventArgs2)

class Event2(object): 
    def __init__(self):
        self._Handers = [] 
    def Add(self, Hander):
        self._Handers.append(Hander)
    def Remove(self, Handler):
        self._Handers.remove(Handler)
    def Invoke(self, Args: Args):
        for Hander in self._Handers:
            Hander(Args)

class Publisher2():
    def __init__(self):
        self.StartEvent = Event2()
        self.StopEvent = Event2()		 

    def OnStart(self):
        Args = EventArgs2(self)
        self.StartEvent.Invoke(Args)

    def OnStop(self):	
        Args = EventArgs2(self)
        self.StopEvent.Invoke(Args)	

    def Start(self):
        self.OnStart()

    def Stop(self):
        self.OnStop()

class Subscriber2():
    def StartedHandler(self, Args: EventArgs2):
        print("Started")

    def StoppedHandler(self, Args: EventArgs2):
        print("Stopped")

def TestEvent2():
    Pub = Publisher2() 

    Sub = Subscriber2()
    Pub.StartEvent.Add(Sub.StartedHandler)
    Pub.StopEvent.Add(Sub.StoppedHandler)

    Pub.Start()
```

### The `main.py` file

```
import Event2

Event2.TestEvent2()
```