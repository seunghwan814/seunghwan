import random

from pico2d import *
import bakground_bg
import Player_item
import monsterpy
import game_framework
import title_state
import hold_state
import end_state
import json
import boss
name = "MainState"

running = None

monster=[]
monster_arrow=[]
player_arrow=[]
items=[]
boss_arrow=[]

def collide(a, b):
        left_a,top_a , right_a, bottom_a = a.get_hitbox()
        left_b, top_b, right_b,  bottom_b= b.get_hitbox()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False

        return True





def enter():

    game_framework.reset_time()

    #open_canvas(800,600)


    global player,font,background,running,stage,total_time,creating,create_next_time,score,monster_number,next_time
    stage=1
    font=load_font('./resource/ENCR10B.TTF')
    background=bakground_bg.BackGround()
    player=Player_item.Player()
    score=0
    running = True;
    total_time=0.0
    creating=False
    create_time=0.0
    monster_number=2
    create_next_time=0.0

    pass


def exit():
    global player,font,background


   # del(font)
    #close_canvas()
    pass


def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    global player,total_time,stage
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_h):
            game_framework.push_state(hold_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F2:
            total_time=148
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F1:
            total_time=58
        else:
           player.handle_event(event,stage);



def collide(a, b):
        left_a,top_a , right_a, bottom_a = a.get_hitbox()
        left_b, top_b, right_b,  bottom_b= b.get_hitbox()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False

        return True

def update(frame_time):
    global current_time,creating,score,create_next_time,background,monster_number,stage,total_time,bossi,player
   # handle_events(frame_time)


       # frame_time = get_time() - current_time
    total_time+= frame_time


    if stage==1 or stage==2:

        for monsteri in monster:
            for p_arrow in player_arrow:
                if collide(p_arrow,monsteri):
                    monsteri.hp-=1;
                    score+=100
                    player_arrow.remove(p_arrow)
            if monsteri.hp==0:
                if random.randint(0,2)==0:
                    items.append(Player_item.Item(monsteri.x,monsteri.y))
                   # print("item creat")
                monster.remove(monsteri)


            if collide(player,monsteri):
                monsteri.hp-=1
                player.hp-=1
                #print("crash")

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
               # print("mon aro crash")


        if total_time>= 100:
            create_time=0.5
        elif total_time>= 80:
            create_time=0.8
        elif total_time>= 60:
           create_time=1.2
        elif total_time>= 40:
            create_time=0.8
        elif total_time>= 20:
            create_time=1.0
        elif total_time>= 0:
            create_time=1.5


        if total_time%create_time<0.05 and creating==False:
            creating=True
            temp=random.randint(1,monster_number)
            if temp==1:
                monster.append(monsterpy.Monster_Lion())
            elif temp==2:
                monster.append(monsterpy.Monster_Sheep())
            else:
                monster.append(monsterpy.Monster_Ghost())
            create_next_time=total_time+create_time

        if total_time>create_next_time:
            creating=False


        for item in items:
            if item.x<-100:
                items.remove(item)

       # clear_canvas()






        for monsteri in monster:
            monsteri.update(frame_time)
        for arrow in monster_arrow:
            arrow.update(frame_time)
            if arrow.x<-150:
                monster_arrow.remove(arrow)
                #print("arrow remove")
    for p_arrow in player_arrow:
            p_arrow.update(frame_time)
            if p_arrow.x>900 or p_arrow.x<-50:
                player_arrow.remove(p_arrow)
    for item in items:
            if collide(player,item):
                #item.eat()
                if item.item_num<3:
                    score+=20
                elif item.item_num==3:
                    player.skill_gauge+=1
                elif item.item_num==4:
                    player.hp+=2
                items.remove(item)
                #background.bgm_call(stage)
            else:
                item.update(frame_time)
    background.update(frame_time,stage)
    player.update(frame_time,stage)
    if total_time>=40 and stage==1:
            background.potal=True
            if player.x>background.potal_x:
                stage=2
                background.bgm2.repeat_play()
                #game_framework.reset_time()
                player.hp=10
                player.skill_gauge=2
                creating=False
                create_time=0.0
                monster_number=3
                create_next_time=0.0
                for monsteri in monster:
                    monster.remove(monsteri)
                #reset_time()
    if total_time>=80 and stage==2:
            background.potal=True
            if player.x>background.potal_x:
                background.potal=False
                stage=3
                background.bgm3.repeat_play()
                player.hp=10
                player.skill_gauge=0
                create_time=5.0
                creating=False
                for monsteri in monster:
                    monster.remove(monsteri)
                bossi=boss.Boss()
                next_time=0
    if stage==3:
        global next_time
        create_time=5.0
        bossi.update(frame_time,player.x,player.y)
        if total_time>=next_time :
            if collide(player,bossi):
                bossi.hp-=1
                player.hp-=2
                #print("crash")
                next_time=total_time+2
        for p_arrow in player_arrow:
             if collide(p_arrow,bossi):
                    bossi.hp-=1;
                    score+=100
                    player_arrow.remove(p_arrow)


        for boss_a in boss_arrow:
             boss_a.update(frame_time)
        if total_time%create_time<0.05 and creating==False:
            creating=True
            temp=random.randint(1,5)
            if temp==1:
               bossi.state=0
            elif temp==2:
                bossi.state=1
            elif temp==3:
                bossi.state=3
            create_next_time=total_time+create_time

        if total_time>create_next_time:
            creating=False
        if bossi.hp==0:
            game_framework.change_state(end_state)
    global player,bossi
    if player.hp<=0 :
            game_framework.change_state(end_state)
            #update_canvas()





def draw(frame_time):
     clear_canvas()
     background.draw(stage)
     if stage!=3:
         for monster_a in monster_arrow:
                   monster_a.draw()

         for monsteri in monster:
                   monsteri.draw()
     else:
         bossi.draw()
         for monsteri in boss_arrow:
             monsteri.draw()
     for p_a in player_arrow:
         p_a.draw()
     for item in items:
         item.draw()
     player.draw()
     font.draw(50,50,'score: %d time: %f'%(score,total_time))
     update_canvas()
     pass





