"""
        F    Move forward
        f    Move forward
        L    Leaf
        B    Blossom
        +    Rotate +X (yaw right)
        -    Rotate -X (yaw left)
        ^    Rotate +Y (roll right)
        &    Rotate -Y (roll left)
        <    Rotate +Z (pitch down)
        >    Rotate -Z (pitch up)
        *    Turtle rotates 180 (as it was facing backwards)
        [    Push current turtle state on the stack
        ]    Pop the current turtle state from the stack

"""
import maya.cmds as cmds

def shaderBranch( branchColor ):
    """
    TODO
    """
    branchMaterial = cmds.shadingNode( 'lambert', asShader=True, name="??") #finish line!!!
    cmds.setAttr( branchMaterial+'.color', branchColor[0], branchColor[1], branchColor[2])
    branchSG = cmds.sets(empty=True, renderable=True, noSurfaceShader=True, name="??")
    cmds.connectAttr( branchMaterial + '.outColor', branchSG + '.surfaceShader', force=True ) #what does force do?
                                        

def shaderBlossom( blossomColor ):
    """
    TODO
    """

def shaderLeaf( leafColor ):
    """
    TODO
    """

def setShader( geometry, shaderType ):
    """
    TODO
    """
    #applies correct shader based on geometry

def createSegment( word, rules, ogPosX, ogPosY, ogPosZ , ogRotX, ogRotY, ogRotZ, subdiv, currlevel, lenScale, radScale, branchColor ):
    """
    TODO
    """

    # make new cmds.polyCylinder
    # cmds.xform?
    # apply shader
    # parent branch 

def createGeometry( word, rad, stepLen, angle, subDiv, lenScale, radScale, turtleSpeed, branchColor, leafColor, blossomColor ):
    """
    TODO
    """

    # set intl pos and rot as 0,0,0
    # iterate over each string character, find what it is (F, +, [,...)