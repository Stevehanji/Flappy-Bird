import pygame
import random
import json

# Call file json
with open("game.json",mode = "r") as json_data:
    file = json.load(json_data)
    json_data.close()

with open("url.json",mode="r") as json_data:
    url = json.load(json_data)
    json_data.close()

with open("url_sound.json",mode = "r") as json_data:
    file_sound = json.load(json_data)
    json_data.close()

pygame.init()
screen_width = file["screen"]["screen_width"]
screen_height = file["screen"]["screen_height"]
screen = pygame.display.set_mode((screen_width,screen_height),pygame.DOUBLEBUF,32)

caption = file["screen"]["caption"]
pygame.display.set_caption(caption)

icon = pygame.image.load(url["icon"])
pygame.display.set_icon(icon)

White = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
black = (0,0,0)

# Set sound
sound_die = pygame.mixer.Sound(file_sound["die"])
sound_hit = pygame.mixer.Sound(file_sound["hit"])
sound_wing = pygame.mixer.Sound(file_sound["wing"])
sound_point = pygame.mixer.Sound(file_sound["point"])

# Set image
    # Background
try:
    bg_img = pygame.image.load(url["background"])
    bg_img = pygame.transform.scale(bg_img,(screen_width,screen_height))
    bg_x = 0
    bg_y = 0
    try:
        velocity_background = file["move"]["velocity_background"]
    except:
        print("error")
except:
    print("No Background image")

    # Create Floor
try:
    floor_img = pygame.image.load(url["floor"])
    floor_img = pygame.transform.scale(floor_img,(screen_width,200))
    floor_x = 0
    floor_y = screen_height - floor_img.get_height() + 100
    velocity_floor = file["move"]["velocity_floor"]
except:
    print("No Floor image")

floor_rect = floor_img.get_rect(topleft = (floor_x,floor_y))

    # Create bird
try:
    bird1 = pygame.image.load(url["bird"]["bird1"])
    bird1 = pygame.transform.scale(bird1,(60,50))
    bird2 = pygame.image.load(url["bird"]["bird2"])
    bird2 = pygame.transform.scale(bird2,(60,50))
    bird3 = pygame.image.load(url["bird"]["bird3"])
    bird3 = pygame.transform.scale(bird3,(60,50))
except:
    print("No Bird Image")

gravity = file["move"]["gravity"]
bird_list = [bird1,bird2,bird3]
bird_index = 1
bird = bird_list[bird_index]
bird_x = 50
bird_y = screen_height // 2
bird_rect = bird.get_rect(center = (bird_x,bird_y))
velocity_drop = 0

bird_flap = pygame.USEREVENT + 0
pygame.time.set_timer(bird_flap,50)

# Create function
def draw_bg(floor_rect):
    screen.blit(bg_img,(bg_x,bg_y))
    screen.blit(bg_img,(bg_x+screen_width,bg_y))
    screen.blit(floor_img,floor_rect)
    screen.blit(floor_img,(floor_rect.x + screen_width,floor_rect.y))

def bird_animtion():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (bird_x,bird_rect.centery))
    return new_bird, new_bird_rect

def bird_rotate(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-velocity_drop*3,1)

    if velocity_drop > 11:
        new_bird = pygame.transform.rotozoom(bird1,-velocity_drop*6,1)
    return new_bird

game_pause = False
count1 = 0

game_over_img = pygame.image.load(url["gameover"])
game_over_img = pygame.transform.scale(game_over_img,(384,84))

