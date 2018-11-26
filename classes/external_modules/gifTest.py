from gifImage import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((250, 250))

    my_sprite1 = GifSprite("imgs/" + "bulbasaur" + "/", 41, "bulbasaur", (30, 30))
    my_group1 = pygame.sprite.Group(my_sprite1)
    my_sprite2 = GifSprite("imgs/cyndaquil/", 50, "cyndaquil", (100, 100))
    my_group2 = pygame.sprite.Group(my_sprite2)

    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        # Calling the 'my_group.update' function calls the 'update' function of all 
        # its member sprites. Calling the 'my_group.draw' function uses the 'image'
        # and 'rect' attributes of its member sprites to draw the sprite.
        my_group1.update()
        my_group1.draw(screen)
        my_group2.update()
        my_group2.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()