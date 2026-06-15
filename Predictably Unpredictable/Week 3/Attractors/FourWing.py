import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random as r
import math

a = 0.2
b = 0.01
c = -0.4
df = 0.01

points = []
floats = []

x = 1.10;
y = 2.00;
z = 7.00;

rotation = 0;

class Floater:
    def __init__(self):
        self.x = r.uniform(-5, 5);
        self.y = r.uniform(-5, 5);
        self.z = r.uniform(-5, 5);
        
        self.trail = [(self.x, self.y, self.z)];
        
        self.clr = [r.uniform(0, 0.25), r.uniform(0, 0.5), r.uniform(0.5, 1)]
        
    def update_pos(self):
        self.dx = (a*self.x+self.y*self.z) * df
        self.dy = (b*self.x + c*self.y - self.x*self.z) * df
        self.dz = (-self.z - self.x*self.y) * df
        
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
    #glTranslatef(0, 0, 25)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3f(1,1,1)
            glVertex3fv(vertices[vertex])
    glEnd()
    #glTranslatef(0, 0, -25)
    
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

glTranslate(0, 0, -50)
glScale(0.4, 0.4, 0.4)
glRotatef(-60, 1, 0, 0) 
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

pygame.font.init()

font = pygame.font.SysFont("Arial", 24)

for i in range(2000):
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
    render_text(25, 2, 2, "X")
    render_text(2, 25, 2, "Y")
    render_text(2, 2, 25, "Z")
    
    #glLoadIdentity()
    glTranslatef(0, 0, 25)
    glRotatef(0.5, 0, 0, 1)
    
    glTranslatef(0, 0, -25)
    
    #glRotatef(0.25, 0, 1, 0)
    #glTranslate(0, 0, -50)
        
    pygame.display.flip()