import maya.cmds as cmds
import math

class Make:

    #firstBranch = True
    currLevel = 0
    val = 0
    
    branchStack = []  #filled with branches
    allBranchCurves = [] #all completed branch curve names to add polygons to

    '''
    word: (string) the grammar to be used to create the l-systems
    name: (string) root name of the tree to be created
    angle: ([i,j,k]) starting angle vector of tree, usually [0,1,0]
    angleChange: (decimal) a number between (0,1) for the angle to change, should NOT multiply into 1
    rad: (decimal) radius of the root
    length: (decimal) staring length of the branch
    point: ((x,y,z)) starting point of the tree
    '''
    
    def __init__( self, word, name, angle, angleChange, rad, length, point ):
        # F[&+F]F[->FL][&FB]

        self.word = word
        self.name = name
        self.angle = angle #[theta, phi] = (angle z, angle x)
        self.angleChange = angleChange
        self.rad = rad
        self.length = length
        self.point = point #usually (0,0,0)

        if 1 % self.angleChange == 0:
            self.angleChange += 0.01

        #taper?

        for let in self.word:
            self.runCommand(let)
        
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

    def createBranch( self, point, currAngle, length ):
        
        #make sure has all!!
        
        branch = {
            "point" : point,
            "angle" : currAngle,
            "length" : length
        }

        return branch

    def forward( self ): 
        #if Make.firstBranch == True:

        #points = [(0, 0, 0), (3, 5, 6), (5, 6, 7), (9, 9, 9)]
        #taper?
        
        self.length *= .95
        #(self.length)
        
        # spherical to cartesian coordinates
        #z = self.point[0] + ( self.length * math.cos(self.angle[0]) * math.sin(self.angle[1]) )  
        #x = self.point[1] + ( self.length * math.sin(self.angle[0]) * math.sin(self.angle[1]) )
        #y = self.point[2] + ( self.length * math.cos(self.angle[1]) )

        x = self.point[0] + ( self.length * self.angle[0] )  
        y = self.point[1] + ( self.length * self.angle[1] )  
        z = self.point[2] + ( self.length * self.angle[2] )  


        
        nextPoint = ( x, y, z )
        points = [self.point, nextPoint]

        curveName = self.name+"_curve_"+str(self.val)
        cmds.curve( name=curveName, p=points, d=1 ) 


        Make.val += 1
        Make.currLevel += 1
        self.point = nextPoint


        Make.allBranchCurves.append(curveName)

        print(curveName + " " + str(x)+ " " + str(y)+ " " + str(z) )
        #PARENT!!!!

            
        ### create geometry ###
        #cmds.polyCylinder(name="base", subdivisionsX=5, subdivisionsY=0, r=5)
        #move cylinder to origin pt
        #cmds.select("curve")
        #cmds.select("base", tgl=True)
        #path = cmds.pathAnimation(fractionMode=True, follow=True, followAxis='y', upAxis='x', startTimeU=True) #move polygon to start and align with normal

        #cmds.select("base", deselect=True)
        #cmds.select("base.f[13]")
        #cmds.polyExtrudeFacet( inputCurve="curve", d=10 )

        #union all together

    def createLeaf( self ):
        """
        TODO
        """

    def createBlossom( self ):
        """
        TODO
        """

    def rotate( self, newAngle, axis ):
        
        #spherical
        #[theta, phi] = (angle z, angle x)
        
        self.angle[axis] += newAngle
        
        #DO WARNING IF MAG HITS 0
        if self.angle == [0,0,0]:
            self.angle[axis] -= newAngle
        #print("\nangle" + str(self.angle))
        
        mag = math.sqrt(math.pow(self.angle[0],2) + math.pow(self.angle[1],2) + math.pow(self.angle[2],2))

        for i in range(len(self.angle)):
            self.angle[i] /= mag

        print("angle" + str(self.angle) + " mag" + str(mag))


    def pushToStack( self ):

        #pushes current settings (point, angle) as a new branch dict to branchStack

        
        #add val to parameters?

        newBranch = self.createBranch( self.point, self.angle, self.length )  #check all parameters entered
        self.branchStack.append(newBranch)



    def popFromStack( self ):

        #pops branch from BranchStack to return turtle to previous branch
        #reset settings to popped branch's settings

        #Make sure all parameters resetted!!!

        pastBranch = self.branchStack.pop()
        self.point = pastBranch["point"]
        self.angle = pastBranch["angle"]
        self.length = pastBranch["length"]

        









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
#grammar = "F[-<[-<F]F[F[->>F+vvF][v+F]]][-<F]F[F[->>F+vvF][v+F]][[-<F]F[F[->>F+^^F][v+F]][->>[-<F]F[F[->>F+^^F][v+F]]+^^[-<F]F[F[->>F+^^F][v+F]]][v+[-<F]F[F[->>F+^^F][v+F]]]]"
#grammar = "F[-F][+F]"
grammar = "F^FvvFvF+F-F"
#( self, word, name, angle, angleChange, rad, length, point )
interpreter = Make( grammar, "Tree", [0,1,0], .3, 5, 10, (0,0,0) )
