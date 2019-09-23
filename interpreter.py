import maya.cmds as cmds
import math

class Make:

    #firstBranch = True
    currLevel = 0
    val = 0
    
    branchStack = []  #filled with branches
    allBranchCurves = [] #all completed branch curve names to add polygons to

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

        for let in self.word:
            self.runCommand(let)
        
        #add mesh
        Make.val = 0
        totalTree = ""
        for curve in Make.allBranchCurves:
            trunkName = name + "_trunk_" + str(Make.val)
            
            cmds.polyCylinder(name=trunkName, subdivisionsX=5, subdivisionsY=1, r=self.rad)
            #move cylinder to origin pt
            #cmds.move( -1, trunkName+".scalePivot", trunkName+".rotatePivot", moveY=True, relative=True)
            
            print(curve)
            
            cmds.select(all=True, deselect=True)
            cmds.select(trunkName, tgl=True)
            cmds.select(curve, add=True)
            cmds.pathAnimation( follow=True, followAxis='y', upAxis='z', startTimeU=True) #move polygon to start and align with normal
            
            
            
            #cmds.select( all=True, deselect=True)
            #cmds.select(trunkName)
            #cmds.move( .2, objectSpace=True, moveY=True )


            cmds.select(all=True, deselect=True)
            cmds.select(trunkName + ".f[6]")
            cmds.polyExtrudeFacet( inputCurve=curve, d=1 )

            Make.val += 1

            #union of all
            #if( totalTree == "" ):
            #    totalTree = trunkName
            #else:
                #parent?
            #    cmds.select( all=True, deselect=True)
            #    cmds.select(trunkName, tgl=True)
            #    cmds.select(totalTree, add=True)
            #    cmds.polyBoolOp( totalTree, trunkName, op=1, n=totalTree )
            

        #union all together, and smooth!!
        totalTree = "Total_Tree"
        for val in range(0, Make.val): #might be one off?
            
            cmds.select( clear=True )
            cmds.select("Tree_trunk_" + str(val+1), add=True)

            if val == 0:
                cmds.select("Tree_trunk_" + str(val))
                cmds.polyBoolOp( "Tree_trunk_" + str(val), "Tree_trunk_" + str(val+1), op=1, n=totalTree )
            else:
                cmds.select(totalTree)
                cmds.polyBoolOp( totalTree, "Tree_trunk_" + str(val+1), op=1, n=totalTree )
            
            
            
            

        
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
        print(points)


        #Names Curve
        curveName = self.name+"_curve_"+str(self.val)
        cmds.curve( name=curveName, p=points, d=3 ) 

        #Updates settings
        Make.val += 1
        Make.currLevel += 1
        self.point = endPoint
        Make.parent = curveName

        #print(curveName + " " + str(x)+ " " + str(y)+ " " + str(z) )
        print(curveName + " " + str(self.length) + "\n" )
        
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
        
        mag = math.sqrt(math.pow(self.angle[0],2) + math.pow(self.angle[1],2) + math.pow(self.angle[2],2))

        #print("angle" + str(self.angle) + " mag" + str(mag))


    def pushToStack( self ):

        #pushes current settings (point, angle) as a new branch dict to branchStack

        
        #add val to parameters?

        
        newBranch = {
            "point" : self.point,
            "angle" : self.angle,
            "length" : self.length,
            "parent" : Make.parent
        }
        #check all parameters entered!!!

        self.branchStack.append(newBranch)



    def popFromStack( self ):

        #pops branch from BranchStack to return turtle to previous branch
        #reset settings to popped branch's settings

        #Make sure all parameters resetted!!!

        pastBranch = self.branchStack.pop()
        self.point = pastBranch["point"]
        self.angle = pastBranch["angle"]
        self.length = pastBranch["length"]
        Make.parent = pastBranch["parent"]

        









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

    def createSegment( self, word, rules, ogPosX, ogPosY, ogPosZ , ogRotX, ogRotY, ogRotZ, subdiv, currlevel, lenScale, radScale, branchColor ):
        """
        TODO
        """
        #Why not extrude out of previous branch instead?
        # make new cmds.polyCylinder
        # cmds.xform?
        # apply shader
        # parent branch 

    def createGeometry( self, word, rad, stepLen, angle, subDiv, lenScale, radScale, turtleSpeed, branchColor, leafColor, blossomColor ):
        """
        TODO
        """

        # set intl pos and rot as 0,0,0
        # iterate over each string character, find what it is (F, +, [,...)

#############

#grammar = "F[-[-[-FL]F[F[-FB-vvF][v>F]]L][-FL]F[F[-FB-vvF][v>F]][[-FL]F[F[-FB-vvF][v>F]][-[-FL]F[F[-FB-vvF][v>F]]B-vv[-FL]F[F[-FB-vvF][v>F]]][v>[-FL]F[F[-FB-vvF][v>F]]]]L][-[-FL]F[F[-FB-vvF][v>F]]L][-FL]F[F[-FB-vvF][v>F]][[-FL]F[F[-FB-vvF][v>F]][-[-FL]F[F[-FB-vvF][v>F]]B-vv[-FL]F[F[-FB-vvF][v>F]]][v>[-FL]F[F[-FB-vvF][v>F]]]][[-[-FL]F[F[-FB-vvF][v>F]]L][-FL]F[F[-FB-vvF][v>F]][[-FL]F[F[-FB-vvF][v>F]][-[-FL]F[F[-FB-vvF][v>F]]B-vv[-FL]F[F[-FB-vvF][v>F]]][v>[-FL]F[F[-FB-vvF][v>F]]]][-[-[-FL]F[F[-FB-vvF][v>F]]L][-FL]F[F[-FB-vvF][v>F]][[-FL]F[F[-FB-vvF][v>F]][-[-FL]F[F[-FB-vvF][v>F]]B-vv[-FL]F[F[-FB-vvF][v>F]]][v>[-FL]F[F[-FB-vvF][v>F]]]]B-vv[-[-FL]F[F[-FB-vvF][v>F]]L][-FL]F[F[-FB-vvF][v>F]][[-FL]F[F[-FB-vvF][v>F]][-[-FL]F[F[-FB-vvF][v>F]]B-vv[-FL]F[F[-FB-vvF][v>F]]][v>[-FL]F[F[-FB-vvF][v>F]]]]][v>[-[-FL]F[F[-FB-vvF][v>F]]L][-FL]F[F[-FB-vvF][v>F]][[-FL]F[F[-FB-vvF][v>F]][-[-FL]F[F[-FB-vvF][v>F]]B-vv[-FL]F[F[-FB-vvF][v>F]]][v>[-FL]F[F[-FB-vvF][v>F]]]]]]"
grammar = "F[-<[-<F]F[F[->>F+^^F][v+F]]][-<F]F[F[->>F+^^F][v+F]][[-<F]F[F[->>F+^^F][v+F]][->>[-<F]F[F[->>F+^^F][v+F]]+^^[-<F]F[F[->>F+^^F][v+F]]][v+[-<F]F[F[->>F+^^F][v+F]]]]"
#grammar = "F[-F][+F]"
#grammar = "F--F"
#( self, word, name, angle, angleChange, rad, length, lengthChange, point )
interpreter = Make( grammar, "Tree", [1.5708,0,1.5708], .3, 2, 10, .95, (0,0,0) )