import maya.cmds as cmds
import numpy as np

class Interpreter:

    #firstBranch = True
    currLevel = 0
    val = 0
    
    branchStack = []  #filled with branches
    allBranchCurves = [] #all completed branch curves to add polygons to

    
    def __init__( self, word, name, angle, rad, length, point ):
        # F[&+F]F[->FL][&FB]

        self.word = word
        self.name = name
        self.angle = angle #[0,0,0]
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
        +   : Rotate +X
        -   : Rotate -X
        ^   : Rotate +Y
        v   : Rotate -Y
        <   : Rotate +Z 
        >   : Rotate -Z 
        [   : push turte state to stack
        ]   : pop turtle state from stack
        '''

        if char == 'f' or char == 'F': 
            self.forward(0.5)
        if char == 'l' or char == 'L':
            self.createLeaf()   
        if char == 'b' or char == 'B':
            self.createBlossom()     
        if char == '+': 
            self.rotate(self.angle, 0)  
        if char == '-': 
            self.rotate(self.angle*-1, 0)      
        if char == '^': 
            self.rotate(self.angle, 1)     
        if char == 'v': 
            self.rotate(self.angle*-1, 1)      
        if char == '<': 
            self.rotate(self.angle, 2)       
        if char == '>': 
            self.rotate(self.angle*-1, 2)
        if char == '[':
            self.pushToStack() 
        if char == ']':
            self.popFromStack()

    def createBranch( self, point, currAngle ):
        
        branch = {
            "point" : point,
            "angle" : currAngle
        }

        return branch

    def forward( self, length ):
        #if Interpreter.firstBranch == True:

        #points = [(0, 0, 0), (3, 5, 6), (5, 6, 7), (9, 9, 9)]
        #taper?
        
        x = point[0] + ( length * np.sin(angle[2]) * np.sin(angle[0]) )  #just do the math
        y = point[1] + ( length * np.sin(angle[2]) * np.cos(angle[0]) )
        z = point[2] + ( length * np.cos(angle[2]) )
        
        nextPoint = ( x, y, z )
        points = [point, nextPoint]

        cmds.curve( name=name+"_curve"+str(val), p=points ) #divisions??? will complain about curve


        val += 1
        point = nextPoint

            
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
        self.angle[axis] += newAngle

    def pushToStack( self ):

        #pushes current settings (point, angle) as a new branch dict to branchStack

        
        #add val to parameters?

        newBranch = createBranch( self, self.point, self.angle )  #check all parameters entered
        branchStack.append(newBranch)



    def popFromStack( self ):

        #pops branch from BranchStack to return turtle to previous branch
        #reset settings to popped branch's settings

        #Make sure all parameters resetted!!!

        pastBranch = branchStack.pop()
        self.point = pastBranch["point"]
        self.angle = pastBranch["angle"]








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
grammar = "F"
interpreter = Interpreter( grammar, "Tree", 0, 5, 10 )
