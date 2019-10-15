import maya.cmds as cmds
import math
import copy

class Make:

    '''
    word: (string) the grammar to be used to create the l-systems
    name: (string) root name of the tree to be created
    angle: ([i,j,k]) starting angle vector of tree, usually [0,1,0]
    angleChange: (decimal) a number between (0,1) for the angle to change, should NOT multiply into 1
    rad: (decimal) radius of the root
    radChange: (decimal) a number between (0,1) for the radius to decrease along a branch
    length: (decimal) staring length of the branch
    lengthChange: (decimal) a number between (0,1) for the length to change at each level
    point: ((x,y,z)) starting point of the tree
    '''
    
    def __init__( self, word, name, angle, angleChange, rad, radChange, length, lengthChange, point, leafColor, blossColor, trunkColor ):
        # F[&+F]F[->FL][&FB]

        self.word = word
        self.name = name
        self.angle = angle #[alpha, beta, gamma]
        self.angleChange = angleChange
        self.rad = rad
        self.radChange = radChange
        self.length = length
        self.lengthChange = lengthChange
        self.point = point #usually (0,0,0)
        self.leafColor = leafColor 
        self.blossColor = blossColor
        self.trunkColor = trunkColor

        self.currLevel = 0
        self.val = 0
        self.blossVal = 0
        self.leafVal = 0
        
        self.branchStack = []  #filled with branches
        self.allBranchCurves = [] #all completed branch dicts names to add polygons to
        self.allTrunks = []
        self.allBlossoms = []
        self.allLeaves = []
        #prevPoints = [] #used for error checking if a curve has already been placed in the position
        self.allBlossCurves = []
        self.allLeafCurves = []

        self.parent = ""


        
        #Correctly group parts
        #group curves
        self.curveGroup = 'All_Curves'
        cmds.group( em=True, name=self.curveGroup )

        #group trunks
        self.trunkGroup = 'All_Trunks'
        cmds.group( em=True, name=self.trunkGroup )

        #group blossoms
        self.blossGroup = 'All_Blossoms'
        cmds.group( em=True, name=self.blossGroup )

        #group leaves
        self.leafGroup = 'All_Leaves'
        cmds.group( em=True, name=self.leafGroup )

        #Group everything under name
        cmds.group( em=True, name=self.name )
        cmds.parent(self.trunkGroup, self.name)
        cmds.parent(self.curveGroup, self.name)
        cmds.parent(self.blossGroup, self.name)
        cmds.parent(self.leafGroup, self.name)
        
        #runs the commands in the grammar to create curve skeleton of tree
        for let in self.word:
            self.runCommand(let)
        
        #Adds polygon mesh to skeleton
        self.addTrunkMesh()
        self.addBlossMesh()
        self.addLeafMesh()

        #add shaders
        for trunk in self.allTrunks:
            self.shadeTrunk(trunk)

        for bloss in self.allBlossoms:
            self.shadeBlossom(bloss)

        for leaf in self.allLeaves:
            self.shadeLeaf(leaf)
        

    def runCommand( self, char ):
        '''
        F/f : Move forward
        L/l : Leaf
        B/b : Blossom
        +   : +i
        -   : -i
        ^   : +j
        v   : -j
        <   : +k
        >   : -k
        [   : push turtle state to stack
        ]   : pop turtle state from stack
        '''

        if char == 'f' or char == 'F': 
            self.forward() 
        if char == 'l' or char == 'L':
            self.createLeaf()   
        if char == 'b' or char == 'B':
            self.createBlossom()     
        if char == '+': 
            self.rotate(self.angleChange*2, 0)  
        if char == '-': 
            self.rotate(self.angleChange*-1, 0)      
        if char == '^': 
            self.rotate(self.angleChange*1, 1)     
        if char == 'v': 
            self.rotate(self.angleChange*-1, 1)      
        if char == '<': 
            self.rotate(self.angleChange, 2)       
        if char == '>': 
            self.rotate(self.angleChange*-1, 2)
        if char == '[':
            self.pushToStack() 
        if char == ']':
            self.popFromStack()

    def forward( self ): 

        #Decreases length during depth change
        self.length *= self.lengthChange

        #endpoint
        x = self.point[0] + ( self.length * math.cos(self.angle[0]) )  
        y = self.point[1] + ( self.length * math.cos(self.angle[1]) )  
        z = self.point[2] + ( self.length * math.cos(self.angle[2]) )  
        endPoint = ( x, y, z )
        diff = ( x-self.point[0], y-self.point[1], z-self.point[2] )

        #creates two points to go along curve
        midpoint_1 = ( self.point[0] + .3*diff[0], self.point[1] + .3*diff[1], self.point[2] + .3*diff[2] )
        midpoint_2 = ( self.point[0] + .6*diff[0], self.point[1] + .6*diff[1], self.point[2] + .6*diff[2] )
        
        #creates array of curve points
        points = [self.point, midpoint_1, midpoint_2, endPoint]
        #(points)

        #This was too help stop some errors when I was trying to Union
        #if a curve has aready been placed at that point, returns and does not finish forward function
        #for prev in Make.prevPoints:
        #    if points == prev:
        #       self.point = endPoint #makes sure that the start point for the next curve is correct
        #        return  
        #If no curve placed there, curve points placed into prevPoints array
        #Make.prevPoints.append(points)

        #Names Curve
        #gets parent curve number to append to curve name MAKE INTO SPLIT
        parentNum = ""
        if self.parent != "":
            parentNum = self.parent.split("_")[2]
        
        curveName = self.name+"_curve_"+str(self.val)+"_p_"+parentNum
        cmds.curve( name=curveName, p=points, d=3 ) 

        #Completed branch added to array
        newBranch = {
            "name" : curveName,
            "point" : copy.deepcopy(self.point),
            "angle" : copy.deepcopy(self.angle),
            "length" : copy.deepcopy(self.length),
            "parent" : copy.deepcopy(self.parent),
            "baseRad" : copy.deepcopy(self.rad),
            "tipRad" : copy.deepcopy(self.rad) * self.radChange
        }

        cmds.parent(curveName, self.curveGroup)
        self.allBranchCurves.append(newBranch)
        
        #Updates settings
        self.val += 1
        self.currLevel += 1
        self.point = endPoint
        self.parent = curveName
        self.rad *= self.radChange


    def createLeaf( self ):
        leafName = "leaf_curve_" + str(self.leafVal) 
        leafLen = self.length * 0.3 #might want to change ratio

        #endpoint
        x = self.point[0] + ( leafLen * math.cos(self.angle[0]) )  
        y = self.point[1] + ( leafLen * math.cos(self.angle[1]) )  
        z = self.point[2] + ( leafLen * math.cos(self.angle[2]) )  
        endPoint = ( x, y, z )
        diff = ( x-self.point[0], y-self.point[1], z-self.point[2] )

        #creates two points to go along curve
        midpoint_1 = ( self.point[0] + .3*diff[0], self.point[1] + .3*diff[1], self.point[2] + .3*diff[2] )
        midpoint_2 = ( self.point[0] + .6*diff[0], self.point[1] + .6*diff[1], self.point[2] + .6*diff[2] )
        
        #creates array of curve points
        points = [self.point, midpoint_1, midpoint_2, endPoint]

        #Makes Curve, adds to array
        cmds.curve( name=leafName, p=points, d=3 ) 
        self.allLeafCurves.append(leafName)

        self.leafVal += 1
        cmds.parent(leafName, self.curveGroup)

    def createBlossom( self ):
        
        blossName = "blossom_curve_" + str(self.blossVal) 
        blossLen = self.length * 0.3 #might want to change ratio

        #endpoint
        x = self.point[0] + ( blossLen * math.cos(self.angle[0]) )  
        y = self.point[1] + ( blossLen * math.cos(self.angle[1]) )  
        z = self.point[2] + ( blossLen * math.cos(self.angle[2]) )  
        endPoint = ( x, y, z )
        diff = ( x-self.point[0], y-self.point[1], z-self.point[2] )

        #creates two points to go along curve
        midpoint_1 = ( self.point[0] + .3*diff[0], self.point[1] + .3*diff[1], self.point[2] + .3*diff[2] )
        midpoint_2 = ( self.point[0] + .6*diff[0], self.point[1] + .6*diff[1], self.point[2] + .6*diff[2] )
        
        #creates array of curve points
        points = [self.point, midpoint_1, midpoint_2, endPoint]

        #Makes Curve, adds to array
        cmds.curve( name=blossName, p=points, d=3 ) 
        print(blossName)
        self.allBlossCurves.append(blossName)

        self.blossVal += 1
        cmds.parent(blossName, self.curveGroup)
        

        

    def rotate( self, newAngle, axis ):
    
        self.angle[axis] += newAngle


    def pushToStack( self ):

        #pushes current settings (point, angle) as a new branch dict to branchStack
        
        newBranch = {
            "point" : copy.deepcopy(self.point),
            "angle" : copy.deepcopy(self.angle),
            "length" : copy.deepcopy(self.length),
            "parent" : copy.deepcopy(self.parent),
            "radius" : copy.deepcopy(self.rad)
        }

        self.branchStack.append(newBranch)

    def popFromStack( self ):

        #pops branch from BranchStack to return turtle to previous branch
        #reset settings to popped branch's settings

        #Make sure all parameters resetted!!!

        pastBranch = self.branchStack.pop()
        self.point = pastBranch["point"]
        self.angle = pastBranch["angle"]
        self.length = pastBranch["length"]
        self.parent = pastBranch["parent"]
        self.rad = pastBranch["radius"]
        
    def addTrunkMesh( self ):
        
        for curve in self.allBranchCurves:
            
            #Names trunk 
            startIdx = len(self.name) + len("_curve_")
            trunkName = self.name + "_trunk_" + curve["name"][startIdx:]
            
            #Creates cylinder and moves it to the origin pt 
            cmds.polyCylinder(name=trunkName, subdivisionsX=20, subdivisionsY=1, r=curve["baseRad"])
            cmds.move( -1, trunkName+".scalePivot", trunkName+".rotatePivot", moveY=True, relative=True)
            
            #move polygon to start and align with normal
            cmds.select(clear=True)
            cmds.select(trunkName, tgl=True)
            cmds.select(curve["name"], add=True)
            cmds.pathAnimation( follow=True, followAxis='y', upAxis='z', startTimeU=True) 
            
            #Selects the face to scale and extrude
            cmds.select(clear=True)
            cmds.select(trunkName + ".f[26]")

            #get Scale of decreased radius
            scale = [curve["tipRad"]/curve["baseRad"] for i in range(3)]  
        
            #extrudes along curve
            cmds.polyExtrudeFacet( inputCurve=curve["name"], d=1, localScale=scale )

            cmds.parent(trunkName, self.trunkGroup)
            self.allTrunks.append(trunkName)

    def addBlossMesh( self ):

        for blossCurve in self.allBlossCurves:

            #Names trunk 
            startIdx = len("blossom_curve_")
            blossMesh = "blossom_" + blossCurve[startIdx:]+"_"+str(self.blossVal)
            
            #Adds blossom mesh
            import os
            pathVar = os.path.dirname(__file__) # This stores the current working directory
            cmds.file( pathVar+"/blossom_geo.mb", i=True )
            #bloss_file = cmds.file( pathVar+"/lotus_OBJ_low.obj", i=True )
            cmds.rename( "polySurface1", blossMesh )
            
            # Places the blossom to the right position and rotates it according to the last branch orientation
            cmds.select( blossMesh )
            yMax = cmds.xform(boundingBox=True, q=True)[4] #values returned as: xmin ymin zmin xmax ymax zmax
            scale = [self.length/yMax for i in range(3)]  
            cmds.select(clear=True)
            cmds.select(blossMesh)
            cmds.scale(0.5*scale[0], 0.5*scale[1], 0.5*scale[2])
            
            #move polygon to branch end and align with normal
            cmds.select(clear=True)
            cmds.select(blossMesh, tgl=True)
            points = cmds.getAttr( blossCurve+'.cv[0:2]' )
            start = points[0]
            cmds.move( start[0], start[1], start[2])

            cmds.select(clear=True)
            cmds.select(blossMesh, tgl=True)
            cmds.select(blossCurve, add=True)
            cmds.pathAnimation( follow=True, followAxis='y', upAxis='z', startTimeU=True) 

            self.allBlossoms.append(blossMesh)
            cmds.parent(blossMesh, self.blossGroup)
            
    def addLeafMesh( self ):

        for leafCurve in self.allLeafCurves:

            #Names trunk 
            startIdx = len("leaf_curve_")
            leafMesh = "leaf_" + leafCurve[startIdx:]+"_"+str(self.leafVal)
            
            #Adds blossom mesh
            import os
            pathVar = os.path.dirname(__file__) # This stores the current working directory
            cmds.file( pathVar+"/leaf_geo.mb", i=True )
            cmds.rename( "pPlane1", leafMesh )
            
            # Places the blossom to the right position and rotates it according to the last branch orientation
            cmds.select( leafMesh )
            yMax = cmds.xform(boundingBox=True, q=True)[4] #values returned as: xmin ymin zmin xmax ymax zmax
            scale = [self.length/yMax for i in range(3)]  
            cmds.select(clear=True)
            cmds.select(leafMesh)
            cmds.scale(3/scale[0], 3/scale[1], 3/scale[2])
            
            #move polygon to branch end and align with normal
            cmds.select(clear=True)
            cmds.select(leafMesh, tgl=True)
            points = cmds.getAttr( leafCurve+'.cv[0:2]' )
            start = points[0]
            cmds.move( start[0], start[1], start[2])

            cmds.select(clear=True)
            cmds.select(leafMesh, tgl=True)
            cmds.select(leafCurve, add=True)
            cmds.pathAnimation( follow=True, followAxis='y', upAxis='z', startTimeU=True) 

            self.allLeaves.append(leafMesh)
            cmds.parent(leafMesh, self.leafGroup)

    def cleanUp( self ):
        
        '''
        This is impossible without an external script. Maya's booleans are to finnicky 
        to work with and make the mesh just disappear. :(
        '''
        
        
        #union all together, and smooth!!
        
        #works range 0-6
        for sectNum in range(0, self.val-1): 
        #for sectNum in range(0, 2): 

            #Unions pairs of two branches into "sections"
            if sectNum == 0:
                firstB = "Tree_trunk_"+str(sectNum)  #Tree_trunk_0
                secondB = "Tree_trunk_"+str(sectNum+1)  #Tree_trunk_1
                cmds.polyBoolOp( firstB, secondB, op=1, n="sect_"+str(sectNum) ) #sect_0
            else:
                lastSect = "sect_"+str(sectNum-1)
                nextB = "Tree_trunk_"+str(sectNum+1)
                cmds.polyBoolOp( lastSect, nextB, op=1, n="sect_"+str(sectNum) )




    
    def shadeTrunk( self, trunk):

        trunkMat = cmds.shadingNode( 'lambert', asShader=True, name="trunkShader") 
        cmds.setAttr( trunkMat+'.color', self.trunkColor[0], self.trunkColor[1], self.trunkColor[2])
        trunkSG = cmds.sets(empty=True, renderable=True, noSurfaceShader=True, name=trunkMat+"SG")
        cmds.connectAttr( trunkMat + '.outColor', trunkSG + '.surfaceShader', force=True ) 
        cmds.sets(trunk, e=True, forceElement=trunkSG)


    def shadeBlossom( self, bloss):
        #same as shadeTrunk, just multiple times w/ diff parts of flower
        
        blossMat = cmds.shadingNode( 'lambert', asShader=True, name="blossShader") 
        cmds.setAttr( blossMat+'.color', self.blossColor[0], self.blossColor[1], self.blossColor[2])
        blossSG = cmds.sets(empty=True, renderable=True, noSurfaceShader=True, name=blossMat+"SG")
        cmds.connectAttr( blossMat + '.outColor', blossSG + '.surfaceShader', force=True ) 
        cmds.sets(bloss, e=True, forceElement=blossSG)


    def shadeLeaf( self, leaf):
        
        leafMat = cmds.shadingNode( 'lambert', asShader=True, name="leafShader") 
        cmds.setAttr( leafMat+'.color', self.leafColor[0], self.leafColor[1], self.leafColor[2])
        leafSG = cmds.sets(empty=True, renderable=True, noSurfaceShader=True, name=leafMat+"SG")
        cmds.connectAttr( leafMat + '.outColor', leafSG + '.surfaceShader', force=True ) 
        cmds.sets(leaf, e=True, forceElement=leafSG)

    



