import main_state
import json
from pico2d import *
import Player_item

init_data_file=open('./resource/init.txt','r')
init_data=json.load(init_data_file)
init_data_file.close()
name = "background_bg"

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
        self.bgm1 = load_music('./resource/1stage.mp3')
        self.bgm1.set_volume(60)
        self.bgm1.repeat_play()


        self.bgm2 = load_music('./resource/2stage.mp3')
        self.bgm2.set_volume(60)
        self.bgm3 = load_music('./resource/boss.mp3')
        self.bgm3.set_volume(60)


        self.block_image = load_image('./resource/BackGround.png')
        self.sky_image=load_image('./resource/desert_BG.png')
        self.hp_image = load_image('./resource/hp_mp.png')
        self.HP_T_image = load_image('./resource/HP.png')
        self.MP_T_image = load_image('./resource/MP.png')
        self.block_image2 = load_image('./resource/BackGround.png')
        self.block_image3 = load_image('./resource/BackGround2.png')
        self.sky_image2=load_image('./resource/desert_BG.png')
        self.potal_imamge=load_image('./resource/potal.png')
        self.stage3_img=load_image('./resource/backgound1.png')
        self.stage3_c_img=load_image('./resource/c.png')


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

    def draw(self,stage):
        x = int(self.left)
        w = min(self.sky_image.w - x, self.screen_width)

        if stage==1:
            self.sky_image.clip_draw(x,0,self.screen_W,self.sky_h,self.sky_x,self.sky_y)
            self.sky_image.clip_draw(0,0,self.screen_W,self.sky_h,self.sky_x2,self.sky_y)
            self.block_image.clip_draw(0,0,self.screen_W,self.block_h,self.block_x,self.block_y)
            self.block_image.clip_draw(0,0,self.screen_W,self.block_h,self.block_x2,self.block_y)






        elif stage==2:
            self.sky_image2.clip_draw(0,0,self.screen_W,self.sky_h,self.sky_x,self.sky_y)
            self.sky_image2.clip_draw(0,0,self.screen_W,self.sky_h,self.sky_x2,self.sky_y)
            self.block_image2.clip_draw(0,0,self.screen_W,self.block_h,self.block_x,self.block_y)
            self.block_image2.clip_draw(0,0,self.screen_W,self.block_h,self.block_x2,self.block_y)

        elif stage==3:
            self.stage3_img.draw(self.block_x,300)
            self.stage3_img.draw(self.block_x2,300)
            self.stage3_c_img.draw(self.sky_x,300)
            self.stage3_c_img.draw(self.sky_x2,300)
            self.block_image3.clip_draw(0,0,self.screen_W,self.block_h,self.block_x,self.block_y)
            self.block_image3.clip_draw(0,0,self.screen_W,self.block_h,self.block_x2,self.block_y)






        if self.potal:
            self.potal_imamge.clip_draw(0,0,144,self.block_h,self.potal_x,self.block_y)




        for i in range(0,int(main_state.player.hp/2)):
            self.hp_image.clip_draw_to_origin(0,0,50,50,100+50*i,500)

        self.HP_T_image.clip_draw_to_origin(0,0,100,50,0,500)
        if stage!=3:
            for i in range(0,int(main_state.player.skill_gauge)):
                self.hp_image.clip_draw_to_origin(50,0,50,50,100+50*i,450)
            self.MP_T_image.clip_draw_to_origin(0,0,100,50,0,450)
    def bgm_call(self,stage):
        if stage==1:
             self.bgm1.repeat_play()
        elif stage==2:
             self.bgm2.repeat_play()
        elif stage==3:
             self.bgm3.repeat_play()
    def update(self,frame_time,stage):

        distance =BackGround.RUN_SPEED_PPS * frame_time
        #self.draw(stage);
        self.block_x-=self.block_moveP* distance
        self.sky_x-=self.sky_moveP* distance
        self.block_x2-=self.block_moveP* distance
        self.sky_x2-=self.sky_moveP* distance
        if self.potal:
            self.potal_x-=self.block_moveP* distance
            if self.potal_x<-200:
                self.potal=False
                self.potal_x=init_data['BackGround']['max_x']

        if self.block_x<=-self.x_move_min:
            self.block_x=self.block_x2+self.x_move_min*2
        if self.block_x2<=-self.x_move_min:
            self.block_x2=self.block_x+self.x_move_min*2
            #self.block_x2=self.x_move_max
        if stage!=3:
            if self.sky_x<=-self.x_move_min:
                self.sky_x=self.sky_x2+self.x_move_min*2
            if self.sky_x2<=-self.x_move_min:
                self.sky_x2=self.sky_x+self.x_move_min*2
                #self.sky_x2=self.x_move_max
        else:
            if self.sky_x<=-self.x_move_min*2:
                self.sky_x=self.sky_x2+self.x_move_min*4
            if self.sky_x2<=-self.x_move_min*2:
                self.sky_x2=self.sky_x+self.x_move_min*4
        #self.left = distance % self.sky_image.w
