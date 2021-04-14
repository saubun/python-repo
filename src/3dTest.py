import pygame

WIDTH = 600
HEIGHT = 480
FPS = 60

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


class WireFrame:
    '''The surface created bound by multiple edges'''

    def __init__(self):
        self.nodes = []
        self.edges = []

    def addNodes(self, nodeList):
        '''Append nodes to the WireFrame's Node List'''
        for node in nodeList:
            self.nodes.append(Node(node))

    def addEdges(self, edgeList):
        '''Append edges to the WireFrame's Edge List'''
        for (start, stop) in edgeList:
            self.edges.append(Edge(self.nodes[start], self.nodes[stop]))

    def outputNodes(self):
        '''List the current nodes in the WireFrame object'''
        print("\nNodes:")
        for i, node, in enumerate(self.nodes):
            print(f"{i}: ({node.x}, {node.y}, {node.z})")

    def outputEdges(self):
        '''List the current edges in the WireFrame object'''
        print("\nEdges:")
        for i, edge, in enumerate(self.edges):
            print(f'{i}: ({edge.start.x}, {edge.start.y}, {edge.start.z})' +
                  f' to ({edge.stop.x}, {edge.stop.y}, {edge.stop.z})')

    def translate(self, axis, d):
        '''Translate each node of a wireframe by d along a given axis'''

        if axis in ['x', 'y', 'z']:
            for node in self.nodes:
                setattr(node, axis, getattr(node, axis) + d)

    def scale(self, centerX, centerY, scale):
        '''Scale the WireFrame from the center of the screen'''

        for node in self.nodes:
            node.x = centerX + scale * (node.x - centerX)
            node.y = centerY + scale * (node.y - centerY)
            node.z *= scale


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
            pygame.K_a: (lambda x: x.translateAll('x', -10)),
            pygame.K_d: (lambda x: x.translateAll('x', 10)),
            pygame.K_s: (lambda x: x.translateAll('y', 10)),
            pygame.K_w: (lambda x: x.translateAll('y', -10)),
            pygame.K_EQUALS: (lambda x: x.scaleAll(1.25)),
            pygame.K_MINUS: (lambda x: x.scaleAll(0.8))
        }

        while running:
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

        for wireframe in self.wireframes.values():
            if self.displayEdges:
                for edge in wireframe.edges:
                    pygame.draw.aaline(self.screen, self.edgeColor,
                                       (edge.start.x, edge.start.y),
                                       (edge.stop.x, edge.stop.y), 1)
            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, self.nodeColor,
                                       (int(node.x), int(node.y)),
                                       self.nodeRadius, 0)

    def translateAll(self, axis, d):
        '''Translate all WireFrames along a given axis by d units'''

        for wireframe in self.wireframes.values():
            wireframe.translate(axis, d)

    def scaleAll(self, scale):
        '''Scale all wireframes by a given scale,
           centered on the center of the screen'''

        centerX = self.width / 2
        centerY = self.height / 2

        for wireframe in self.wireframes.values():
            wireframe.scale(centerX, centerY, scale)


def main():
    '''Main function containing everything'''

    # Calculate nodes and edges of a cube
    r = (50, 250)
    cubeNodes = [(x, y, z) for x in r for y in r for z in r]
    cubeEdges = [(n, n + 4) for n in range(0, 4)]
    cubeEdges += [(n, n + 1) for n in range(0, 8, 2)]
    cubeEdges += [(n, n + 2) for n in (0, 1, 3, 5)]

    # Create a WireFrame
    cube = WireFrame()
    cube.addNodes(cubeNodes)
    cube.addEdges(cubeEdges)

    # Create display and begin
    pv = ProjectionViewer(WIDTH, HEIGHT)
    pv.addWireFrame('cube', cube)
    pv.run()


if __name__ == '__main__':
    main()

# Thanks to the tutorial from
# https://www.petercollingridge.co.uk/tutorials/3d/pygame
