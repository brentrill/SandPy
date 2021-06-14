from direct.showbase.ShowBase import ShowBase
#import direct.directbase.DirectStart
from panda3d.core import WindowProperties
from panda3d.core import AmbientLight
from panda3d.core import Vec2, Vec3, Vec4
from panda3d.core import DirectionalLight
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletSphereShape, BulletCylinderShape
from panda3d.bullet import ZUp, XUp
from panda3d.core import TransformState
from panda3d.core import Plane, Point3
from panda3d.core import PStatClient


world = BulletWorld()
world.setGravity(Vec3(0, 0, -9.81))


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()

        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)

        # Box Model
        self.boxTex = loader.loadTexture("mymodels/wood.jpg")
        self.environment = loader.loadModel("mymodels/box")
        self.boxPhysics()

        # Filling Box
        self.rocks()

        # Camera
        self.camera.setPos(0, 0, 32)
        # Tilt the camera down by setting its pitch.
        self.camera.setP(-90)

        # Lights
        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambientLightNodePath = render.attachNewNode(ambientLight)
        render.setLight(self.ambientLightNodePath)

        mainLight = DirectionalLight("main light")
        self.mainLightNodePath = render.attachNewNode(mainLight)
        # Turn it around by 45 degrees, and tilt it down by 45 degrees
        self.mainLightNodePath.setHpr(45, -45, 0)
        render.setLight(self.mainLightNodePath)
        render.setShaderAuto()

        # Controls
        self.keyMap = {
            "rake": False
        }

        self.accept("mouse1", self.updateKeyMap, ["rake", True])
        self.accept("mouse1-up", self.updateKeyMap, ["rake", False])

        self.lastMousePos = Vec2(0,0)
        self.groundPlane = Plane(Vec3(0, 0, 1), Vec3(0, 0, 0))
        self.yVector = Vec2(0, 1)

        # Rake
        # Declare the rake's structure here
        radius = 0.25
        height = 2.4
        shape1 = BulletCylinderShape(radius, height, ZUp)
        #self.rake = render.attachNewNode(self.rakeNP(radius, height))
        #world.attachRigidBody(self.rakeNP(radius, height))

        self.rake = self.rakeNP(radius, height)
        self.rakeNode = render.attachNewNode(self.rake)
        world.attachRigidBody(self.rake)

    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState



    def boxPhysics(self):
        self.environment.setTexture(self.boxTex, 1)
        self.environment.setH(90)
        self.environment.setScale(5)
        self.environment.reparentTo(render)

        shape1 = BulletBoxShape((2.4, 1.7, 0.2)) # Base
        shape2 = BulletBoxShape((2.4, 0.1, 0.5)) # Bottom Wall
        shape3 = BulletBoxShape((2.4, 0.1, 0.5)) # Top Wall
        shape4 = BulletBoxShape((0.1, 1.7, 0.5)) # Left Wall
        shape5 = BulletBoxShape((0.1, 1.7, 0.5)) # Right Wall

        bodyNP = BulletRigidBodyNode('Box')
        bodyNP.addShape(shape1, TransformState.makePos(Point3(0, 0, -0.46)))
        bodyNP.addShape(shape2, TransformState.makePos(Point3(0, -1.71, 0)))
        bodyNP.addShape(shape3, TransformState.makePos(Point3(0, 1.71, 0)))
        bodyNP.addShape(shape4, TransformState.makePos(Point3(-2.46, 0, 0)))
        bodyNP.addShape(shape5, TransformState.makePos(Point3(2.46, 0, 0)))

        np = render.attachNewNode(bodyNP)
        np.setPos(0, 0, 0)
        np.setScale(4)
        world.attachRigidBody(bodyNP)

    def rocks(self):
        size = 0.1
        scale = 0.2
        count = 0
        model = loader.loadModel('mymodels/ball.egg')
        model.setScale(scale)
        # model.flattenLight()
        #model.reparentTo(np)
        #shape = BulletBoxShape(Vec3(size, size, size))
        shape = BulletSphereShape(size)
        for x in range(-92,92,5):
            for y in range(-60,65,5):
                for z in range(2,4,1):
                    node = BulletRigidBodyNode('Box')
                    node.setMass(1)
                    node.set_angular_damping(0.9)
                    node.addShape(shape)
                    np = render.attachNewNode(node)
                    np.setPos(x/10, y/10, z)
                    world.attachRigidBody(node)
                    model.copyTo(np)
                    count += 1
        print('Particle Count: ', count)

    def rakeNP(self, radius, height):
        shape1 = BulletCylinderShape(radius, height, ZUp)
        shape2 = BulletCylinderShape(radius, height, ZUp)
        shape3 = BulletCylinderShape(radius, height, ZUp)
        shape4 = BulletCylinderShape(radius, height, ZUp)
        shape5 = BulletCylinderShape(0.4, 3.5, XUp)
        bodyNP = BulletRigidBodyNode('Rake')
        bodyNP.addShape(shape1, TransformState.makePos(Point3(1 + .5, 0, -0.8)))
        bodyNP.addShape(shape2, TransformState.makePos(Point3(0 + .5, 0, -0.8)))
        bodyNP.addShape(shape3, TransformState.makePos(Point3(-1 + .5, 0, -0.8)))
        bodyNP.addShape(shape4, TransformState.makePos(Point3(-2 + .5, 0, -0.8)))
        bodyNP.addShape(shape5, TransformState.makePos(Point3(0, 0, 1 - .2)))
        return bodyNP
        #np = render.attachNewNode(bodyNP)
        #np.setPos(0, 0, 0)
        #world.attachRigidBody(bodyNP)


    def updatePhys(self, task):
        dt = globalClock.getDt()
        world.doPhysics(dt, 10)#, 1.0/180.0)

        # If the mouse goes off screen
        mouseWatcher = base.mouseWatcherNode
        if mouseWatcher.hasMouse():
            mousePos = mouseWatcher.getMouse()
        else:
            mousePos = self.lastMousePos

        mousePos3D = Point3()
        nearPoint = Point3()
        farPoint = Point3()
        base.camLens.extrude(mousePos, nearPoint, farPoint)
        self.groundPlane.intersectsLine(mousePos3D,
                                        render.getRelativePoint(base.camera, nearPoint),
                                        render.getRelativePoint(base.camera, farPoint))
        # print(mousePos3D)
        # Rake Position Calculation based on Lesson 10
        rakeDirection = Vec3(mousePos3D - self.rakeNode.getPos())
        rakeDirection2D = rakeDirection.getXy()
        rakeDirection2D.normalize()
        rakeDirection.normalize()

        self.rakeNode.setPos(mousePos3D.getX(), mousePos3D.getY(), mousePos3D.getZ() + 10)
        #print(self.rakeNode.getPos())
        heading = self.yVector.signedAngleDeg(rakeDirection2D)

        self.rakeNode.setH(heading)

        # if rakeDirection.length() > 0.001:
        # self.ray.setOrigin(self.actor.getPos())
        # self.ray.setDirection(rakeDirection)

        self.lastMousePos = mousePos

        # When Mouse1 is pressed, drag rake
        if self.keyMap["rake"]:
            #print("Raking")
            self.rakeNode.setZ(0)
        else:
            #print("Stopped")
            None

        return task.cont

#PStatClient.connect()
game = Game()
game.setFrameRateMeter(True)

# Debug Node
"""
debugNode = BulletDebugNode('Debug')
debugNode.showWireframe(True)
debugNode.showConstraints(True)
debugNode.showBoundingBoxes(False)
debugNode.showNormals(False)
debugNP = render.attachNewNode(debugNode)
debugNP.show()
world.setDebugNode(debugNP.node())
"""


taskMgr.add(game.updatePhys, 'update')
game.run()
