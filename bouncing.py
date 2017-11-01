"""
Bouncing balls with collision


"""


import simplegui
import math
import random

WIDTH = 800
HEIGHT = 600

def rand(a,b):
    return a + (b-a)*random.random()

class Vector:
    #Class static methods to create Vectors from other data types
    
    def from_list(lst):
         return Vector(lst[0], lst[1])
    
    def from_angle(a):
        return Vector(math.cos(a), math.sin(a))
    
    #Object methods
    def __init__(self, x ,y):
        self.x = x
        self.y = y
        
    def as_list(self):
        return [self.x, self.y]
        
    def dist_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def angle(self):
        return math.atan2(self.y, self.x)
        
    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)
    
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self
    
    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)
    
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self
    
    def __mul__(self, other):
        return Vector(self.x*other.x, self.y*other.y)
    
    def __imul__(self, other):
        self.x *= other.x
        self.y *= other.y
        return self
    
    def __div__(self, other):
        return Vector(self.x/other, self.y/other)
    
    def __idiv__(self, other):
        self.x /= other
        self.y /= other
        return self
    
    def rotate(self, origin, angle):
        x = self.x - origin.x
        y = self.y - origin.y
        x2 = x*math.cos(angle) - y*math.sin(angle)
        y2 = x*math.sin(angle) + y*math.cos(angle)
        self.x = x2 + origin.x
        self.y = y2 + origin.y
        
    
    def __mod__(self, other):
        return Vector(self.x % other.x, self.y % other.y)
    
    def dot_product(self, other):
        return self.x*other.x + self.y*other.y
    
    
    def __str__(self):
        return "Vector[" + str(self.x) + ", " + str(self.y) +"]" 
    
    def clone(self):
        return Vector(self.x, self.y)

class Ball:
    def __init__(self, pos, vel, radius):
        self.pos=Vector.clone(pos)
        self.vel=Vector.clone(vel)
        self.radius = radius
        self.mass = radius*radius
        
    def collide(self, other):
        return self.pos.dist_to(other.pos)<=self.radius+other.radius
    
    def update(self):
        #Update position and handle bouncing off the walls
        self.pos = (self.pos + self.vel)
        if self.pos.x<self.radius:
            self.pos.x = 2*self.radius-self.pos.x
            self.vel.x*=-1
        elif self.pos.x>WIDTH-self.radius:
            self.pos.x = 2*(WIDTH-self.radius) - self.pos.x
            self.vel.x*=-1
            
        if self.pos.y<self.radius:
            self.pos.y = 2*self.radius-self.pos.y
            self.vel.y*=-1
        elif self.pos.y>HEIGHT-self.radius:
            self.pos.y = 2*(HEIGHT-self.radius) - self.pos.y
            self.vel.y*=-1 
            
            
    def draw(self, canvas):
        canvas.draw_circle(self.pos.as_list(), self.radius, 1, "White", "blue")
        
# Handler for mouse click
def click():
    global message
    message = "Good job!"

# Handler to draw on canvas
def draw(canvas):
   
        
    #Handle bal collisions
    for i1, b1 in enumerate(ball_list):
        for b2 in ball_list[i1+1:]:
            if b1.collide(b2):             
                n = b2.pos-b1.pos
                n/=n.magnitude()
                p = 2*(b1.vel.dot_product(n) - b2.vel.dot_product(n))/(b1.mass + b2.mass)
                
                b1.vel = b1.vel -Vector(p*b2.mass, p*b2.mass) * n
                b2.vel = b2.vel +Vector(p*b1.mass, p*b1.mass) * n

        #Update positions and draw
        b1.update() 
        b1.draw(canvas)


#Calculate sum of velocity magnitudes to check we aren't
#increasing overall 'energy' of the system
    E=sum([ball.vel.magnitude() for ball in ball_list])
    canvas.draw_text(str(E), (5,20), 20, "White", "sans-serif")
                
# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", WIDTH, HEIGHT)
frame.set_draw_handler(draw)


#Create a list of random balls
ball_list = []
for n in range(15):
    ok = False
    while not ok:
        ok=True
        r=rand(10,50)
        ball = Ball(Vector(rand(r,WIDTH-r),rand(r,HEIGHT-r)),
                    Vector(rand(-2,2),rand(-1.8,1.8)), r)
        for b in ball_list:
            if b.collide(ball):
                ok = False
                break
        if ok:
            ball_list.append(ball)
    


# Start the frame animation
frame.start()

