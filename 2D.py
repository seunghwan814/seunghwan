# hero_controller.py : control hero move with left and right key
import time
import random
import json
from pico2d import *


monster=[]
monster_arrow=[]
player_arrow=[]
items=[]
init_data_file=open('init.txt','r')
init_data=json.load(init_data_file)
init_data_file.close()
class Player_Attack:
    #SKILL,HIT=None
    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH = 40.0 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self,x,y):
        self.image= load_image('./resource/p_attack.png')
        self.x=x
        self.y=y
        self.total_frames=0.0
    def update(self,frame_time):
        distance = Player_Attack.RUN_SPEED_PPS * frame_time
        self.x+=distance
        self.draw()
    def get_hitbox(self):
         return self.x - 30, self.y +30, self.x + 30, self.y-30
    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_hitbox())

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
        self.image_attack = load_image('./resource/player_attack1.png')
        self.image_skill=load_image('./resource/Untitled-3.png')
        self.image_skill_effect=load_image('./resource/skill.png')
        self.image_skill_effect2=load_image('./resource/skill2.png')
        self.frame_y = 0
        self.frame_x = 0
        self.state = self.STANDING
        self.old_state=self.state
        self.x=200
        self.y=200
        self.hp=20
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
                for monsteri in monster:
                    monsteri.hp=0
        else:
            self.image.clip_draw(self.frame_x * 117, self.frame_y * 115, 117, 115, self.x, self.y)
        draw_rectangle(*self.get_hitbox())
        font.draw(self.x-30,self.y+60,'hp -> %d ,gauge->%d'%(self.hp,self.skill_gauge))
    def get_hitbox(self):
         return self.x - 40, self.y+50 , self.x + 40, self.y-50
    def update(self, frame_time):
        distance = Player.RUN_SPEED_PPS * frame_time
        self.total_frames += Player.FRAMES_PER_ACTION * Player.ACTION_PER_TIME * frame_time
        #self.frame = int(self.total_frames) % 8
        #self.frame = int(self.total_frames) % 8
        if self.state==self.ATTACK:
           # Player.ACTION_PER_TIME=9
            self.frame_x = int(self.total_frames + 1) % 9
            if self.frame_x==5 and self.attack_start==False:
                self.attack_start=True
                player_arrow.append(Player_Attack(self.x+30,self.y))
            if self.frame_x>5:
                self.attack_start=False
        elif self.state==self.SKILL:
           # Player.ACTION_PER_TIME=13
            self.frame_x = int(self.total_frames + 1) % 13
            if self.frame_x==12:
                self.frame_x=0
                self.state=self.old_state

        else:
            #Player.ACTION_PER_TIME=5
            self.frame_x = int(self.total_frames + 1) % 5

       # self.frame_x = int(self.total_frames)% Player.ACTION_PER_TIME

        if self.state == self.RIGHT_MOVE:
            self.x = min(750, self.x + distance)
        elif self.state == self.LEFT_MOVE:
            self.x = max(50, self.x - distance)
        elif self.state == self.UP_MOVE:
            self.y = min(325, self.y + distance)
        elif self.state == self.DOWN_MOVE:
            self.y = max(50, self.y - distance)



        self.draw();
    def handle_event(self, event):

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state==self.SKILL:
                self.old_state=self.LEFT_MOVE
            else:
                self.state=self.LEFT_MOVE
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state==self.SKILL:
                self.old_state=self.RIGHT_MOVE
            else:
                self.state=self.RIGHT_MOVE
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
    def __init__(self,x,y):
        if Item.image==None:
            self.image = load_image('./resource/item.png')

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
    def update(self,frame_time):
        distance = Item.RUN_SPEED_PPS * frame_time

        self.x-=distance
        self.draw()
    def draw(self):
         self.image.clip_draw(self.item_num* 50, 0, 50, 50, self.x, self.y)
         draw_rectangle(*self.get_hitbox())
    def get_hitbox(self):
        return self.x - 20, self.y+20 , self.x + 20, self.y-20




def collide(a, b):
        left_a,top_a , right_a, bottom_a = a.get_hitbox()
        left_b, top_b, right_b,  bottom_b= b.get_hitbox()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False

        return True


def handle_events():
    global running
    global player
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event);

