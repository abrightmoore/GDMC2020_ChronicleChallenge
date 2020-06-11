# @TheWorldFoundry

from random import randint, random
from pymclevel import BoundingBox
import Settlevolver_v1 as Settlevolver
import GEN_Cottage

def create(generatorName, level, boxGlobal, box, agents, allStructures, materialScans, agent):
	print "Building a Mine at", box," by ",str(agent)

	boxes = [ box ]
	
	MINEPLOT_SZ = 12
	
	keepGoing = True
	while keepGoing == True:
		results = []
		for A in boxes:
			width = A.maxx-box.minx
			depth = A.maxz-box.minz
			height = A.maxy-box.miny

			keepGoing = False
			if width >= MINEPLOT_SZ or depth >= MINEPLOT_SZ:
				splits = Settlevolver.chopBoundingBoxRandom2D(A)
				for B in splits:
					results.append(B)
					if B.maxx-B.minx >= MINEPLOT_SZ or B.maxz-B.minz >= MINEPLOT_SZ and random() < 0.5:
						keepGoing = True
			else:
				results.append(A)
				keepGoing = False
		boxes = results
	
	# Make one or more mineshafts!
	shaft = results.pop(randint(0,len(results)-1))
	MAT_LOCAL = materialScans[1]
	materials = []
	for mat, tpos in MAT_LOCAL:
		materials.append(mat)
	makeShaft(level, shaft, materials, agent.pattern)
	GEN_Cottage.create(generatorName, level, box, BoundingBox((shaft.minx,shaft.miny+4,shaft.minz),(shaft.maxx-shaft.minx,shaft.maxy-shaft.miny,shaft.maxz-shaft.minz)), agents, allStructures, materialScans, agent)
	
	resultAreas = []
	# Delegate the buildings out
	for C in results:
		if random() > 0.3: # Skip some space so it's a bit varied
			areas = GEN_Cottage.create(generatorName, level, box, C, agents, allStructures, materialScans, agent)
			for area in areas:
				resultAreas.append(area)
			
	return resultAreas
	
def makeShaft(level, box, materials, pattern):
	# print "makeShaft at", box, material
	y = box.miny
	depth = 0
	if y > 2:
		depth = randint(box.miny>>2,box.miny)
	
	for i in xrange(y-depth, y+2):
		# print "Mining level", i
		for x in xrange(box.minx, box.maxx):
			for z in xrange(box.minz, box.maxz):
				if x == box.minx or x == box.maxx-1 or z == box.minz or z == box.maxz-1:
					Settlevolver.placeBlock(level, (x, i, z), materials, pattern)
				else:
					level.setBlockAt(x,i,z,0)
					level.setBlockDataAt(x,i,z,0)
	
	for i in xrange(y+2, 255):
		for x in xrange(box.minx, box.maxx):
			for z in xrange(box.minz, box.maxz):
				level.setBlockAt(x,i,z,0)
				level.setBlockDataAt(x,i,z,0)				