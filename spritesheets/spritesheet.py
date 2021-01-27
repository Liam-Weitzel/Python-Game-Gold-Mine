import pygame
import json

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename + '.png'
        self.sprite_sheet = pygame.image.load(self.filename).convert()
        self.meta_data = filename + '.json'
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close() #add try catch exception

    def get_sprite(self, x, y, w, h, r, g, b):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((r, g, b))
        sprite.blit(self.sprite_sheet, (0,0), (x, y, w, h))
        return sprite

    def parse_sprite(self, name, r, g, b):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h, r, g, b)
        return image