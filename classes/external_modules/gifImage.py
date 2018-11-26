"""https://stackoverflow.com/questions/14044147/animated-sprite-from-few-images"""

import pygame
import math
import sys

def load_image(name):
    image = pygame.image.load(name)
    return image

class GifSprite(pygame.sprite.Sprite):
    def __init__(self, fileDir, frames, pkmnName, pos):
        super(GifSprite, self).__init__()
        # fileDir = "imgs/bulbasaur/"
        self.fileDir = fileDir
        self.frames = int(frames) + 1
        self.pkmnName = pkmnName
        self.images = []
        for i in range(1, self.frames):
            self.images.append(load_image(fileDir + self.pkmnName + str(i) + ".png"))
        # assuming both images are 64x64 pixels

        self.index = 0
        self.counter = 0 # for timer
        self.image = self.images[self.index]
        # self.rect = pygame.Rect(5, 5, 45, 49)
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''
        self.index += 0.70
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[math.floor(self.index)]

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