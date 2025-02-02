__author__ = 'zklinger'
import maya.cmds as cmds


class AOShader(object):
    def __init__(self, imageName, dirName):
        self._imageName = imageName
        self._dirName = dirName
        self._layerNum = imageName[11:14]
        self._surfaceShader = cmds.shadingNode('surfaceShader',
                                               n='AOSurfaceShader_' +
                                               self._layerNum,
                                               asShader=True)
        self._layeredShader = cmds.shadingNode('layeredShader',
                                               n='AOLayeredShader_' +
                                                 self._layerNum,
                                               asShader=True)
#setAttr "zLayeredShader_001.compositingFlag" 1
        cmds.setAttr(self._layeredShader + '.compositingFlag', 1)
        self._shaderGroup = cmds.sets(empty=True, renderable=True,
                                      noSurfaceShader=True,
                                      name='AOShaderSG_' +
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
        self._imgFile = cmds.shadingNode('file', n='AOFile_' +
                                                   self._layerNum,
                                         asTexture=True)
        self._mib_amb = cmds.shadingNode('mib_amb_occlusion', n='AO_mib_' +
                                                   self._layerNum,
                                         asTexture=True)
        self._place2D = cmds.shadingNode('place2dTexture', n='AOPlace2D',
                                         asUtility=True)

#setAttr "ramp1.colorEntryList[0].color" -type double3 1 1 1 ;
#setAttr "ramp1.colorEntryList[2].color" -type double3 0 0 0 ;
        cmds.setAttr(self._mib_amb + '.samples', 64)
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

# connecting reverse_001.output.outputX to layeredShader1.inputs.transparency.transparencyR. //
        cmds.connectAttr(self._imgFile + '.outTransparency',
                         self._layeredShader + '.inputs[0].transparency')

        #cmds.connectAttr(self._imgFile + '.outColor',
        #                 self._shader + '.diffuse',
        #                 force=True)

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

        cmds.connectAttr(self._mib_amb + '.outValue',
                         self._surfaceShader + '.outColor',
                         force=True)

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
