# @TheWorldFoundry

# GDMC 2020 code entry

# Create a settlement on an arbitrary landscape.

# Method:
#		Given an arbitrary selection box
#		Create a starting 'character' and 'diary'
#		Based on the character's preferred process, find a location, build a dwelling. Log the action
#		Scan the area and take appropriate actions (gather, etc).
#		Expand the homestead
#		


#	Stop when time exceeded or no further action possible (no more land).

import time

import pygame
from pygame import Surface
from pymclevel import alphaMaterials, BoundingBox
import random
from random import random, randint
from math import pi, sin, cos, atan2, sqrt

inputs = (
		("Settlevolver", "label"),
		("Time limit (Seconds)", 60),
		("Number of agents", 4),
		("adrian@theworldfoundry.com", "label"),
		("http://theworldfoundry.com", "label"),
)

def nameRandom():
	FNAMES = [ "Sam", "Sandy",
			"Adlai",
			"Alex",
			"Alexis",
			"Ali",
			"Amari",
			"Amory",
			"Angel",
			"Arden",
			"Ariel",
			"Armani",
			"Arrow",
			"Auden",
			"Austen",
			"Avery",
			"Avis",
			"Azariah",
			"Baker",
			"Bellamy",
			"Bergen",
			"Blair",
			"Blake",
			"Blue",
			"Bowie",
			"Breslin",
			"Briar",
			"Brighton",
			"Callaway",
			"Campbell",
			"Carmel",
			"Channing",
			"Charleston",
			"Charlie",
			"Clancy",
			"Clarke",
			"Cleo",
			"Dakota",
			"Dallas",
			"Denver",
			"Devon",
			"Drew",
			"Eden",
			"Egypt",
			"Elliot",
			"Elliott",
			"Ellis",
			"Ellison",
			"Emerson",
			"Emery",
			"Ever",
			"Everest",
			"Finley",
			"Frankie",
			"Gentry",
			"Grey",
			"Halo",
			"Harley",
			"Haven",
			"Hayden",
			"Holland",
			"Hollis",
			"Honor",
			"Indiana",
			"Indigo",
			"Jamie",
			"Jazz",
			"Jordan",
			"Jules",
			"Justice",
			"Kamryn",
			"Karter",
			"Kendall",
			"Kingsley",
			"Kirby",
			"Kyrie",
			"Lake",
			"Landry",
			"Laramie",
			"Lennon",
			"Lennox",
			"Linden",
			"London",
			"Lyric",
			"Marley",
			"Marlo",
			"Memphis",
			"Mercury",
			"Merit",
			"Milan",
			"Miller",
			"Monroe",
			"Morgan",
			"Murphy",
			"Navy",
			"Nicky",
			"Oakley",
			"Ocean",
			"Oswin",
			"Parker",
			"Payton",
			"Peace",
			"Perry",
			"Peyton",
			"Phoenix",
			"Poet",
			"Quincy",
			"Quinn",
			"Raleigh",
			"Ramsey",
			"Rebel",
			"Reese",
			"Reilly",
			"Remi",
			"Remington",
			"Remy",
			"Revel",
			"Ridley",
			"Riley",
			"Rio",
			"Ripley",
			"River",
			"Robin",
			"Rory",
			"Rowan",
			"Royal",
			"Rumi",
			"Rylan",
			"Sage",
			"Sailor",
			"Sam",
			"Sawyer",
			"Scout",
			"Seneca",
			"Shannon",
			"Shay",
			"Shiloh",
			"Sidney",
			"Skyler",
			"Spencer",
			"Stevie",
			"Storm",
			"Sutton",
			"Tatum",
			"Taylor",
			"Tennessee",
			"Tennyson",
			"Texas",
			"Timber",
			"Tobin",
			"Tory",
			"Valentine",
			"Wilder",
			"Wisdom",
			"Wren",
			"Wynn",
			"Zephyr",
			"Smith", "Jones", "Stone"
	]
	SNAMES = FNAMES	
	return FNAMES[randint(0,len(FNAMES))-1], SNAMES[randint(0,len(SNAMES))-1]

class Materials:
	MAT_WATER = [ 9 ] # Water
	MAT_WOOD = [ 5, 17, 162, 99, 100, 5, 265] # Oak, leaves, Dark oak, Mushroom, Mushroom(Red), planks, stripped oak
	MAT_ORE = [ 73, 14, 15, 56 ] # Redstone, gold, iron, diamond, coal
	MAT_LAVA = [ 11 ] # Lava
	MAT_SOLID = [ 3, 1, 12, 4 ] # Dirt, stone, sand, cobblestone
	MATS_LIB = [ MAT_WATER, MAT_WOOD, MAT_ORE, MAT_LAVA, MAT_SOLID ]
	MAT_IGNORE = [ 18, 161, 31, 38, 175, 0, 9, 11 ] # Things that should be ignored for landscape height determination

