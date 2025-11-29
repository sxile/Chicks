#pomodoro
import os
import pygame as pg
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
    countdown_max = STUDY_TIME
    timer_display = {"minutes": 0, "seconds":0}


    # BACKGROUND & TITLE CARD IMAGES #
    background_image = pg.image.load("data/grass.png")
    background_image = pg.transform.scale(background_image, (1280, 720))

    title_card = pg.image.load("data/title_card.png").convert_alpha()
    title_card = pg.transform.scale(title_card, (1240, 680))

    screen.blit(background_image, (0,0))
    screen.blit(title_card,(20,20))
    pg.display.flip()

    # BUTTON IMAGES #
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
    chicks_left = 5
    allsprites = pg.sprite.RenderPlain(chick)

    # TEXT (needs to be replaced) #
    font = pg.font.Font(None,50)

    # CLOCK #
    clock = pg.time.Clock() 

    # LOOP CONDITIONS #
    atTitle = True
    isEnding = False
    going = True
    rules_read = False
    extra_study_time = False
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

        # Paint Background
        screen.blit(background_image, (0,0))

        # Title Screen
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
        # Main Game
        else:

            # Update timer variables
            seconds_left = int(countdown_max - (pg.time.get_ticks() - start_time) / 1000)
            timer_display["minutes"] = int(seconds_left / 60)
            timer_display["seconds"] = seconds_left % 60 

            # Update Sprites (Chicks)
            allsprites.update()

            # When timers run out, switch focus
            if seconds_left <= 0:
                if focus == 's':
                    extra_study_time = True
                    if break_button.draw(screen):
                        focus = 'b'
                        countdown_max = BREAK_TIME
                        start_time = pg.time.get_ticks()
                        extra_study_time = False
                elif focus == 'b':
                    focus = 'o'
                    countdown_max = OVERTIME
                    start_time = pg.time.get_ticks()
                elif focus == 'o':
                    focus = 's'
                    countdown_max = STUDY_TIME
                    pg.mixer.Sound.play(gunshot_sound)
                    chick[5 - chicks_left].kill()
                    chicks_left = chicks_left - 1
                    start_time = pg.time.get_ticks()
            
            # Draw Sprites (Chicks)
            allsprites.draw(screen)
                    

            # When gone over study or break time
            if focus == 'o':
                    if end_break_button.draw(screen):
                        focus = 's'
                        countdown_max = STUDY_TIME
                        start_time = pg.time.get_ticks()
            elif not extra_study_time and chicks_left > 0:
                timer_text = font.render(f"Time remaining: {timer_display['minutes']}:{"0" if timer_display['seconds'] < 10 else ""}{timer_display['seconds']}", True, (255, 255, 255))
                screen.blit(timer_text, (300, 250))

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