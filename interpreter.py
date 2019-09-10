import maya.cmds as cmds
import math

class Make:

    #firstBranch = True
    currLevel = 0
    val = 0
    
    branchStack = []  #filled with branches
    allBranchCurves = [] #all completed branch curve names to add polygons to

    
    def __init__( self, word, name, angle, angleChange, rad, length, point ):
        # F[&+F]F[->FL][&FB]

        self.word = word
        self.name = name
        self.angle = angle #[theta, phi] = (angle z, angle x)
        self.angleChange = angleChange
        self.rad = rad
        self.length = length
        self.point = point #usually (0,0,0)

        #taper?

        for let in self.word:
            self.runCommand(let)
        
        #add shaders

    def runCommand( self, char ):
        '''
        F/f : Move forward
        L/l : Leaf
        B/b : Blossom
        +   : Rotate +theta
        -   : Rotate -theta
        ^   : Rotate +phi
        v   : Rotate -phi
        #<   : Rotate +Z 
        #>   : Rotate -Z 
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
            self.rotate(self.angleChange, 0)  
        if char == '-': 
            self.rotate(self.angleChange*-1, 0)      
        if char == '^': 
            self.rotate(self.angleChange, 1)     
        if char == 'v': 
            self.rotate(self.angleChange*-1, 1)      
        #if char == '<': 
        #    self.rotate(self.angleChange, 2)       
        #if char == '>': 
        #    self.rotate(self.angleChange*-1, 2)
        if char == '[':
            self.pushToStack() 
        if char == ']':
            self.popFromStack()

    def createBranch( self, point, currAngle, level ):
        
        #make sure has all!!
        
        branch = {
            "point" : point,
            "angle" : currAngle,
            "level" : level
        }

        return branch

    def forward( self ): 
        #if Make.firstBranch == True:

        #points = [(0, 0, 0), (3, 5, 6), (5, 6, 7), (9, 9, 9)]
        #taper?
        
        # spherical to cartesian coordinates
        x = self.point[0] + ( self.length * math.cos(self.angle[0]) * math.sin(self.angle[1]) )  
        y = self.point[1] + ( self.length * math.sin(self.angle[0]) * math.sin(self.angle[1]) )
        z = self.point[2] + ( self.length * math.cos(self.angle[1]) )
        
        nextPoint = ( x, y, z )
        points = [self.point, nextPoint]

        curveName = self.name+"_curve_"+str(self.val)
        cmds.curve( name=curveName, p=points, d=1 ) #divisions??? will complain about curve


        Make.val += 1
        Make.currLevel += 1
        self.point = nextPoint


        Make.allBranchCurves.append(curveName)

            
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

    def pushToStack( self ):

        #pushes current settings (point, angle) as a new branch dict to branchStack

        
        #add val to parameters?

        newBranch = self.createBranch( self.point, self.angle, Make.currLevel )  #check all parameters entered
        self.branchStack.append(newBranch)



    def popFromStack( self ):

        #pops branch from BranchStack to return turtle to previous branch
        #reset settings to popped branch's settings

        #Make sure all parameters resetted!!!

        pastBranch = self.branchStack.pop()
        self.point = pastBranch["point"]
        self.angle = pastBranch["angle"]
        Make.currLevel = pastBranch["level"]

        









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

#grammar = "F[&+F]F[->FL][&FB]"
grammar = "--F"
#( self, word, name, angle, angleChange, rad, length, point )
interpreter = Make( grammar, "Tree", [0,0], 10, 5, 10, (0,0,0) )