class Structures:
	PATH = 1
	FARM = 2
	COTTAGE = 3
	BLACKSMITH = 4
	MINE = 5
	MEGA = 6
	Names = ["Nothing","Path","Farm","Cottage","Blacksmith","Mine","Megalith"]

class EventLog:
	def __init__(self):
		self.events = []
		
	def addEvent(self,event):
		self.events.append((time.localtime(),event))
		if True: # Debug
			print time.localtime(),event
			
		
	def printEntries(self):
		for ts, evt in self.events:
			print time.strftime("%H:%M:%S", ts),evt

class Agent:
	def __init__(self, fname, sname, pos, age, birthdate, structures):
		self.name = fname+" "+sname
		self.sname = sname
		self.fname = fname
		self.pos = pos
		self.age = age
		self.birthdate = birthdate
		self.structures = structures
		self.alive = True
		self.deathdate = None
		# Each agent has their own 'style' of building, determined by an interference pattern
		self.pattern = []
		for i in xrange(0,randint(2,5)):
			px = random()*16
			py = random()*16
			pz = random()*16
			wavelength = random()*8
			amplitude = 0.3+random()*0.7
			self.pattern.append((px,py,pz,wavelength,amplitude))
		self.materials = []
		baseMaterials = [ 236, 159, 35 ] # Concrete
		baseMaterialID = baseMaterials[randint(0,len(baseMaterials)-1)]
		for i in xrange(0,randint(2,5)):
			self.materials.append((baseMaterialID,randint(0,15)))
	
	def __str__(self):
		result = "I am "+self.name+" at "+str(self.pos)+", aged "+str(self.age)+", born "+str(time.strftime("%H:%M:%S", self.birthdate))
		if self.alive == False:
			result = result+", and died "+str(time.strftime("%H:%M:%S", self.deathdate))
		return result
	
	def doBirthday(self, eventLog):
		self.age += 1
		
		chanceOfDeath = float(self.age)/84.0
		if random() < chanceOfDeath:
			self.alive = False
			self.deathdate = time.localtime()
			eventLog.addEvent("[DIED] "+str(self))
		else:
			eventLog.addEvent("[BIRTHDAY] "+str(self))


def makeAgents(box,now,AGENTSMAX):
	agents = []
	names = [ None ]
	for i in xrange(0,AGENTSMAX):
		name = None
		count = 100
		while name in names and count > 0: # Try to make unique (but we don't really care...)
			fname, sname = nameRandom()
			name = fname+" "+sname
			count -= 1
		names.append(name)
		x = randint(box.minx,box.maxx)  # (box.maxx-box.minx)>>1
		z = randint(box.minz,box.maxz)  #(box.maxz-box.minz)>>1
		age = 21
		birthdate = time.localtime()
		structuresList = []
		newAgent = Agent(fname, sname, (x,z), age, birthdate, structuresList)
		agents.append(newAgent) # Metadata for each agent
	return agents

def findResourcesCloseToMe(pos, materialScans, searchRadius):
	x,z = pos
	
	resources = []
	
	# For everything in the resource map, find those that are within spitting distance
	# Randomly shuffle the search however, because otherwise we'll be here forever
	
	SR2 = searchRadius**2  # Precalculate
	
	count = 10
	keepGoing = True
	while count > 0 and keepGoing == True:
		count -= 1
		list = materialScans[randint(0,len(materialScans)-3)]  # Exclude the heights list (and 'solid list')
		if len(list) > 0:
			resource = list[randint(0,len(list)-1)] # Possible duplicates, so sue me...
			if resource not in resources: # Expensive? Omit if required
				(rID,rDATA),(rx,ry,rz) = resource
				dx = rx-x
				dz = rz-z
				if dx*dx+dz*dz < SR2: # Resource is within the search area
					resources.append(resource)
	return resources

def getHeightHere(level, box, x, z):
	result = -1
	
	y = box.maxy-1
	while y >= box.miny:
		bID = level.blockAt(x,y,z)
		if bID != 0 and bID not in Materials.MAT_WOOD and bID not in Materials.MAT_IGNORE: # Ignore Air or plant matter
			result = y
			return result # Break
		y -= 1
	return result

