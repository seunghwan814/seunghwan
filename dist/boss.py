import main_state
from pico2d import *

class Boss:
    image=None
    image_attack=None
    MOVE,ATTACK=0,1
    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH = 5 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME =1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 5
    def __init__(self):

        self.image = load_image('./resource/boss.png')
        self.image_attack = load_image('./resource/boss_at.png')
        self.state=self.MOVE
        self.frame_x = 0
        self.tempframe_x=0
        self.frame_y=self.MOVE
        self.x=900
        self.y=300
        self.hp=30
        self.total_frames=0.0
        self.sense=False
        self.attack_start=False
    def set(self,x,y):
        self.x=x
        self.y=y
    def draw(self):
        if self.state==self.MOVE:
            self.image.clip_draw(self.frame_x * 225, self.frame_y* 250, 225, 250, self.x, self.y)
        else:
            self.image_attack.clip_draw((self.frame_x) * 300, self.frame_y* 240, 300, 240, self.x, self.y)
        #draw_rectangle(*self.get_hitbox())

    def get_hitbox(self):

            return self.x - 80, self.y+120 , self.x + 80, self.y-120


    def update(self,frame_time,p_X,p_Y):

        distance =  Boss.RUN_SPEED_PPS * frame_time
        self.total_frames += Boss.FRAMES_PER_ACTION * Boss.ACTION_PER_TIME * frame_time
        if self.state==self.MOVE:
            self.frame_x =  int(self.total_frames ) % 6

        elif self.state==self.ATTACK:
            self.frame_x =  int(self.total_frames +1) % 11
            if self.frame_x==5 and self.attack_start==False:
                self.attack_start=True
                main_state.boss_arrow.append(Boss_Attack(self.x,self.y+30,self.frame_y))
                main_state.boss_arrow.append(Boss_Attack(self.x,self.y,self.frame_y))
                main_state.boss_arrow.append(Boss_Attack(self.x,self.y-30,self.frame_y))
                main_state.boss_arrow.append(Boss_Attack(self.x,self.y-60,self.frame_y))
            if self.frame_x>5:
                self.attack_start=False

            if self.frame_x ==10:
                self.state=self.MOVE
        elif self.state==3:
            distance=distance*2
        if p_X>=self.x:
            self.frame_y = 0
            self.x+=distance
        if p_X<self.x:
            self.frame_y = 1
            self.x-=distance
        if p_Y>=self.y:
            self.y+=distance
        if p_Y<self.y:
            self.y-=distance

class Boss_Attack:
    #SKILL,HIT=None
    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH =60.0 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self,x,y,dir):
        self.image= load_image('./resource/b_fire.png')
        self.x=x
        self.y=y
        self.total_frames=0.0
        self.dir=dir
    def update(self,frame_time):
        distance = Boss_Attack.RUN_SPEED_PPS * frame_time
        if self.dir:
            self.x-=distance
        else:
            self.x+=distance
        #self.draw()
    def get_hitbox(self):
         return self.x - 50, self.y +50, self.x + 50, self.y-50
    def draw(self):
        self.image.draw(self.x, self.y)
        #draw_rectangle(*self.get_hitbox())