import pygame
import math
pygame.init()

width, height = 1200, 800
center_x = width/2
center_y = height/2
EH_R = 22
E=1
d_lamda= 1
# starting_y = 170.096189435
# starting_y = 10
# b = 675
# L = math.sqrt(b*EH_R/2)


white = (255, 255, 255)
black = (0, 0, 0)

WIN =pygame.display.set_mode((width, height))
pygame.display.set_caption("light simulation")


def xy_to_rphi(x, y):
    r = math.sqrt((x - center_x)**2 + (y - center_y)**2)
    phi = math.atan2(y - center_y, x - center_x)
    return r, phi

def rphi_to_xy(r, phi):
    x = center_x + r * math.cos(phi)
    y = center_y + r * math.sin(phi)
    return x, y

def calculations(r, phi, dr_sign, L):
        # d_r = math.sqrt(E**2 - (1 - (EH_R/r)) * (L/r)**2)
        term = (1 - EH_R/r) * (L/r)**2
        inside = E**2 - term

        # print(r, inside, dr_sign)
         # turning point: inside becomes negative very slightly
        if inside < 0:
            inside = abs(inside)
            dr_sign *= -1  # flip direction (bounce)

        d_r = dr_sign * math.sqrt(inside) * d_lamda
        d_phi = (L/r**2) * d_lamda

        return d_r, d_phi, dr_sign



class light:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.starting_y = y
        self.path = []
        self.dr_sign = -1

        # self.r = math.sqrt((x - center_x)**2 + (y - center_y)**2)
        # self.phi = math.atan2( x - center_x , y - center_y)
        # return(self.r , self.phi)
    
    def draw(self, win):
        x = self.x
        y = self.y

        pygame.draw.line(win, white, (x, y), (x, y), 4)

        if len(self.path) > 2:
            updated_path = []
            for point in self.path:
                updated_path.append((point))
            
            pygame.draw.lines(win, white , False, updated_path, 1)


        
    
    def update_light(self):

        x = self.x
        y = self.y
        starting_y = self.starting_y
        # d_r, d_phi = calculations(r, phi)
        b = abs(starting_y - center_y)
        L = b * E

        r, phi = xy_to_rphi(x , y)

        d_r, d_phi, self.dr_sign = calculations(r, phi, self.dr_sign, L)

        

        if r > EH_R :
            r += d_r
            if starting_y <= center_y:
                phi += d_phi
            else: phi -= d_phi

            self.x, self.y = rphi_to_xy(r, phi)
            self.path.append((self.x , self.y))



class mass:
    def __init__(self, R):
        self.x = center_x
        self.y = center_y
        self.R = R

    def draw_c(self, win):
        pygame.draw.circle(win, white, (self.x, self.y), self.R)




def main():
    run = True
    clock = pygame.time.Clock()

    black_hole = mass(EH_R)
    light1 = light(0, 342.8423233502)   #for EH_R = 22

    light_rays = []
    for x in range(0, 800, 20):
        light_rays.append(light(0, x))

    while run:
        clock.tick(60)

        WIN.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        black_hole.draw_c(WIN)

        for rays in light_rays:
            rays.draw(WIN)
            rays.update_light()

        # light1.draw(WIN)
        # light1.update_light()
        
        pygame.display.update()

    pygame.quit()

main()