import pygame
import numpy as np

WIDTH = 600
HEIGHT = 480
FPS = 60
counter = 0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
clock = pygame.time.Clock()


class Node:
    '''A point with three coordinates'''

    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]


class Edge:
    '''Lines connectiong two nodes'''

    def __init__(self, start, stop):
        self.start = start
        self.stop = stop


def translationMatrix(dx=0, dy=0, dz=0):
    '''Return a matrix for translation along a vector (dx, dy, dz)'''

    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [dx, dy, dz, 1]])


def scaleMatrix(sx=0, sy=0, sz=0):
    '''Return a matrix for scaling all axes centered on point (sx, sy, sz)'''

    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, sz, 0],
                     [0, 0, 0, 1]])


def rotateXMatrix(radians):
    '''Return a matrix for rotating about the x-axis by given radians'''

    c = np.cos(radians)
    s = np.sin(radians)

    return np.array([[1, 0, 0, 0],
                     [0, c, -s, 0],
                     [0, s, c, 0],
                     [0, 0, 0, 1]])


def rotateYMatrix(radians):
    '''Return a matrix for rotating about the y-axis by given radians'''

    c = np.cos(radians)
    s = np.sin(radians)

    return np.array([[c, 0, s, 0],
                     [0, 1, 0, 0],
                     [-s, 0, c, 0],
                     [0, 0, 0, 1]])


def rotateZMatrix(radians):
    '''Return a matrix for rotating about the z-axis by given radians'''

    c = np.cos(radians)
    s = np.sin(radians)

    return np.array([[c, -s, 0, 0],
                     [s, c, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])


class WireFrame:
    '''The surface created bound by multiple edges'''

    def __init__(self):
        self.nodes = np.zeros((0, 4))
        self.edges = []

    def addNodes(self, nodeArray):
        '''Append nodes to the WireFrame's Node Array'''
        onesColumn = np.ones((len(nodeArray), 1))
        onesAdded = np.hstack((nodeArray, onesColumn))
        self.nodes = np.vstack((self.nodes, onesAdded))

    def addEdges(self, edgeList):
        '''Append edges to the WireFrame's Edge List'''
        self.edges += edgeList

    def outputNodes(self):
        '''List the current nodes in the WireFrame object'''
        print("\nNodes:")
        for i, (x, y, z, _), in enumerate(self.nodes):
            print(f"{i}: ({x}, {y}, {z})")

    def outputEdges(self):
        '''List the current edges in the WireFrame object'''
        print("\nEdges:")
        for i, (node1, node2) in enumerate(self.edges):
            print(f'{i}: {node1} -> {node2}')

    def transform(self, matrix):
        '''Apply a transformation defined by given a matrix'''
        self.nodes = np.dot(self.nodes, matrix)

    def findCenter(self):
        '''Find the center of the WireFrame'''

        numNodes = len(self.nodes)
        meanX = sum([node[0] for node in self.nodes]) / numNodes
        meanY = sum([node[1] for node in self.nodes]) / numNodes
        meanZ = sum([node[2] for node in self.nodes]) / numNodes

        return (meanX, meanY, meanZ)


class ProjectionViewer:
    '''Displays 3D objects on a 2D display'''

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("WireFrame display")
        self.backgroundColor = (10, 10, 50)

        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = True
        self.nodeColor = (255, 255, 255)
        self.edgeColor = (200, 200, 200)
        self.nodeRadius = 4

    def run(self):
        '''Begin the game loop'''

        running = True

        keyToFunction = {
            pygame.K_LEFT: (lambda x: x.translateAll([-10, 0, 0])),
            pygame.K_RIGHT: (lambda x: x.translateAll([10, 0, 0])),
            pygame.K_DOWN: (lambda x: x.translateAll([0, 10, 0])),
            pygame.K_UP: (lambda x: x.translateAll([0, -10, 0])),
            pygame.K_EQUALS: (lambda x: x.scaleAll([1.25, 1.25, 1.25])),
            pygame.K_MINUS: (lambda x: x.scaleAll([0.8, 0.8, 0.8])),
            pygame.K_q: (lambda x: x.rotateAll('x', 0.1)),
            pygame.K_w: (lambda x: x.rotateAll('x', -0.1)),
            pygame.K_a: (lambda x: x.rotateAll('y', 0.1)),
            pygame.K_s: (lambda x: x.rotateAll('y', -0.1)),
            pygame.K_z: (lambda x: x.rotateAll('z', -0.1)),
            pygame.K_x: (lambda x: x.rotateAll('z', 0.1)),
        }

        while running:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in keyToFunction:
                        keyToFunction[event.key](self)

            self.display()
            pygame.display.update()

    def addWireFrame(self, name, wireframe):
        '''Add a named WireFrame object'''
        self.wireframes[name] = wireframe

    def display(self):
        '''Draw the wireframes onto the screen'''

        self.screen.fill(self.backgroundColor)

        global counter
        counter += 0.001

        for wireframe in self.wireframes.values():
            if self.displayEdges:
                for n1, n2 in wireframe.edges:
                    pygame.draw.aaline(self.screen, self.edgeColor,
                                       wireframe.nodes[n1][:2],
                                       wireframe.nodes[n2][:2], 1)
            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, self.nodeColor,
                                       (int(node[0]), int(node[1])),
                                       self.nodeRadius, 0)

            matrix = rotateXMatrix(counter)
            wireframe.transform(matrix)
            matrix = rotateYMatrix(counter)
            wireframe.transform(matrix)
            matrix = rotateZMatrix(counter)
            wireframe.transform(matrix)

    def translateAll(self, vector):
        '''Translate all WireFrames along a given axis by d units'''

        matrix = translationMatrix(*vector)
        for wireframe in self.wireframes.values():
            wireframe.transform(matrix)

    def scaleAll(self, vector):
        '''Scale all wireframes by a given vector,
           centered on the center of the screen'''

        matrix = scaleMatrix(*vector)
        for wireframe in self.wireframes.values():
            wireframe.transform(matrix)

    def rotateAll(self, axis, theta):
        '''Rotate all wireframes along the given axis by the given angle'''

        axis = axis.lower()
        for wireframe in self.wireframes.values():
            if axis in ['x', 'y', 'z']:
                if axis == 'x':
                    matrix = rotateXMatrix(theta)
                elif axis == 'y':
                    matrix = rotateYMatrix(theta)
                elif axis == 'z':
                    matrix = rotateZMatrix(theta)
                wireframe.transform(matrix)
            else:
                print("Invalid axis provided in rotateAll()")


def main():
    '''Main function containing everything'''

    # Calculate nodes of a cube
    r = (WIDTH/2, WIDTH/2 + 50)
    cubeNodes = [(x, y, z) for x in r for y in r for z in r]

    # Create a WireFrame
    cube = WireFrame()
    cube.addNodes(np.array(cubeNodes))
    cube.addEdges([(n, n + 4) for n in range(0, 4)])
    cube.addEdges([(n, n + 1) for n in range(0, 8, 2)])
    cube.addEdges([(n, n + 2) for n in (0, 1, 4, 5)])

    # Create display
    pv = ProjectionViewer(WIDTH, HEIGHT)
    pv.addWireFrame('cube', cube)

    # Begin main loop
    pv.run()


if __name__ == '__main__':
    main()

# Thanks to the tutorial from
# https://www.petercollingridge.co.uk/tutorials/3d/pygame