#############                         

#grammar = "F[-<[-<F]F[F[->>F+^^F][v+F]]][-<F]F[F[->>F+^^F][v+F]][[-<F]F[F[->>F+^^F][v+F]][->>[-<F]F[F[->>F+^^F][v+F]]+^^[-<F]F[F[->>F+^^F][v+F]]][v+[-<F]F[F[->>F+^^F][v+F]]]]"
#grammar = "F[vv>>F][^^<<F][vv>>F[vv>>F][^^<<F]][^^<<F[vv>>F][^^<<F]][vv>>F[++>F][--<F][++>F[++>F][--<F]][--<F[++>F][--<F]]][^^<<F[++>F][--<F][++>F[++>F][--<F]][--<F[vv>>F][^^<<F]]][vv>>F[++>F][--<F][++>F[++>F][--<F]][--<F[++>F][--<F]][vv>>F[++>F][--<F][++>F[vv>>F][^^<<F]][--<F[++>F][--<F]]][^^<<F[++>F][--<F][++>F[++>F][--<F]][--<F[vv>>F][^^<<F]]]][^^<<F[++>F][--<F][++>F[++>F][--<F]][--<F[++>F][--<F]][vv>>F[vv>>F][^^<<F][vv>>F[++>F][--<F]][^^<<F[++>F][--<F]]][^^<<F[++>F][--<F][vv>>F[vv>>F][^^<<F]][^^<<F[++>F][--<F]]]][vv>>F[++>F][--<F][++>F[++>F][--<F]][--<F[vv>>F][^^<<F]][++>F[vv>>F][^^<<F][++>F[++>F][--<F]][--<F[vv>>F][^^<<F]]][--<F[++>F][--<F][++>F[vv>>F][^^<<F]][--<F[++>F][--<F]]][vv>>F[vv>>F][^^<<F][++>F[++>F][--<F]][--<F[++>F][--<F]][++>F[++>F][--<F][++>F[++>F][--<F]][--<F[++>F][--<F]]][--<F[vv>>F][^^<<F][++>F[++>F][--<F]][--<F[vv>>F][^^<<F]]]][^^<<F[++>F][--<F][++>F[++>F][--<F]][--<F[vv>>F][^^<<F]][++>F[vv>>F][^^<<F][++>F[++>F][--<F]][--<F[++>F][--<F]]][--<F[vv>>F][^^<<F][vv>>F[++>F][--<F]][^^<<F[++>F][--<F]]]]][^^<<F[++>F][--<F][vv>>F[++>F][--<F]][^^<<F[++>F][--<F]][++>F[++>F][--<F][++>F[++>F][--<F]][--<F[++>F][--<F]]][--<F[++>F][--<F][++>F[++>F][--<F]][--<F[++>F][--<F]]][vv>>F[++>F][--<F][++>F[++>F][--<F]][--<F[vv>>F][^^<<F]][++>F[++>F][--<F][vv>>F[++>F][--<F]][^^<<F[++>F][--<F]]][--<F[vv>>F][^^<<F][++>F[vv>>F][^^<<F]][--<F[++>F][--<F]]]][^^<<F[++>F][--<F][vv>>F[vv>>F][^^<<F]][^^<<F[++>F][--<F]][vv>>F[++>F][--<F][vv>>F[++>F][--<F]][^^<<F[vv>>F][^^<<F]]][^^<<F[++>F][--<F][vv>>F[++>F][--<F]][^^<<F[++>F][--<F]]]]][vv>>F[++>F][--<F][++>F[++>F][--<F]][--<F[++>F][--<F]][vv>>F[++>F][--<F][vv>>F[++>F][--<F]][^^<<F[++>F][--<F]]][^^<<F[++>F][--<F][++>F[vv>>F][^^<<F]][--<F[++>F][--<F]]][vv>>F[vv>>F][^^<<F][vv>>F[++>F][--<F]][^^<<F[vv>>F][^^<<F]][++>F[++>F][--<F][++>F[vv>>F][^^<<F]][--<F[++>F][--<F]]][--<F[++>F][--<F][++>F[vv>>F][^^<<F]][--<F[++>F][--<F]]]][^^<<F[++>F][--<F][++>F[++>F][--<F]][--<F[vv>>F][^^<<F]][vv>>F[++>F][--<F][++>F[++>F][--<F]][--<F[++>F][--<F]]][^^<<F[vv>>F][^^<<F][vv>>F[++>F][--<F]][^^<<F[vv>>F][^^<<F]]]][vv>>F[vv>>F][^^<<F][++>F[++>F][--<F]][--<F[vv>>F][^^<<F]][vv>>F[vv>>F][^^<<F][++>F[++>F][--<F]][--<F[++>F][--<F]]][^^<<F[++>F][--<F][++>F[++>F][--<F]][--<F[vv>>F][^^<<F]]][++>F[++>F][--<F][++>F[++>F][--<F]][--<F[++>F][--<F]][++>F[vv>>F][^^<<F][++>F[++>F][--<F]][--<F[vv>>F][^^<<F]]][--<F[vv>>F][^^<<F][vv>>F[++>F][--<F]][^^<<F[vv>>F][^^<<F]]]][--<F[vv>>F][^^<<F][vv>>F[++>F][--<F]][^^<<F[++>F][--<F]][++>F[++>F][--<F][++>F[++>F][--<F]][--<F[vv>>F][^^<<F]]][--<F[++>F][--<F][++>F[++>F][--<F]][--<F[++>F][--<F]]]]][^^<<F[++>F][--<F][++>F[++>F][--<F]][--<F[++>F][--<F]][++>F[++>F][--<F][++>F[vv>>F][^^<<F]][--<F[++>F][--<F]]][--<F[++>F][--<F][++>F[++>F][--<F]][--<F[++>F][--<F]]][++>F[vv>>F][^^<<F][++>F[vv>>F][^^<<F]][--<F[++>F][--<F]][vv>>F[++>F][--<F][vv>>F[++>F][--<F]][^^<<F[++>F][--<F]]][^^<<F[++>F][--<F][++>F[vv>>F][^^<<F]][--<F[++>F][--<F]]]][--<F[++>F][--<F][++>F[++>F][--<F]][--<F[vv>>F][^^<<F]][++>F[++>F][--<F][++>F[++>F][--<F]][--<F[++>F][--<F]]][--<F[++>F][--<F][++>F[++>F][--<F]][--<F[++>F][--<F]]]]]][^^<<F[++>F][--<F][++>F[++>F][--<F]][--<F[++>F][--<F]][++>F[++>F][--<F][vv>>F[++>F][--<F]][^^<<F[++>F][--<F]]][--<F[vv>>F][^^<<F][++>F[++>F][--<F]][--<F[vv>>F][^^<<F]]][++>F[vv>>F][^^<<F][++>F[++>F][--<F]][--<F[++>F][--<F]][++>F[++>F][--<F][++>F[++>F][--<F]][--<F[vv>>F][^^<<F]]][--<F[vv>>F][^^<<F][++>F[++>F][--<F]][--<F[++>F][--<F]]]][--<F[++>F][--<F][++>F[vv>>F][^^<<F]][--<F[++>F][--<F]][++>F[++>F][--<F][++>F[++>F][--<F]][--<F[vv>>F][^^<<F]]][--<F[vv>>F][^^<<F][++>F[++>F][--<F]][--<F[++>F][--<F]]]][++>F[++>F][--<F][vv>>F[vv>>F][^^<<F]][^^<<F[++>F][--<F]][++>F[vv>>F][^^<<F][vv>>F[++>F][--<F]][^^<<F[++>F][--<F]]][--<F[++>F][--<F][vv>>F[vv>>F][^^<<F]][^^<<F[vv>>F][^^<<F]]][++>F[++>F][--<F][vv>>F[++>F][--<F]][^^<<F[++>F][--<F]][vv>>F[++>F][--<F][vv>>F[++>F][--<F]][^^<<F[++>F][--<F]]][^^<<F[++>F][--<F][++>F[vv>>F][^^<<F]][--<F[vv>>F][^^<<F]]]][--<F[++>F][--<F][++>F[vv>>F][^^<<F]][--<F[++>F][--<F]][vv>>F[++>F][--<F][++>F[++>F][--<F]][--<F[++>F][--<F]]][^^<<F[++>F][--<F][++>F[vv>>F][^^<<F]][--<F[++>F][--<F]]]]][--<F[vv>>F][^^<<F][vv>>F[++>F][--<F]][^^<<F[++>F][--<F]][++>F[vv>>F][^^<<F][++>F[++>F][--<F]][--<F[++>F][--<F]]][--<F[++>F][--<F][++>F[++>F][--<F]][--<F[++>F][--<F]]][++>F[++>F][--<F][++>F[vv>>F][^^<<F]][--<F[++>F][--<F]][vv>>F[++>F][--<F][vv>>F[vv>>F][^^<<F]][^^<<F[++>F][--<F]]][^^<<F[vv>>F][^^<<F][++>F[vv>>F][^^<<F]][--<F[++>F][--<F]]]][--<F[++>F][--<F][++>F[++>F][--<F]][--<F[++>F][--<F]][++>F[vv>>F][^^<<F][++>F[++>F][--<F]][--<F[++>F][--<F]]][--<F[++>F][--<F][++>F[++>F][--<F]][--<F[vv>>F][^^<<F]]]]]]"
#grammar = "[-[-F]F[F[-F-vv>F][v>F]]]F[+F][-F][vF][^F]F[F[+F][-F][vF][^F]F[-[-F]F[F[-F-vv>F][v>F]]-vv>F[+F][-F][vF][^F]F][v>[-F]F[F[-F-vv>F][v>F]]]]"
#grammar = "F[-F[^^FB]]"
#grammar = "F"
#( self, word, name, angle, angleChange, rad, radChange, length, lengthChange, point )
#interpreter = Make( grammar, "Tree", [1.5708,0,1.5708], .3, 1, .8, 10, .95, (0,0,0), (0,0,0), (0,0,0), (0.4,0.15,0.12) )