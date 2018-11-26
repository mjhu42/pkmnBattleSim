import pygame
import copy

# CITATION: https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
class RotatingButton(pygame.sprite.Sprite):
    def __init__(self, image, pos): # pass in image and the center of the image
        super().__init__()
        self.image = image
        self.baseImage = self.image
        self.rect = self.image.get_rect(center = pos)
        self.angle = 0

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.angle -= 1
            self.rotate()

    def rotate(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = pygame.transform.rotozoom(self.baseImage, self.angle, 1)
            # create a new rect with the center of the old rect
            self.rect = self.image.get_rect(center = self.rect.center)
    
    def getRectCoords(self):
        return self.rect