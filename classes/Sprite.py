import pygame
import os


class Animation:
    """Loads all frames of an animation from a given folder."""
    def __init__(self, folder, base_name, frames):
        self.frames = []
        for i in range(frames):
            filename = f"{base_name}{i:03}.png"
            path = os.path.join(folder, filename)
            image = pygame.image.load(path).convert_alpha()
            self.frames.append(image)


class AnimatedSprite(pygame.sprite.Sprite):
    """A sprite that cycles through a list of frames to animate."""
    def __init__(self, animation, pos, frame_duration=5):
        super().__init__()
        self.frames = animation.frames
        self.index = 0
        self.frame_duration = frame_duration
        self.counter = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        """Update the animation frame based on the frame duration."""
        self.counter += 1
        
        if self.counter >= self.frame_duration:
            self.counter = 0
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]