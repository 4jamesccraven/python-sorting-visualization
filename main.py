import pygame as pg
import sortvis
from sortvis import SORTED
from random import shuffle
from dataclasses import dataclass


ALGORITHMS = {1: sortvis.insertion,
              2: sortvis.bubble,
              3: sortvis.quick,
              4: sortvis.radix,
              5: sortvis.selection,
              6: sortvis.merge,
              7: sortvis.heap,
              8: sortvis.bogo}


@dataclass
class drawable:
    '''
    An area that can be drawn to
    '''
    left: int
    right: int
    width: int
    top: int
    bottom: int
    height: int


def render_curr_state(state: list[tuple[int, pg.Color]],
                      draw: drawable,
                      WINDOW: pg.Surface,
                      num_elems: int = 100) -> None:
    '''
    Renders the state of the algorithm generator
    '''
    for i, vals in enumerate(state):
        val, color = vals

        height = int((val / num_elems) * draw.height)
        width = draw.width // num_elems

        rect = pg.rect.Rect(draw.left + (i * width),
                            draw.top + (draw.height - height),
                            width,
                            height)

        pg.draw.rect(WINDOW, color, rect)


def pause() -> None:
    '''
    Pauses the program.
    '''

    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_p:
                    return

            if event.type == pg.QUIT:
                quit()


def render_menu(draw: drawable,
                WINDOW: pg.Surface,
                color: pg.color,
                font: pg.font.Font) -> list[pg.rect.Rect]:
    '''
    Renders the algorithm selection menu
    '''
    button_width = int((draw.width // 2) * 0.9)
    button_height = int((draw.height // 4) * 0.9)
    padding_x = int((draw.width // 2) * 0.05)
    padding_y = int((draw.height // 2) * 0.05)

    buttons: list[tuple[int, int]] = [
        (padding_x, padding_y),
        (padding_x, padding_y + (button_height + padding_y)),
        (padding_x, padding_y + 2 * (button_height + padding_y)),
        (padding_x, padding_y + 3 * (button_height + padding_y)),
        (2 * padding_x + (button_width + padding_x), padding_y),
        (2 * padding_x + (button_width + padding_x),
         padding_y + (button_height + padding_y)),
        (2 * padding_x + (button_width + padding_x),
         padding_y + 2 * (button_height + padding_y)),
        (2 * padding_x + (button_width + padding_x),
         padding_y + 3 * (button_height + padding_y))
    ]

    buttons = [(val[0] + draw.left, val[1] + draw.top) for val in buttons]

    buttons = [pg.rect.Rect(val[0],
                            val[1],
                            button_width,
                            button_height)
               for val in buttons]

    for button in buttons:
        pg.draw.rect(WINDOW, color, button, border_radius=15)

    button_titles = ['Insertion',
                     'Bubble',
                     'Quick',
                     'Radix',
                     'Selection',
                     'Merge',
                     'Heap',
                     'Bogo'
                     ]

    button_titles = [font.render(title, True, pg.Color(0, 0, 0))
                     for title in button_titles]

    for rect, title in zip(buttons, button_titles):
        text_rect = title.get_rect(center=rect.center)

        WINDOW.blit(title, text_rect)

    return buttons


def main() -> None:
    pg.init()

    # Pseudo Globals
    SCREEN_HEIGHT = 800
    SCREEN_W_RATIO, SCREEN_H_RATIO = (16, 9)
    SCREEN_WIDTH = (SCREEN_HEIGHT * SCREEN_W_RATIO) // SCREEN_H_RATIO
    SCREEN_FLAGS = pg.SCALED
    SPEED = 120

    # Initialise the window
    pg.display.set_caption('Algorithm Visualizer - James Craven')
    WINDOW = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                 flags=SCREEN_FLAGS,
                                 vsync=1)
    FONT = pg.font.SysFont("Arial", 36)
    LEGEND_FONT = pg.font.SysFont('Arial', 24)

    icon = pg.image.load('icon.png')
    pg.display.set_icon(icon)

    CLOCK = pg.time.Clock()

    # A rectangle to hold the data to be displayed
    vis_space = pg.rect.Rect(SCREEN_WIDTH // 7,
                             (SCREEN_HEIGHT // 21) * 3,
                             (SCREEN_WIDTH * 5) // 7,
                             (SCREEN_HEIGHT * 5) // 7)

    # Information about the area that can be drawn to
    # in the visualisation space
    draw = drawable(left=vis_space.left + 25,
                    right=vis_space.right - 25,
                    width=(vis_space.right - vis_space.left) - 50,
                    top=vis_space.top + 25,
                    bottom=vis_space.bottom - 25,
                    height=(vis_space.bottom - vis_space.top) - 50,
                    )

    # A rectangle to hold the legend
    legend_space = pg.rect.Rect(draw.left - 25,
                                25,
                                draw.width + 50,
                                (SCREEN_HEIGHT // 21) * 2)

    event_loop: bool = True
    choose_algo = True
    visualisation_done = False
    algo = 0
    curr_state = None
    while event_loop:
        # Allows maximum of SPEED FPS
        CLOCK.tick(SPEED)

        # Makes background and display area
        pg.display.get_surface().fill((255, 255, 255))
        pg.draw.rect(WINDOW, (207, 210, 211), vis_space, border_radius=25)
        pg.draw.rect(WINDOW, (207, 210, 211), legend_space, border_radius=15)

        # Make legend
        legend_surface = LEGEND_FONT.render('R: Reset current algorithm    '
                                            'N: Select new algorithm    '
                                            'P: Pause program   '
                                            'ESC: Exit',
                                            True,
                                            pg.Color(0, 0, 0))
        legend_rect = legend_surface.get_rect(center=legend_space.center)
        WINDOW.blit(legend_surface, legend_rect)

        # User selects algorithm
        if choose_algo:
            if algo == 0:
                buttons = render_menu(draw, WINDOW,
                                      pg.Color(255, 255, 255),
                                      FONT)
            else:
                num_elems: int = 100 if algo != 8 else 7
                array = [i for i in range(1, num_elems + 1)]
                shuffle(array)
                algorithm: callable = ALGORITHMS[algo](array)
                choose_algo = False

        # Visualization in progress
        elif not visualisation_done and not choose_algo:
            try:
                curr_state = next(algorithm)
                render_curr_state(curr_state, draw, WINDOW, num_elems)
            except StopIteration:
                visualisation_done = True
                prev_state = [(val, SORTED) for val in array]

        # Continue rendering sorted values waiting for user
        else:
            render_curr_state(prev_state, draw, WINDOW, num_elems)

        # Input handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                event_loop = False
                break

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    pause()
                if event.key == pg.K_ESCAPE:
                    quit()
                # Reset current algorithm
                if event.key == pg.K_r:
                    choose_algo = True
                    visualisation_done = False
                    break
                # Select new algorithm
                if event.key == pg.K_n:
                    choose_algo = True
                    visualisation_done = False
                    algo = 0
                    break

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for idx, button in enumerate(buttons, start=1):
                        if button.collidepoint(event.pos):
                            algo = idx

        pg.display.update()

    pg.quit()


if __name__ == '__main__':
    main()
