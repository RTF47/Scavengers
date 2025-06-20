"""НЕКОТОРЫЕ НАСТРОЙКИ/ПЕРЕМЕННЫЕ, ЧТОБЫ ИЗБЕЖАТЬ MAGIC_CONST"""
#Параметры игры
WIDTH = 1280
HEIGHT = 720
FPS = 60
FPS_PAUSE = 10

#Параметры анимации
FRAME_SPEED = 0.15 #Скорость переключения кадров анимации
FRAME_IND = 0 #Начальный индекс кадров

#Параметры игрока
HEALTH = 6 #ХП
POWER = 10 #Атака
P_SPEED = 6 #Скорость ходьбы

#Параметры руны
RUNE_RADIUS = 100 #Радиус притягивания руны
RUNE_SPEED = 3 #Скорость притягивания руны

#POSITIONS
PROMPT_POS = (100, 100)
NAME_SURF_POS = (100, 150) #Позиция поля для ввода имени
WARN_POS = (100, 200) #Позиция предупреждения на экране
TIMER_POS = (WIDTH - 150, 10) #Позиция таймера на экране
WEAPON_POS = (10, 630) #Позиция UI оружия на экране
HEART_POS = (10,15) #Позиция сердечек на экране
RUNE_UI_POS = (200, 10) #Позиция UI Руны на экране
CHEST_POS = (1216, 1792) #Позиция сундука на карте
OVERLAY_POS = (0,0) #Позиция оверлея, то есть самое начало
DEATH_POS = (WIDTH // 3 + 55, HEIGHT // 2 - 110)
LEADERBOARD_POS = (800,340) #Позиция лидерборда в меню
FINISH_POS = (1280, 640) #Позиция финиша

#SIZES
BUTTON_SIZE = (250, 64) #Размер кнопок
HEART_SIZE = (25,24) #Размер сердечек
CHEST_SIZE = (128,128) #Размер сундука
FINISH_SIZE = 128 #Размер квадратной зоны финиша
TILE_SIZE = 64 #Размер тайла игры
ITEM_BOX_SIZE = 80 #Размер UI бокса с оружием
SBOX_WIDTH = 3 #Ширина обводки UI бокса
FONT_SIZE = 120 #Размер титульного шрифта
SMALL_FONT_SIZE = 30 #Размер основного шрифта
UI_FONT_SIZE = 18 #Размер шрифта UI

#OFFSETS
Y_OFFSET = 30 #Смещение по Y для кнопки play
OFFSETXY = 130 #Смещение по X и Y для кнопки play и quit
RMX_OFFSET = 35 #Смещение по X для кнопки resume и menu
MY_OFFSET = 100 #Смещение по Y для кнопки menu
LB_OFFSET = 60 #Смещение по Y для Toп5 после You:
TOP_OFFSET = 50 #Смещение по Y для You: после Best Time
TITLE_OFFSET = 120 #Смещение названия игры относительно y
HEART_GAP = 5 #Смещение каждого сердечка на промежуток

#CSV ids
NOTHING_ID = '-1' #Буквально - айди ничего
PLAYER_ID = '394' #Айди игрока
BAMBOO_ID = '390' #Айди врага бамбук
RACCOON_ID = '392' #Айди врага енот
SPIRIT_ID = '391' #Айди врага дух

#Все пути, графика, карта
CLAW_F = '../graphics/particles/claw' #кадры атаки енота
SLASH_F = '../graphics/particles/slash' #кадры атаки игрока
SPARKLE_F = '../graphics/particles/sparkle' #кадры атаки сквида
LEAF_F = '../graphics/particles/leaf_attack'  #кадры атаки бамбука
THUNDER_F = '../graphics/particles/thunder' #кадры атаки духа
SQUID_D = '../graphics/particles/smoke_orange' #Графика сквида
RACCOON_D = '../graphics/particles/raccoon' #Графика енота
SPIRIT_D = '../graphics/particles/nova' #Графика духа
BAMBOO_D = '../graphics/particles/bamboo' #Графика бамбука
BOUNDARY_CSV = '../map/map_Boundary.csv' #Карта границ
ENTITY_CSV = '../map/map_Entitys.csv' #Карта энтити
PLAY_B = '../graphics/buttons/Play.png' #Кнопка play
MENU_B = '../graphics/buttons/Menu.png' #Кнопка menu
QUIT_B = '../graphics/buttons/Quit.png' #Кнопка quit
RESUME_B ='../graphics/buttons/Resume.png' #Кнопка resume
REPLAY_B = '../graphics/buttons/Replay.png' #Кнопка replay
F_HEART = "../graphics/HP/OneHeart.png" #full - полный, полное сердечко
E_HEART = "../graphics/HP/VoidHeart.png" #empty - пустой, пустое сердечко
RUNE_PATH = '../graphics/runes/1-32x32.png' #Обычная руна
E_RUNE_PATH = "../graphics/runes/dark1-32x32.png" #empty - пустой, пустая руна
MAP = '../graphics/tilemap/Map3.png' #Карта, по которой ходит игрок
LOGO_PATH = '../graphics/runes/6-32x32.png' #Логотип игры
PLAYER_IMG = '../graphics/player/down_idle/idle_down.png' #Картинка игрока
PLAYER_PATH = '../graphics/player/' #Папка со всеми взаимодействиями игрока
CHEST_FOLDER = '../graphics/chest' #Папка с кажрами сундука

#Все пути, звуки. Приписка _S означает sound
MAIN_S = '../audio/main.ogg' #музыка
WIN_S = '../audio/win.wav' #звук победы
GO_S = '../audio/death.wav' #звук проигрыша
DEATH_S = '../audio/death.wav' #звук смерти
HIT_S = '../audio/hit.wav' #звук попадания
SWORD_S = '../audio/sword.wav' #звук удара
CHEST_OPEN_S = '../audio/chest.mp3' #звук открытия сундука

#Все пути, шрифты.
SMALL_FONT_PATH = '../graphics/font/joystix.ttf' #Основной шрифт
FONT_PATH = '../graphics/font/alagard-12px-unicode.ttf' #Титульный шрифт
UI_FONT = SMALL_FONT_PATH #UI шрифт

#Громкости звуков и каналы. Приписка _V значает volume
CHANNELS = 16 #количество каналов, чтобы все звуки проигрывались
MAIN_V = 0.05
WIN_V = 0.2
GO_V = 0.4
GO_CHANNEL = 7 #Закрепляем за звуком проигрыша свой канал, иначе не работает
ENEMY_V = 0.1 #Общая громкость врага
SWORD_V = 0.2
CHEST_OPEN_V = 0.2

#Цвета
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
UI_BORDER_COLOR_ACTIVE = 'gold'
WHITE = (255,255,255)
YELLOW = (255,255,0)
RED = (255,0,0)
OVERLAY_FILL = (50,50,50)

#Всё, что связано с боем
ATTACK_CD = 400 #Время, еоторое проходит до следующей атаки
INVICIBILITY_DUR = 300 #время, которое проходит, после удара игрока
INVULN_CD = 500 #время, которое проходит, после удара врага
CHANGE_CD = 200 #Время, которое проходит до еще одной смены оружия


#Цельные характеристики
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'../graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30,'graphic':'../graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'../graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'../graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic':'../graphics/weapons/sai/full.png'}}

monster_data = {
	'squid': {'health': 100,'exp':100,'damage':1,'attack_type': 'slash', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 300,'exp':250,'damage':3,'attack_type': 'claw',  'attack_sound':'../audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 100,'exp':110,'damage':1,'attack_type': 'thunder', 'attack_sound':'../audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 70,'exp':120,'damage':1,'attack_type': 'leaf_attack', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}
