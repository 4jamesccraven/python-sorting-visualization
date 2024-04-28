import pygame as pg
import sortvis
from random import randint
from dataclasses import dataclass


@dataclass
class drawable:
    left: int
    right: int
    width: int
    top: int
    bottom: int
    height: int


def main() -> None:
    # Pseudo Globals
    SCREEN_HEIGHT = 800
    SCREEN_W_RATIO, SCREEN_H_RATIO = (16, 9)
    SCREEN_WIDTH = (SCREEN_HEIGHT * SCREEN_W_RATIO) // SCREEN_H_RATIO

    pg.display.set_caption('Algorithm Visualizer - James Craven')
    WINDOW = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pg.time.Clock()
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

    choose_algo = True
    event_loop: bool = True
    while event_loop:
        clock.tick(60)
        pg.display.get_surface().fill((255, 255, 255))
        pg.draw.rect(WINDOW, (207, 210, 211), vis_space, border_radius=25)

        # TO BE IMPLEMENTED: SELECTABLE ALGORITHM
        if choose_algo:
            choose_algo = False
            list = [randint(0, 100) for _ in range(100)]
            algorithm = sortvis.insertion.Insertion(list).vis_steps()
            ...
        else:
            for i, vals in enumerate(next(algorithm)):
                val, color = vals

                height = int((val / 100) * draw.height)
                width = draw.width // 100

                rect = pg.rect.Rect(left=draw.left + (i * width),
                                    top=draw.top + (draw.height - height),
                                    width=width,
                                    height=height)

                pg.draw.rect(WINDOW, color, rect)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                event_loop = False
                break

        pg.display.update()

    pg.quit()


if __name__ == '__main__':
    main()
