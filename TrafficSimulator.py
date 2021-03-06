import sys, socket, traceback, random, sched, time

class TrafficSimulator:
	USERNAME = "paulo.tanaka"
	CHARACTERS = "0123456789abcdefghijklmnopqrstuvxwyzABCDEFGHIJKLMNOPQRSTUVXWYZ"
	# How Many seconds in between generations
	DELAY = 1
	# Priority of scheduling
	PRIORITY = 1
	
	""" Construc a new Traffic Simulator """
	def __init__(self, addr, port, rate, size, runningTime):
		self.serverAddr  = addr
		self.serverPort  = int(port)
		self.sendRate    = int(rate)
        	self.payloadSize = int(size)
        	self.runningTime = int(runningTime)
        	self.seqNumber   = 0
        	self.scheduler   = sched.scheduler(time.time, time.sleep)
		self.connectToServer()

	def connectToServer(self):
		"""Connect to the Server. """
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.socket.connect((self.serverAddr, self.serverPort))
		except:
			print 'Connection Failed', 'Connection to ' + self.serverAddr + ' failed.'
			sys.exit(0)

	def run(self):
		self.schedGenerations()
		self.scheduler.run()

	def schedGenerations(self):
		"""Schedule when to generate packets"""
		for i in range(self.runningTime):
			self.scheduler.enter(i * self.DELAY, 1, self.generate, ())

	def generate(self):
		"""Generate rate number of packets"""
		for i in range(self.sendRate):
			payload =  self.USERNAME          + ":"
			payload += str(self.seqNumber)    + ":"
			payload += str(self.sendRate)     + ":"
			payload += str(self.payloadSize)  + ":"
			payload += str(self.runningTime ) + ":"
			payload += self.getRandomData(self.payloadSize - len(payload))
			self.socket.sendto(payload, (self.serverAddr, self.serverPort))
			self.seqNumber += 1
		
	def getRandomData(self, size):
		if size < 0:
			print "Size is too small, exiting"
			sys.exit(0)
		
		data = ""
		for i in range(size):
			data += self.CHARACTERS[random.randint(0,len(self.CHARACTERS) - 1)]
		return data
	

if __name__ == "__main__":
	try:
		serverAddr  = sys.argv[1]
		serverPort  = sys.argv[2]
		packPerSec  = sys.argv[3]
		payloadSize = sys.argv[4]
        	timeToRun   = sys.argv[5]
	except:
		print "Usage: TrafficSimulator.py Server_host Server_port packets_per_second payload_size_in_bytes second_to_run"
		sys.exit(0)

	# Create a new client
	simulator = TrafficSimulator(serverAddr, serverPort, packPerSec, payloadSize, timeToRun)

	# For the time to run
	simulator.run()
	sys.exit(0)