def checkForCollisions(A,listOfStructures):
	result = []
	
	px = A.minx
	py = A.miny
	pz = A.minz
	pX = A.maxx
	pY = A.maxy
	pZ = A.maxz
	
	# Iterate through the listOfBoxes and then add any intersecting objects to the result list
	for agent, type, box in listOfStructures:
		x = box.minx
		y = box.miny
		z = box.minz
		X = box.maxx
		Y = box.maxy
		Z = box.maxz
		
		collide = True
		if px > X:
			collide = False
		elif pz > Z:
			collide = False
		elif pX < x:
			collide = False
		elif pZ < z:
			collide = False
		elif pY < y:
			collide = False
		elif py > Y:
			collide = False

		if collide == True:
			result.append((type,box))
	
	return result

def tryToPlaceStructure(level, box, allStructures, potentialStructureSize, potentialStructureLocation, resource):
	(resourceBlockID, resourceBlockData), (resourceX, resourceY, resourceZ) = resource
	szx,szy,szz = potentialStructureSize
	pslx, psly, pslz = potentialStructureLocation
	if not (pslx < box.minx or pslx+szx >= box.maxx or pslz < box.minz or pslz+szz >= box.maxz):
		# Ok to try to position this structure. Check for height here
		y = psly
		# Some past solutions I've seen to this problem don't work with the existing terrain and, instead, create a bit of urban sprawl.
		if not (y < box.miny or y+szy >= box.maxy):
			# It can fit in the allocated space! Check for collisions
			newBox = BoundingBox((pslx, y, pslz),(szx, szy, szz))
			collidesWith = checkForCollisions(newBox, allStructures)
			if len(collidesWith) == 0:
				return newBox # All good - pop this thing here
			else: # Else... Merge? Stack? Ignore?
				# Try stacking
				topY = newBox.maxy
				topBox = newBox
				for t,b in collidesWith:
					if b.maxy > topY:
						topBox = b
				if topBox != newBox: # Found a new box. Try to place this one on top of it.
					tryToPlaceStructure(level, box, allStructures, potentialStructureSize, (pslx, topY, pslz), resource)
				else:
					return None # We cannot place this box, sadly.