class BackGround:
    global stage

    PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
    RUN_SPEED_KMPH = 10.0 # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    def __init__(self):
        self.speed = 0
        self.left = 0
        self.screen_width = 800
        self.screen_height = 350



        self.block_image = load_image('./resource/BackGround_Block.png')
        self.sky_image=load_image('./resource/BackGround_sky.png')
        self.hp_image = load_image('./resource/hp_mp.png')
        self.HP_T_image = load_image('./resource/HP.png')
        self.MP_T_image = load_image('./resource/MP.png')
        self.block_image2 = load_image('./resource/BackGround_Block2.png')
        self.sky_image2=load_image('./resource/BackGround_sky2.png')
        self.potal_imamge=load_image('./resource/potal.png')



        self.x_move_max=init_data['BackGround']['max_x']
        self.x_move_min=init_data['BackGround']['min_x']
        self.block_x=init_data['BackGround']['min_x']
        self.block_x2=init_data['BackGround']['max_x']
        self.sky_x=init_data['BackGround']['min_x']
        self.sky_x2=init_data['BackGround']['max_x']
        self.block_moveP=init_data['BackGround']['block_moveP']
        self.sky_moveP=init_data['BackGround']['sky_moveP']
        self.screen_W=init_data['BackGround']['screen_w']
        self.sky_h=init_data['BackGround']['sky_draw_h']
        self.sky_y=init_data['BackGround']['sky_y']
        self.block_h=init_data['BackGround']['block_draw_h']
        self.block_y=init_data['BackGround']['block_y']
        self.potal_x=init_data['BackGround']['max_x']
        self.potal=False

    def draw(self):
        x = int(self.left)
        w = min(self.sky_image.w - x, self.screen_width)

        if stage==1:
            self.sky_image.clip_draw(x,0,self.screen_W,self.sky_h,self.sky_x,self.sky_y)
            self.sky_image.clip_draw(0,0,self.screen_W,self.sky_h,self.sky_x2,self.sky_y)
            self.block_image.clip_draw(0,0,self.screen_W,self.block_h,self.block_x,self.block_y)
            self.block_image.clip_draw(0,0,self.screen_W,self.block_h,self.block_x2,self.block_y)

           # self.sky_image.clip_draw_to_origin(x, 0, w, self.screen_height, 0, 0)
           # self.sky_image.clip_draw_to_origin(0,0, self.screen_width-w,self.screen_height, w, 0)




        elif stage==2:
            self.sky_image2.clip_draw(0,0,self.screen_W,self.sky_h,self.sky_x,self.sky_y)
            self.sky_image2.clip_draw(0,0,self.screen_W,self.sky_h,self.sky_x2,self.sky_y)
            self.block_image2.clip_draw(0,0,self.screen_W,self.block_h,self.block_x,self.block_y)
            self.block_image2.clip_draw(0,0,self.screen_W,self.block_h,self.block_x2,self.block_y)








        if self.potal:
            self.potal_imamge.clip_draw(0,0,144,self.block_h,self.potal_x,self.block_y)




        for i in range(0,int(player.hp/2)):
            self.hp_image.clip_draw_to_origin(0,0,50,50,100+50*i,500)
        for i in range(0,int(player.skill_gauge)):
            self.hp_image.clip_draw_to_origin(50,0,50,50,100+50*i,450)
        self.HP_T_image.clip_draw_to_origin(0,0,100,50,0,500)
        self.MP_T_image.clip_draw_to_origin(0,0,100,50,0,450)
    def update(self,frame_time):

        distance =BackGround.RUN_SPEED_PPS * frame_time
        self.draw();
        self.block_x-=self.block_moveP* distance
        self.sky_x-=self.sky_moveP* distance
        self.block_x2-=self.block_moveP* distance
        self.sky_x2-=self.sky_moveP* distance
        if self.potal:
             self.potal_x-=self.block_moveP* distance

        if self.block_x<=-self.x_move_min:
            self.block_x=self.x_move_max
        if self.sky_x<=-self.x_move_min:
            self.sky_x=self.x_move_max
        if self.block_x2<=-self.x_move_min:
            self.block_x2=self.x_move_max
        if self.sky_x2<=-self.x_move_min:
            self.sky_x2=self.x_move_max
        #self.left = distance % self.sky_image.w

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
        draw_rectangle(*self.get_hitbox())
    def get_hitbox(self):
         return self.x - 40, self.y+40 , self.x + 30, self.y-50
    def update(self,frame_time):
        distance = Monster_Lion.RUN_SPEED_PPS * frame_time
        self.total_frames += Monster_Lion.FRAMES_PER_ACTION * Monster_Lion.ACTION_PER_TIME * frame_time
        self.frame_x = int(self.total_frames + 1) % 4
        self.x-=distance
        self.draw()
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
        draw_rectangle(*self.get_hitbox())
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
                monster_arrow.append(Ghost_Arrow(self.x,self.y))
            if self.frame_x>5:
                 self.attack=False
        elif self.state==self.MOVE:
            self.frame_x =  int(self.total_frames + 1) % 6
        self.x-=distance
        self.draw()
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

        self.draw()
    def get_hitbox(self):
         return self.x - 10, self.y +10, self.x + 10, self.y-10
    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_hitbox())
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
            self.image = load_image('./resource/monster_sheep_stand.png')
        if Monster_Sheep.image_attack==None:
            self.image_attack = load_image('./resource/monster_sheep_attack.png')
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
            self.image_attack.clip_draw((self.frame_x) * 275, self.frame_y* 85, 275, 85, self.x, self.y)
        draw_rectangle(*self.get_hitbox())
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
        self.draw()
    def detecting(self,a):
        left_a,top_a , right_a, bottom_a = a.get_hitbox()
        left_b, top_b, right_b,  bottom_b= self.get_hitbox()

        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
        if left_a > right_b: return False

        if right_a < left_b-150: return False
        if right_a > left_b-150: return True








