import maya.cmds as cmds
import pydoc
from string_write import *
from interpreter import *



def createUI():
    #if cmds.window("window", exists = True):
    #    print("window existed")
    #    cmds.deleteUI("window")
    
    window = cmds.window( title="window", widthHeight=(400, 500) )
    cmds.columnLayout( adjustableColumn=True )
    cmds.text(label="L-System Tree Generator", font="boldLabelFont")

    #cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1, 406)],)
    cmds.intSliderGrp( "depthIntField", l="Depth: ", v=3, cw3=[40,30,200], min=1, max=10, fmx=20, f=True)
    
    #axiom
    cmds.rowColumnLayout( nc=2, cw=[(1,40),(2,30)], p=window )
    cmds.text("Axiom:")
    cmds.textField( "axiomTextField", en=True, tx="F")
    
    #Rule columns
    cmds.rowColumnLayout( nc=7, cal=[(1,"right")], cw=[(1,40),(2,30),(3,20),(4,245),(5,40),(6,5),(7,20)], p=window )
    
    #Rule 1
    cmds.text( l="Rule 1: ", en=True )
    cmds.textField( "prodRulePred1", en=True, tx="F" )
    cmds.text( l="->", en=True )
    cmds.textField( "prodRuleSucc1", en=True, tx="F[&+F]F[->FL][&FB]" )
    cmds.intField( "prodRuleProb1", minValue=0, maxValue=100, value=100)
    cmds.separator( st="none" )
    cmds.separator( st="none" )
    

    #Rule 2
    cmds.text( l="Rule 2: ", en=True )
    cmds.textField( "prodRulePred2", en=True )
    cmds.text( l="->", en=True )
    cmds.textField( "prodRuleSucc2", en=True )
    cmds.intField( "prodRuleProb2", minValue=0, maxValue=100, value=0 )
    cmds.separator( st="none" )
    cmds.checkBox( 'prodRuleCheckBox2', v=False )

    #Rule 3
    cmds.text( l="Rule 3: ", en=True )
    cmds.textField( "prodRulePred3", en=True)
    cmds.text( l="->", en=True )
    cmds.textField( "prodRuleSucc3", en=True)
    cmds.intField( "prodRuleProb3", minValue=0, maxValue=100, value=0 )
    cmds.separator( st="none" )
    cmds.checkBox( 'prodRuleCheckBox3', v=False )

    #depth
    #cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1, 406)],)
    #cmds.intSliderGrp( "depthIntField", l="Depth: ", v=3, cw3=[40,30,200], min=1, max=10, fmx=20, f=True)
    
    lstring = ""
    def generateString(*args):
        ''' Queries all the fields related to the string generation and calls the procedure. '''
        axiom = cmds.textField( "axiomTextField", q=True, tx=True )
        depth = cmds.intSliderGrp( "depthIntField", q=True, v=True )

        rules = []

        prodRuleProb1 = str(cmds.intField( "prodRuleProb1", q=True, v=True ))
        prodRulePred1 = str(cmds.textField( "prodRulePred1", q=True, tx=True ))
        prodRuleSucc1 = str(cmds.textField("prodRuleSucc1", q=True, tx=True))

        prodRuleCheckBox2 = cmds.checkBox( "prodRuleCheckBox2", q=True, value=True )
        prodRuleProb2 = str(cmds.intField( "prodRuleProb2", q=True, v=True ))
        prodRulePred2 = str(cmds.textField( "prodRulePred2", q=True, tx=True ))
        prodRuleSucc2 = str(cmds.textField("prodRuleSucc2", q=True, tx=True))

        prodRuleCheckBox3 = cmds.checkBox( "prodRuleCheckBox3", q=True, value=True )
        prodRuleProb3 = str(cmds.intField( "prodRuleProb3", q=True, v=True ))
        prodRulePred3 = str(cmds.textField( "prodRulePred3", q=True, tx=True ))
        prodRuleSucc3 = str(cmds.textField("prodRuleSucc3", q=True, tx=True))

        rules.append([prodRuleProb1, prodRulePred1, prodRuleSucc1])
        if prodRuleCheckBox2 == True:
            rules.append([prodRuleProb2, prodRulePred2, prodRuleSucc2]) 
        if prodRuleCheckBox3 == True:
            rules.append([prodRuleProb3, prodRulePred3, prodRuleSucc3]) 
        

        # ensure sum of all probabilities is 100.
        probSum = int(prodRuleProb1) + int(prodRuleProb2) + int(prodRuleProb3)
        if probSum > 100:
            cmds.textField( "warningsTextField", edit=True, tx="Be careful with percentages. They don't add to 100." )
            cmds.textField( "output", edit=True, tx="ERROR. Take a look at the warning text line." )
        else:
            lstring = writeString( axiom, rules, depth )
            cmds.textField( "string_output", edit=True, tx=lstring )

    
    #cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1,100), (2,10), (3,230)], p=window)
    cmds.button( label='Generate String', command=generateString )
    cmds.separator( h=5, st="none" )
    cmds.textField("string_output")

    cmds.rowColumnLayout( numberOfColumns=7, columnWidth=[(1,80), (2,40), (3,30), (4,40), (5,30), (6,40), (7,30),], p=window)
    cmds.text("Starting Point:", en=True)
    cmds.text("x: ", en=True)
    cmds.textField( "xPoint", en=True, tx="0")
    cmds.text("y: ", en=True)
    cmds.textField( "yPoint", en=True, tx="0")
    cmds.text("z: ", en=True)
    cmds.textField( "zPoint", en=True, tx="0")
    
    #word, name, angle, angleChange, rad, radChange, length, lengthChange, point, leafColor, blossColor, trunkColor
    cmds.rowColumnLayout( nc=2, cw=[(1,40),(2,30)], p=window )
    cmds.text("Name: ", en=True)
    cmds.textField( "tree_name", en=True, tx="Tree") #must connect this to some variable
    tree_name = "Tree"

    cmds.rowColumnLayout( numberOfColumns=7, columnWidth=[(1,80), (2,40), (3,30), (4,40), (5,30), (6,40), (7,30),], p=window)
    cmds.text("Angle:", en=True )
    cmds.text("x: ", en=True)
    cmds.textField( "xAngle", en=True, tx="1.5708" )
    cmds.text("y: ", en=True)
    cmds.textField( "yAngle", en=True, tx="0")
    cmds.text("z: ", en=True)
    cmds.textField( "zAngle", en=True, tx="1.5708")
    
    cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1,410)], p=window )
    cmds.intSliderGrp( "angle_atenuation", l="Angle Atenuation: ", v=95, cw3=[92,40,788], min=0, max=100, fmx=100, f=True )
    cmds.floatSliderGrp( "radius", l="Segment Radius: ", pre=2, v=0.20, cw3=[92,40,788], min=0, max=0.5, fmx=2, f=True )
    cmds.intSliderGrp( "radius_atenuation", l="Rad. Atenuation: ", v=85, cw3=[92,40,788], min=0, max=100, fmx=100, f=True )
    cmds.floatSliderGrp( "length", l="Segment Length: ", pre=2, v=1.20, cw3=[92,40,788], min=0, max=10, fmx=100, f=True )
    cmds.intSliderGrp( "length_atenuation", l="Len. Atenuation: ", v=95, cw3=[92,40,788], min=0, max=100, fmx=100, f=True )
    cmds.colorSliderGrp( "rgb_branchField", l="Branches: ", rgb=(0.430,0.230,0.11), cw3=[52,30,328], ann="Branch colour." )
    cmds.separator( h=6, st="none" )
    cmds.colorSliderGrp( "rgb_leafField", l="Leaves: ", rgb=(0,0.624,0), cw3=[52,30,328], ann="Leaf colour." )
    cmds.separator( h=6, st="none" )
    cmds.colorSliderGrp('rgb_blossomField', l="Blossoms: ", rgb=(0.624,0,0), cw3=[52,30,328], ann="Blossoms colour." )
    cmds.separator( h=2, st="none" )
    


    #Generate Mesh
    def generateMesh(*args):
        #lstring
        #word, name, angle, angleChange, rad, radChange, length, lengthChange, point, leafColor, blossColor, trunkColor
        name = cmds.textField( "tree_name", q=True, tx=True )
        
        xAngle = cmds.text("xAngle: ", q=True, tx=True )
        yAngle = cmds.text("yAngle: ", q=True, tx=True )
        zAngle = cmds.text("zAngle: ", q=True, tx=True )
        
        angleChange = cmds.intSliderGrp( "angle_atenuation", q=True, tx=True )
        rad = cmds.floatSliderGrp( "radius", q=True, tx=True )
        radChange = cmds.intSliderGrp( "radius_atenuation", q=True, tx=True )
        length = cmds.floatSliderGrp( "length", q=True, tx=True )
        lengthChange = cmds.intSliderGrp( "length_atenuation", q=True, tx=True )
        
        xPoint = cmds.text("xPoint: ", q=True, tx=True )
        yPoint = cmds.text("yPoint: ", q=True, tx=True )
        zPoint = cmds.text("zPoint: ", q=True, tx=True )

        leafColor = cmds.colorSliderGrp( "rgb_branchField", q=True, tx=True )
        blossColor = cmds.colorSliderGrp('rgb_blossomField', q=True, tx=True )
        trunkColor = cmds.colorSliderGrp( "rgb_leafField", q=True, tx=True )
        
        Make( lstring, name, [xAngle,yAngle,zAngle], angleChange, rad, radChange, length, lengthChange, (xPoint,yPoint,zPoint), leafColor, blossColor, trunkColor )
    
    
    
    cmds.rowColumnLayout( numberOfColumns=1, p=window )
    cmds.button( label='Generate Mesh', command=generateMesh )


    #close UI
    def closeUI(*args):
        cmds.deleteUI(window)
    
    cmds.button( label='close', command=closeUI )
    
    

    #cmds.setParent( '..' )
    cmds.showWindow( window )