def perform(level, box, options):
	print "perform"

	width = box.maxx-box.minx
	depth = box.maxz-box.minz

	ALLOTTEDTIME = options["Time limit (Seconds)"] #60*1 #0 # 10 minutes
	
	eventLog = EventLog()
	
	STARTTIME = time.clock()

	# Check the selection for items of interest
	materialScans = profileLandscape(level,box,options)  # Check what type of landscape we've been handed...
	print "Material Scans are now completed" #, materialScans

	# Initialise agents
	AGENTSMAX = options["Number of agents"]
	agents = makeAgents(box,STARTTIME,AGENTSMAX)
	for agent in agents:
		eventLog.addEvent("[BORN] "+str(agent))
		print agent

	allStructures = []

	iterationCount = 0
	# Simulate and evolve
	keepGoing = True
	lastTime = STARTTIME
	while keepGoing == True:
		# HOUSEKEEPING
		iterationCount += 1
		now = time.clock()
		elapsedTime = now - STARTTIME
		# print elapsedTime
		
		# STEP THROUGH THE SIMULATION
		#   FOR EACH AGENT:
		#	Find a resource to exploit, locate an area to build out, add a structure that exploits that resource.
		#		materialScans has: MAT_WATER(0), MAT_WOOD(1), MAT_ORE(2), MAT_LAVA(3), MAT_SOLID(4), HEIGHTS(5)
		#		
		#		We want crop fields near water
		#		Cottage near Wood
		#		Mine shaft near ore
		#		Blacksmith near Lava
		#		Castle / Tower near solid?
		#		Temple near heights
		keepGoing = False
		for agent in agents:		
			if agent.alive == True:
				keepGoing = True
				searchRadius = 4
				localResources = findResourcesCloseToMe(agent.pos, materialScans, searchRadius)
				if len(localResources) > 0:
					# Choose a resource type near to the player
					resource = localResources[randint(0,len(localResources)-1)]
					
					potentialStructureSize = randint(3,6),randint(1,3),randint(3,3)
					structureType = Structures.PATH
					# Build something... what? Determine what to build based on something in the landscape.
					(resourceBlockID, resourceBlockData), (resourceX, resourceY, resourceZ) = resource
					if resourceBlockID in Materials.MAT_WATER:
						# Find a location to build a farm
						# eventLog.addEvent("[PLAN] "+str(agent)+" Thought about building a farm")
						# print str(agent),"Build a farm"
						potentialStructureSize = randint(16,32),randint(5,16),randint(16,32)
						structureType = Structures.FARM
						
					elif resourceBlockID in Materials.MAT_LAVA:
						# Find a location to build a Blacksmith
						#print str(agent),"Build a blacksmith"
						potentialStructureSize = randint(8,12),randint(5,8),randint(8,12)
						structureType = Structures.BLACKSMITH
						
					elif resourceBlockID in Materials.MAT_WOOD:
						# Find a location to build a Cottage... start here?
						#print str(agent),"Build a cottage"
						potentialStructureSize = randint(6,12),randint(5,16),randint(6,12)
						structureType = Structures.COTTAGE

					elif resourceBlockID in Materials.MAT_ORE:
						# Find a location to build a Mine shaft
						#print str(agent),"Build a mine"
						potentialStructureSize = randint(16,24),randint(5,16),randint(16,24)
						structureType = Structures.MINE

					elif resourceBlockID in Materials.MAT_SOLID:
						# Find a location to build a Castle/Tower
						# ... possibly a temple up high
						#print str(agent),"Build a castle, tower, or temple"
						potentialStructureSize = randint(16,32),randint(16,32),randint(16,32)
						structureType = Structures.MEGA

					szx,szy,szz = potentialStructureSize
					potentialStructureLocation = resourceX+randint(-szx,szx),-1,resourceZ+randint(-szz,szz)
					pslx, psly, pslz = potentialStructureLocation					
					y = getHeightHere(level, box, pslx+(szx>>1), pslz+(szz>>1))
					newBox = tryToPlaceStructure(level, box, allStructures, potentialStructureSize, (pslx, y, pslz), resource)
					
					if newBox is not None:
						allStructures.append((agent,structureType,newBox))
						agent.structures.append((structureType,newBox))
						eventLog.addEvent("[BUILD] "+str(agent)+" Built a "+Structures.Names[structureType]+" of dimension "+str(newBox))
					
				# Move somewhere else to try again/ Brownian motion.
				x,z = agent.pos
				direction = random()*2.0*pi
				distance = 2.0
				dx = distance*cos(direction)
				dz = distance*sin(direction)
				agent.pos = (int(x+dx-box.minx)%width)+box.minx, (int(z+dz-box.minz)%depth)+box.minz
				if False: # Debug = plot the agent's position as a block in the sky
					x,z = agent.pos
					level.setBlockAt(x,255,z,35) # Debug
					level.setBlockDataAt(x,255,z,2) # Debug
		
		# New year celebrations followed by possible baby agents!
		if now-lastTime > 10: # seconds in a simulation year
			countAgents = 0
			for agent in agents:		
				if agent.alive == True:
					countAgents += 1
					agent.doBirthday(eventLog)
			lastTime = now # Happy New "Year"
			eventLog.addEvent("[TIME] Happy New Year!" )
		
			babyAgents = []
			birthProximity = 4
			for agent in agents: # Check proximity
				for agent2 in agents: # Check proximity
					if agent != agent2 and agent.alive == True and agent2.alive == True and agent.sname != agent2.sname:
						x,z = agent.pos
						x2,z2 = agent2.pos
						dx = x-x2
						dz = z-z2
						dist2 = dx*dx+dz*dz
						if dist2 < birthProximity and random() <= 0.001:
							fname, sname = nameRandom()
							sname = agent.sname+"-"+agent2.sname # Convention - hyphenated surname of both parents
							name = fname+" "+sname # Duplicates allowed
							babyx = (x+x2)>>1	# Midpoint
							babyz = (z+z2)>>1	# Midpoint
							age = 5
							birthdate = time.localtime()
							structuresList = []
							newAgent = Agent(fname, sname, (x,z), age, birthdate, structuresList)
							babyAgents.append(newAgent) # Metadata for each agent
							keepGoing = True
			for baby in babyAgents:
				agents.append(baby)
		
		# HOUSEKEEPING
		if elapsedTime >= ALLOTTEDTIME: 
			keepGoing = False
			eventLog.addEvent("Life is too short. Here ends our story, after "+str(int(elapsedTime))+" seconds")
	
	#for i in xrange(0, len(agents)):
		# for type,box in agents[i].structures:
