from pandac.PandaModules import *

from core.pTexturePainter import texturePainter
from core.pConfigDefs import * # imports Enum

TextureStage_ModeEnum = Enum(
  MModulate = TextureStage.MModulate,
  MDecal = TextureStage.MDecal,
  MBlend = TextureStage.MBlend,
  MReplace = TextureStage.MReplace,
  MAdd = TextureStage.MAdd,
  MCombine = TextureStage.MCombine,
  MBlendColorScale = TextureStage.MBlendColorScale,
  MModulateGlow = TextureStage.MModulateGlow,
  MModulateGloss = TextureStage.MModulateGloss,
  MNormal = TextureStage.MNormal,
  MNormalHeight = TextureStage.MNormalHeight,
  MGlow = TextureStage.MGlow,
  MGloss = TextureStage.MGloss,
  MHeight = TextureStage.MHeight,
  MSelector = TextureStage.MSelector,
)

TextureStage_CombineModeEnum = Enum(
  CMUndefined = TextureStage.CMUndefined,
  CMReplace = TextureStage.CMReplace,
  CMModulate = TextureStage.CMModulate,
  CMAdd = TextureStage.CMAdd,
  CMAddSigned = TextureStage.CMAddSigned,
  CMInterpolate = TextureStage.CMInterpolate,
  CMSubtract = TextureStage.CMSubtract,
  CMDot3Rgb = TextureStage.CMDot3Rgb,
  CMDot3Rgba = TextureStage.CMDot3Rgba,
)

TextureStage_CombineSourceEnum = Enum(
  CSUndefined = TextureStage.CSUndefined,
  CSTexture = TextureStage.CSTexture,
  CSConstant = TextureStage.CSConstant,
  CSPrimaryColor = TextureStage.CSPrimaryColor,
  CSPrevious = TextureStage.CSPrevious,
  CSConstantColorScale = TextureStage.CSConstantColorScale,
  CSLastSavedResult = TextureStage.CSLastSavedResult,
)

TextureStage_CombineOperandEnum = Enum(
  COUndefined        = TextureStage.COUndefined,
  COSrcColor         = TextureStage.COSrcColor,
  COOneMinusSrcColor = TextureStage.COOneMinusSrcColor,
  COSrcAlpha         = TextureStage.COSrcAlpha,
  COOneMinusSrcAlpha = TextureStage.COOneMinusSrcAlpha,
)

TexGenAttrib_PandaCompareFuncEnum = Enum(
  MNone = TexGenAttrib.MNone,
  MNever = TexGenAttrib.MNever,
  MLess = TexGenAttrib.MLess,
  MEqual = TexGenAttrib.MEqual,
  MLessEqual = TexGenAttrib.MLessEqual,
  MGreater = TexGenAttrib.MGreater,
  MNotEqual = TexGenAttrib.MNotEqual,
  MGreaterEqual = TexGenAttrib.MGreaterEqual,
  MAlways = TexGenAttrib.MAlways,
)

TexGenAttrib_TexGenModeEnum = Enum(
  MOff = TexGenAttrib.MOff,
  MEyeSphereMap = TexGenAttrib.MEyeSphereMap,
  MWorldCubeMap = TexGenAttrib.MWorldCubeMap,
  MEyeCubeMap = TexGenAttrib.MEyeCubeMap,
  MWorldNormal = TexGenAttrib.MWorldNormal,
  MEyeNormal = TexGenAttrib.MEyeNormal,
  MWorldPosition = TexGenAttrib.MWorldPosition,
  MUnused = TexGenAttrib.MUnused,
  MEyePosition = TexGenAttrib.MEyePosition,
  MPointSprite = TexGenAttrib.MPointSprite,
  MLightVector = TexGenAttrib.MLightVector,
  MConstant = TexGenAttrib.MConstant,
)

Texture_WrapModeEnum = Enum(
  WMClamp = Texture.WMClamp,
  WMRepeat = Texture.WMRepeat,
  WMMirror = Texture.WMMirror,
  WMMirrorOnce = Texture.WMMirrorOnce,
  WMBorderColor = Texture.WMBorderColor,
  WMInvalid = Texture.WMInvalid,
)

Texture_CompressionMode = Enum(
  CMDefault = Texture.CMDefault,
  CMOff = Texture.CMOff,
  CMOn = Texture.CMOn,
  CMFxt1 = Texture.CMFxt1,
  CMDxt1 = Texture.CMDxt1,
  CMDxt2 = Texture.CMDxt2,
  CMDxt3 = Texture.CMDxt3,
  CMDxt4 = Texture.CMDxt4,
  CMDxt5 = Texture.CMDxt5,
)

class TextureLayer:
  ''' a texturelayer consists of a texture and a stage
  '''
  def __init__(self, texture=None, stage=None):
    self.texture = texture
    self.stage = stage

def getTextureLayers(nodePath):
  ''' return a TextureLayer object for each texture and stage that is found on
  a object '''
  def getStages(gnode, state, texStages): #, textures):
    for i in range(gnode.getNumGeoms()):
      gstate = state.compose(gnode.getGeomState(i))
      attrib = gstate.getAttrib(TextureAttrib.getClassSlot())
      if attrib != None:
        for j in range(attrib.getNumOnStages()):
          texStage = attrib.getOnStage(j)
          texture = attrib.getTexture()
          if (texStage not in texStages) or (texture not in textures):
            texStages.append(TextureLayer(stage=texStage, texture=texture))
    return texStages
  
  def rec(parent, state, texStages):
    for child in parent.getChildren():
      texStages = rec(child, state, texStages)
      if child.node().isGeomNode():
        texStages = getStages(child.node(), state, texStages)
    return texStages
  
  texStages = rec(nodePath, nodePath.getNetState(), [])
  return texStages

class ObjectEditor:
  def __init__(self):
    self.editObject = None
  
  def setEditObject(self, editObject):
    self.editObject = editObject
  
  def enableEditor(self):
    # this is just for testing
    texStages = self.getTextureLayers()
    if len(texStages) > 0:
      self.startPaint(texStages[0])
    else:
      pass
  
  def disableEditor(self):
    # this is just for testing
    self.stopPaint()
  
  def getTextureLayers(self):
    if self.editObject:
      return getTextureLayers(self.editObject)
    return []
  
  def separateModel(self):
    ''' creates a new separate model from the selected object
    '''
    pass
  
  def startPaint(self, textureLayer):
    texturePainter.selectPaintModel(self.editObject)
    texturePainter.enableEditor()
    texturePainter.startEdit(textureLayer.texture)
  
  def stopPaint(self):
    texturePainter.stopEdit()
    texturePainter.disableEditor()

objectEditor = ObjectEditor()