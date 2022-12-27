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