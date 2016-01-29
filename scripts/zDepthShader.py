__author__ = 'zklinger'
import maya.cmds as cmds


class ZDepthShader(object):
    def __init__(self, imageName, dirName, oldMinX, oldMaxX):
        self._imageName = imageName
        self._dirName = dirName
        self._layerNum = imageName[11:14]
        self._surfaceShader = cmds.shadingNode('surfaceShader',
                                               n='zSurfaceShader_' +
                                               self._layerNum,
                                               asShader=True)
        self._layeredShader = cmds.shadingNode('layeredShader',
                                               n='zLayeredShader_' +
                                                 self._layerNum,
                                               asShader=True)
#setAttr "zLayeredShader_001.compositingFlag" 1
        cmds.setAttr(self._layeredShader + '.compositingFlag', 1)
        self._shaderGroup = cmds.sets(empty=True, renderable=True,
                                      noSurfaceShader=True,
                                      name='zDepthShaderSG_' +
                                           self._layerNum)
        #cmds.connectAttr(self._layeredShader + '.message',
        #                 self._shaderGroup + ".miMaterialShader",
        #                 force=True)
        #cmds.connectAttr(self._layeredShader + '.message',
        #                 self._shaderGroup + ".miPhotonShader",
        #                 force=True)
        #cmds.connectAttr(self._layeredShader + '.message',
        #                 self._shaderGroup + ".miShadowShader",
        #                 force=True)
        self._imgFile = cmds.shadingNode('file', n='zFile_' +
                                                   self._layerNum,
                                         asTexture=True)
        self._place2D = cmds.shadingNode('place2dTexture', n='zPlace2D',
                                         asUtility=True)
        # creating a reverse node to use in Transparency
        self._reverse = cmds.shadingNode('reverse',
                                         n='zReverse_' + self._layerNum,
                                         asUtility=True)
        # creating the samplerInfo node
        self._sampler = cmds.shadingNode('samplerInfo',
                                         n='zSamplerInfo' +
                                           self._layerNum,
                                         asUtility=True)
        self._distance = cmds.shadingNode('distanceBetween',
                                          n='zDistanceBetween' +
                                            self._layerNum,
                                          asUtility=True)
        self._range = cmds.shadingNode('setRange',
                                       n='zSetRange' + self._layerNum,
                                       asUtility=True)
#// Result: Connected samplerInfo1.pointCamera to distanceBetween1.point1. //
#connectAttr -f samplerInfo1.pointCamera distanceBetween1.point1;
        cmds.connectAttr(self._sampler + '.pointCamera', self._distance + '.point1',
                         force=True)
#connectAttr -f zDistanceBetween001.distance zSetRange001.valueX;
#// connecting zDistanceBetween001.distance to zSetRange001.value.valueX. //
        cmds.connectAttr(self._distance + '.distance', self._range + '.value.valueX')
        #setAttr "setRange1.minX" -1;

        self._ramp = cmds.shadingNode('ramp',
                                      n='zRamp' + self._layerNum,
                                      asUtility=True)
#setAttr ($node+".colorEntryList[0].position") 0;
        cmds.setAttr(self._ramp + '.colorEntryList[0].position', 0)
        cmds.setAttr(self._ramp + '.colorEntryList[0].color', 1, 1, 1)
        cmds.setAttr(self._ramp + '.colorEntryList[1].position', 1)
        cmds.setAttr(self._ramp + '.colorEntryList[1].color', 0, 0, 0)
        ### creating the multiplyDivide node
#        self._multDiv = cmds.shadingNode('multiplyDivide',
#                                         n='zMultDiv' + self._layerNum,
#                                         asUtility=True)
#### connecting multiplyDivide2.output.outputX to setRange2.value.valueX
####connectAttr -f multiplyDivide2.outputX setRange2.valueX;
#        cmds.connectAttr(self._multDiv + '.outputX',
#                         self._range + '.valueX',
#                         force=True)
####setAttr "multiplyDivide2.input2X" -1;
#        cmds.setAttr(self._multDiv + '.input2X', -1)
### connecting samplerInfo.pointCamera.pointCameraZ to multiplyDivide.input1.input1X
###connectAttr -f samplerInfo2.pointCameraZ multiplyDivide2.input1X;
#       cmds.connectAttr(self._sampler + '.pointCameraZ',
#                         self._multDiv + '.input1X',
#                         force=True)
#// Result: Connected setRange1.outValue.outValueX to ramp1.uvCoord.vCoord. //
#connectAttr -f setRange1.outValueX ramp1.vCoord;
        cmds.connectAttr(self._range + '.outValue.outValueX',
                         self._ramp + '.uvCoord.vCoord',
                         force=True)
#setAttr "zSetRange001.maxX" 1
        cmds.setAttr(self._range + '.maxX', 1)
#setAttr "zSetRange001.oldMinX" 34;
        cmds.setAttr(self._range + '.oldMinX', oldMinX)
