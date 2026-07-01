import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random as r
import math
import sys

glutInit(sys.argv)

sigma = 10
rho = 28
beta = 8/3
df = 0.01

points = []
floats = []

x = 1.10;
y = 2.00;
z = 7.00;

rotation = 0;

class Floater:
    def __init__(self):
        self.x = r.randint(-50, 50);
        self.y = r.randint(-50, 50);
        self.z = r.randint(-50, 50);
        
        self.trail = [(self.x, self.y, self.z)];
        
        self.clr = [r.uniform(0, 0.25), r.uniform(0, 0.5), r.uniform(0.5, 1)]
        
    def update_pos(self):
        self.dx = (sigma*(-self.x + self.y)) * df
        self.dy = (-self.x*self.z + rho*self.x - self.y) * df
        self.dz = (self.x*self.y - beta*self.z) * df
        
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz
        
        self.trail.append((self.x, self.y, self.z))
        
        if len(self.trail) > 10:
            self.trail = self.trail[1:]
        
    def draw(self):
        glColor3f(*self.clr)
        
        glBegin(GL_POINTS)
        glVertex3f(self.x, self.y, self.z)
        glEnd()
        
    def draw_trail(self):
        speed = math.sqrt(self.dx*self.dx + self.dy*self.dy + self.dz*self.dz)
        
        glBegin(GL_LINE_STRIP)
        for point in self.trail:
            glColor3f(speed, 0, 1-speed)
            glVertex3f(*point)
        glEnd()

def draw_axis():
    edges = (
        (0,1),(2,3),(4,5)
    )
    
    vertices = (
        (-25, 0, 0),
        ( 25, 0, 0),
        ( 0,-25, 0),
        ( 0, 25, 0),
        ( 0, 0,-25),
        ( 0, 0, 25),
    )
    glTranslatef(0, 0, 25)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3f(1,1,1)
            glVertex3fv(vertices[vertex])
    glEnd()
    glTranslatef(0, 0, -25)
    
def render_text(x, y, z, text):
    glRasterPos3f(x, y, z)
    
    for c in text:
        glutBitmapCharacter(
            GLUT_BITMAP_HELVETICA_18, # type: ignore
            ord(c)
        )
    

pygame.init()

pygame.display.set_mode(
    (800, 600),
    DOUBLEBUF | OPENGL
)

gluPerspective(
    45,         # FOV
    800/800,    # aspect ratio
    0.1,        # near clipping plane
    100.0        # far clipping plane
)

glTranslate(0, -10, -50)
glScale(0.4, 0.4, 0.4)
glRotatef(-60, 1, 0, 0) 
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

pygame.font.init()

font = pygame.font.SysFont("Arial", 24)

for i in range(1000):
    floats.append(Floater())

# Essential Graphics Loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    dt = clock.tick(60) / 1000;      
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glPointSize(2)
    for blob in floats:
        blob.draw()
        blob.update_pos()
        blob.draw_trail()
        
    
    draw_axis()
    glTranslatef(0, 0, 25)
    render_text(25, 2, 2, "X")
    render_text(2, 25, 2, "Y")
    render_text(2, 2, 25, "Z")
    
    #glLoadIdentity()
    
    glRotatef(0.5, 0, 0, 1)
    
    glTranslatef(0, 0, -25)
    
    #glRotatef(0.25, 0, 1, 0)
    #glTranslate(0, 0, -50)
        
    pygame.display.flip()