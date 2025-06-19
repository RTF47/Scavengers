"""НЕКОТОРЫЕ НАСТРОЙКИ/ПЕРЕМЕННЫЕ, ЧТОБЫ ИЗБЕЖАТЬ MAGIC_CONST"""

WIDTH = 1280
HEIGHT = 720
FPS = 60
FPS_PAUSE = 10
TILE_SIZE = 64
ITEM_BOX_SIZE = 80
FRAME_SPEED = 0.15
FRAME_IND = 0
MAP = '../graphics/tilemap/Map3.png'
LOGO_PATH = '../graphics/runes/6-32x32.png'

PLAYER_IMG = '../graphics/player/down_idle/idle_down.png'
PLAYER_PATH = '../graphics/player/'
HEALTH = 6
POWER = 10
P_SPEED = 6

TITLE_OFFSET = 120

FINISH_POS = (1280, 640)
FINISH_SIZE = 128

OVERLAY_POS = (0,0)

DEATH_POS = (WIDTH // 3 + 55, HEIGHT // 2 - 110)

FONT_PATH = '../graphics/font/alagard-12px-unicode.ttf'
FONT_SIZE = 120
SMALL_FONT_PATH = '../graphics/font/joystix.ttf'
SMALL_FONT_SIZE = 30
UI_FONT = SMALL_FONT_PATH
UI_FONT_SIZE = 18

LEADERBOARD_POS = (800,340)

CHEST_SIZE = (128,128)
CHEST_FOLDER = '../graphics/chest'
CHEST_POS = (1216, 1792)
CHEST_OPEN_S = '../audio/chest.mp3'
CHEST_OPEN_V = 0.2

RUNE_PATH = '../graphics/runes/1-32x32.png'
E_RUNE_PATH = "../graphics/runes/dark1-32x32.png"
RUNE_RADIUS = 100
RUNE_SPEED = 3
RUNE_UI_POS = (200, 10)

F_HEART = "../graphics/HP/OneHeart.png"
E_HEART = "../graphics/HP/VoidHeart.png"
HEART_SIZE = (25,24)
HEART_POS = (10,15)
HEART_GAP = 5

SBOX_WIDTH = 3
WEAPON_POS = (10, 630)

ATTACK_CD = 400
INVICIBILITY_DUR = 300
INVULN_CD = 500
CHANGE_CD = 200

LB_OFFSET = 60
TOP_OFFSET = 50

TIMER_POS = (WIDTH - 150, 10)
RMX_OFFSET = 35
MY_OFFSET = 100

PROMPT_POS = (100, 100)
NAME_SURF_POS = (100, 150)
WARN_POS = (100, 200)

OVERLAY_FILL = (50,50,50)

OFFSETXY = 130
BUTTON_SIZE = (250, 64)
Y_OFFSET = 30

WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
UI_BORDER_COLOR_ACTIVE = 'gold'
WHITE = (255,255,255)
YELLOW = (255,255,0)
RED = (255,0,0)

CHANNELS = 16
MAIN_S = '../audio/main.ogg'
MAIN_V = 0.05
WIN_S = '../audio/win.wav'
WIN_V = 0.2
GO_S = '../audio/death.wav'
GO_V = 0.4
GO_CHANNEL = 7
DEATH_S = '../audio/death.wav'
HIT_S = '../audio/hit.wav'
ENEMY_V = 0.1
SWORD_S = '../audio/sword.wav'
SWORD_V = 0.2

PLAY_B = '../graphics/buttons/Play.png'
MENU_B = '../graphics/buttons/Menu.png'
QUIT_B = '../graphics/buttons/Quit.png'
RESUME_B ='../graphics/buttons/Resume.png'
REPLAY_B = '../graphics/buttons/Replay.png'

BOUNDARY_CSV = '../map/map_Boundary.csv'
ENTITY_CSV = '../map/map_Entitys.csv'
NOTHING_ID = '-1'
PLAYER_ID = '394'
BAMBOO_ID = '390'
RACCOON_ID = '392'
SPIRIT_ID = '391'

CLAW_F = '../graphics/particles/claw'
SLASH_F = '../graphics/particles/slash'
SPARKLE_F = '../graphics/particles/sparkle'
LEAF_F = '../graphics/particles/leaf_attack'
THENDER_F = '../graphics/particles/thunder'
SQUID_D = '../graphics/particles/smoke_orange'
RACCOON_D = '../graphics/particles/raccoon'
SPIRIT_D = '../graphics/particles/nova'
BAMBOO_D = '../graphics/particles/bamboo'

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