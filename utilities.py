
def gravity(self):
    # Gravity
    self.velocity_y += 1
    if self.velocity_y > 20:
        self.velocity_y = 20
    self.dy += self.velocity_y

def collision_blocks(self):
        # Collision with the blocks
        for block in self.game.blocks:
            # Collision in X-axis
            if block.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                self.dx = 0
            # Collision in Y-axis
            if block.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                if self.velocity_y < 0:
                    self.dy = block.rect.bottom - self.rect.top
                    self.velocity_y = 0
                    # self.Jumping = False
                    self.falling = True
                elif self.velocity_y >= 0:
                    self.dy = block.rect.top - self.rect.bottom
                    self.velocity_y = 0
                    # self.Jumping = False
                    self.falling = False
        

        # Update the position of the player
        if self.dy > 0:
            self.falling = True
        self.rect.x += self.dx
        self.rect.y += self.dy

