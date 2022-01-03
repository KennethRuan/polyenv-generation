import pygame
import bisect
import numpy as np

# Define colours
black = (0, 0, 0)
white = (255, 255, 255)

# Initialize simulation variables
pygame.init()
run = True
screen = pygame.display.set_mode((640, 400))
LMB = 1
mouse_down = False
update_screen = False
lobf_exists = False
point_list = []
lobf = {}

def pixel(surface, color, pos):
    pygame.draw.line(surface, color, pos, pos)

def polyfit(x, y):
    results = {}

    old_fit = -1
    cur_fit = 0
    n=1
    while old_fit < cur_fit and n <= 10:
        old_fit = cur_fit

        coeffs = np.polyfit(x, y, n)

        # Find r^2 to determine fit
        p = np.poly1d(coeffs)
        yhat = p(x)                        
        ybar = np.sum(y)/len(y)        
        ssreg = np.sum((yhat-ybar)**2)   
        sstot = np.sum((y - ybar)**2) 
        cur_fit = ssreg / sstot
        n += 1

    coeffs = np.polyfit(x, y, n-1)
    results['polynomial'] = coeffs.tolist()
    results['determination'] = old_fit

    print(n-1)
    poly = np.poly1d(coeffs)
    nx = np.linspace(0,640,num=641)
    ny = poly(nx)

    points = []
    for i in range(len(nx)):
        points.append((nx[i], ny[i]))
    results['points'] = points
    return results

screen.fill(white)
while run:
    # print("running")

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
                lobf = polyfit(x_vals, y_vals)
                lobf_exists = True
                # print(lobf["points"])
                update_screen = True

        if mouse_down:
            x, y = pygame.mouse.get_pos()
            bisect.insort(point_list, (x, y))
            update_screen = True

    if update_screen:
        update_screen = False
        screen.fill(white)
        for pos in point_list:
            pixel(screen, black, pos)
        if lobf_exists:
            func_points = lobf["points"]
            for i in range(0, len(lobf["points"])-1):
                pygame.draw.line(screen, (255, 0, 0), func_points[i], func_points[i+1])

    pygame.display.update()