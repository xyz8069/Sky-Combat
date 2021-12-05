# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 17:33:47 2021

@author: admin
"""
import pygame
import time
import random
import pickle

width = 480
height = 852
score = 0
enemy_list = []
bullet_list = []
supply_list = []

def maingame():
    global width, height
    global score
    global enemy_list
    global bullet_list
    global supply_list
    
    pygame.init()
    window_screen = pygame.display.set_mode((width, height), 0, 32)
    pygame.display.set_caption('Ace Combat')
    background = pygame.image.load('./image/bg.png').convert()
    score_label = Label(window_screen, width - 120, 0, 120, 30)
    pygame.joystick.init()
    controller_num = pygame.joystick.get_count()
    if(controller_num != 0):
        controller = []
        for i in range(controller_num):
            controller.append(pygame.joystick.Joystick(i))
            controller[i].init()
    mode = 'single'
    start = False
    button_list = [Button(window_screen, 160, 350, 160, 100, 'New Game'), 
                Button(window_screen, 160, 450, 160, 100, 'Continue'), 
                Button(window_screen, 160, 550, 160, 100, 'Settings'), 
                Button(window_screen, 160, 650, 160, 100, 'Exit')]
    
    while not start:
        operation = -1
        window_screen.blit(background, (0,0))
        label = Label(window_screen, width / 2 - 120, height / 2 - 200, 240, 120)
        
        label.display('Ace Combat', 72)
        for button in button_list:
            button.display()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if(len(button_list) == 4):
                    if button_list[0].click():
                        button_list.clear()
                        button_list = [Button(window_screen, 160, 350, 160, 100, 'Single Player'), 
                                Button(window_screen, 160, 650, 160, 100, 'Double Player')]
                    elif button_list[1].click():
                        #game = Game.load_game()
                        pass
                    elif button_list[2].click():
                        pass
                    elif button_list[3].click():
                        pygame.quit()
                else:
                    if button_list[0].click():
                        start = True
                        break
                    elif button_list[1].click():
                        mode = 'double'
                        start = True
                        break
                    
        if operation == 0:
            break
            
        time.sleep(0.01)
        pygame.display.update()
        
    if mode == 'single':
        player_list = [PlayerCraft(window_screen, x = 95, y = 700, image_name = 'ADF11', hp_amount = 200, player_no = 0)]
    else:
        player_list = [PlayerCraft(window_screen, x = 95, y = 700, image_name = 'ADF11', hp_amount = 200, player_no = 0),
                       PlayerCraft(window_screen, x = 295, y = 700, image_name = 'ADF11', hp_amount = 100, player_no = 1)]
        
    while True:
        window_screen.blit(background, (0,0))
        for player in player_list:
            player.display()
            
        create_enemy(window_screen)
        for enemy in enemy_list:
            enemy.display()
            enemy.move()
        bullet_list = []
        bullet_list = sum_bullet(player_list, enemy_list)
        #bullet_del_list = []
        for item in bullet_list:
            if item.judge():
                item.display()
                item.move()
        '''    else:
                bullet_del_list.append(item)
        for item in bullet_del_list:
            bullet_list.remove(item)'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            for player in player_list:
                key_control(player, event)
                
        if player_list[0].hp <= 0:
            player_list.clear()
            enemy_list.clear()
            pygame.display.update()
            label1 = Label(window_screen, width / 2 - 120, height / 2 - 200, 240, 120)
            label2 = Label(window_screen, width / 2 - 60, height / 2 - 30, 120, 60)
            button1 = Button(window_screen, width / 2 - 80, height / 2 + 100, 160, 100, 'Restart')
            button2 = Button(window_screen, width / 2 - 80, height / 2 + 250, 160, 100, 'Back')
            while True:
                label1.display('Game Over!', 72)
                label2.display('Your Score:' + str(score))
                button1.display()
                button2.display()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                pygame.display.update()
                time.sleep(0.01)
            
        if(controller_num != 0):
            joystick_control(player_list[0], controller[0])
        
        for player in player_list:
            player.move()
            
        score_label.display('Score:' + str(score))
        time.sleep(0.01)
        pygame.display.update()

class Base(object):
    def __init__(self, screen_temp, x, y, image_name):
        self.x = x
        self.y = y
        self.screen = screen_temp
        self.image = pygame.image.load('./image/' + image_name + '.png').convert_alpha()
        self.w = self.image.get_rect().size[0]
        self.h = self.image.get_rect().size[1]

class Game(object):
    def __init__(self, screen, player_list, enemy_list):
        self.player_list = player_list
        self.enemy_list = enemy_list
    
    #保存游戏
    def save_game(self):
        with open('save.dat', 'wb') as f:
            pickle.dump(self, f)
    
    #读取游戏
    def load_game(self):
        with open('save.dat', 'rb+') as f:
            model = pickle.load(f)
        return model

#标签   
class Label(object):
    def __init__(self, screen, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.screen = screen
        
    def display(self, text, size = 32):
        font = pygame.font.SysFont('Times New Romans', size) #设置字体及大小
        textSurf = font.render(text, True, (0, 0, 0))
        textRect = textSurf.get_rect()
        textRect.center = ((self.x + (self.w / 2)), (self.y + (self.h / 2)))
        self.screen.blit(textSurf, textRect) #绘制标签

#按钮         
class Button(object):
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
            return True
        
class Aircraft(Base):
    global bullet_list
    global enemy_list
    global width, height
    def __init__(self, screen_temp, x, y, image_name, authority_type, hp_amount):
        super().__init__(screen_temp, x, y, image_name)
        self.authority_type = authority_type
        self.hp_amount = hp_amount
        self.hp = hp_amount
        self.bullet_list = []
        self.time = 0
        if self.authority_type == 'enemy':
            self.image = pygame.transform.rotate(self.image, 180)
            
    def display(self):
        global score
        if self.hp > 0:
            self.screen.blit(self.image, (self.x, self.y))
            self.hit()
        else:
            if self.time < 100:
                explode_image = pygame.image.load('./image/explode.png').convert_alpha()
                self.screen.blit(self.image, (self.x, self.y))
                self.screen.blit(explode_image, (self.x, self.y))
                self.time += 1
            else:
                if self.authority_type == 'enemy' and self.hp <= 0:
                    enemy_list.remove(self)
                    score += 1
        for item in self.bullet_list:
            if not item.judge():
                self.bullet_list.remove(item)
    
    def hit(self):
        if bullet_list and self.hp:
            for bullet in bullet_list:
                if bullet.authority_type != self.authority_type:
                    if bullet.x < self.x + self.w and bullet.x > self.x and bullet.y < self.y + self.h and bullet.y > self.y:
                        self.hp -= bullet.damage
                        bullet.damage = 0
                        bullet.visible = False
                        
    
    def pos_check(self):
        if self.x < 0:
            self.x = self.w
        elif self.x > width:
            self.x = 0
        if self.authority_type == 'player':
            if self.y < 0:
                self.y = 0
            elif self.y > height - self.h:
                self.y = height - self.h
        if self.authority_type == 'enemy' and self.y > height:
            enemy_list.remove(self)
        
class PlayerCraft(Aircraft):
    def __init__(self, screen_temp, x, y, image_name, hp_amount, player_no):
        super().__init__(screen_temp, x, y, image_name, 'player', hp_amount)
        self.hp_amount = hp_amount
        self.player_no = player_no
        self.level = 1
        self.exp = 0
        self.move_dict = {'horizontal' : 0, 'vertical' : 0, 'space' : 0}
    
    def levelup(self):
        self.level += 1
        
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
            if len(self.bullet_list) != 0:
                if self.y - 14 - 80 > self.bullet_list[-1].y:
                    self.bullet_list.append(Bullet(self.screen, self.x+40, self.y-14, 'bullet', 'player'))
            else:
                self.bullet_list.append(Bullet(self.screen, self.x+40, self.y-14, 'bullet', 'player'))
                
    
class EnemyCraft(Aircraft):
    def __init__(self, screen_temp, x, y, image_name, hp_amount):
        super().__init__(screen_temp, x, y, image_name, 'enemy', hp_amount)
        self.hp_amount = hp_amount
        self.direction = 'right'
        
    def move(self):
        self.pos_check()
        self.fire()
        if self.hp > 0:
            if self.direction == 'right':
                self.x += 1
            elif self.direction == 'left':
                self.x -= 1
            if self.x > 430:
                self.direction = 'left'
            elif self.x < 0:
                self.direction = 'right'
            self.y += 3
            
    def fire(self):
        if len(self.bullet_list) != 0:
            if self.y - 14 - 80 > self.bullet_list[-1].y:
                self.bullet_list.append(Bullet(self.screen, self.x+40, self.y+84, 'bullet', 'enemy'))
        else:
            self.bullet_list.append(Bullet(self.screen, self.x+40, self.y+84, 'bullet', 'enemy'))
                
class Bullet(Base):
    def __init__(self, screen_temp, x, y, image_name, authority_type):
        super().__init__(screen_temp, x, y, image_name)
        self.authority_type = authority_type
        self.damage = 10
        self.visible = True
        if self.authority_type == 'enemy':
            self.image = pygame.transform.rotate(self.image, 180)
        
    def display(self):
        if self.visible == True:
            self.screen.blit(self.image, (self.x, self.y))
        
    def judge(self):
        if self.y > 0 and self.y < 852:
            return True
        else:
            return False
        
    def move(self):
        if self.authority_type == 'player':
            self.y -= 8
        elif self.authority_type == 'enemy':
            self.y += 8

class Supply(Base):
    def __init__(self, screen_temp, x, y, image_name, supply_type):
        super().__init__(screen_temp, x, y, image_name)
        
    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        
    def move(self):
        self.y += 1
            
def sum_bullet(player_list, enemy_list):
    global bullet_list
    for item in player_list:
        bullet_list.extend(item.bullet_list)
    for item in enemy_list:
        bullet_list.extend(item.bullet_list)
    return bullet_list
    
def create_enemy(screen):
    global width
    global enemy_list
    if len(enemy_list) < 5:
        enemy_list.append(EnemyCraft(screen, x = random.randint(0, width), y = -100, image_name = '补给船', hp_amount = 10))

def game_fail():
    pass

def pause(player):
    button_list = [Button(player.screen, 160, 200, 160, 100, 'Back'), 
                Button(player.screen, 160, 300, 160, 100, 'Restart'),
                Button(player.screen, 160, 400, 160, 100, 'Save'), 
                Button(player.screen, 160, 500, 160, 100, 'Settings'), 
                Button(player.screen, 160, 600, 160, 100, 'Exit')]
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
        controller_num = pygame.joystick.get_count()
        if(controller_num != 0):
            controller = pygame.joystick.Joystick(0)
            controller.init()
            if controller.get_button(7):
                isPause = False
        pygame.display.update()
        time.sleep(0.01)

def ai_save_data():
    pass

#自动游戏，ai控制移动和开火
def ai_control(player, event):
    '''model = load_model('lstm_300.h5', custom_objects={'r2': r2})
    player.move_dict['horizontal'] = model.predict(test_x)'''
    pass
    
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