def draw_game_over():
    screen.blit(game_over_img,(screen_width//2 - 190,screen_height // 2-84))

# Create pipe
spawnpipe = pygame.USEREVENT
velocity_pipe = file["move"]["velocity_pipe"]
pygame.time.set_timer(spawnpipe, 1000)
pipe_image = pygame.image.load(url["pipe"])
pipe_image = pygame.transform.scale2x(pipe_image)
pipe_list = []

def create_pipe():
    random_pipe_pos = random.randint(260,400)
    bottom_pipe = pipe_image.get_rect(midtop = (screen_width+100,random_pipe_pos))
    top_pipe = pipe_image.get_rect(midtop = (screen_width+100,random_pipe_pos - 700))
    return bottom_pipe, top_pipe

def create_line_score():
    bottom_score = pygame.Rect(screen_width + 100,0,1,screen_height)
    return bottom_score

def move_pipe(pipes,velocity_pipe):
    for pipe in pipes:
        pipe.centerx -= velocity_pipe
    
    return pipes, velocity_pipe

velocity_line = velocity_pipe

def move_line(lines, velocity_line):
    for line in lines:
        line.x -= velocity_line
    
    return lines, velocity_line

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= screen_height - 100:
            screen.blit(pipe_image,pipe)
        else:
            screen.blit(pygame.transform.flip(pipe_image,False,True),pipe)

def draw_rect_alpha(screen,color,rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size,pygame.SRCALPHA)
    pygame.draw.rect(shape_surf,color,(shape_surf.get_rect()))
    screen.blit(shape_surf,rect)

def draw_line(lines):
    for line in lines:
        draw_rect_alpha(screen,(255,255,255,0),line)

collision_floor = False

score = 0
high_score = file["high_score"]
score_line_pipe = []
count2 = 0

def draw_score(score):
    font = pygame.font.SysFont("04B_19.TTF",50)
    score_txt = font.render(f"Score: {score}",True,black)
    screen.blit(score_txt,(screen_width // 2 - score_txt.get_width() + 70, 50))

def draw_high_score(high_score,score):
    font = pygame.font.SysFont("04B_19.TTF",60)
    if high_score < score:
        high_score = score

    score_txt = font.render(f"High Score: {high_score}",True,black)
    screen.blit(score_txt,(screen_width // 2 - score_txt.get_width() + 140, 100))

    return high_score

count3 = 0

game_Start = True
start_img = pygame.image.load(url["gamestart"])
start_img = pygame.transform.scale(start_img,(145*2,210*2))

def main():
    global bg_x
    global floor_x
    global velocity_drop
    global gravity
    global bird_index
    global bird_rect
    global bird
    global game_pause
    global velocity_floor
    global velocity_background
    global count1
    global pipe_list
    global velocity_pipe
    global collision_floor
    global score
    global velocity_line
    global score_line_pipe
    global count2
    global high_score
    global count3
    global game_Start

    run = True
    FPS = 60
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        screen.fill(White)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                file["high_score"] = high_score

                with open("game.json",mode = "w") as json_file:
                    json.dump(file,json_file,indent=4,separators=(",",": "))
                run = False
                break
            
            if game_Start == False:
                if game_pause == False:
                    
                    if event.type == spawnpipe:
                        score_line_pipe.append(create_line_score())
                        pipe_list.extend(create_pipe())
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                            sound_wing.play()
                            velocity_drop = 0
                            velocity_drop -= file["move"]["velocity_drop"]
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1 or event.button == 2 or event.button == 3:
                            sound_wing.play()
                            velocity_drop = 0
                            velocity_drop -= file["move"]["velocity_drop"]
            
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w) and game_Start == True:
                    game_Start = False
                    velocity_drop = 0
                    velocity_drop -= file["move"]["velocity_drop"]
                
                if event.key == pygame.K_ESCAPE:
                    file["high_score"] = high_score

                    with open("game.json",mode = "w") as json_file:
                        json.dump(file,json_file,indent=4,separators=(",",": "))
                    run = False
                    break
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button == 1 or event.button == 2 or event.button == 3) and game_Start == True:
                    game_Start = False
                    velocity_drop = 0
                    velocity_drop -= file["move"]["velocity_drop"]
            
            if game_pause:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                        if collision_floor == True:
                            bird = pygame.transform.rotozoom(bird,90,1)
                        bird_rect.centery = bird_y
                        gravity = file["move"]["gravity"]
                        velocity_background = file["move"]["velocity_background"]
                        velocity_floor = file["move"]["velocity_floor"]
                        count1 = 0
                        pipe_list.clear()
                        score_line_pipe.clear()
                        velocity_pipe = file["move"]["velocity_pipe"]
                        velocity_line = file["move"]["velocity_pipe"]
                        collision_floor = False
                        score = 0
                        game_pause = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 or event.button == 2 or event.button == 3:
                        if collision_floor == True:
                            bird = pygame.transform.rotozoom(bird,90,1)
                        bird_rect.centery = bird_y
                        gravity = file["move"]["gravity"]
                        velocity_background = file["move"]["velocity_background"]
                        velocity_floor = file["move"]["velocity_floor"]
                        count1 = 0
                        pipe_list.clear()
                        score_line_pipe.clear()
                        velocity_pipe = file["move"]["velocity_pipe"]
                        velocity_line = file["move"]["velocity_pipe"]
                        collision_floor = False
                        score = 0
                        game_pause = False


        # Draw
        draw_bg(floor_rect)

        # pipe
        if game_Start == False:
            pipe_list, velocity_pipe = move_pipe(pipe_list,velocity_pipe)
            score_line_pipe, velocity_line = move_line(score_line_pipe,velocity_line)
            draw_pipe(pipe_list)
            draw_line(score_line_pipe)

        if len(pipe_list) > 6:
            del pipe_list[0]
        
        # Score
        draw_score(score)
        
        # Bird

        # Animation
        if game_pause == False and count3 == 10:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            
            count3 = 0
            bird, bird_rect = bird_animtion()

        count3 += 1

        bird_rotated = bird_rotate(bird)
        screen.blit(bird_rotated,bird_rect)
        bg_x -= velocity_background
        floor_rect.x -= velocity_floor

        if bg_x < -screen_width:
            bg_x = 0
        
        if floor_rect.x < -screen_width:
            floor_rect.x = 0
        
        if game_Start == False:
            velocity_drop += gravity
            bird_rect.centery += velocity_drop

        # Collision
        # if bird_rect.y > floor_y-50:
        for line in score_line_pipe:
            if bird_rect.colliderect(line) and game_pause == False:
                if count2 == 0:
                    score += 1
                    sound_point.play()
                
                count2 += 1
        
        if count2 == 12:
            count2 = 0

        if bird_rect.colliderect(floor_rect) or bird_rect.y > floor_y - 50:
            velocity_line = 0
            count2 = 0
            velocity_drop = 0
            gravity = 0
            bird = bird_list[1]
            velocity_background = 0
            velocity_floor = 0
            bird = pygame.transform.rotozoom(bird,-90,1)
            draw_game_over()
            if count1 == 0:
                sound_hit.play()
            count1 += 1
            velocity_pipe = 0
            collision_floor = True
            game_pause = True
            high_score = draw_high_score(high_score,score)
            count3 = 0
        
        for pipe in pipe_list:
            if bird_rect.colliderect(pipe):
                count2 = 0
                draw_game_over()
                gravity = 0
                velocity_background = 0 
                velocity_floor = 0
                velocity_drop = 0
                velocity_pipe = 0
                velocity_line = 0
                if count1 == 0:
                    sound_hit.play()
                count1 += 1
                game_pause = True
                high_score = draw_high_score(high_score,score)
                count3 = 0
        

        if game_Start ==True:
            screen.blit(start_img,(screen_width // 2 - 145, screen_height // 2-210))

        
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()