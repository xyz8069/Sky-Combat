# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 17:33:47 2021

@author: admin
"""
import pygame
import time

width = 480
height = 852
bullet_list = []
enemy_list = []

def maingame():
    global width, height
    global bullet_list
    global enemy_list
    pygame.init()
    window_screen = pygame.display.set_mode((width, height), 0, 32)
    player0 = PlayerCraft(window_screen, x = 95, y = 700, image_name = 'ADF11', hp_amount = 100, player_no = 0)
    #player1 = PlayerCraft(window_screen, x = 295, y = 700, image_name = 'ADF11', hp_amount = 100, player_no = 1)
    enemy = EnemyCraft(window_screen, x = 195, y = 100, image_name = '补给船', hp_amount = 10)
    pygame.display.set_caption('Ace Combat')
    background = pygame.image.load('./image/bg.png').convert()
    pygame.joystick.init()
    controller_num = pygame.joystick.get_count()
    if(controller_num != 0):
        controller = []
        for i in range(controller_num):
            controller.append(pygame.joystick.Joystick(i))
            controller[i].init()
    
    while True:
        window_screen.blit(background, (0,0))
        player0.display()
        #player1.display()
        enemy.display()
        enemy.move()
        bullet_del_list = []
        for item in bullet_list:
            if item.judge():
                item.display()
                item.move()
            else:
                bullet_del_list.append(item)
        for item in bullet_del_list:
            bullet_list.remove(item)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            key_control(player0, event)
            #key_control(player1, event)
        if(controller_num != 0):
            joystick_control(player0, controller[0])
        player0.move()
        #player1.move()
        time.sleep(0.01)
        pygame.display.update()
        
class Base(object):
    def __init__(self, screen_temp, x, y, image_name):
        self.x = x
        self.y = y
        self.screen = screen_temp
        self.image = pygame.image.load('./image/' + image_name + '.png').convert_alpha()      
        
class button(object):
    def __init__(self, screen, x, y, w, h, text):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.screen = screen
        
    def display(self):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < self.x + self.w and mouse_pos[0] > self.x and mouse_pos[1] < self.y + self.h and mouse_pos[1] > self.y:
            pygame.draw.rect(self.screen, (178, 178, 178), (self.x, self.y, self.w, self.h)) #鼠标进入按钮，颜色设置为（178，178，178）
        else:
            pygame.draw.rect(self.screen, (128, 128, 128), (self.x, self.y, self.w, self.h)) #鼠标离开按钮，颜色设置为（128，128，128）
        font = pygame.font.SysFont('宋体', 32) #设置字体及大小
        textSurf = font.render(self.text, True, (0, 0, 0))
        textRect = textSurf.get_rect()
        textRect.center = ((self.x + (self.w / 2)), (self.y + (self.h / 2)))
        self.screen.blit(textSurf, textRect) #绘制按钮
         
    def click(self):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < self.x + self.w and mouse_pos[0] > self.x and mouse_pos[1] < self.y + self.h and mouse_pos[1] > self.y:
            if self.text == 'Back':
                pass
            elif self.text == 'Restart':
                pass
            elif self.text == 'Settings':
                pass
            elif self.text == 'Restart':
                pass
                
        
class Aircraft(Base):
    global bullet_list
    def __init__(self, screen_temp, x, y, image_name, authority_type, hp_amount):
        super().__init__(screen_temp, x, y, image_name)
        self.authority_type = authority_type
        self.hp_amount = hp_amount
        self.hp = hp_amount
        if self.authority_type == 'enemy':
            self.image = pygame.transform.rotate(self.image, 180)
            
    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        self.hit()
    
    def hit(self):
        if bullet_list and self.hp:
            for bullet in bullet_list:
                if bullet.x > self.x + 0.05 * bullet.width and bullet.x < self.x + 0.95 * bullet.width and bullet.y + 0.1 * bullet.height > self.y and bullet.y < self.y + 0.8 * bullet.height:
                    self.hp -= 10
                    bullet_list.remove(bullet)
                    self.hitted = True
    
    def pos_check(self):
        if self.x < 0:
            self.x = 410
        elif self.x > 410:
            self.x = 0
        
class PlayerCraft(Aircraft):
    global bullet_list
    def __init__(self, screen_temp, x, y, image_name, hp_amount, player_no):
        super().__init__(screen_temp, x, y, image_name, 'player', hp_amount)
        self.hp_amount = hp_amount
        self.player_no = player_no
        self.move_dict = {'horizontal' : 0, 'vertical' : 0, 'space' : 0}
    
    def move(self):
        self.pos_check()
        if self.move_dict['horizontal'] != 0 and self.move_dict['vertical'] != 0:
            self.x += 3 * self.move_dict['horizontal']
            self.y += 3 * self.move_dict['vertical']
        elif self.move_dict['horizontal'] != 0:
            self.x += 5 * self.move_dict['horizontal']
        elif self.move_dict['vertical'] != 0:
            self.y += 5 * self.move_dict['vertical']
        if self.move_dict['space'] == 1:
            if len(bullet_list) != 0:
                if self.y - 14 - 80 > bullet_list[-1].y:
                    bullet_list.append(Bullet(self.screen, self.x+40, self.y-14, 'bullet', 'player'))
            else:
                bullet_list.append(Bullet(self.screen, self.x+40, self.y-14, 'bullet', 'player'))
    
class EnemyCraft(Aircraft):
    def __init__(self, screen_temp, x, y, image_name, hp_amount):
        super().__init__(screen_temp, x, y, image_name, 'enemy', hp_amount)
        self.hp_amount = hp_amount
        
    def move(self):
        self.pos_check()
        self.x += 5
        
class Bullet(Base):
    def __init__(self, screen_temp, x, y, image_name, authority_type):
        super().__init__(screen_temp, x, y, image_name)
        self.authority_type = authority_type
        self.width = 9
        self.height = 21
        
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

def plane_destroy(plane):
    """回收被击中的敌机的对象"""
    global hero
    global hit_score
    global enemy0_list
    global enemy1_list
    global enemy2_list
    if plane in enemy0_list: #回收对象为enemy0
        enemy0_list.remove(plane)
    elif plane in enemy1_list:
        enemy1_list.remove(plane)
    elif plane in enemy2_list:
        enemy2_list.remove(plane)
    elif plane == hero:#回收对象为hero
        hit_score = 0
        hero = None

def pause(player):
    button_list = [button(player.screen, 160, 200, 160, 100, 'Back'), 
                button(player.screen, 160, 300, 160, 100, 'Restart'), 
                button(player.screen, 160, 400, 160, 100, 'Settings'), 
                button(player.screen, 160, 500, 160, 100, 'Exit')]
    isPause = True
    while isPause:
        for item in button_list:
            item.display()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                isPause = False
                break
            elif event.type == event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                isPause = False
                break
        controller = pygame.joystick.Joystick(0)
        controller.init()
        if controller.get_button(7):
            isPause = False
        pygame.display.update()
        time.sleep(0.01)
    
#键盘控制移动和开火
#玩家一：WASD+空格
#玩家二：方向键+小键盘回车键
def key_control(player, event):
    global isPause
    if event.type == pygame.KEYDOWN:
        if player:
            if player.player_no == 0:
                if event.key == pygame.K_a:
                    player.move_dict['horizontal'] = -1
                    print(player.move_dict)
                if event.key == pygame.K_d:
                    player.move_dict['horizontal'] = 1
                if event.key == pygame.K_w:
                    player.move_dict['vertical'] = -1
                if event.key == pygame.K_s:
                    player.move_dict['vertical'] = 1
                if event.key == pygame.K_SPACE:
                    player.move_dict['space'] = 1
            elif player.player_no == 1: 
                if event.key == pygame.K_LEFT:
                    player.move_dict['horizontal'] = -1
                if event.key == pygame.K_RIGHT:
                    player.move_dict['horizontal'] = 1
                if event.key == pygame.K_UP:
                    player.move_dict['vertical'] = -1
                if event.key == pygame.K_DOWN:
                    player.move_dict['vertical'] = 1
                if event.key == pygame.K_KP_ENTER:
                    player.move_dict['space'] = 1
        if event.key == pygame.K_ESCAPE: #按下ESC键暂停游戏
            pause(player)
                
                    
    elif event.type == pygame.KEYUP and player:
        if player.player_no == 0:
            if event.key == pygame.K_a:
                player.move_dict['horizontal'] = 0
            if event.key == pygame.K_d:
                player.move_dict['horizontal'] = 0
            if event.key == pygame.K_w:
                player.move_dict['vertical'] = 0
            if event.key == pygame.K_s:
                player.move_dict['vertical'] = 0
            if event.key == pygame.K_SPACE:
                player.move_dict['space'] = 0
        elif player.player_no == 1: 
            if event.key == pygame.K_LEFT:
                player.move_dict['horizontal'] = 0
            if event.key == pygame.K_RIGHT:
                player.move_dict['horizontal'] = 0
            if event.key == pygame.K_UP:
                player.move_dict['vertical'] = 0
            if event.key == pygame.K_DOWN:
                player.move_dict['vertical'] = 0
            if event.key == pygame.K_KP_ENTER:
                player.move_dict['space'] = 0
        
            

#手柄控制移动和开火
#左摇杆+A（Xbox）/×（Playstation）/B（Nintendo）
def joystick_control(player, controller):
    if abs(controller.get_axis(0)) > 0.1:
        player.move_dict['horizontal'] = controller.get_axis(0)
    else:
        player.move_dict['horizontal'] = 0
    if abs(controller.get_axis(0)) > 0.1:
        player.move_dict['vertical'] = controller.get_axis(1)
    else:
        player.move_dict['vertical'] = 0
    if controller.get_button(0):
        player.move_dict['space'] = 1
    else:
        player.move_dict['space'] = 0
    if controller.get_button(7):
        pause(player)
    
                         
if __name__ == "__main__":
    maingame()