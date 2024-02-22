import pygame
import math
import numpy as np

running = True

width = 1200
height = 700

#############

tileSize = 50
fov = math.pi/3
half_fov = fov/2

rayCount = 8
rayLength  = 80
#raySpread = math.pi + math.pi
raySpread = math.pi

arrayA = []


####################3

###########car rotation
max_vel = 100
ratation_vel= 0

angle = 0

############### CAR Posistion


player_pos =pygame.Vector2(700,590)

def distance(x1,y1,x2,y2):
    return math.hypot(x2-x1,y2-y1)

def lerp(A,B,t):
    return A+(B-A)*t
def line_intersection(x1,y1,x2,y2,x3,y3,x4,y4):
    d =(y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)
    s = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3))/d
    t = ((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3))/d

    if (0<= s <=1 and 0 <= t <= 1):
        x = x1+s * (x2 - x1)
        y = y1 + s*(y2-y1)
        return x,y

    else:
        return None
        
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((width,height))

def add_ray():
    rays = []
    for ray in range(rayCount):
        rayAngle = lerp(raySpread/2,-raySpread/2,ray/(rayCount-1))
        #print("rayAngle is ",rayAngle)

        start = [player_pos.x,player_pos.y]
        b = math.sin(rayAngle)*rayLength
        c = math.cos(rayAngle)*rayLength

        #print("b is ",b,"c is ",c)
        end = [
        player_pos.x - math.sin(rayAngle+angle)*rayLength,
        player_pos.y - math.cos(rayAngle+angle)*rayLength
        ]
        rays.append([start,end])

    for i in range(len(rays)):
        pygame.draw.line(screen,(233,22,2),rays[i][0],rays[i][1],4)
    return rays

while running:

    #filled screen with black color to
    #avoid the trail

    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()
            break
            
    add_ray()

    pygame.draw.circle(screen,(30,200,179),[player_pos.x,player_pos.y],20)
    
    pygame.draw.line(screen,(233,222,2),[800,100],[800,600],4)
    pygame.draw.line(screen,(233,222,2),[80,100],[800,100],4)
    pygame.draw.line(screen,(233,222,2),[600,300],[600,600],4)
    pygame.draw.line(screen,(233,222,2),[80,300],[600,300],4)

    pygame.draw.line(screen,(233,222,2),[80,100],[80,300])
    pygame.draw.line(screen,(233,222,2),[800,600],[600,600])

    wallNp = np.array([
    [800,100,800,600],
    [80,100,800,100],
    [600,300,600,600],
    [80,300,600,300],
    [80,100,80,300],
    [800,600,600,600]
    ])

    arrayA= add_ray()
    #print(arrayA)
    arrayB=[]
    arrayC=[]

    arrayD = []
    for i in range(len( arrayA)):
        arrayD.append([*arrayA[i][0],*arrayA[i][1]])


    for a in arrayA:
        arrayB.append(a)
        
    movement_vector = np.array([arrayB])

    distN =[]

    for wall in wallNp:

        for a in arrayD:

            result =line_intersection(*a,*wall)
            
            if result:
                done = True
                x = int(result[0])

                y = int(result[1])

                distN.append([x,y])
                
                pygame.draw.circle(screen,(200,200,200),[x,y],5)

    #print("dist Is ",distN)

    Dist=[]

    for a in distN:
        z = distance(*a,player_pos.x,player_pos.y)
        Dist.append(z)
        
    #print("distance between is ",Dist)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_pos.y += 1
        angle += 0.01

    if keys[pygame.K_DOWN]:
        player_pos.y -= 1
        angle -= 0.01

    if keys[pygame.K_RIGHT]:

        player_pos.x -= 1

    if keys[pygame.K_LEFT]:
        player_pos.x += 1


    pygame.display.update()
    clock.tick(30)



pygame.quit()
print("exit")
print("exit")
