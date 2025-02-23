"""
objects/button.py
    Definira se klasa Button za prikazivanje Play buttona.
"""

import pygame.font

class Button:
    """ Play button se pokazuje kada igra završi ili je neaktivna."""
    def __init__(self, settings, screen, msg):

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 200,100
        self.button_color = (194, 69, 177)
        self.text_color = (255,255,255)
        self.font=pygame.font.SysFont(None,64)

        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg)

    def prep_msg(self,msg):
        """ Renderira text gumba. """
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center=self.rect.center
    
    def draw_button(self):
        """ Crta gumb na ekranu."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)