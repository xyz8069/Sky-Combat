# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 17:33:47 2021

@author: admin
"""
import pygame
import time

bullet_list = []

def maingame():
    global bullet_list
    window_screen = pygame.display.set_mode((480, 852), 0, 32)
    player = PlayerCraft(window_screen, x = 195, y = 700, image_name = 'ADF11', hp_amount = 100, player_no = 1)
    enemy = EnemyCraft(window_screen, x = 195, y = 100, image_name = '补给船', hp_amount = 10)
    pygame.display.set_caption('Ace Combat')
    background = pygame.image.load('./image/bg.png').convert()
    
    while True:
        window_screen.blit(background, (0,0))
        player.display()
        enemy.display()
        bullet_del_list = []
        for item in bullet_list:
            if item.judge():
                item.display()
                item.move()
            else:
                bullet_del_list.append(item)
        for item in bullet_del_list:
            bullet_list.remove(item)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            key_control(player, event)
        time.sleep(0.01)
        
class Base(object):
    def __init__(self, screen_temp, x, y, image_name):
        self.x = x
        self.y = y
        self.screen = screen_temp
        self.image = pygame.image.load('./image/' + image_name + '.png').convert_alpha()
        
class Aircraft(Base):
    def __init__(self, screen_temp, x, y, image_name, authority_type, hp_amount):
        super().__init__(screen_temp, x, y, image_name)
        self.authority_type = authority_type
        self.hp_amount = hp_amount
        if self.authority_type == 'enemy':
            self.image = pygame.transform.rotate(self.image, 180)
            
    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
    
    def hit(self):
        self.screen.blit(self.image, (self.x, self.y))
        
class PlayerCraft(Aircraft):
    global bullet_list
    def __init__(self, screen_temp, x, y, image_name, hp_amount, player_no):
        super().__init__(screen_temp, x, y, image_name, 'player', hp_amount)
        self.hp_amount = hp_amount
        self.player_no = player_no
        self.move_list = []
    
    def move(self):
        for item in self.move_list:
            if item == pygame.K_LEFT:
                self.x -= 5
            elif item == pygame.K_RIGHT:
                self.x += 5
            elif item == pygame.K_UP:
                self.y -= 5
            elif item == pygame.K_DOWN:
                self.y += 5
            elif item == pygame.K_SPACE:
                bullet_list.append(Bullet(self.screen, self.x+40, self.y-14, 'bullet', 'player'))
    
class EnemyCraft(Aircraft):
    def __init__(self, screen_temp, x, y, image_name, hp_amount):
        super().__init__(screen_temp, x, y, image_name, 'enemy', hp_amount)
        self.hp_amount = hp_amount
        
class Bullet(Base):
    def __init__(self, screen_temp, x, y, image_name, authority_type):
        super().__init__(screen_temp, x, y, image_name)
        self.authority_type = authority_type

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        
    def judge(self):
        if self.y > 0 or self.y < 852:
            return True
        else:
            return False
        
    def move(self):
        if self.authority_type == 'player':
            self.y -= 8
        elif self.authority_type == 'enemy':
            self.y += 8
        
def key_control(player, event):
    if event.type == pygame.KEYDOWN:
        if player:
            player.move_list.append(event.key)
            player.move()
    elif event.type == pygame.KEYUP and player:
        if len(player.move_list) != 0: #判断是否为空
            try:
                player.move_list.remove(event.key)
            except Exception:
                pass
    
                         
if __name__ == "__main__":
    maingame()