import pygame
from calc import  * 
# Define colours
black = (0, 0, 0)
white = (255, 255, 255)
midnight_blue = pygame.Color("#23283D")
dark_navy = pygame.Color("#101116")

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
            pygame.draw.rect(screen, dark_navy, self.rect)
            txt = self.font.render(self.text, True, white)
            txt_rect = txt.get_rect(center=self.rect.center)
            screen.blit(txt, txt_rect)
    
    def clicked(self):
        self.func()


# Initialize UI components
buttons = []
# Button 1
def_button = Button(20, VIEWPORT_H+20, text="FIT")
buttons.append(def_button)

def pixel(surface, color, pos):
    # pygame.draw.line(surface, color, pos, pos)
    pygame.draw.circle(surface, color, pos, 2)

def drawUI():
    pygame.draw.rect(screen, midnight_blue, (0,VIEWPORT_H,VIEWPORT_R,SCREEN_H))
    def_button.draw()
    
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
                x_vals, y_vals = zip(*point_list)
                # print(x_vals)
                # print(y_vals)
                lobf = polyfit(x_vals, y_vals, 0, VIEWPORT_W)
                lobf_exists = True
                # print(lobf["points"])
                update_screen = True

        if mouse_down:
            x, y = pygame.mouse.get_pos()
            if VIEWPORT_L <= x <= VIEWPORT_R and y <= VIEWPORT_H: 
                bisect.insort(point_list, (x, y))
                update_screen = True
            for i, button in enumerate(buttons):
                if button.rect.collidepoint((x,y)):
                    button_clicked = i
        else: # mouse up
            button_clicked = -1

    # Processing button presses
    if button_clicked == 0:
        try:
            x_vals, y_vals = zip(*point_list)
        except:
            pass
        lobf = polyfit(x_vals, y_vals, 0, VIEWPORT_W)
        lobf_exists = True
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

        for pos in point_list:
            pixel(screen, black, pos)

        drawUI()
        
    pygame.display.update()