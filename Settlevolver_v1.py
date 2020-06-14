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
from pymclevel import alphaMaterials, BoundingBox, TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
import random
from random import random, randint
from math import pi, sin, cos, atan2, sqrt

inputs = (
		("Settlevolver", "label"),
		("Number of iterations", 3),
		("Time limit (Seconds)", 60),
		("Number of agents", 8),
		("Resource hunt radius", 4),
		("Chance to build", 0.18),
		("Chance of child", 0.5),
		("Breeding range", 16),
		("Seconds per year", 3),
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
	MAT_WATER = [ 9, 79 ] # Water, Ice
	MAT_WOOD = [ 5, 17, 162, 99, 100, 5, 265] # Oak, leaves, Dark oak, Mushroom, Mushroom(Red), planks, stripped oak
	MAT_ORE = [ 73, 14, 15, 56 ] # Redstone, gold, iron, diamond, coal
	MAT_LAVA = [ 11 ] # Lava
	MAT_SOLID = [ 3, 1, 12, 4 ] # Dirt, stone, sand, cobblestone
	MATS_LIB = [ MAT_WATER, MAT_WOOD, MAT_ORE, MAT_LAVA, MAT_SOLID ]
	MAT_IGNORE = [ 18, 161, 31, 38, 175, 0, 79, 78 ] # Things that should be ignored for landscape height determination

class Structures:
	PATH = 1
	FARM = 2
	COTTAGE = 3
	BLACKSMITH = 4
	MINE = 5
	MEGA = 6
	BIRTHTREE = 7
	TOWER = 8
	Names = ["Nothing","Path","Farm","Cottage","Blacksmith","Mine","Megalith","BirthTree","Tower"]

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
		self.direction = 2.0*pi*random()
		self.speed = 1.5+1.0*random()
		# Each agent has their own 'style' of building, determined by an interference pattern
		self.pattern = []
		for i in xrange(0,randint(2,5)):
			px = random()*16
			py = random()*16
			pz = random()*16
			wavelength = random()*8.0
			amplitude = 0.4+random()*0.6
			self.pattern.append((px,py,pz,wavelength,amplitude))
		self.materials = [ ] # Occasional Glowstone, Sea Lantern
		if random() > 0.5:
			if random() > 0.5:
				self.materials.append((89,0))
			else:
				self.materials.append((169,0))
		baseMaterials = [ 251, 159, 35 ] # Concrete is 238 on bedrock
		baseMaterialID = baseMaterials[randint(0,len(baseMaterials)-1)]
		for i in xrange(0,randint(3,7)):
			self.materials.append((baseMaterialID,randint(0,15)))
	
	def __str__(self):
		result = "I am "+self.name+" at "+str(self.pos)+", aged "+str(self.age)+", born "+str(time.strftime("%H:%M:%S", self.birthdate))
		if self.alive == False:
			result = result+", and died "+str(time.strftime("%H:%M:%S", self.deathdate))
		return result
	
	def doBirthday(self, eventLog):
		self.age += 1
		
		chanceOfDeath = float(self.age)/100.0
		if random() < chanceOfDeath:
			self.alive = False
			self.deathdate = time.localtime()
			eventLog.addEvent("[DIED] "+str(self))
			return False
		else:
			eventLog.addEvent("[BIRTHDAY] "+str(self))
			return True


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
		list = materialScans[randint(0,len(materialScans)-2)]  # Exclude the heights list #(and 'solid list')
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

def tryToPlaceStructure(level, box, allStructures, potentialStructureSize, potentialStructureLocation, resource, recurse):
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
				if topBox != newBox and recurse == True: # Found a new box. Try to place this one on top of it.
					tryToPlaceStructure(level, box, allStructures, potentialStructureSize, (pslx, topY, pslz), resource, recurse)
				else:
					return None # We cannot place this box, sadly.


def perform(level, box, options):
	print "perform"
	BUILDCHANCE = options["Chance to build"]

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


	for loop in xrange(0, options["Number of iterations"]):
		print "Simulation number:",str(loop)
		agents = makeAgents(box,STARTTIME,AGENTSMAX)
		for agent in agents:
			eventLog.addEvent("[BORN] "+str(agent))
			print agent
		STARTTIME = time.clock()
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
					searchRadius = options["Resource hunt radius"]

					localResources = findResourcesCloseToMe(agent.pos, materialScans, searchRadius)
					if len(localResources) > 0:
						# Choose a resource type near to the player
						resource = localResources[randint(0,len(localResources)-1)]
						
						potentialStructureSize = randint(3,6),randint(1,3),randint(3,3)
						structureType = Structures.PATH
						# Build something... what? Determine what to build based on something in the landscape.
						(resourceBlockID, resourceBlockData), (resourceX, resourceY, resourceZ) = resource
						if random() <= BUILDCHANCE and resourceBlockID in Materials.MAT_WATER:
							# Find a location to build a farm
							# eventLog.addEvent("[PLAN] "+str(agent)+" Thought about building a farm")
							# print str(agent),"Build a farm"
							potentialStructureSize = randint(16,32),randint(5,16),randint(16,32)
							structureType = Structures.FARM
							
						elif random() <= BUILDCHANCE and resourceBlockID in Materials.MAT_LAVA:
							# Find a location to build a Blacksmith
							#print str(agent),"Build a blacksmith"
							potentialStructureSize = randint(8,12),randint(5,8),randint(8,12)
							structureType = Structures.BLACKSMITH
							
						elif random() <= BUILDCHANCE and resourceBlockID in Materials.MAT_WOOD:
							# Find a location to build a Cottage... start here?
							#print str(agent),"Build a cottage"
							potentialStructureSize = randint(6,12),randint(5,16),randint(6,12)
							structureType = Structures.COTTAGE

						elif random() <= BUILDCHANCE and resourceBlockID in Materials.MAT_ORE:
							# Find a location to build a Mine shaft
							#print str(agent),"Build a mine"
							potentialStructureSize = randint(16,24),randint(5,16),randint(16,24)
							structureType = Structures.MINE

						elif random() <= BUILDCHANCE and resourceBlockID in Materials.MAT_SOLID:
							# Find a location to build a Castle/Tower
							# ... possibly a temple up high
							#print str(agent),"Build a castle, tower, or temple"
							potentialStructureSize = randint(16,32),randint(16,32),randint(16,32)
							if random() < 0.7:
								structureType = Structures.MEGA
							else:
								structureType = Structures.TOWER
						else:
							potentialStructureSize = 3,3,3
							structureType = Structures.PATH
						
						szx,szy,szz = potentialStructureSize
						potentialStructureLocation = resourceX,-1,resourceZ
						if structureType != Structures.PATH:
							potentialStructureLocation = resourceX+randint(-szx,szx),-1,resourceZ+randint(-szz,szz)
						pslx, psly, pslz = potentialStructureLocation					
						y = getHeightHere(level, box, pslx+(szx>>1), pslz+(szz>>1))
						newBox = BoundingBox((pslx, y, pslz),potentialStructureSize)
						if structureType != Structures.PATH:
							newBox = tryToPlaceStructure(level, box, allStructures, potentialStructureSize, (pslx, y, pslz), resource, True)
						
						
						if newBox is not None:
							allStructures.append((agent,structureType,newBox))
							agent.structures.append((structureType,newBox))
							if structureType != Structures.PATH:
								eventLog.addEvent("[BUILD] "+str(agent)+" Built a "+Structures.Names[structureType]+" of dimension "+str(newBox))
						
					# Move somewhere else to try again/ (was Brownian motion)
					x,z = agent.pos
					agent.direction += 2.0*pi/72-random()*(2.0*pi/36) # 2 degrees shift left/right
					distance = agent.speed
					dx = distance*cos(agent.direction)
					dz = distance*sin(agent.direction)
					agent.pos = (int(x+dx-box.minx)%width)+box.minx, (int(z+dz-box.minz)%depth)+box.minz
					if False: # Debug = plot the agent's position as a block in the sky
						x,z = agent.pos
						level.setBlockAt(x,255,z,35) # Debug
						level.setBlockDataAt(x,255,z,2) # Debug
			
			# New year celebrations followed by possible baby agents!
			if now-lastTime > options["Seconds per year"]: # seconds in a simulation year
				countAgents = 0
				for agent in agents:		
					if agent.alive == True:
						countAgents += 1
						agent.doBirthday(eventLog)
				lastTime = now # Happy New "Year"
				eventLog.addEvent("[TIME] Happy New Year!" )
			
				babyAgents = []
				birthProximity = options["Breeding range"]
				birthProximity2 = birthProximity*birthProximity
				for agent in agents: # Check proximity
					for agent2 in agents: # Check proximity
						if agent != agent2 and agent.alive == True and agent2.alive == True and agent.sname != agent2.sname and agent.age > 18 and agent2.age > 18:
							x,z = agent.pos
							x2,z2 = agent2.pos
							dx = x-x2
							dz = z-z2
							dist2 = dx*dx+dz*dz
							if dist2 < birthProximity2 and random() <= options["Chance of child"]:
								fname, sname = nameRandom()
								sname = agent.sname+"-"+agent2.sname # Convention - hyphenated surname of both parents
								name = fname+" "+sname # Duplicates allowed
								babyx = (x+x2)>>1	# Midpoint
								babyz = (z+z2)>>1	# Midpoint
								age = 17 # Youngsters have to work for a living in this cruel world
								birthdate = time.localtime()
								structuresList = []
								newAgent = Agent(fname, sname, (babyx,babyz), age, birthdate, structuresList)
								
								# Make a combined list of materials from each parent, plus the ones the child is born with
								babymaterials = []
								for m in agent.materials:
									if m not in babymaterials:
										babymaterials.append(m)
								for m in agent2.materials:
									if m not in babymaterials:
										babymaterials.append(m)
								for m in newAgent.materials:
									if m not in babymaterials:
										babymaterials.append(m)
								newAgent.materials = babymaterials
								babyAgents.append(newAgent) # Metadata for each agent
								sz = randint(3,6)
								babyBox = BoundingBox((babyx,getHeightHere(level, box, babyx, babyz),babyz),(sz*2,sz*3,sz*2))
								newAgent.structures.append((Structures.BIRTHTREE,babyBox))
								allStructures.append((newAgent,Structures.BIRTHTREE,babyBox))
								keepGoing = True
								eventLog.addEvent("[BORN] "+str(newAgent)+" to "+str(agent)+" and "+str(agent2) )
				for baby in babyAgents:
					agents.append(baby)
			
			# HOUSEKEEPING
			if elapsedTime >= ALLOTTEDTIME: 
				keepGoing = False
				eventLog.addEvent("Life is too short. Here ends our story for now, after "+str(int(elapsedTime))+" seconds")
		
		#for i in xrange(0, len(agents)):
			# for type,box in agents[i].structures:
	#	for type,box in allStructures:
	#		colour = type # Hack... for debug
	#		fill(level, box, (35,colour%16))  # Temp build a structure

		renderBuildings(level, box, agents, allStructures, materialScans)
	
	eventLog.printEntries() # Move the chronicle into a book or two
	level.markDirtyBox(box)
	level.saveInPlace() # Checkpoint here
	
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
		generatorName = "GEN_"+Structures.Names[t]
		module = __import__(generatorName)
		areas = module.create(generatorName, level, box, b, agents, allStructures, materialScans, agent) # This attempts to invoke the create() method on the nominated generator
		if t != Structures.PATH:
			print "Built the structure created by",agent.name
			y = getHeightHere(level, box, b.minx, b.minz)
			texts = [ Structures.Names[t], "Built by", agent.fname, agent.sname ]
			createSign(level, b.minx, y+1, b.minz, texts)
		
		

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
		if blockID in Materials.MAT_IGNORE or blockID in Materials.MAT_WATER or blockID in Materials.MAT_LAVA:
			level.setBlockAt(x, y, z, mID)
			level.setBlockDataAt(x, y, z, mData)
		else:
			keepGoing = False
		y -= 1
		
def chopBoundingBoxRandom2D(A):
	width = A.maxx-A.minx
	depth = A.maxz-A.minz
	height = A.maxy-A.miny
	result = []
	B = None
	C = None

	if width > depth:
		B = BoundingBox((A.minx,A.miny,A.minz),(width>>1,height,depth))
		C = BoundingBox((A.minx+(width>>1),A.miny,A.minz),(width>>1,height,depth))
	else:
		B = BoundingBox((A.minx,A.miny,A.minz),(width,height,depth>>1))
		C = BoundingBox((A.minx,A.miny,A.minz+(depth>>1)),(width,height,depth>>1))
	
	return [ B, C ]
		
def createSign(level, x, y, z, texts): #abrightmoore - convenience method. Due to Jigarbov - this is not a Sign.
	# This is Java only. Bedrock has one line of text with line breaks.
	CHUNKSIZE = 16
	STANDING_SIGN = 63
	
	if level.blockAt(x,y,z) != STANDING_SIGN: # Don't try to create a duplicate set of NBT - it confuses the game.
		level.setBlockAt(x,y,z,STANDING_SIGN)
		level.setBlockDataAt(x,y,z,randint(0,15))
		#setBlock(level, (STANDING_SIGN,randint(0,15)), x, y, z)
		level.setBlockDataAt(x,y-1,z,1)
		level.setBlockDataAt(x,y-1,z,0)
		#setBlock(level, (1,0), x, y-1, z)
		control = TAG_Compound()
		# control["TileEntity"] = TAG_String("minecraft:sign")
		control["x"] = TAG_Int(x)
		control["Text4"] = TAG_String("{\"text\":\""+texts[3]+"\"}")
		control["y"] = TAG_Int(y)
		control["Text3"] = TAG_String("{\"text\":\""+texts[2]+"\"}")
		control["z"] = TAG_Int(z)
		control["Text2"] = TAG_String("{\"text\":\""+texts[1]+"\"}")
		control["id"] = TAG_String("minecraft:sign")
		control["Text1"] = TAG_String("{\"text\":\""+texts[0]+"\"}")
		
		chunka = level.getChunk((int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE))
		chunka.TileEntities.append(control)
		chunka.dirty = True

def createBirthTree(level, box, x, y, z, agent):
	# Make a tree shape in the unit box
	print "createBirthTree",x,y,z,agent
	width = box.maxx-box.minx
	depth = box.maxz-box.minz
	height = box.maxy-box.miny
	cx = (box.minx+box.maxx)>>1
	cz = (box.minz+box.maxz)>>1
	cy = (box.miny+int(height/3)+1+box.maxy)>>1
	
	for y in xrange(box.miny, box.miny+int(height/3)):
		placeBlock(level, (cx, y, cz), agent.materials, agent.pattern)
	for y in xrange(box.miny+int(height/3), box.maxy):	
		for x in xrange(box.minx, box.maxx):
			for z in xrange(box.minz, box.maxz):
				if random() < 0.9:
					dx = x-cx
					dy = y-cy
					dz = z-cz
					dist = sqrt(dx*dx+dy*dy+dz*dz)
					if dist <= width>>1:
						placeBlock(level, (x, y, z), agent.materials, agent.pattern)
	x = cx+2
	z = cz+2
	y = getHeightHere(level, box, x, z)
	setBlockToGround(level, (x, y, z), (98,0)) # Plinth
	texts = [
		"Born:",
		"",
		agent.fname,
		agent.sname,
	]
	createSign(level, x, y+1, z, texts)	