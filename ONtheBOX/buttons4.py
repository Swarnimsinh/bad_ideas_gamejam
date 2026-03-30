import pygame
import random


class Button:
    def __init__(self, screen, text, x, y, w=160, h=50):
        self.screen  = screen
        self.text    = text
        self.base_x  = x
        self.base_y  = y
        self.w       = w
        self.h       = h
        self.font    = pygame.font.SysFont("arialblack", 26)

    def draw(self):
        mouse_pos     = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # shift button when hovered or clicked for a "press" feel
        offset_x, offset_y = 0, 0
        base_rect = pygame.Rect(self.base_x - self.w//2, self.base_y - self.h//2, self.w, self.h)
        if base_rect.collidepoint(mouse_pos):
            offset_x, offset_y = 5, 3
            if mouse_pressed:
                offset_x, offset_y = 10, 6

        draw_rect = pygame.Rect(
            self.base_x - self.w//2 + offset_x,
            self.base_y - self.h//2 + offset_y,
            self.w, self.h
        )
        pygame.draw.rect(self.screen, (180, 80, 80), draw_rect, border_radius=8)

        label = self.font.render(self.text, True, (255, 255, 255))
        self.screen.blit(label, (
            draw_rect.centerx - label.get_width()  // 2,
            draw_rect.centery - label.get_height() // 2
        ))

    def is_clicked(self, mouse_pos):
        rect = pygame.Rect(self.base_x - self.w//2, self.base_y - self.h//2, self.w, self.h)
        return rect.collidepoint(mouse_pos)


class SpecialObject:
    """Girl sprite — player must stand near her to freeze the RunawayButton."""

    def __init__(self, screen, x, y, image_path="girl.png", size=60):
        self.screen = screen
        self.x      = x
        self.y      = y
        self.size   = size
        raw         = pygame.image.load(image_path).convert_alpha()
        self.image  = pygame.transform.smoothscale(raw, (size, size))

    def draw(self):
        # centre the image on (self.x, self.y)
        self.screen.blit(self.image, (self.x - self.size // 2, self.y - self.size // 2))


class RunawayButton:
    """
    A circular mute button that runs away from the player.
    It freezes only when the player stands near the SpecialObject (girl).
    When frozen the player can click it to win.
    """

    def __init__(self, screen, x, y, radius=40, image_path="mute.png"): # the image_path parameter allows us to specify the path to the mute button image, and defaults to "mute.png" if not provided
        self.screen     = screen
        self.x          = x
        self.y          = y
        self.radius     = radius # the radius of the circular button, used for drawing and click detection
        self.SCREEN_W   = screen.get_width()
        self.SCREEN_H   = screen.get_height()
        self.can_escape = True

        # load mute image and scale it to fit the button size
        raw        = pygame.image.load(image_path).convert_alpha()
        icon_size  = radius * 2
        self.icon  = pygame.transform.smoothscale(raw, (icon_size, icon_size))

    def update(self, player, special_object, escape_distance=120):
        # check if player is close enough to the girl
        dist_to_girl = ((player.x - special_object.x) ** 2 +
                        (player.y - special_object.y) ** 2) ** 0.5

        # freeze the button if player is near the girl, otherwise it can run
        self.can_escape = dist_to_girl >= escape_distance

        # if button can still run, teleport away when player gets close
        if self.can_escape:
            dist_to_btn = ((player.x - self.x) ** 2 +
                           (player.y - self.y) ** 2) ** 0.5 # calculate distance from player to button
            if dist_to_btn < 150:
                self._teleport_away(player)

    def _teleport_away(self, player):
        """Pick a random screen position that is far from the player."""
        for _ in range(20):
            new_x = random.randint(self.radius + 20, self.SCREEN_W - self.radius - 20)
            new_y = random.randint(self.radius + 20, self.SCREEN_H - self.radius - 80)
            far_enough = ((new_x - player.x) ** 2 +
                          (new_y - player.y) ** 2) ** 0.5 > 200
            if far_enough:
                self.x = new_x
                self.y = new_y
                break

    def draw(self):
        # just draw mute.png — no circles, no text
        self.screen.blit(self.icon, (self.x - self.radius, self.y - self.radius))

    def is_clicked(self, mouse_pos):
        # button can only be clicked when frozen
        if self.can_escape:
            return False

        # circle math: if distance to centre <= radius, it's a hit
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        return (dx * dx + dy * dy) <= self.radius * self.radius
