import pygame
import math
pygame.init()

width, height = 1200, 800
center_x = width/2
center_y = height/2
EH_R = 25
E=1
d_lamda= 2
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
        # d_r = dr_sign * math.sqrt(abs(inside)) * d_lamda
        # if phi < -1.5708:
        #     d_r = - math.sqrt(inside)
        # else:
        #     d_r = math.sqrt(inside)

        d_phi = (L/r**2) * d_lamda

        return d_r, d_phi, dr_sign

def RK4(r, phi, dr_sign, L, starting_y):
    if starting_y <= center_y:
        k1 = calculations(r, phi, dr_sign, L)
        k2 = calculations(r + k1[0]/2, phi + k1[1]/2, dr_sign, L)
        k3 = calculations(r + k2[0]/2, phi + k2[1]/2, dr_sign, L)
        k4 = calculations(r + k3[0], phi + k3[1], dr_sign, L)

        d_rt = (k1[0] + 2* k2[0] + 2* k3[0] + k4[0])/6
        d_phit = (k1[1] + 2* k2[1] + 2* k3[1] + k4[1])/6
        

        if d_rt > 0:
            dr_sign *= -1

        print(k1[0], d_rt, k1[2])
        return d_rt, d_phit, k1[2]
        # return k1[0], k1[1], k1[2]
           
        
    else:
        k1 = calculations(r, phi, dr_sign, L)
        k2 = calculations(r + k1[0]/2, phi - k1[1]/2, k1[2], L)
        k3 = calculations(r + k2[0]/2, phi - k2[1]/2, k2[2], L)
        k4 = calculations(r + k3[0], phi - k3[1], k3[2], L)

        d_r = (k1[0] + 2* k2[0] + 2* k3[0] + k4[0])/6
        d_phi = (k1[1] + 2* k2[1] + 2* k3[1] + k4[1])/6

        if d_r > 0:
            dr_sign *= -1
            
        print(d_r, dr_sign)
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

        # r, phi = xy_to_rphi(x, y)
        # print(x, y, r, math.degrees(phi))
        # if self.r >= EV_R :
        #     pygame.draw.line(win, white, (x, y), (x, y), 4)
        #     # pygame.draw.circle(win, white, (int(self.x), int(self.y)), 3)
        #     if len(self.path) > 2:
        #         updated_path = []
        #         for point in self.path:
        #             updated_path.append((point))
        #         pygame.draw.lines(win, white , False, updated_path, 1)

        pygame.draw.line(win, white, (x, y), (x, y), 4)

        if len(self.path) > 2:
            updated_path = []
            for point in self.path:
                updated_path.append((point))
            
            pygame.draw.lines(win, white , False, updated_path, 1)

        # pygame.draw.lines(win, white, False, self.path, 1)

        
    
    def update_light(self):

        x = self.x
        y = self.y
        starting_y = self.starting_y
        # d_r, d_phi = calculations(r, phi)
        b = abs(starting_y - center_y)
        L = b * E

        r, phi = xy_to_rphi(x , y)

        d_r, d_phi, self.dr_sign = RK4(r, phi, self.dr_sign, L, starting_y)

        

        if r > EH_R :
            r += d_r
            if starting_y <= center_y:
                phi += d_phi
            else: phi -= d_phi

            self.x, self.y = rphi_to_xy(r, phi)
            # self.x += 5
            # self.y += 0
            # print(self.x , self.y)
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

    # light1 = light(0, 170)
    black_hole = mass(EH_R)

    light1 = light(0, 10)
    light2 = light(0, 100)
    light3 = light(0, 200)
    light4 = light(0, 300)
    light5 = light(0, 350)
    light6 = light(0, 400)
    light7 = light(0, 450)
    light8 = light(0, 500)
    light9 = light(0, 600)
    light10 = light(0, 700)
    light11 = light(0, 790)
    light12 = light(0, 50)
    light13 = light(0, 150)
    light14 = light(0, 250)
    light15 = light(0, 375)
    light16 = light(0, 425)
    light17 = light(0, 550)
    light18 = light(0, 650)
    light19 = light(0, 750)

    light1 = light(0, 335.0480947)
    
    
    light_rays = [light1, light2, light3, light4, light5, light6, light7, light8, light9, light10, light11, light12, light13, light14, light15, light16, light17, light18, light19]

    while run:
        clock.tick(60)

        WIN.fill(black)
        # pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        black_hole.draw_c(WIN)

        # for rays in light_rays:
        #     rays.draw(WIN)
        #     rays.update_light()

        light3.draw(WIN)
        light3.update_light()
        
        pygame.display.update()

    pygame.quit()

main()