# main.py
import pygame
import time
import importlib

import gui
import supply
import config
import tools
import empty
import plugin
import listener
import plane
import bullet
import level

from pygame.locals import *
from random import *

# 加载配置
conf = config.Config()
conf.init()

# 设置事件系统
eventBus = plugin.EventBus()
plugins = importlib.import_module('plugins')
print('EventBus:',eventBus)
for item in dir(plugins):
    if item[:2] == '__':
        continue
    getattr(plugins,item).init(eventBus)

# 初始化pygame
pygame.init()
pygame.mixer.pre_init(48000,32,8,1024*1024*512)
pygame.mixer.init()

# 加载音乐
if conf.settings['music']:
    empty.load_music(conf.assets_path + "sound/gui_music.ogg", eventBus, locals())
    pygame.mixer.music.set_volume(0.2)

# 初始化参数
bg_size = width, height = conf.get_screen_size()
tool = tools.Tools(bg_size,conf)

# 初始化加载字体
load_font = pygame.font.Font(conf.font,72)
load_text = load_font.render(conf.language.get('game.label.loading.text',conf._lang),load_font,config.COLOR['WHITE'])
load_rect = load_text.get_rect()

# 设置加载屏幕
screen = pygame.display.set_mode(bg_size, DOUBLEBUF|HWSURFACE|NOFRAME)
pygame.display.set_caption(conf.language.get('game.title.text',conf._lang))
load_rect.center = screen.get_rect().center
background = empty.load_image(conf.assets_path + "images/background.png", eventBus, locals()).convert()
load_img = empty.load_image(conf.assets_path + "images/load.png", eventBus, locals()).convert()
background = pygame.transform.scale(background, bg_size)
load_img = pygame.transform.scale(load_img, bg_size)

# 绘制加载屏幕
screen.blit(load_img,(0,0))
screen.blit(load_text,load_rect)
pygame.display.flip()

# 发布预初始化事件
eventBus.addEvent(plugin.event.PreInitEvent(screen,locals()))

# 设置事件监听器
eventBus.addListener(plugin.event.EventType.EXIT_EVENT,listener.ExitListener())
eventBus.addListener(plugin.event.EventType.RELOAD_EVENT,listener.ReloadListener())
eventBus.addListener(plugin.event.EventType.SUPPLY_EVENT,listener.SupplyListener())
eventBus.addListener(plugin.event.EventType.DOUBLE_BULLET_EVENT,listener.DoubleBulletListener())
eventBus.addListener(plugin.event.EventType.NO_HIT_EVENT,listener.NoHitListener())
eventBus.addListener(plugin.event.EventType.BOMB_EVENT,listener.BombListener())

