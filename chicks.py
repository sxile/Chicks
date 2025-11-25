#pomodoro

import sys
import os
import pygame as pg
from chick import Chick
from button import Button
from spritesheet import SpriteSheet

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    sound = pg.mixer.Sound(fullname)

    return sound

def main():
    # Basic Window Initialization
    pg.init()
    screen = pg.display.set_mode((1280, 720), pg.SCALED)
    pg.display.set_caption("Pomodoro Chicks")
    pg.mouse.set_visible(True)

    # Focus - 's' for study, 'b' for break, 'o' for overtime
    focus = 's'
    extra_study_time = False

    # Reusable timer variables (constants in seconds)
    STUDY_TIME = 8
    BREAK_TIME = 8
    OVERTIME = 2
    countdown_max = STUDY_TIME
    timer_display = {"minutes": 0, "seconds":0}


    # Sprites / text / buttons / sounds / background
    background_image = pg.image.load("data/grass.png")
    background_image = pg.transform.scale(background_image, (1280, 720))

    screen.blit(background_image, (0,0))
    pg.display.flip()

    break_img = pg.image.load('data/start_break_button.png').convert_alpha()
    end_break_img = pg.image.load('data/end_break_button.png').convert_alpha()
    break_hover_img = pg.image.load('data/start_break_button_hover.png').convert_alpha()
    end_break_hover_img = pg.image.load('data/end_break_button_hover.png').convert_alpha()
    
    gunshot_sound = pg.mixer.Sound("data/gunshot.wav")

    break_button = Button(100,200,break_img, break_hover_img, 3)
    end_break_button = Button(50,200,end_break_img,end_break_hover_img,3)

    chick = [Chick(), Chick(), Chick(), Chick(), Chick()]
    chicks_left = 5
    allsprites = pg.sprite.RenderPlain(chick)

    font = pg.font.Font(None,50)

    # Start timer
    clock = pg.time.Clock()
    start_time = pg.time.get_ticks()

    # Main loop condtion
    going = True

    #Main loop
    while going:
        # Maximum FPS
        clock.tick(60)

        # Update timer variables
        seconds_left = int(countdown_max - (pg.time.get_ticks() - start_time) / 1000)
        timer_display["minutes"] = int(seconds_left / 60)
        timer_display["seconds"] = seconds_left % 60 


        
        # Run events
        for event in pg.event.get():
            # If 'X' buttom pressed
            if event.type == pg.QUIT:
                going = False

        # Repaint and update
        allsprites.update()

        screen.blit(background_image, (0,0))
        allsprites.draw(screen)

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
                

        # When gone over study or break time
        if focus == 'o':
                if end_break_button.draw(screen):
                    focus = 's'
                    countdown_max = STUDY_TIME
                    start_time = pg.time.get_ticks()
        elif not extra_study_time:
            timer_text = font.render(f"Time remaining: {timer_display['minutes']}:{"0" if timer_display['seconds'] < 10 else ""}{timer_display['seconds']}", True, (255, 255, 255))
            screen.blit(timer_text, (300, 250))

        # End if there are no longer chicks to tend
        if chicks_left == 0:
            going = False
        
        pg.display.flip()
    pg.quit()

if __name__ == "__main__":
    main()