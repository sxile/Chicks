#pomodoro
import os
import pygame as pg
import numpy as np
from chick import Chick
from button import Button
from spritesheet import SpriteSheet

# main_dir = os.path.split(os.path.abspath(__file__))[0]
# data_dir = os.path.join(main_dir, "data")

def main():
    # Basic Window Initialization
    pg.init()
    screen = pg.display.set_mode((1280, 720), pg.SCALED)
    pg.display.set_caption("Pomodoro Chicks")
    pg.mouse.set_visible(True)


    # TIMER CONSTANTS #
    STUDY_TIME = 8
    BREAK_TIME = 8
    OVERTIME = 2

    # BACKGROUND & TITLE CARD IMAGES #

    background_spritesheet_image = pg.image.load("data/grass_spritesheet.png")
    background_spritesheet = SpriteSheet(background_spritesheet_image)
    background_frames = [None,None,None,None,None,
                         None,None,None,None]
    
    for i in range(9):
        background_frames[i] = background_spritesheet.get_image(i, 320, 180, 4)

    title_card = pg.image.load("data/title_card.png").convert_alpha()
    title_card = pg.transform.scale(title_card, (1240, 680))

    screen.blit(background_frames[0], (0,0))
    screen.blit(title_card,(20,20))
    pg.display.flip()

    # BUTTON IMAGES #
    zero = pg.image.load('data/0.png')
    one = pg.image.load('data/1.png')
    two = pg.image.load('data/2.png')
    three = pg.image.load('data/3.png')
    four = pg.image.load('data/4.png')
    five = pg.image.load('data/5.png')
    six = pg.image.load('data/6.png')
    seven = pg.image.load('data/7.png')
    eight= pg.image.load('data/8.png')
    nine = pg.image.load('data/9.png')
    colon = pg.image.load('data/colon.png')
    num_imgs = [zero, one, two, three, four, 
                five, six, seven, eight, nine,]
    i=0
    for img in num_imgs:
        num_imgs[i] = pg.transform.scale(img,(40,80))
        i = i+1
    colon = pg.transform.scale(colon,(40,80))

    start_img = pg.image.load('data/start_game_button.png').convert_alpha()
    start_hover_img = pg.image.load('data/start_game_button_hover.png')
    rules_img = pg.image.load('data/rules_button.png').convert_alpha()
    rules_hover_img = pg.image.load('data/rules_button_hover.png').convert_alpha()
    back_img = pg.image.load('data/back_button.png').convert_alpha()
    back_hover_img = pg.image.load('data/back_button_hover.png').convert_alpha()
    rules_list_img = pg.image.load('data/rules.png')
    break_img = pg.image.load('data/start_break_button.png').convert_alpha()
    end_break_img = pg.image.load('data/end_break_button.png').convert_alpha()
    break_hover_img = pg.image.load('data/start_break_button_hover.png').convert_alpha()
    end_break_hover_img = pg.image.load('data/end_break_button_hover.png').convert_alpha()
    
    # SOUNDS #
    gunshot_sound = pg.mixer.Sound("data/gunshot.wav")

    # BUTTON & CHICK OBJECTS #
    start_game_button = Button(400,500,start_img,start_hover_img,6)
    rules_button = Button(900, 500, rules_img, rules_hover_img, 6)
    back_button = Button(900, 500, back_img, back_hover_img, 6)
    break_button = Button(20,20,break_img, break_hover_img, 6)
    end_break_button = Button(20,20,end_break_img,end_break_hover_img,6)

    chick = [Chick(), Chick(), Chick(), Chick(), Chick()]
    # chick = [Chick()]
    dead_chick = []
    chicks_left = 5
    allsprites = pg.sprite.RenderPlain(chick)

    # TEXT (needs to be replaced) #
    font = pg.font.Font(None,50)

    # CLOCK #
    clock = pg.time.Clock() 

    # TIMERS #
    countdown_max = STUDY_TIME
    timer_display = {"minutes": 0, "seconds":0}
    refresh_background_interval = 3
    background_loop_timer = pg.time.get_ticks()

    # LOOP CONDITIONS #
    atTitle = True
    isEnding = False
    going = True
    rules_read = False
    #     Focus - 's' for study, 'b' for break, 'o' for overtime
    focus = 's'
    #     Title Focus - 'm' for main, 'r' for rules.
    title_focus = 'm'


    #Main loop
    while going:
        #     Maximum FPS
        clock.tick(60)

        #     Run Events
        for event in pg.event.get():
            # If 'X' button pressed
            if event.type == pg.QUIT:
                going = False

        #     Paint Background
        # If between animations
        if not refresh_background_interval == -1:
            screen.blit(background_frames[0],(0,0))
            if (pg.time.get_ticks() - background_loop_timer) / 1000 > refresh_background_interval:
                i = 0
                refresh_background_interval = -1
                background_loop_timer = pg.time.get_ticks()
                background_animation_speed = int(np.random.rand() * 50 + 150)
        # If animating
        else:
            i = int((pg.time.get_ticks() - background_loop_timer) / background_animation_speed)
            if i < len(background_frames):
                screen.blit(background_frames[i],(0,0))
            else:
                refresh_background_interval = int(np.random.rand() * 4) + 3
                screen.blit(background_frames[0],(0,0))

        #     Title Screen
        if atTitle:
            screen.blit(title_card,(20,20))
            if title_focus == 'm':
                if start_game_button.draw(screen):
                    atTitle = False
                    start_time = pg.time.get_ticks()
                if rules_button.draw(screen):
                    title_focus = 'r'
            elif title_focus == 'r':
                screen.blit(rules_list_img,(370,450))
                if back_button.draw(screen):
                    if rules_read:
                        title_focus = 'm'
                    rules_read = True
        #     Main Game
        else:

            #     Update timer variables
            seconds_left = int(countdown_max - (pg.time.get_ticks() - start_time) / 1000)
            timer_display["minutes"] = int(seconds_left / 60) if int(seconds_left / 60) >= 0 else 0
            timer_display["seconds"] = seconds_left % 60 if seconds_left >= 0 else 0 

            for bird in dead_chick:
                bloody_chicks = pg.sprite.spritecollide(bird, chick, False)
                for c in bloody_chicks:
                    c.standingInBlood()

            #     Update Sprites (Chicks)
            allsprites.update(screen)

            #     When timers run out, switch focus
            if seconds_left <= 0:
                if focus == 's':
                    if break_button.draw(screen):
                        focus = 'b'
                        countdown_max = BREAK_TIME
                        start_time = pg.time.get_ticks()
                elif focus == 'b':
                    focus = 'o'
                    countdown_max = OVERTIME
                    start_time = pg.time.get_ticks()
                elif focus == 'o':
                    focus = 's'
                    countdown_max = STUDY_TIME
                    pg.mixer.Sound.play(gunshot_sound)
                    chick[0].kill()
                    dead_chick.append(chick[0])
                    del chick[0]
                    chicks_left = chicks_left - 1
                    # for chicklet in chick:
                    #     if chicklet.kill():
                    #         chicks_left = chicks_left - 1
                    #         break
                    start_time = pg.time.get_ticks()
            
            tens_minutes = int(timer_display['minutes'] / 10)
            ones_minutes = int(timer_display['minutes'] % 10)
            tens_seconds = int(timer_display['seconds'] / 10)
            ones_seconds = int(timer_display['seconds'] % 10)


            # When gone over study or break time
            if focus == 'o':
                    if end_break_button.draw(screen):
                        focus = 's'
                        countdown_max = STUDY_TIME
                        start_time = pg.time.get_ticks()
                    tens_minutes = 0
                    ones_minutes = 0
                    tens_seconds = 0
                    ones_seconds = 0
            #elif chicks_left > 0:

            #     Paint Timer
            screen.blit(num_imgs[tens_minutes], (548, 300))
            screen.blit(num_imgs[ones_minutes], (584, 300))
            screen.blit(colon,(620,300))
            screen.blit(num_imgs[tens_seconds], (656, 300))
            screen.blit(num_imgs[ones_seconds], (692, 300))

            #     Draw Sprites (Chicks)
            all_chicks = chick + dead_chick
            all_chicks.sort(key=lambda obj: obj.rect.y)

            allsprites = pg.sprite.RenderPlain(all_chicks)
            allsprites.draw(screen)


            # Countdown to end if there are no longer chicks to tend
            if isEnding and int((pg.time.get_ticks() - ending_timer) / 1000) == 5:
                going = False
            if chicks_left == 0:
                if not isEnding:
                    ending_timer = pg.time.get_ticks()
                isEnding = True
                
        pg.display.flip()
    # If not 'going', end
    pg.quit()

if __name__ == "__main__":
    main()