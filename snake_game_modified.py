import pygame
import time
import random
 
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (0, 0, 225)
 
dis_width = 600
dis_height = 400
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game modified by REX')

clock = pygame.time.Clock()

snake_img = pygame.image.load('snake2.png')
apple_img = pygame.image.load("apple.png")
tail_img = pygame.image.load('tail1.png')
apple_img_rect = apple_img.get_rect()

snake_block = 10
snake_speed = 15
 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 25)
level_font = pygame.font.SysFont("comicsansms", 25)
scores_font = pygame.font.SysFont("comicsansms", 20)

 
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

def Your_level(level):
    value = level_font.render("Level: " + str(level), True, white)
    dis.blit(value, [dis_width - 125, 0])
 
def our_snake(snake_block, snake_list, x1_change, y1_change, tail_img):
    snake_img_rotate = snake_img # initialize snake_img_rotate to snake_img
    for i, x in enumerate(snake_list):
        if i == len(snake_list) - 1: # the head of the snake
            if x1_change == snake_block:
                snake_img_rotate = pygame.transform.rotate(snake_img, 270) # rotate counterclockwise
            elif x1_change == -snake_block:
                snake_img_rotate = pygame.transform.rotate(snake_img, 90) # rotate clockwise
            elif y1_change == snake_block:
                snake_img_rotate = pygame.transform.rotate(snake_img, 180) # no rotation
            elif y1_change == -snake_block:
                snake_img_rotate = pygame.transform.rotate(snake_img, 0) # upside down
            dis.blit(snake_img_rotate, [x[0], x[1], snake_block, snake_block])
        elif i == 0: # the tail of the snake
            tail_rect = pygame.Rect(x[0], x[1], snake_block, snake_block)
            dis.blit(tail_img, tail_rect)
        else:
            pygame.draw.rect(dis, blue, [x[0], x[1], snake_block, snake_block])

def write_score(score):
    with open('scores.txt', 'a') as file:
        file.write(str(score) + '\n')
    
def read_scores():
    with open('scores.txt') as file:
        scores = file.readlines()
        scores = [int(score.strip()) for score in scores]
        scores.sort(reverse=True)
        return scores[:10]
    
def display_scores(scores):
    y = 50
    text = score_font.render("Top Scores", True, white)
    dis.blit(text, [dis_width - 600, y])
    y += 30
    for score in scores:
        text = score_font.render(str(score), True, white)
        dis.blit(text, [dis_width - 550, y])
        y += 30

                
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
 
def gameLoop():
    
    global snake_speed
    
    game_over = False
    game_close = False
 
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Length_of_snake = 1

    level = 1
    level_up_score = 10
 
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
 
    while not game_over:
 
        while game_close == True:
            dis.fill(black)
            message("You Lost! Press P-Play Again or Q-Quit", red)
            Your_score(Length_of_snake - 1)
            write_score(Length_of_snake - 1)
            scores = read_scores()
            display_scores(scores)
            Your_level(level)
            pygame.display.update()
            
            if game_close:
                snake_speed = 15
                level = 1
                level_up_score = 10
                Length_of_snake = 1
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_p:
                        gameLoop()
                        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_close = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                    
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(black)
        dis.blit(apple_img, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List, x1_change, y1_change, tail_img)
        Your_score(Length_of_snake - 1)
        Your_level(level)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

            if Length_of_snake - 1 == level_up_score:
                level += 1
                level_up_score += 10
                snake_speed += 50

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