#setAttr "zSetRange001.oldMaxX" 55;
        cmds.setAttr(self._range + '.oldMaxX', oldMaxX)
#setAttr "ramp1.colorEntryList[0].color" -type double3 1 1 1 ;
#setAttr "ramp1.colorEntryList[2].color" -type double3 0 0 0 ;

        # connecting stuff I don't know about
        #cmds.connectAttr(self._layeredShader + '.message',
        #                 self._shaderGroup + ".miMaterialShader",
        #                 force=True)
        #cmds.connectAttr(self._layeredShader + '.message',
        #                 self._shaderGroup + ".miPhotonShader",
        #                 force=True)
        #cmds.connectAttr(self._layeredShader + '.message',
        #                 self._shaderGroup + ".miShadowShader",
        #                 force=True)



        # connecting the File node
        cmds.setAttr(self._imgFile + '.fileTextureName',
                     self._dirName + self._imageName,
                     type='string')
        cmds.setAttr(self._imgFile + '.filterType', 0)
        #cmds.connectAttr(self._imgFile + '.outAlpha',
        #                 self._shader + '.cutout_opacity',
        #                 force=True)
        # connecting the Placement node
        cmds.connectAttr(self._place2D + '.outUV', self._imgFile + '.uv')
        # connecting the Reverse node
        cmds.connectAttr(self._imgFile + '.outAlpha',
                         self._reverse + '.inputX')

# connecting reverse_001.output.outputX to layeredShader1.inputs.transparency.transparencyR. //
        cmds.connectAttr(self._reverse + '.outputX',
                         self._layeredShader + '.inputs[0].transparencyR')
# connecting reverse_001.output.outputX to layeredShader1.inputs.transparency.transparencyG. //
        cmds.connectAttr(self._reverse + '.outputX',
                         self._layeredShader + '.inputs[0].transparencyG')
# connecting reverse_001.output.outputX to layeredShader1.inputs.transparency.transparencyB. //
        cmds.connectAttr(self._reverse + '.outputX',
                         self._layeredShader + '.inputs[0].transparencyB')
        #cmds.connectAttr(self._imgFile + '.outColor',
        #                 self._shader + '.diffuse',
        #                 force=True)
# connecting setRange2.outValue.outValueX to surfaceShader2.outColor.outColorR. //
#connectAttr -f setRange2.outValueX surfaceShader2.outColorR;
        cmds.connectAttr(self._ramp + '.outColor',
                         self._surfaceShader + '.outColor',
                         force=True)
# connecting setRange2.outValue.outValueX to surfaceShader2.outColor.outColorG. //
#connectAttr -f setRange2.outValueX surfaceShader2.outColorG;
#        cmds.connectAttr(self._ramp + '.outValueX',
#                         self._surfaceShader + '.outColorG',
#                         force=True)
# connecting setRange2.outValue.outValueX to surfaceShader2.outColor.outColorB. //
#connectAttr -f setRange2.outValueX surfaceShader2.outColorB;
#        cmds.connectAttr(self._ramp + '.outValueX',
#                         self._surfaceShader + '.outColorB',
#                         force=True)
# connecting zSurfaceShader_001.outColor to zLayeredShader_001.inputs.color. //
#connectAttr -force zSurfaceShader_001.outColor zLayeredShader_001.inputs[0].color;
        cmds.connectAttr(self._surfaceShader + '.outColor',
                         self._layeredShader + '.inputs[0].color',
                         force=True)
# connecting zLayeredShader_002.outColor to zDepthShaderSG_002.surfaceShader. //
#connectAttr -f zLayeredShader_002.outColor zDepthShaderSG_002.surfaceShader;
        cmds.connectAttr(self._layeredShader + '.outColor',
                         self._shaderGroup + '.surfaceShader',
                         force=True)

    def getSG(self):
        return self._shaderGroup

    def getShader(self):
        return self._layeredShader

    def __repr__(self):
        return '[Shader: %s, %s, %s]' % (self._layerNum,
                                         self._layeredShader,
                                         self._shaderGroup)

"""
if __name__ == '__main__':                      # When run for testing only
    # self-test code

    #createRenderLayer -name "layer1" -number 1 -noRecurse `ls -selection`;
    cmds.createRenderLayer(empty=True, name='zDepthRenderLayer', number=1, noRecurse=True)

    dirName = 'C:\Users\zklinger\Google Drive\Docs\PROJECTS\SB\IMG\SB_010\\'
    imageName = 'sb010_card_001_001.tif'
    shader = ZDepthShader(imageName, dirName, 34, 55)
    print shader

    # Set the textured display mode.
    currentPanel = cmds.getPanel(withLabel='Persp View')
    if currentPanel != '':
        cmds.modelEditor(currentPanel, edit=True, da='smoothShaded', displayTextures=True, dl='default',
                         rnm='vp2Renderer')

"""