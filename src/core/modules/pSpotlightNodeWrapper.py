import pickle

from pandac.PandaModules import *

from src.modules.baseWrapper import *
from src.modelController import modelController

class SpotlightNodeWrapper( BaseWrapper ):
  wrapperTypeTag = 'SpotlightNodeWrapper'
  
  def onCreate( self, parent ):
    # this is called when the user presses the button to create
    # a nodePathWrapper
    node = SpotlightNodeWrapper( parent )
    # enable this object to be editable
    node.enableEditmode()
    # the editor should select this model
    modelController.selectModel( node )
  onCreate = classmethod(onCreate)
  
  def __init__( self, parent=None ):
    print "I: SpotlightNodeWrapper.__init__:"
    # define the name of this object
    name = 'lightNode'
    BaseWrapper.__init__( self, name, parent )
    
    # create the spotLight
    self.spotLight = Spotlight('Spotlight')
    self.spotLight.setColor(VBase4(1, 1, 1, 1))
    lens = PerspectiveLens()
    self.spotLight.setLens(lens)
    self.spotLightNodePath = self.attachNewNode(self.spotLight)
    render.setLight(self.spotLightNodePath)
  
  def destroy( self ):
    # destroy this object
    self.stopEdit()
    self.disableEditmode()
    modelIdManager.delObjectId( self.id )
    render.clearLight(self.spotLightNodePath)
    #self.spotLight.detachNode()
    self.model.detachNode()
    self.model.removeNode()
    BaseWrapper.destroy( self )
  
  def enableEditmode( self ):
    # enables the edit methods of this object
    # makes it pickable etc.
    # edit mode is enabled
    BaseWrapper.enableEditmode( self )
    # load a dummy model
    self.model = loader.loadModel( SPOTLIGHT_WRAPPER_DUMMYOBJECT )
    # set the model invisible in the scenegraphbrowser
    self.model.setTag(EXCLUDE_SCENEGRAPHBROWSER_MODEL_TAG,'')
    self.model.setLightOff()
    # make the model visible
    self.model.reparentTo( self )
    # enable picking of the object
    self.setCollideMask( DEFAULT_EDITOR_COLLIDEMASK )
  def disableEditmode( self ):
    # disables the edit methods of this object
    # -> performance increase
    # edit mode is disabled
    BaseWrapper.disableEditmode( self )
    # remove the dummy model
    self.model.removeNode()
    self.model.detachNode()
    # disable picking of the object
    self.setCollideMask( BitMask32.allOff() )
  
  def startEdit( self ):
    # the object is selected to be edited
    # creates a directFrame to edit this object
    self.model.showBounds()
    BaseWrapper.startEdit( self )
  def stopEdit( self ):
    # the object is deselected from being edited
    self.model.hideBounds()
    BaseWrapper.stopEdit( self )
  
  def getSaveData( self, relativeTo ):
    ''' link the egg-file into the egg we save
    '''
    name = self.getName()
    # convert the matrix, very ugly right now
    om = self.getMat()
    nm = Mat4D()
    for x in xrange(4):
        for y in xrange(4):
            nm.setCell( x, y, om.getCell(x,y) )
    # the matrix we define must be applied to the nodes in "local space"
    instance = EggGroup( name+"-Group" )
    instance.setGroupType(EggGroup.GTInstance)
    instance.setTransform3d( nm )
    # userdata is not written to the eggFile
    #instance.setUserData( self.wrapperTypeTag )
    instance.setTag( MODEL_WRAPPER_TYPE_TAG, self.wrapperTypeTag )
    # add the reference to the egg-file
    #ext = EggExternalReference( name+"-EggExternalReference", self.modelFilename )
    data = list()
    parameters = pickle.dumps( data )
    comment = EggComment( 'parameters', parameters )
    instance.addChild(comment)
    return instance
  
  def loadFromEggGroup( self, eggGroup, parent ):
    print "I: NodePathWrapper.loadFromEggGroup:"
    eggComment = eggGroup.getChildren()[0]
    print eggComment
    #filename = str(eggExternalReference.getFilename())
    objectInstance = SpotlightNodeWrapper( parent )
    return objectInstance
  loadFromEggGroup = classmethod(loadFromEggGroup)

if __name__ == '__main__':
  print "testing notdePathWrapper"
  a = NodePathWrapper.onCreate( 'test2' )
  print a.baseName, a.nodeName