def main():
    open_canvas(800,600)
    score=0

    global player,font,background,running,stage
    stage=1
    font=load_font('./resource/ENCR10B.TTF')
    background = BackGround()
    player=Player()

    running = True;
    current_time = get_time()
    total_time=0.0
    creating=False
    create_time=0.0
    monster_number=2
    create_next_time=0.0
    total_time=0.0
    while running:
        frame_time = get_time() - current_time
        current_time += frame_time
        handle_events()



        for monsteri in monster:
            for p_arrow in player_arrow:
                if collide(p_arrow,monsteri):
                    monsteri.hp-=1;
                    player_arrow.remove(p_arrow)
            if monsteri.hp==0:
                if random.randint(0,2)==0:
                    items.append(Item(monsteri.x,monsteri.y))
                    print("item creat")
                monster.remove(monsteri)


            if collide(player,monsteri):
                monsteri.hp-=1
                player.hp-=1
                print("crash")

            if monsteri.detecting(player) and monsteri.sense==False:
                monsteri.sense=True
                monsteri.change_state()
            elif monsteri.detecting(player)==False and monsteri.sense==True:
                monsteri.sense=False
                monsteri.change_state()
        for arrow in monster_arrow:
            if collide(player,arrow):
                monster_arrow.remove(arrow)
                player.hp-=1;
                print("mon aro crash")



        if current_time>= 40:
            create_time=0.5
        elif current_time>= 20:
            create_time=1.0
        elif current_time>= 0:
            create_time=1.5


        if current_time%create_time<0.05 and creating==False:
            creating=True
            temp=random.randint(1,monster_number)
            if temp==1:
                monster.append(Monster_Lion())
            elif temp==2:
                monster.append(Monster_Sheep())
            else:
                monster.append(Monster_Ghost())
            create_next_time=current_time+create_time

        if current_time>create_next_time:
            creating=False


        for item in items:
            if item.x<-100:
                items.remove(item)

        clear_canvas()
        background.update(frame_time)

        font.draw(50,50,'score: %d time: %f, f time:%f'%(score, current_time,frame_time))
        for item in items:
            if collide(player,item):
                if item.item_num<3:
                    score+=200
                elif item.item_num==3:
                    player.skill_gauge+=1
                else:
                    player.hp+=2
                items.remove(item)

            else:
                item.update(frame_time)
        for p_arrow in player_arrow:
            p_arrow.update(frame_time)
            if p_arrow.x>1000:
                player_arrow.remove(p_arrow)

        for monsteri in monster:
            monsteri.update(frame_time)
        for arrow in monster_arrow:
            arrow.update(frame_time)
            if arrow.x<-150:
                monster_arrow.remove(arrow)
                print("arrow remove")

        player.update(frame_time)
        if current_time>=60:
            background.potal=True
            if player.x>background.potal_x:
                stage=2
                total_time=current_time
                current_time = 0.0
                player.hp=20
                player.skill_gauge=2
                creating=False
                create_time=0.0
                monster_number=3
                create_next_time=0.0
                for monsteri in monster:
                    monster.remove(monsteri)
                #reset_time()
        update_canvas()



    del(font)
    close_canvas()


if __name__ == '__main__':
    main()