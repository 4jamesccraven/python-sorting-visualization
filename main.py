import pygame as pg
import sortvis
from random import shuffle
from dataclasses import dataclass


@dataclass
class drawable:
    left: int
    right: int
    width: int
    top: int
    bottom: int
    height: int


def render_curr_state(state: list[tuple[int, pg.Color]],
                      draw: drawable,
                      WINDOW: pg.Surface) -> None:
    '''
    Renders the state of the algorithm generator
    '''
    for i, vals in enumerate(state):
        val, color = vals

        height = int((val / 100) * draw.height)
        width = draw.width // 100

        rect = pg.rect.Rect(draw.left + (i * width),
                            draw.top + (draw.height - height),
                            width,
                            height)

        pg.draw.rect(WINDOW, color, rect)


def main() -> None:
    # Pseudo Globals
    SCREEN_HEIGHT = 800
    SCREEN_W_RATIO, SCREEN_H_RATIO = (16, 9)
    SCREEN_WIDTH = (SCREEN_HEIGHT * SCREEN_W_RATIO) // SCREEN_H_RATIO
    SCREEN_FLAGS = pg.SCALED

    # Initialise the window
    pg.display.set_caption('Algorithm Visualizer - James Craven')
    WINDOW = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                 flags=SCREEN_FLAGS,
                                 vsync=1)
    clock = pg.time.Clock()

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

    curr_state = None
    visualisation_done = False
    choose_algo = True
    event_loop: bool = True
    while event_loop:
        # Allows maximum of 120 FPS
        clock.tick(120)

        # Makes background and display area
        pg.display.get_surface().fill((255, 255, 255))
        pg.draw.rect(WINDOW, (207, 210, 211), vis_space, border_radius=25)

        # TO BE IMPLEMENTED: SELECTABLE ALGORITHM
        if choose_algo:
            choose_algo = False
            list = [i for i in range(100)]
            shuffle(list)
            algorithm = sortvis.bubble(list)
            ...

        if not visualisation_done and not choose_algo:
            try:
                curr_state = next(algorithm)
                render_curr_state(curr_state, draw, WINDOW)
            except StopIteration:
                visualisation_done = True
                prev_state = [(val, pg.Color(255, 255, 255)) for val in list]

        else:
            render_curr_state(prev_state, draw, WINDOW)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                event_loop = False
                break

        pg.display.update()

    pg.quit()


if __name__ == '__main__':
    main()
