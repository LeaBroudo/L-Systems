import maya.cmds as cmds
import math
import copy

class Make:

    #firstBranch = True
    currLevel = 0
    val = 0
    
    branchStack = []  #filled with branches
    allBranchCurves = [] #all completed branch curve names to add polygons to
    prevPoints = [] #used for error checking if a curve has already been placed in the position

    parent = None

    '''
    word: (string) the grammar to be used to create the l-systems
    name: (string) root name of the tree to be created
    angle: ([i,j,k]) starting angle vector of tree, usually [0,1,0]
    angleChange: (decimal) a number between (0,1) for the angle to change, should NOT multiply into 1
    rad: (decimal) radius of the root
    length: (decimal) staring length of the branch
    lengthChange: (decimal) a number between (0,1) for the length to change at each level
    point: ((x,y,z)) starting point of the tree
    '''
    
    def __init__( self, word, name, angle, angleChange, rad, length, lengthChange, point ):
        # F[&+F]F[->FL][&FB]

        self.word = word
        self.name = name
        self.angle = angle #[alpha, beta, gamma]
        self.angleChange = angleChange
        self.rad = rad
        self.length = length
        self.lengthChange = lengthChange
        self.point = point #usually (0,0,0)

        #taper?

        #runs the commands in the grammar to create curve skeleton of tree
        for let in self.word:
            self.runCommand(let)
        
        #Adds polygon mesh to skeleton
        self.addMesh()

        #Unions polygons together, averages vertices a bit
        self.cleanUp()

        
        
            
            

        
        #add shaders

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
        [   : push turte state to stack
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

        #taper?
        
        #Decreases length during depth change
        self.length *= self.lengthChange

        #endpoint
        x = self.point[0] + ( self.length * math.cos(self.angle[0]) )  
        y = self.point[1] + ( self.length * math.cos(self.angle[1]) )  
        z = self.point[2] + ( self.length * math.cos(self.angle[2]) )  
        endPoint = ( x, y, z )
        diff = ( x-self.point[0], y-self.point[1], z-self.point[2] )

        #Dr. Seuss Curvy Trees
        #midpoint_1 = ( self.point[0] + .3*x, self.point[1] + .3*y, self.point[2] + .3*z )
        #midpoint_2 = ( self.point[0] + .6*x, self.point[1] + .6*y, self.point[2] + .6*z )
        
        #creates two points to go along curve
        midpoint_1 = ( self.point[0] + .3*diff[0], self.point[1] + .3*diff[1], self.point[2] + .3*diff[2] )
        midpoint_2 = ( self.point[0] + .6*diff[0], self.point[1] + .6*diff[1], self.point[2] + .6*diff[2] )
        
        #creates array of curve points
        points = [self.point, midpoint_1, midpoint_2, endPoint]
        #(points)

        #if a curve has aready been placed at that point, returns and does not finish forward function
        for prev in Make.prevPoints:
            if points == prev:
                self.point = endPoint #makes sure that the start point for the next curve is correct
                return  
        #If no curve placed there, curve points placed into prevPoints array
        Make.prevPoints.append(points)

        #Names Curve
        curveName = self.name+"_curve_"+str(self.val)
        cmds.curve( name=curveName, p=points, d=3 ) 

        #Updates settings
        Make.val += 1
        Make.currLevel += 1
        self.point = endPoint
        Make.parent = curveName

        #print(curveName + " " + str(x)+ " " + str(y)+ " " + str(z) )
        #print(curveName + " " + str(self.length) + "\n" )
        
        #PARENT!!!!
        #if( Make.parent != None ):
            #cmds.parent(curveName, Make.parent)
        
        

        #Completed branch added to array
        Make.allBranchCurves.append(curveName)


    def createLeaf( self ):
        """
        TODO
        """

    def createBlossom( self ):
        """
        TODO
        """

    def rotate( self, newAngle, axis ):
    
        self.angle[axis] += newAngle
        
        #mag = math.sqrt(math.pow(self.angle[0],2) + math.pow(self.angle[1],2) + math.pow(self.angle[2],2))

        #print("angle" + str(self.angle) + " mag" + str(mag))


    def pushToStack( self ):

        #pushes current settings (point, angle) as a new branch dict to branchStack

        
        #add val to parameters?

        
        newBranch = {
            "point" : copy.deepcopy(self.point),
            "angle" : copy.deepcopy(self.angle),
            "length" : copy.deepcopy(self.length),
            "parent" : copy.deepcopy(Make.parent)
        }
        #check all parameters entered!!!

        self.branchStack.append(newBranch)
        print("pushed")
        print(newBranch)



    def popFromStack( self ):

        #pops branch from BranchStack to return turtle to previous branch
        #reset settings to popped branch's settings

        #Make sure all parameters resetted!!!

        pastBranch = self.branchStack.pop()
        self.point = pastBranch["point"]
        self.angle = pastBranch["angle"]
        self.length = pastBranch["length"]
        Make.parent = pastBranch["parent"]
        print("popped")
        print(pastBranch)

        
    def addMesh( self ):
        Make.val = 0
        
        for curve in Make.allBranchCurves:
            
            trunkName = self.name + "_trunk_" + str(Make.val)
            
            cmds.polyCylinder(name=trunkName, subdivisionsX=5, subdivisionsY=1, r=self.rad)
            #move cylinder to origin pt
            #cmds.move( -1, trunkName+".scalePivot", trunkName+".rotatePivot", moveY=True, relative=True)
            

            
            cmds.select(all=True, deselect=True)
            cmds.select(trunkName, tgl=True)
            cmds.select(curve, add=True)
            cmds.pathAnimation( follow=True, followAxis='y', upAxis='z', startTimeU=True) #move polygon to start and align with normal
            
            cmds.select(all=True, deselect=True)
            cmds.select(trunkName + ".f[6]")
            cmds.polyExtrudeFacet( inputCurve=curve, d=1 )

            Make.val += 1


    def cleanUp( self ):
        #union all together, and smooth!!
        
        #works range 0-6
        for sectNum in range(0, Make.val-1): #might be one off?

            #Unions pairs of two branches into "sections"
            if sectNum == 0:
                firstB = "Tree_trunk_"+str(sectNum)  #Tree_trunk_0
                secondB = "Tree_trunk_"+str(sectNum+1)  #Tree_trunk_1
                cmds.polyBoolOp( firstB, secondB, op=1, n="sect_"+str(sectNum) ) #sect_0
            else:
                lastSect = "sect_"+str(sectNum-1)
                nextB = "Tree_trunk_"+str(sectNum+1)
                cmds.polyBoolOp( lastSect, nextB, op=1, n="sect_"+str(sectNum) )





    def shaderBranch( self, branchColor ):

        branchMaterial = cmds.shadingNode( 'lambert', asShader=True, name="??") #finish line!!!
        cmds.setAttr( branchMaterial+'.color', branchColor[0], branchColor[1], branchColor[2])
        branchSG = cmds.sets(empty=True, renderable=True, noSurfaceShader=True, name="??")
        cmds.connectAttr( branchMaterial + '.outColor', branchSG + '.surfaceShader', force=True ) #what does force do?


    def shaderBlossom( self, blossomColor ):
        #same as shaderBranch, just multiple times w/ diff parts of flower
        """
        TODO
        """

    def shaderLeaf( self, leafColor ):
        """
        TODO
        """

    def setShader( self, geometry, shaderType ):
        """
        TODO
        """
        #applies correct shader based on geometry



#############

#grammar = "F[-[-[-FL]F[F[-FB-vvF][v>F]]L][-FL]F[F[-FB-vvF][v>F]][[-FL]F[F[-FB-vvF][v>F]][-[-FL]F[F[-FB-vvF][v>F]]B-vv[-FL]F[F[-FB-vvF][v>F]]][v>[-FL]F[F[-FB-vvF][v>F]]]]L][-[-FL]F[F[-FB-vvF][v>F]]L][-FL]F[F[-FB-vvF][v>F]][[-FL]F[F[-FB-vvF][v>F]][-[-FL]F[F[-FB-vvF][v>F]]B-vv[-FL]F[F[-FB-vvF][v>F]]][v>[-FL]F[F[-FB-vvF][v>F]]]][[-[-FL]F[F[-FB-vvF][v>F]]L][-FL]F[F[-FB-vvF][v>F]][[-FL]F[F[-FB-vvF][v>F]][-[-FL]F[F[-FB-vvF][v>F]]B-vv[-FL]F[F[-FB-vvF][v>F]]][v>[-FL]F[F[-FB-vvF][v>F]]]][-[-[-FL]F[F[-FB-vvF][v>F]]L][-FL]F[F[-FB-vvF][v>F]][[-FL]F[F[-FB-vvF][v>F]][-[-FL]F[F[-FB-vvF][v>F]]B-vv[-FL]F[F[-FB-vvF][v>F]]][v>[-FL]F[F[-FB-vvF][v>F]]]]B-vv[-[-FL]F[F[-FB-vvF][v>F]]L][-FL]F[F[-FB-vvF][v>F]][[-FL]F[F[-FB-vvF][v>F]][-[-FL]F[F[-FB-vvF][v>F]]B-vv[-FL]F[F[-FB-vvF][v>F]]][v>[-FL]F[F[-FB-vvF][v>F]]]]][v>[-[-FL]F[F[-FB-vvF][v>F]]L][-FL]F[F[-FB-vvF][v>F]][[-FL]F[F[-FB-vvF][v>F]][-[-FL]F[F[-FB-vvF][v>F]]B-vv[-FL]F[F[-FB-vvF][v>F]]][v>[-FL]F[F[-FB-vvF][v>F]]]]]]"
grammar = "F[-<[-<F]F[F[->>F+^^F][v+F]]][-<F]F[F[->>F+^^F][v+F]][[-<F]F[F[->>F+^^F][v+F]][->>[-<F]F[F[->>F+^^F][v+F]]+^^[-<F]F[F[->>F+^^F][v+F]]][v+[-<F]F[F[->>F+^^F][v+F]]]]"
#grammar = "F[-F][+F]F"
#grammar = "F[-F]FF"
#( self, word, name, angle, angleChange, rad, length, lengthChange, point )
interpreter = Make( grammar, "Tree", [1.5708,0,1.5708], .3, 1, 10, .95, (0,0,0) )