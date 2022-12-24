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