#	for type,box in allStructures:
#		colour = type # Hack... for debug
#		fill(level, box, (35,colour%16))  # Temp build a structure

	renderBuildings(level, box, agents, allStructures, materialScans)
	
	eventLog.printEntries() # Move the chronicle into a book or two
	
def profileLandscape(level, box, options):
	'''
		The strategy here is to 'sample' the landscape for resources and geometry.
		Rather than do it exhaustively, the method is grid-wise analysis of columns of material
	'''
	
	MINMAPSIZE = 16
	
	result = []
	for i in xrange(0, len(Materials.MATS_LIB)+1):
		result.append([]) # Initialise result set
	
	WIDTH = box.maxx-box.minx
	DEPTH = box.maxz-box.minz
	HEIGHT = box.maxy-box.miny
	gridsize = 4
	if WIDTH < MINMAPSIZE or DEPTH < MINMAPSIZE:
		gridsize = 1
		
	cursorZ = box.minz
	while cursorZ < box.maxz:
		# print cursorZ
		cursorX = box.minx
		while cursorX < box.maxx:
			cursorY = box.miny
			maxSolid = 0
			while cursorY < box.maxy:
				blockID = level.blockAt(cursorX, cursorY, cursorZ)
				for i in xrange(0, len(Materials.MATS_LIB)):
					if blockID in Materials.MATS_LIB[i]:
						result[i].append(((blockID,level.blockDataAt(cursorX, cursorY, cursorZ)),(cursorX, cursorY, cursorZ))) # Block, position
						maxSolid = cursorY
				cursorY += 1 # Scan the entire column
			if maxSolid > 0:
				result[len(result)-1].append(((0,0),(cursorX,maxSolid,cursorZ))) # Mark the high point at this point
			cursorX += gridsize
		cursorZ += gridsize
	
	return result



def logMessage(source,msg):
	print time.strftime("%H:%M:%S", time.localtime()),"[",source,"]",msg

def logEvent(log, event):
	print "logEvent"
	log.append((time.localtime(),event))

def printEventLog(log):
	for ts, ev in log:
		print time.strftime("%H:%M:%S", ts), ev

def gatherResources():
	print "gatherResources"


def expandBuilding():
	print "expandBuilding"

# Export plan to the world
	
def renderBuildings(level, box, agents, allStructures, materialScans):
	print "renderBuildings"
	
	# Based on the structure type, invoke a generator to render it.
	# 1) Render a building of the type specified within the bounding box.
	# 2) Sweep through and place the foundations
	# 3) Connect some of them
	
	areas = []
	
	for agent, t, b in allStructures:
		print "Building the structures created by",agent.name
		generatorName = "GEN_"+Structures.Names[t]
		module = __import__(generatorName)
		areas = module.create(generatorName, level, box, b, agents, allStructures, materialScans, agent) # This attempts to invoke the create() method on the nominated generator
		
		

def renderEvents():
	print "renderEvents"

def fill(level, box, material):
	bid, bdata = material
	
	for z in xrange(box.minz, box.maxz):
		for x in xrange(box.minx, box.maxx):
			for y in xrange(box.miny, box.maxy):
				level.setBlockAt(x,y,z,bid)
				level.setBlockDataAt(x,y,z,bdata)

def agentFill(agent, level, box):
	for z in xrange(box.minz, box.maxz):
		for x in xrange(box.minx, box.maxx):
			for y in xrange(box.miny, box.maxy):
				placeBlock(level, (x,y,z), agent.materials, agent.pattern)
				
def placeBlock(level, position, materials, pattern):
	x,y,z = position
	pi2 = pi*2.0
	
	valueHere = 0
	for px,py,pz,wl,amp in pattern:
		dx = px-x
		dy = py-y
		dz = pz-z
		dist = sqrt(dx*dx+dy*dy+dz*dz)
		phase = dist/wl*pi2
		contribution = amp*sin(phase)
		valueHere += contribution
	valueHere = abs(valueHere/float(len(pattern)))*float(len(materials))

	blockID,blockData = materials[int(valueHere)%len(materials)]
	level.setBlockAt(x,y,z,blockID)
	level.setBlockDataAt(x,y,z,blockData)
	
def setBlockToGround(level, position, material):
	x, y, z = position
	mID,mData = material
	keepGoing = True
	while keepGoing and y >= 0:
		blockID = level.blockAt(x, y, z)
		if blockID in Materials.MAT_IGNORE:
			level.setBlockAt(x, y, z, mID)
			level.setBlockDataAt(x, y, z, mData)
		else:
			keepGoing = False
		y -= 1