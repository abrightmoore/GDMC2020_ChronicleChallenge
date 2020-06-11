# @TheWorldFoundry

import Settlevolver_v1 as Settlevolver
from pymclevel import BoundingBox

from random import randint, random

def create(generatorName, level, boxGlobal, box, agents, allStructures, materialScans, agent):
	print "Building a",generatorName,"at", box," by ",str(agent)
	pattern = [ (10,10,10,0.2+0.8*random(),1.0),(0,0,0,0.5+0.5*random(),1.0) ]
	
	materials = [  (2,0), (13,0), (4,0), (1,1), (1,3), (1,5) ] # (208,0), Path block needs nothing on top
	
	y = box.maxy-1
	#for y in xrange(box.miny, box.maxy):
	while y >= box.miny:
		for z in xrange(box.minz, box.maxz):
			for x in xrange(box.minx, box.maxx):
				Settlevolver.placeBlock(level, (x, y, z), materials, pattern)
		y -= 1