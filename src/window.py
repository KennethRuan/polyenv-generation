import pygame
from calc import  * 
# Define colours
black = (0, 0, 0)
white = (255, 255, 255)
midnight_blue = pygame.Color("#23283D")
dark_navy = pygame.Color("#101116")
mid_blue = pygame.Color("#323F5C")

# Define Screen Sizes
SCREEN_W = 960
SCREEN_H = 540
VIEWPORT_W = 960
VIEWPORT_H = 360
VIEWPORT_L = SCREEN_W//2 - VIEWPORT_W//2
VIEWPORT_R = SCREEN_W//2 + VIEWPORT_W//2

# Initialize simulation variables
pygame.init()
run = True
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
LMB = 1
mouse_down = False
update_screen = False
lobf_exists = False
button_clicked = -1
slider_clicked = -1
point_list = []
lobf = {}

class Button():
    def __init__(self, x, y, w=100, h=50, text="def", image=None, func=None):
        self.hasImage = True if image else False
        self.font = pygame.font.SysFont('Helvetica', 25)
        self.text = text
        self.func = func

        if self.hasImage:
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
        else:
            self.rect = pygame.Rect(x, y, w, h)
        
    def draw(self):
        if self.hasImage:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(screen, dark_navy, self.rect, border_radius=10)
            txt = self.font.render(self.text, True, white)
            txt_rect = txt.get_rect(center=self.rect.center)
            screen.blit(txt, txt_rect)
    
    def clicked(self):
        self.func()

class Slider():
    def __init__(self, val, mini, maxi, x, y, w=920, h=50):
        self.val = val
        self.mini = mini
        self.maxi = maxi
        self.per = (val-mini)/maxi
        
        # bar dimensions
        self.b_x = x
        self.b_y = y
        self.b_w = w
        self.b_h = h
        self.b_rect = pygame.Rect(self.b_x, self.b_y, self.b_w, self.b_h)

        # slider dimensions
        self.s_x = self.b_x+self.per*(self.b_w)
        self.s_y = y
        self.s_w = 10
        self.s_h = 30
        self.s_rect = pygame.Rect(0, 0, self.s_w, self.s_h)
        self.s_rect.center = (self.s_x, self.b_y+self.b_h//2)

    def draw(self):
        pygame.draw.rect(screen, dark_navy, self.b_rect, border_radius=10)
        pygame.draw.rect(screen, mid_blue, self.s_rect)

    def setVal(self, val):
        self.val = max(self.mini, min(self.b_w, val))
        self.per = (self.val-self.mini)/(self.b_w)
        self.s_rect.centerx = self.b_x+(self.per*self.b_w)
        # print("val", self.val, "per", self.per, "x", self.s_rect.centerx)

# Initialize UI components
buttons = []
sliders = []
# Button 1
def_button = Button(20, VIEWPORT_H+20, text="FIT")
buttons.append(def_button)

# Slider 1
left_slider = Slider(100, 0, VIEWPORT_W-20, 20, 450, VIEWPORT_W-40, 15)
sliders.append(left_slider)

#Slider 2
right_slider = Slider(800, 0, VIEWPORT_W-20, 20, 500, VIEWPORT_W-40, 15)
sliders.append(right_slider)

def pixel(surface, color, pos):
    # pygame.draw.line(surface, color, pos, pos)
    pygame.draw.circle(surface, color, pos, 2)

def drawUI():
    pygame.draw.rect(screen, midnight_blue, (0,VIEWPORT_H,VIEWPORT_R,SCREEN_H))
    def_button.draw()
    left_slider.draw()
    right_slider.draw()
    
screen.fill(white)
drawUI()
while run:

    # Processing inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LMB:
            mouse_down = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == LMB:
            mouse_down = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                point_list.clear()
                update_screen = True
            if event.key == pygame.K_c:
                if point_list:
                    x_vals, y_vals = zip(*point_list)
                    # print(x_vals)
                    # print(y_vals)
                    lobf = polyfit(x_vals, y_vals, 0, VIEWPORT_W)
                    lobf_exists = True
                    # print(lobf["points"])
                    update_screen = True
            if event.key == pygame.K_r:
                if lobf_exists:
                    print(arclength(left_slider.s_rect.centerx, right_slider.s_rect.centerx, lobf["polynomial"]))

        if mouse_down:
            x, y = pygame.mouse.get_pos()
            if button_clicked == -1 and slider_clicked == -1:
                if VIEWPORT_L <= x <= VIEWPORT_R and y <= VIEWPORT_H: 
                    bisect.insort(point_list, (x, y))
                    update_screen = True
                for i, button in enumerate(buttons):
                    if button.rect.collidepoint(x, y):
                        button_clicked = i
                for i, slider in enumerate(sliders):
                    if slider.s_rect.collidepoint(x, y):
                        # print(i, "clicked")
                        slider_clicked = i
        else: # mouse up
            # Processing button presses
            # Only processes upon mouse up
            if button_clicked == 0:
                if point_list:
                    x_vals, y_vals = zip(*point_list)
                    lobf = polyfit(x_vals, y_vals, 0, VIEWPORT_W)
                    lobf_exists = True
                    update_screen = True
            button_clicked = -1
            slider_clicked = -1

        # Processing slider movement
        if slider_clicked >= 0:
            x, y = pygame.mouse.get_pos()
            sliders[slider_clicked].setVal(x - sliders[slider_clicked].b_x)
            update_screen = True
            
    # Processing visual updates
    if update_screen:
        update_screen = False

        # Plot points and curve
        screen.fill(white)
        
        if lobf_exists:
            func_points = lobf["points"]
            for i in range(0, len(lobf["points"])-1):
                pygame.draw.rect(screen, (50,120,50), (func_points[i][0],func_points[i+1][1], func_points[i+1][0]-func_points[i][0], VIEWPORT_H-func_points[i+1][1]))
                pygame.draw.line(screen, (255, 0, 0), func_points[i], func_points[i+1])

            # Red Pole controlled by slider 0
            red_pole = pygame.Rect(0,0,2,30)
            red_pole.centerx = sliders[0].s_rect.centerx
            red_pole.bottom = lobf["points"][red_pole.centerx][1]
            pygame.draw.rect(screen, (255,0,0), (red_pole))

            # Blue Pole controlled by slider 1
            blue_pole = pygame.Rect(0,0,2,30)
            blue_pole.centerx = sliders[1].s_rect.centerx
            blue_pole.bottom = lobf["points"][blue_pole.centerx][1]
            pygame.draw.rect(screen, (0,0,255), (blue_pole))

        for pos in point_list:
            pixel(screen, black, pos)

        drawUI()
        
    pygame.display.update()