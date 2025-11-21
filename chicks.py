#pomodoro

import sys
import os
import pygame as pg
from chick import Chick
from button import Button

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

# def load_image(name, colorkey=None, scale=1):
#     fullname = os.path.join(data_dir, name)
#     image = pg.image.load(fullname)
#     image = image.convert()

#     size = image.get_size()
#     size = (size[0] * scale, size[1] * scale)
#     image = pg.transform.scale(image, size)

#     if colorkey is not None:
#         if colorkey == -1:
#             colorkey = image.get_at((0, 0))
#         image.set_colorkey(colorkey, pg.RLEACCEL)
#     return image, image.get_rect()

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
    STUDY_TIME = 10
    PLAY_TIME = 10
    OVERTIME = 10
    timer_display = {"minutes": 1, "seconds":0}


    # Create The Background
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((170, 238, 187))

    screen.blit(background, (0,0))
    pg.display.flip()

    # Sprites / text / buttons
    break_img = pg.image.load('data/start_break_button.png').convert_alpha()
    end_break_img = pg.image.load('data/end_break_button.png').convert_alpha()
    break_hover_img = pg.image.load('data/start_break_button_hover.png').convert_alpha()
    end_break_hover_img = pg.image.load('data/end_break_button_hover.png').convert_alpha()

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

        
        if focus == 's':
            countdown_max = STUDY_TIME
        elif focus == 'b':
            countdown_max = PLAY_TIME
        elif focus == 'o':
            countdown_max = OVERTIME

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

        screen.blit(background, (0,0))
        allsprites.draw(screen)

        # When timers run out
        if seconds_left <= 0:
            if focus == 's':
                extra_study_time = True
                if break_button.draw(screen):
                    focus = 'b'
                    start_time = pg.time.get_ticks()
                    extra_study_time = False
            elif focus == 'b':
                focus = 'o'
                start_time = pg.time.get_ticks()
            elif focus == 'o':
                focus = 's'
                chick[chicks_left - 1].kill()
                chicks_left = chicks_left - 1
                start_time = pg.time.get_ticks()
                

        
        if focus == 'o':
                if end_break_button.draw(screen):
                    focus = 's'
                    start_time = pg.time.get_ticks()
        elif not extra_study_time:
            timer_text = font.render(f"Time remaining: {timer_display['minutes']}:{"0" if timer_display['seconds'] < 10 else ""}{timer_display['seconds']}", True, (255, 255, 255))
            screen.blit(timer_text, (300, 250))


        
        pg.display.flip()
    pg.quit()

if __name__ == "__main__":
    main()