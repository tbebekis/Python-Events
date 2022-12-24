from Classes import Publisher, Subscriber

Pub = Publisher() 

Sub = Subscriber()
Pub.StartEvent += Sub.StartedHandler
Pub.StopEvent += Sub.StoppedHandler	

Pub.Start()
