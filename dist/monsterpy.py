from pico2d import *
import random

import main_state

name = "monster"
class Monster_Lion:
    image = None
    MOVE,HIT=2,1
    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH = 30.0 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME =1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 5
    def __init__(self):
        if Monster_Lion.image==None:
            self.image = load_image('./resource/monster_lion.png')
        self.frame_x = 0
        self.frame_y=self.MOVE
        self.x=900
        self.y=random.randint(50,325)
        self.hp=1
        self.sense=False
        self.total_frames=0.0
    def set(self,x,y):
        self.x=x
        self.y=y
    def draw(self):
        self.image.clip_draw(self.frame_x * 110, self.frame_y* 110, 110, 110, self.x, self.y)
        #draw_rectangle(*self.get_hitbox())
    def get_hitbox(self):
         return self.x - 40, self.y+40 , self.x + 30, self.y-50
    def update(self,frame_time):
        distance = Monster_Lion.RUN_SPEED_PPS * frame_time
        self.total_frames += Monster_Lion.FRAMES_PER_ACTION * Monster_Lion.ACTION_PER_TIME * frame_time
        self.frame_x = int(self.total_frames + 1) % 4
        self.x-=distance
        #self.draw()
    def change_state(self):
        pass
    def detecting(a, self):
        pass

class Monster_Ghost:
    image = None
    image_attack = None
    MOVE,ATTACK=0,1
    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME =1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 5
    def __init__(self):
        #self.arrow=[]
        if Monster_Ghost.image==None:
            self.image = load_image('./resource/monster_ghost_stand.png')
        if Monster_Ghost.image_attack==None:
            self.image_attack = load_image('./resource/monster_ghost_attack.png')
        self.frame_x = 0
        self.frame_y=self.MOVE
        self.x=900
        self.y=random.randint(50,325)
        self.hp=1
        self.tempframe_x=0
        self.state=self.MOVE
        self.sense=False
        self.total_frames=0.0
        self.attack=False
    def set(self,x,y):
        self.x=x
        self.y=y
    def draw(self):
        if self.state==self.MOVE:
            self.image.clip_draw(self.frame_x * 60, self.frame_y* 55, 60, 55, self.x, self.y)
        elif self.state==self.ATTACK:
           self.image_attack.clip_draw((self.frame_x) * 150, self.frame_y* 75, 150, 75, self.x, self.y)
        #draw_rectangle(*self.get_hitbox())
    def get_hitbox(self):
         return self.x - 30, self.y +30, self.x + 20, self.y-30
    def change_state(self):
        if self.state==self.MOVE and self.sense==True:
            self.state=self.ATTACK
            frame_x=0
        elif self.state==self.ATTACK and self.sense==False:
            self.state=self.MOVE
            frame_x=0
    def update(self,frame_time):
        distance = Monster_Ghost.RUN_SPEED_PPS * frame_time
        self.total_frames += Monster_Ghost.FRAMES_PER_ACTION * Monster_Ghost.ACTION_PER_TIME * frame_time

        if self.state==self.ATTACK:
            self.frame_x =  int(self.total_frames + 1) % 10
            if self.frame_x==5 and self.attack==False:
                self.attack=True
                #print("new arrow")
                main_state.monster_arrow.append(Ghost_Arrow(self.x,self.y))
            if self.frame_x>5:
                 self.attack=False
        elif self.state==self.MOVE:
            self.frame_x =  int(self.total_frames + 1) % 6
        self.x-=distance
        #self.draw()
    def detecting(self,a):
        left_a,top_a , right_a, bottom_a = a.get_hitbox()
        left_b, top_b, right_b,  bottom_b= self.get_hitbox()
        if right_a < left_b:
            if top_a-10 < bottom_b: return False
            if bottom_a+10 > top_b: return False
            if left_a > right_b: return False
            return True
class Ghost_Arrow:
    image=None
    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH = 40.0 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    def __init__(self,x,y):

        self.x=x
        self.y=y
        if Ghost_Arrow.image==None:
            self.image = load_image('./resource/ghost_arrow.png')
    def update(self,frame_time):
        distance = Ghost_Arrow.RUN_SPEED_PPS * frame_time
        #print("a update")
        self.x-=distance

        #self.draw()
    def get_hitbox(self):
         return self.x - 10, self.y +10, self.x + 10, self.y-10
    def draw(self):
        self.image.draw(self.x, self.y)
        #draw_rectangle(*self.get_hitbox())
class Monster_Sheep:
    image=None
    image_attack=None
    MOVE,ATTACK=0,1
    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH = 15.0 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME =1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 5
    def __init__(self):
        if Monster_Sheep.image==None:
            self.image = load_image('./resource/mummy1.png')
        if Monster_Sheep.image_attack==None:
            self.image_attack = load_image('./resource/mummy1.png')
        self.state=self.MOVE
        self.frame_x = 0
        self.tempframe_x=0
        self.frame_y=self.MOVE
        self.x=900
        self.y=random.randint(50,325)
        self.hp=1
        self.total_frames=0.0
        self.sense=False
    def set(self,x,y):
        self.x=x
        self.y=y
    def draw(self):
        if self.state==self.MOVE:
            self.image.clip_draw(self.frame_x * 90, self.frame_y* 65, 90, 65, self.x, self.y)
        elif self.state==self.ATTACK:
            self.image_attack.clip_draw(self.frame_x * 90, self.frame_y* 65, 90, 65, self.x, self.y)
        #draw_rectangle(*self.get_hitbox())
    def change_state(self):
        if self.state==self.MOVE and self.sense==True:
            self.state=self.ATTACK
            frame_x=0
        elif self.state==self.ATTACK and self.sense==False:
            self.state=self.MOVE
            frame_x=0
    def get_hitbox(self):
        if self.state==self.MOVE:
            return self.x - 40, self.y+30 , self.x + 30, self.y-30
        elif self.state==self.ATTACK:
            return self.x - 30-((self.frame_x-1)*8), self.y+30 , self.x + 40, self.y-30

    def update(self,frame_time):

        distance =  Monster_Sheep.RUN_SPEED_PPS * frame_time
        self.total_frames += Monster_Sheep.FRAMES_PER_ACTION * Monster_Sheep.ACTION_PER_TIME * frame_time
        if self.state==self.MOVE:
            self.frame_x =  int(self.total_frames ) % 4
        elif self.state==self.ATTACK:
            self.frame_x =  int(self.total_frames +1) % 13
        self.x-=distance
        #self.draw()
    def detecting(self,a):
        left_a,top_a , right_a, bottom_a = a.get_hitbox()
        left_b, top_b, right_b,  bottom_b= self.get_hitbox()

        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
        if left_a > right_b: return False

        if right_a < left_b-150: return False
        if right_a > left_b-150: return True
