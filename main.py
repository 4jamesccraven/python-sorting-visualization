import pygame as pg


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

    event_loop: bool = True
    while event_loop:
        clock.tick(60)
        pg.display.get_surface().fill((255, 255, 255))
        pg.draw.rect(WINDOW, (207, 210, 211), vis_space, border_radius=25)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                event_loop = False
                break

        pg.display.update()

    pg.quit()


if __name__ == '__main__':
    main()