# 主程序
def main(s=True,p=True,set=False):
    pygame.mixer.stop()
    screen.blit(load_img,(0,0))
    screen.blit(load_text,load_rect)
    pygame.display.flip()
    if set:
        conf.reload()
    me_destroy_index = 0
    if conf.settings['mix']:
        button_over_sound = empty.load_sound(conf.assets_path + "sound/button.wav", eventBus, {**locals(), **globals()})
        button_over_sound.set_volume(0.3)
        button_click_sound = empty.load_sound(conf.assets_path + "sound/button_click.wav", eventBus, {**locals(), **globals()})
        button_click_sound.set_volume(0.2)
    if not s and not set:
        if conf.settings['mix']:
            bullet_sound = empty.load_sound(conf.assets_path + "sound/bullet.wav", eventBus, {**locals(), **globals()})
            bullet_sound.set_volume(0.1)
            bomb_sound = empty.load_sound(conf.assets_path + "sound/use_bomb.wav", eventBus, {**locals(), **globals()})
            bomb_sound.set_volume(0.2)
            fail_sound = empty.load_sound(conf.assets_path + "sound/fail.wav", eventBus, {**locals(), **globals()})
            fail_sound.set_volume(0.5)
            supply_sound = empty.load_sound(conf.assets_path + "sound/supply.wav", eventBus, {**locals(), **globals()})
            supply_sound.set_volume(0.2)
            get_bomb_sound = empty.load_sound(conf.assets_path + "sound/get_bomb.wav", eventBus, {**locals(), **globals()})
            get_bomb_sound.set_volume(0.2)
            get_bullet_sound = empty.load_sound(conf.assets_path + "sound/get_bullet.wav", eventBus, {**locals(), **globals()})
            get_bullet_sound.set_volume(0.2)
            upgrade_sound = empty.load_sound(conf.assets_path + "sound/upgrade.wav", eventBus, {**locals(), **globals()})
            upgrade_sound.set_volume(0.2)
            me_down_sound = empty.load_sound(conf.assets_path + "sound/player_destroy.wav", eventBus, {**locals(), **globals()})
            me_down_sound.set_volume(0.2)

        # 加载图片
        pause_nor_image = empty.load_image(conf.assets_path + "images/pause_nor.png", eventBus, {**locals(), **globals()}).convert_alpha()
        pause_pressed_image = empty.load_image(conf.assets_path + "images/pause_pressed.png", eventBus, {**locals(), **globals()}).convert_alpha()
        resume_nor_image = empty.load_image(conf.assets_path + "images/resume_nor.png", eventBus, {**locals(), **globals()}).convert_alpha()
        resume_pressed_image = empty.load_image(conf.assets_path + "images/resume_pressed.png", eventBus, {**locals(), **globals()}).convert_alpha()
        paused_rect = pause_nor_image.get_rect()
        paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
        paused_image = pause_nor_image
        life_image = empty.load_image(conf.assets_path + "images/life.png", eventBus, {**locals(), **globals()}).convert_alpha()
        life_rect = life_image.get_rect()
        bomb_image = empty.load_image(conf.assets_path + "images/bomb.png", eventBus, {**locals(), **globals()}).convert_alpha()

        # 生成我方飞机
        me = plane.PlayerPlane(bg_size,conf.assets_path, conf.settings['sensitivity'],eventBus,{**locals(),**globals()})

        enemies = pygame.sprite.Group()

        # 生成敌方小型飞机
        small_enemies = pygame.sprite.Group()
        tool.add_small_enemies(small_enemies, enemies, 15, eventBus, {**locals(),**globals()})

        # 生成敌方中型飞机
        mid_enemies = pygame.sprite.Group()
        tool.add_mid_enemies(mid_enemies, enemies, 4, eventBus, {**locals(),**globals()})

        # 生成敌方大型飞机
        big_enemies = pygame.sprite.Group()
        tool.add_big_enemies(big_enemies, enemies, 2, eventBus, {**locals(),**globals()})

        # 生成普通子弹
        bullet1 = []
        bullet1_index = 0
        BULLET1_NUM = 16
        for i in range(BULLET1_NUM):
            bullet1.append(bullet.SingleBullet(me.rect.midtop,conf.assets_path,eventBus,{**locals(),**globals()}))

        # 生成超级子弹
        bullet2 = []
        bullet2_index = 0
        BULLET2_NUM = 32
        for i in range(BULLET2_NUM//2):
            bullet2.append(bullet.DoubleBullet((me.rect.centerx-33, me.rect.centery),conf.assets_path,eventBus,{**locals(),**globals()}))
            bullet2.append(bullet.DoubleBullet((me.rect.centerx+30, me.rect.centery),conf.assets_path,eventBus,{**locals(),**globals()}))

        # 统计得分
        score = 0
        score_font = pygame.font.Font(conf.font, 36)

        # 设置难度级别
        level = 1
        level_font = pygame.font.Font(conf.font, 24)
    
        # 全屏炸弹
        bomb_rect = bomb_image.get_rect()
        bomb_font = pygame.font.Font(conf.font, 48)
        bomb_num = [3]
    
        # 每30秒发放一个补给包
        bullet_supply = supply.BulletSupply(bg_size, conf.assets_path, eventBus, {**locals(),**globals()})
        bomb_supply = supply.BombSupply(bg_size, conf.assets_path, eventBus, {**locals(),**globals()})
        supplyEvent = plugin.EventTimer(plugin.event.SupplyEvent(screen, {**locals(),**globals()}), eventBus, (30, plugin.TimerUnit.SEC), -1)
        supplyEvent.start()
    
        # 标志是否使用超级子弹
        is_double_bullet = [False]
        doubleBulletEvent = plugin.EventTimer(plugin.event.DoubleBulletEvent(screen, {**locals(),**globals()}), eventBus, (18, plugin.TimerUnit.SEC), 1)
        noHitEvent = plugin.EventTimer(plugin.event.NoHitEvent(screen, {**locals(),**globals()}), eventBus, (3, plugin.TimerUnit.SEC), 1)
        
    if p and conf.settings['music']:
        empty.load_music(conf.assets_path + "sound/gui_music.ogg", eventBus, {**locals(), **globals()})
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
    
    # 生命数量
    life_num = [3]

    # 用于阻止重复打开记录文件
    recorded = [False]

    # 标志是否暂停游戏
    paused = [False]

    # 游戏UI初始化
    def _start(_in):
        if conf.settings['mix']:button_click_sound.play()
        if conf.settings['music']:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            empty.load_music(conf.assets_path + "sound/game_music.ogg", eventBus, {**locals(), **globals()})
            pygame.mixer.music.play(-1)
        # 调用main函数，重新开始游戏
        main(p=False,s=False)
    
    def _again(_in):
        if conf.settings['mix']:button_click_sound.play()
        if conf.settings['music']:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            empty.load_music(conf.assets_path + "sound/game_music.ogg", eventBus, {**locals(), **globals()})
            pygame.mixer.music.play(-1)
        main(False)

    def _over(_in):
        if conf.settings['mix']:button_over_sound.play()
    
    def _continue(_in):
        if conf.settings['mix']:button_click_sound.play()
        pygame.mixer.music.unpause()
        pause_UI.close()
        _in['pause'][0] = False
    
    def _back(_in):
        if conf.settings['mix']:button_click_sound.play()
        supplyEvent.stop()
        if conf.settings['music']:
            pygame.mixer.music.unpause()
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            empty.load_music(conf.assets_path + "sound/gui_music.ogg", eventBus, {**locals(), **globals()})
            pygame.mixer.music.play(-1)
        _in['recorded'][0] = False
        time.sleep(0.2)
        _in['life'][0] = 0
    
    def _settings(_in):
        if conf.settings['mix']:button_click_sound.play()
        start_UI.close()
        settings_UI.open()
    
    def _main(_in):
        if conf.settings['mix']:button_click_sound.play()
        if main(p=False):
            pygame.quit()
            supplyEvent.stop()
            eventBus.addEvent(plugin.event.ReloadEvent())

    def _exit(_in):
        if conf.settings['mix']:button_click_sound.play()
        eventBus.addEvent(plugin.event.ExitEvent(screen,{**locals(),**globals(),**_in}))
    
    def configPageOpen(**_in):
        settings_UI.close()
        about_UI.open()
    
    def configPageClose(_in):
        about_UI.close()
        settings_UI.open()

    # 设置开始UI
    start_UI = gui.GUI(screen,*bg_size,is_open=s)
    if conf.demo:
        s_label_1 = gui.components.Label(screen,'game.label.welcome.text',conf.language,48,('center',0,300),screen,color=config.COLOR['WHITE'])
        s_label_2 = gui.components.Label(screen,'0',conf.language,60,('center_obj',0,-70),father_obj=s_label_1,color=config.COLOR['WHITE'])
        s_button_1 = gui.components.UIButton(screen,'game.button.try.text',conf.language,eventBus,{**locals(),**globals()},_start,_over,('center_obj',0,-350),father_obj=s_label_1,recorded=recorded,asset_path=conf.assets_path,conf_name=conf.config_name)
        s_button_3 = gui.components.UIButton(screen,'game.button.exit.text',conf.language,eventBus,{**locals(),**globals()},_exit,_over,('center_obj',0,-50),father_obj=s_button_1,asset_path=conf.assets_path,conf_name=conf.config_name)
        start_UI.add_label(s_label_1)
        start_UI.add_button(s_button_1)
        start_UI.add_button(s_button_3)
    elif not conf.record:
        s_label_1 = gui.components.Label(screen,'game.label.welcome.text',conf.language,48,('center',0,300),screen,color=config.COLOR['WHITE'])
        s_label_2 = gui.components.Label(screen,'0',conf.language,60,('center_obj',0,-70),father_obj=s_label_1,color=config.COLOR['WHITE'])
        s_button_1 = gui.components.UIButton(screen,'game.button.start.text',conf.language,eventBus,{**locals(),**globals()},_start,_over,('center_obj',0,-350),father_obj=s_label_1,recorded=recorded,asset_path=conf.assets_path,conf_name=conf.config_name)
        s_button_2 = gui.components.UIButton(screen,'game.button.settings.text',conf.language,eventBus,{**locals(),**globals()},_settings,_over,('center_obj',0,-50),father_obj=s_button_1,asset_path=conf.assets_path,conf_name=conf.config_name)
        s_button_3 = gui.components.UIButton(screen,'game.button.exit.text',conf.language,eventBus,{**locals(),**globals()},_exit,_over,('center_obj',0,-50),father_obj=s_button_2,asset_path=conf.assets_path,conf_name=conf.config_name)
        start_UI.add_label(s_label_1)
        start_UI.add_button(s_button_1)
        start_UI.add_button(s_button_2)
        start_UI.add_button(s_button_3)
    else:
        s_label_1 = gui.components.Label(screen,'game.label.source.best.text',conf.language,48,('center',0,300),screen,color=config.COLOR['WHITE'])
        s_label_2 = gui.components.Label(screen,'0',conf.language,60,('center_obj',0,-70),father_obj=s_label_1,color=config.COLOR['WHITE'])
        s_button_1 = gui.components.UIButton(screen,'game.button.start.text',conf.language,eventBus,{**locals(),**globals()},_start,_over,('center_obj',0,-230),father_obj=s_label_2,recorded=recorded,asset_path=conf.assets_path,conf_name=conf.config_name)
        s_button_2 = gui.components.UIButton(screen,'game.button.settings.text',conf.language,eventBus,{**locals(),**globals()},_settings,_over,('center_obj',0,-50),father_obj=s_button_1,asset_path=conf.assets_path,conf_name=conf.config_name)
        s_button_3 = gui.components.UIButton(screen,'game.button.exit.text',conf.language,eventBus,{**locals(),**globals()},_exit,_over,('center_obj',0,-50),father_obj=s_button_2,asset_path=conf.assets_path,conf_name=conf.config_name)
        start_UI.add_label(s_label_1)
        start_UI.add_label(s_label_2)
        start_UI.add_button(s_button_1)
        start_UI.add_button(s_button_2)
        start_UI.add_button(s_button_3)

    # 设置暂停UI
    pause_UI = gui.GUI(screen,*bg_size)
    p_label_1 = gui.components.Label(screen,'game.label.source.your.text',conf.language,48,('center',0,300),screen,color=config.COLOR['WHITE'])
    p_label_2 = gui.components.Label(screen,'0',conf.language,60,('center_obj',0,-70),father_obj=p_label_1,color=config.COLOR['WHITE'])
    p_button_1 = gui.components.UIButton(screen,'game.button.continue.text',conf.language,eventBus,{**locals(),**globals()},_continue,_over,('center_obj',0,-230),father_obj=p_label_2,pause=paused,asset_path=conf.assets_path,conf_name=conf.config_name)
    p_button_2 = gui.components.UIButton(screen,'game.button.exit.text',conf.language,eventBus,{**locals(),**globals()},_back,_over,('center_obj',0,-50),father_obj=p_button_1,life=life_num,recorded=recorded,asset_path=conf.assets_path,conf_name=conf.config_name)
    pause_UI.add_label(p_label_1)
    pause_UI.add_label(p_label_2)
    pause_UI.add_button(p_button_1)
    pause_UI.add_button(p_button_2)

    # 设置设置UI
    settings_UI = gui.PageUI(screen,*bg_size,'game.label.settings.text',conf.language,start_UI,conf.assets_path,conf.config_name,eventBus,{**locals(),**globals()})
    settings_UI.is_open = set
    if conf.settings['music']:
        s_option_1 = gui.components.PageThing(screen,'game.set_option.music.0',conf.language,eventBus,{**locals(),**globals()},1,'bool',1,2,conf.assets_path,conf.config_name)
    else:
        s_option_1 = gui.components.PageThing(screen,'game.set_option.music.0',conf.language,eventBus,{**locals(),**globals()},1,'bool',2,2,conf.assets_path,conf.config_name)
    if conf.settings['mix']:
        s_option_2 = gui.components.PageThing(screen,'game.set_option.mix.0',conf.language,eventBus,{**locals(),**globals()},2,'bool',1,2,conf.assets_path,conf.config_name)
    else:
        s_option_2 = gui.components.PageThing(screen,'game.set_option.mix.0',conf.language,eventBus,{**locals(),**globals()},2,'bool',2,2,conf.assets_path,conf.config_name)
    try:
        s_option_3 = gui.components.PageThing(screen,'game.set_option.language.@',conf.language,eventBus,{**locals(),**globals()},3,'choose',list(conf.language.get_language_list().keys()).index(conf._lang)+1,len(conf.language.get_language_list().keys()),conf.assets_path,conf.config_name)
    except:
        s_option_3 = gui.components.PageThing(screen,'game.set_option.language.@',conf.language,eventBus,{**locals(),**globals()},3,'choose',0,len(conf.language.get_language_list().keys()),conf.assets_path,conf.config_name)
    s_option_4 = gui.components.PageThing(screen,'game.set_option.screen_width.0',conf.language,eventBus,{**locals(),**globals()},4,'choose',[0,1750,1400,1050].index(conf.settings['screen_width'])+1,max=4,asset_path=conf.assets_path,conf_name=conf.config_name)
    s_option_5 = gui.components.PageThing(screen,'game.set_option.fps.0',conf.language,eventBus,{**locals(),**globals()},4,'choose',[30,60,120,144,0].index(conf.settings['fps'])+1,max=5,asset_path=conf.assets_path,conf_name=conf.config_name)
    s_option_6 = gui.components.PageThing(screen,'game.set_option.sensitivity.0',conf.language,eventBus,{**locals(),**globals()},4,'choose',[300,600,900].index(conf.settings['sensitivity'])+1,max=3,asset_path=conf.assets_path,conf_name=conf.config_name)
    s_option_7 = gui.components.PageThing(screen,'game.set_option.about.0',conf.language,eventBus,{**locals(),**globals()},5,'enter',1,2,conf.assets_path,conf.config_name,jump_to=configPageOpen,argv={**locals()})
    settings_UI.add_thing(s_option_1)
    settings_UI.add_thing(s_option_2)
    settings_UI.add_thing(s_option_3)
    settings_UI.add_thing(s_option_4)
    settings_UI.add_thing(s_option_5)
    settings_UI.add_thing(s_option_6)
    settings_UI.add_thing(s_option_7)

    # 设置结束UI
    end_UI = gui.GUI(screen,*bg_size)
    if conf.record and not conf.demo:
        e_label_1 = gui.components.Label(screen,'game.label.source.best.text',conf.language,24,('center',0,280),screen,color=config.COLOR['WHITE'])
        e_label_2 = gui.components.Label(screen,'0',conf.language,36,('center_obj',0,-30),father_obj=e_label_1,color=config.COLOR['WHITE'])
        e_label_3 = gui.components.Label(screen,'game.label.source.your.text',conf.language,48,('center_obj',0,-80),father_obj=e_label_2,color=config.COLOR['WHITE'])
        e_label_4 = gui.components.Label(screen,'0',conf.language,60,('center_obj',0,-70),father_obj=e_label_3,color=config.COLOR['WHITE'])
        e_button_1 = gui.components.UIButton(screen,'game.button.again.text',conf.language,eventBus,{**locals(),**globals()},_again,_over,('center_obj',0,-230),father_obj=e_label_2,pause=paused,asset_path=conf.assets_path,conf_name=conf.config_name)
        e_button_2 = gui.components.UIButton(screen,'game.button.exit.text',conf.language,eventBus,{**locals(),**globals()},_main,_over,('center_obj',0,-50),father_obj=e_button_1,life=life_num,asset_path=conf.assets_path,conf_name=conf.config_name)
        end_UI.add_label(e_label_1)
        end_UI.add_label(e_label_2)
        end_UI.add_label(e_label_3)
        end_UI.add_label(e_label_4)
        end_UI.add_button(e_button_1)
        end_UI.add_button(e_button_2)
    else:
        e_label_1 = gui.components.Label(screen,'game.label.source.best.text',conf.language,24,('center',0,280),screen,color=config.COLOR['WHITE'])
        e_label_2 = gui.components.Label(screen,'0',conf.language,36,('center_obj',0,-30),father_obj=e_label_1,color=config.COLOR['WHITE'])
        e_label_3 = gui.components.Label(screen,'game.label.source.your.text',conf.language,48,('center',0,280),screen,color=config.COLOR['WHITE'])
        e_label_4 = gui.components.Label(screen,'0',conf.language,60,('center_obj',0,-70),father_obj=e_label_3,color=config.COLOR['WHITE'])
        e_button_1 = gui.components.UIButton(screen,'game.button.again.text',conf.language,eventBus,{**locals(),**globals()},_again,_over,('center_obj',0,-400),father_obj=e_label_3,pause=paused,asset_path=conf.assets_path,conf_name=conf.config_name)
        e_button_2 = gui.components.UIButton(screen,'game.button.exit.text',conf.language,eventBus,{**locals(),**globals()},_main,_over,('center_obj',0,-50),father_obj=e_button_1,life=life_num,asset_path=conf.assets_path,conf_name=conf.config_name)
        end_UI.add_label(e_label_3)
        end_UI.add_label(e_label_4)
        end_UI.add_button(e_button_1)
        end_UI.add_button(e_button_2)
    
    #设置关于UI
    about_UI = gui.GUI(screen,*bg_size)
    a_label_1 = gui.components.Label(screen,conf.language.get('game.label.about.version.text',conf._lang)+conf.app_info['version'],conf.language,60,('center',0,0),screen,color=config.COLOR['WHITE'])
    a_button_1 = gui.components.UIButton(screen,'game.button.about.know.text',conf.language,eventBus,{**locals(),**globals()},configPageClose,_over,('center',0,-100),screen,asset_path=conf.assets_path,argv={**locals()})
    about_UI.add_label(a_label_1)
    about_UI.add_button(a_button_1)

    # 用于切换图片
    switch_image = True

    # 用于延迟
    delay = 200
    delay_time = time.time()
    temp_time = time.time()
    start_time = time.time()
    if conf.settings['fps']:
        timer = pygame.time.Clock()

    running = True
    is_running = [not(s or set or paused[0])]

    eventBus.addEvent(plugin.event.InitEvent(screen,{**locals(),**globals()}))

    while running:
        is_running = [not(s or set or paused[0])]
        delay_time = time.time() - temp_time
        if delay_time > 0.01: delay_time = 0.01
        temp_time = time.time()
        screen.blit(background, (0, 0))
        bombEvent = plugin.event.BombEvent(screen, {**locals(),**globals()})
        for event in pygame.event.get():
            if event.type == QUIT:
                eventBus.addEvent(plugin.event.ExitEvent(screen,globals()))
            if is_running[0]:
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        eventBus.addEvent(bombEvent)
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and paused_rect.collidepoint(event.pos) and not paused[0]:
                        paused[0] = not paused[0]
                        if paused[0]:
                            supplyEvent.stop()
                            pygame.mixer.music.pause()
                            pygame.mixer.pause()
                        else:
                            pass

                elif event.type == MOUSEMOTION:
                    if paused_rect.collidepoint(event.pos):
                        if paused[0]:
                            paused_image = resume_pressed_image
                        else:
                            paused_image = pause_pressed_image
                    else:
                        if paused[0]:
                            paused_image = resume_nor_image
                        else:
                           paused_image = pause_nor_image

        # 根据用户的得分增加难度
        if not is_running[0]:
            pass
        elif level == 1 and score >= 5000:
            level = 2
            if conf.settings['mix']:upgrade_sound.play()
            # 增加3架小型敌机、2架中型敌机和1架大型敌机
            tool.add_small_enemies(small_enemies, enemies, 3, eventBus, {**locals(),**globals()})
            tool.add_mid_enemies(mid_enemies, enemies, 2, eventBus, {**locals(),**globals()})
            tool.add_big_enemies(big_enemies, enemies, 1, eventBus, {**locals(),**globals()})
            # 提升小型敌机的速度
            tool.inc_speed(small_enemies, 50)
            tool.inc_speed(mid_enemies, 50)
        elif level == 2 and score >= 10000:
            level = 3
            if conf.settings['mix']:upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            tool.add_small_enemies(small_enemies, enemies, 5, eventBus, {**locals(),**globals()})
            tool.add_mid_enemies(mid_enemies, enemies, 3, eventBus, {**locals(),**globals()})
            tool.add_big_enemies(big_enemies, enemies, 2, eventBus, {**locals(),**globals()})
            # 提升小型敌机的速度
            tool.inc_speed(small_enemies, 50)
            tool.inc_speed(mid_enemies, 50)
        elif level == 3 and score >= 50000:
            level = 4
            if conf.settings['mix']:upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            tool.add_small_enemies(small_enemies, enemies, 5, eventBus, {**locals(),**globals()})
            tool.add_mid_enemies(mid_enemies, enemies, 3, eventBus, {**locals(),**globals()})
            tool.add_big_enemies(big_enemies, enemies, 2, eventBus, {**locals(),**globals()})
            # 提升小型敌机的速度
            tool.inc_speed(small_enemies, 50)
            tool.inc_speed(mid_enemies, 50)
        elif level == 4 and score >= 100000:
            level = 5
            if conf.settings['mix']:upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            tool.add_small_enemies(small_enemies, enemies, 5, eventBus, {**locals(),**globals()})
            tool.add_mid_enemies(mid_enemies, enemies, 3, eventBus, {**locals(),**globals()})
            tool.add_big_enemies(big_enemies, enemies, 2, eventBus, {**locals(),**globals()})
            # 提升小型敌机的速度
            tool.inc_speed(small_enemies, 50)
            tool.inc_speed(mid_enemies, 50)
        elif level == 5 and score >= 500000:
            level = 6
            if conf.settings['mix']:upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            tool.add_small_enemies(small_enemies, enemies, 5, eventBus, {**locals(),**globals()})
            tool.add_mid_enemies(mid_enemies, enemies, 3, eventBus, {**locals(),**globals()})
            tool.add_big_enemies(big_enemies, enemies, 2, eventBus, {**locals(),**globals()})
            # 提升小型敌机的速度
            tool.inc_speed(small_enemies, 50)
            tool.inc_speed(mid_enemies, 50)
        elif level == 6 and score >= 1000000:
            level = 7
            if conf.settings['mix']:upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            tool.add_small_enemies(small_enemies, enemies, 5, eventBus, {**locals(),**globals()})
            tool.add_mid_enemies(mid_enemies, enemies, 3, eventBus, {**locals(),**globals()})
            tool.add_big_enemies(big_enemies, enemies, 2, eventBus, {**locals(),**globals()})
            # 提升小型敌机的速度
            tool.inc_speed(small_enemies, 50)
            tool.inc_speed(mid_enemies, 50)
        elif level == 7 and score >= 5000000:
            level = 8
            if conf.settings['mix']:upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            tool.add_small_enemies(small_enemies, enemies, 5, eventBus, {**locals(),**globals()})
            tool.add_mid_enemies(mid_enemies, enemies, 3, eventBus, {**locals(),**globals()})
            tool.add_big_enemies(big_enemies, enemies, 2, eventBus, {**locals(),**globals()})
            # 提升小型敌机的速度
            tool.inc_speed(small_enemies, 50)
            tool.inc_speed(mid_enemies, 50)
        elif level == 8 and score >= 10000000:
            level = 9
            if conf.settings['mix']:upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            tool.add_small_enemies(small_enemies, enemies, 5, eventBus, {**locals(),**globals()})
            tool.add_mid_enemies(mid_enemies, enemies, 3, eventBus, {**locals(),**globals()})
            tool.add_big_enemies(big_enemies, enemies, 2, eventBus, {**locals(),**globals()})
            # 提升小型敌机的速度
            tool.inc_speed(small_enemies, 50)
            tool.inc_speed(mid_enemies, 50)
        elif level == 9 and score >= 50000000:
            level = 10
            if conf.settings['mix']:upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            tool.add_small_enemies(small_enemies, enemies, 5, eventBus, {**locals(),**globals()})
            tool.add_mid_enemies(mid_enemies, enemies, 3, eventBus, {**locals(),**globals()})
            tool.add_big_enemies(big_enemies, enemies, 2, eventBus, {**locals(),**globals()})
            # 提升小型敌机的速度
            tool.inc_speed(small_enemies, 50)
            tool.inc_speed(mid_enemies, 50)
        elif level == 10 and score >=100000000:
            level = -1
            if conf.settings['mix']:upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机和2架大型敌机
            tool.add_small_enemies(small_enemies, enemies, 5, eventBus, {**locals(),**globals()})
            tool.add_mid_enemies(mid_enemies, enemies, 3, eventBus, {**locals(),**globals()})
            tool.add_big_enemies(big_enemies, enemies, 2, eventBus, {**locals(),**globals()})
            # 提升小型敌机的速度
            tool.inc_speed(small_enemies, 50)
            tool.inc_speed(mid_enemies, 50)
                
        if life_num[0] and is_running[0]:
            # 绘制暂停按钮
            screen.blit(paused_image, paused_rect)

            # 检测用户的键盘操作
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp(delay_time)
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown(delay_time)
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft(delay_time)
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight(delay_time)

            # 绘制全屏炸弹补给并检测是否获得
            if bomb_supply.active:
                bomb_supply.move(delay_time)
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    if conf.settings['mix']:get_bomb_sound.play()
                    if bomb_num[0] < 3:
                        bomb_num[0] += 1
                    bomb_supply.active = False

            # 绘制超级子弹补给并检测是否获得
            if bullet_supply.active:
                bullet_supply.move(delay_time)
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    if conf.settings['mix']:get_bullet_sound.play()
                    is_double_bullet[0] = True
                    doubleBulletEvent.start()
                    bullet_supply.active = False

            # 发射子弹
            if not(delay % 10):
                if conf.settings['mix']:bullet_sound.play()
                if is_double_bullet[0]:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx-33, me.rect.centery))
                    bullets[bullet2_index+1].reset((me.rect.centerx+30, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

                
            # 检测子弹是否击中敌机
            try:
                for b in bullets:
                    if b.active:
                        b.move(delay_time)
                        screen.blit(b.image, b.rect)
                        enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                        if enemy_hit:
                            b.active = False
                            for e in enemy_hit:
                                if e in mid_enemies or e in big_enemies:
                                    e.hit = True
                                    e.energy -= 1
                                    if e.energy == 0:
                                        e.active = False
                                else:
                                    e.active = False
            except:
                pass
            
            # 绘制大型敌机
            for each in big_enemies:
                if each.active:
                    each.move(delay_time)
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, config.COLOR['BLACK'], \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)
                    # 当生命大于20%显示绿色，否则显示红色
                    energy_remain = each.energy / plane.BigEnemyPlane.energy
                    if energy_remain > 0.2:
                        energy_color = config.COLOR['GREEN']
                    else:
                        energy_color = config.COLOR['RED']
                    pygame.draw.line(screen, energy_color, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, \
                                      each.rect.top - 5), 2)
                        
                    # 即将出现在画面中，播放音效
                    if each.rect.bottom == -50:
                        if conf.settings['mix']:
                            each.fly_sound.play(-1)
                else:
                    # 毁灭
                    if not(delay % 12):
                        if each.destroy_index == 0:
                            if conf.settings['mix']:
                                each.down_sound.play()
                        screen.blit(each.destroy_images[each.destroy_index], each.rect)
                        each.destroy_index = (each.destroy_index + 1) % 6
                        if each.destroy_index == 0:
                            if conf.settings['mix']:
                                each.fly_sound.stop()
                            score += 10000
                            each.reset()

            # 绘制中型敌机：
            for each in mid_enemies:
                if each.active:
                    each.move(delay_time)

                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, config.COLOR['BLACK'], \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)
                    # 当生命大于20%显示绿色，否则显示红色
                    energy_remain = each.energy / plane.MiddleEnemyPlane.energy
                    if energy_remain > 0.2:
                        energy_color = config.COLOR['GREEN']
                    else:
                        energy_color = config.COLOR['RED']
                    pygame.draw.line(screen, energy_color, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, \
                                      each.rect.top - 5), 2)
                else:
                    # 毁灭
                    if not(delay % 12):
                        if each.destroy_index == 0:
                            if conf.settings['mix']:
                                each.down_sound.play()
                        screen.blit(each.destroy_images[each.destroy_index], each.rect)
                        each.destroy_index = (each.destroy_index + 1) % 4
                        if each.destroy_index == 0:
                            score += 6000
                            each.reset()

            # 绘制小型敌机：
            for each in small_enemies:
                if each.active:
                    each.move(delay_time)
                    screen.blit(each.image, each.rect)
                else:
                    # 毁灭
                    if not(delay % 20):
                        if each.destroy_index == 0:
                            if conf.settings['mix']:
                                each.down_sound.play()
                        screen.blit(each.destroy_images[each.destroy_index], each.rect)
                        each.destroy_index = (each.destroy_index + 1) % 4
                        if each.destroy_index == 0:
                            score += 1000
                            each.reset()

            # 检测我方飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for e in enemies_down:
                    e.active = False
            
            # 绘制我方飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                # 毁灭
                if not(delay % 12):
                    if me_destroy_index == 0:
                        if conf.settings['mix']:me_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num[0] -= 1
                        me.reset()
                        noHitEvent.start()

            # 绘制全屏炸弹数量
            bomb_text = bomb_font.render("× %d" % bomb_num[0], True, config.COLOR['WHITE'])
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))

            # 绘制剩余生命数量
            if life_num[0]:
                for i in range(life_num[0]):
                    screen.blit(life_image, \
                                (width-10-(i+1)*life_rect.width, \
                                 height-10-life_rect.height))

            # 绘制得分
            score_text = score_font.render(str(score), True, config.COLOR['WHITE'])
            screen.blit(score_text, (width/2-(score_text.get_rect().width)/2, 5))

            if level==-1:
                level_text = level_font.render("Lv. MAX", True, config.COLOR['WHITE'])
            else:
                level_text = level_font.render("Lv."+str(level), True, config.COLOR['WHITE'])
            screen.blit(level_text, (10, 5))

        elif start_UI.is_open:
            if not recorded[0]:
                recorded[0] = True
                # 读取历史最高得分gameover_text
                record_score = conf.app_info['record']
            
            s_label_2.set_text(str(record_score))

            start_UI.draw()
            if conf.uicheck:
                start_UI.check()
        elif settings_UI.is_open:
            settings_UI.draw()
            if conf.uicheck:
                if settings_UI.check():
                    pygame.mixer.music.stop()
                    conf.reload()
                    if conf.app_info['settings']['language'] != conf.settings['language']:
                        conf.init()
                        return main(s=False,set=True)
                    elif conf.app_info['settings']['screen_width'] != conf.settings['screen_width']:
                        conf.init()
                        if conf.app_info['settings']['screen_width'] == 0:
                            conf.app_info['settings']['screen_height'] = 0
                        elif conf.app_info['settings']['screen_width'] == 1750:
                            conf.app_info['settings']['screen_height'] = 1200
                        elif conf.app_info['settings']['screen_width'] == 1400:
                            conf.app_info['settings']['screen_height'] = 960
                        elif conf.app_info['settings']['screen_width'] == 1050:
                            conf.app_info['settings']['screen_height'] = 720
                        conf.write(conf)
                        return True
                    else:
                        conf.init()
                        return main(s=False,set=True)
        
        elif life_num[0] and paused[0]:
            # 绘制全屏炸弹补给并检测是否获得
            if bomb_supply.active:
                screen.blit(bomb_supply.image, bomb_supply.rect)

            # 绘制超级子弹补给并检测是否获得
            if bullet_supply.active:
                screen.blit(bullet_supply.image, bullet_supply.rect)
                
            # 检测子弹是否击中敌机
            try:
                for b in bullets:
                    if b.active:
                        screen.blit(b.image, b.rect)
            except:
                pass
            
            # 绘制大型敌机
            for each in big_enemies:
                if each.active:
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, config.COLOR['BLACK'], \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)
                    # 当生命大于20%显示绿色，否则显示红色
                    energy_remain = each.energy / plane.BigEnemyPlane.energy
                    if energy_remain > 0.2:
                        energy_color = config.COLOR['GREEN']
                    else:
                        energy_color = config.COLOR['RED']
                    pygame.draw.line(screen, energy_color, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, \
                                      each.rect.top - 5), 2)
                else:
                    # 毁灭
                    if not(delay % 12):
                        screen.blit(each.destroy_images[each.destroy_index], each.rect)

            # 绘制中型敌机：
            for each in mid_enemies:
                if each.active:
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                    else:
                        screen.blit(each.image, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, config.COLOR['BLACK'], \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)
                    # 当生命大于20%显示绿色，否则显示红色
                    energy_remain = each.energy / plane.MiddleEnemyPlane.energy
                    if energy_remain > 0.2:
                        energy_color = config.COLOR['GREEN']
                    else:
                        energy_color = config.COLOR['RED']
                    pygame.draw.line(screen, energy_color, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, \
                                      each.rect.top - 5), 2)
                else:
                    # 毁灭
                    if not(delay % 12):
                        screen.blit(each.destroy_images[each.destroy_index], each.rect)

            # 绘制小型敌机：
            for each in small_enemies:
                if each.active:
                    screen.blit(each.image, each.rect)
                else:
                    # 毁灭
                    if not(delay % 12):
                        screen.blit(each.destroy_images[each.destroy_index], each.rect)
            
            # 绘制我方飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                # 毁灭
                if not(delay % 12):
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))

            # 绘制剩余生命数量
            if life_num[0]:
                for i in range(life_num[0]):
                    screen.blit(life_image, \
                                (width-10-(i+1)*life_rect.width, \
                                 height-10-life_rect.height))
            
            if level==-1:
                level_text = level_font.render("Lv. MAX", True, config.COLOR['WHITE'])
            else:
                level_text = level_font.render("Lv."+str(level), True, config.COLOR['WHITE'])
            screen.blit(level_text, (10, 5))
            # 背景音乐停止
            pygame.mixer.music.pause()

            # 停止发放补给
            supplyEvent.stop()

            p_label_2.set_text(str(score))

            pause_UI.draw()
            if conf.uicheck:
                pause_UI.check()

        # 绘制游戏结束画面
        elif life_num[0] == 0:
            # 停止发放补给
            supplyEvent.stop()

            if not recorded[0]:
                if conf.settings['music']:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    empty.load_music(conf.assets_path + "sound/gui_music.ogg", eventBus, {**locals(), **globals()})
                    pygame.mixer.music.play(-1)
                if conf.settings['mix']:fail_sound.play()
                # 读取历史最高得分
                if conf.record and not conf.demo:
                    record_score = conf.app_info['record']
                else:
                    record_score = 0

                # 如果玩家得分高于历史最高得分，则存档
                if score > record_score and not conf.demo:
                    conf.app_info['record'] = score
                    conf.write(conf)
                    record_score = score

            e_label_2.set_text(str(record_score))
            e_label_4.set_text(str(score))
            recorded[0] = True
            
            end_UI.draw()
            if conf.uicheck:
                end_UI.check()
        elif about_UI.is_open:
            about_UI.draw()
            about_UI.check()
            
        # 切换图片
        if not(delay % 10):
            switch_image = not switch_image
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= 0.001 and not conf.settings['fps']:
            delay -= 0.5
            start_time = current_time
        
        elif conf.settings['fps']:
            timer.tick(conf.settings['fps'])
            delay -= (200-conf.settings['fps'])//5

        eventBus.addEvent(plugin.event.Event())
        pygame.display.flip()
        
if __name__ == "__main__":
    try:
        while True:
            if main():
                eventBus.addEvent(plugin.event.ReloadEvent())
    except SystemExit:
        pass
