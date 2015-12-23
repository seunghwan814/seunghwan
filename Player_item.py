import random
from pico2d import *
import monsterpy
import main_state
name = "Player_item"
class Player_Attack:
    #SKILL,HIT=None
    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH = 40.0 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self,x,y,dir):
        self.image= load_image('./resource/p_attack.png')
        self.x=x
        self.y=y
        self.total_frames=0.0
        self.dir=dir
    def update(self,frame_time):
        distance = Player_Attack.RUN_SPEED_PPS * frame_time
        if self.dir:
            self.x+=distance
        else:
            self.x-=distance
        #self.draw()
    def get_hitbox(self):
         return self.x - 30, self.y +30, self.x + 30, self.y-30
    def draw(self):
        self.image.draw(self.x, self.y)
        #draw_rectangle(*self.get_hitbox())

class Player:
    global font
    STANDING,LEFT_MOVE,RIGHT_MOVE,UP_MOVE,DOWN_MOVE=0,1,2,3,4
    ATTACK,SKILL=5,6
    #SKILL,HIT=None
    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME =1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 10
    def __init__(self):
        self.skill_gauge=2
        self.image = load_image('./resource/player1.png')
        self.image_attack = load_image('./resource/player_attack11.png')
        self.image_skill=load_image('./resource/player_skill.png')
        self.image_skill_effect=load_image('./resource/skill.png')
        self.image_skill_effect2=load_image('./resource/skill2.png')
        self.frame_y = 1
        self.frame_x = 0
        self.state = self.STANDING
        self.old_state=self.state
        self.x=200
        self.y=200
        self.hp=10
        self.total_frames=0.0
        self.attack_start=False
    def draw(self):
        if self.state==self.ATTACK:
            self.image_attack.clip_draw(self.frame_x * 200, self.frame_y * 115, 200, 115, self.x, self.y)
        elif self.state==self.SKILL:
            self.image_skill.clip_draw(self.frame_x * 230, self.frame_y * 150, 230, 130, self.x, self.y)
            if self.frame_x>=3 and self.frame_x<=7:
                if self.frame_x%2==0:
                    self.image_skill_effect.draw(400,300)
                else:
                    self.image_skill_effect2.draw(400,300)
                for monsteri in main_state.monster:
                    monsteri.hp=0
        else:
            self.image.clip_draw(self.frame_x * 117, self.frame_y * 115, 117, 115, self.x, self.y)
        #draw_rectangle(*self.get_hitbox())
        #font.draw(self.x-30,self.y+60,'hp -> %d ,gauge->%d'%(self.hp,self.skill_gauge))
    def get_hitbox(self):
         return self.x - 40, self.y+50 , self.x + 40, self.y-50
    def update(self, frame_time,stage):
        distance = Player.RUN_SPEED_PPS * frame_time
        self.total_frames += Player.FRAMES_PER_ACTION * Player.ACTION_PER_TIME * frame_time

        if self.state==self.ATTACK:

            self.frame_x = int(self.total_frames + 1) % 9
            if self.frame_x==5 and self.attack_start==False:
                self.attack_start=True
                main_state.player_arrow.append(Player_Attack(self.x+30,self.y,self.frame_y))
            if self.frame_x>5:
                self.attack_start=False
        elif self.state==self.SKILL:

            self.frame_x = int(self.total_frames + 1) % 13
            if self.frame_x==12:
                self.frame_x=0
                self.state=self.old_state

        else:

            self.frame_x = int(self.total_frames + 1) % 5



        if self.state == self.RIGHT_MOVE:
            self.x = min(750, self.x + distance)
        elif self.state == self.LEFT_MOVE:
            self.x = max(50, self.x - distance)
        elif self.state == self.UP_MOVE:
            if stage!=3:
                self.y = min(325, self.y + distance)
            else:

                self.y = min(450, self.y + distance)
        elif self.state == self.DOWN_MOVE:
            self.y = max(50, self.y - distance)



        #self.draw();
    def handle_event(self, event,stage):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state==self.SKILL:
                self.old_state=self.LEFT_MOVE
            else:
                self.state=self.LEFT_MOVE
            if stage==3:
                self.frame_y=0
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state==self.SKILL:
                self.old_state=self.RIGHT_MOVE
            else:
                self.state=self.RIGHT_MOVE
            if stage==3:
                self.frame_y=1
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.state==self.SKILL:
                self.old_state=self.UP_MOVE
            else:
                self.state=self.UP_MOVE
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if self.state==self.SKILL:
                self.old_state=self.DOWN_MOVE
            else:
                self.state=self .DOWN_MOVE
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state==self.LEFT_MOVE:
                self.state=self .STANDING
            elif self.state==self.SKILL:
                self.old_state=self.STANDING
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state==self.RIGHT_MOVE:
                self.state=self.STANDING
            elif self.state==self.SKILL:
                self.old_state=self.STANDING
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            if self.state==self.UP_MOVE:
                self.state=self.STANDING
            elif self.state==self.SKILL:
                self.old_state=self.STANDING
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            if self.state==self.DOWN_MOVE:
                self.state=self.STANDING
            elif self.state==self.SKILL:
                self.old_state=self.STANDING
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            if self.state==self.SKILL:
                self.old_state=self.ATTACK
            else:
                self.total_frames=0
                self.frame_x=0
                self.state=self.ATTACK
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_SPACE):
            if self.state==self.ATTACK:
                self.frame_x=0
                self.state=self .STANDING
            elif self.state==self.SKILL:
                self.old_state=self.STANDING
        elif (event.type, event.key) ==(SDL_KEYDOWN,SDLK_z):
            if self.state!=self.SKILL and self.skill_gauge>0:
                self.total_frames=0
                self.skill_gauge-=1
                self.frame_x=0
                self.old_state=self.state
                self.state=self.SKILL


class Item:
    image=None
    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH = 10.0 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    SCORE_ITEM1,SCORE_ITEM2,SCORE_ITEM3,SKILL_ITEM,HP_ITEM=0,1,2,3,4
    bgm=None
    def __init__(self,x,y):
        if Item.image==None:
            Item.bgm=load_music('./resource/item.wav')
            Item.image = load_image('./resource/item.png')
            Item.bgm.set_volume(80)

        self.item_num=random.randint(1,13)
        if self.item_num<=9:
            self.item_num=(int)(self.item_num/3-1)
        elif self.item_num<=11:
            self.item_num=self.SKILL_ITEM
        else:
            self.item_num=self.HP_ITEM
        #self.item_num=0

        self.x=x
        self.y=y
    def eat(self):
        self.bgm.play();
    def update(self,frame_time):
        distance = Item.RUN_SPEED_PPS * frame_time

        self.x-=distance
        self.draw()
    def draw(self):
         self.image.clip_draw(self.item_num* 50, 0, 50, 50, self.x, self.y)
         #draw_rectangle(*self.get_hitbox())
    def get_hitbox(self):
        return self.x - 20, self.y+20 , self.x + 20, self.y-20
