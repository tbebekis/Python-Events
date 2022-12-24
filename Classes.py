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