#!/usr/bin/env python3
import pygame, sys, json, os

from settings import *
from level import Level
from timer import Timer
from leaderboard2 import Leaderboard


class Game:
    def __init__(self, state_status = 'reg'):
        """Класс, определяющий всю игру и состояния
        Args:
            state_status (reg): Начальное состояние при запуске игры.
        """
        pygame.init()
        pygame.display.set_caption("SCAVENGERS")
        logo = pygame.image.load(LOGO_PATH)
        pygame.display.set_icon(logo)

        # Устанавливаем статус или же сценарий для простой стейт машины
        self.state_status = state_status
        # Проверка, зарегистрировался ли пользователь, если да - то сразу пустить в меню
        if os.path.exists('leaderboard.json'):
            self.state_status = 'menu'

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = None
        self.finish_zone = pygame.Rect(FINISH_POS[0], FINISH_POS[1], FINISH_SIZE, FINISH_SIZE) #Зона завершения уровня

        # Переменные для регистрации пользователей
        self.username = None #Имя игрока
        self.name_taken = False #Занято ли имя
        self.input_name = '' #Имя, которое игрок вводит в момент регистарции
        self.name_active = True #Написано ли имя в поле регистрации

        # Шрифты
        font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.font_small = pygame.font.Font(SMALL_FONT_PATH, SMALL_FONT_SIZE)

        # Определяем центральную точку нашего экрана
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 2

        # Добавляем таймер
        self.timer = Timer()

        # Добавляем лидерборд для отображения лучшего времени прохождения
        self.leaderboard = Leaderboard()

        # Звуки
        pygame.mixer.init(channels=CHANNELS)
        self.game_over_channel = pygame.mixer.Channel(GO_CHANNEL)
        self.main_sound = pygame.mixer.Sound(MAIN_S)
        self.main_sound.set_volume(MAIN_V)
        self.main_sound.play(loops=-1)
        self.win_sound = pygame.mixer.Sound(WIN_S)
        self.win_sound.set_volume(WIN_V)
        self.game_over_sound = pygame.mixer.Sound(GO_S)
        self.game_over_sound.set_volume(GO_V)

        # Кнопки и их картинки
        self.title_text = font.render("SCAVENGERS", True, WHITE)
        self.title_rect = self.title_text.get_rect(center=(self.center_x, self.center_y - TITLE_OFFSET))
        self.play_image   = pygame.image.load(PLAY_B).convert_alpha()
        self.quit_image   = pygame.image.load(QUIT_B).convert_alpha()
        self.resume_image = pygame.image.load(RESUME_B).convert_alpha()
        self.replay_image = pygame.image.load(REPLAY_B).convert_alpha()
        self.menu_image   = pygame.image.load(MENU_B).convert_alpha()
        self.play_rect    = self.play_image.get_rect()
        self.quit_rect    = self.quit_image.get_rect()
        self.resume_rect  = self.resume_image.get_rect()
        self.replay_rect  = self.replay_image.get_rect()
        self.menu_rect    = self.menu_image.get_rect()


    def run(self):
        """Здесь происходит обработка смен состояний, а также запуск всех процессов."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()



                # Общая проверка ESC для паузы
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.state_status == 'play':
                        self.timer.pause()           # ставим таймер на паузу
                        self.state_status = 'pause'

                # Обработка событий для состояния регистрации
                if self.state_status == 'reg':
                    self.handle_reg_events(event)
                # Обработка событий для состояния меню
                elif self.state_status == 'menu':
                    self.handle_menu_events(event)
                # Обработка событий для состояния окончания игры (проигрыш/победа)
                elif self.state_status in ('game_over', 'win'):
                    self.handle_game_over_events(event)

            # Отрисовка / логика для каждого из состояний (уже после обработки событий)
            if self.state_status == 'reg':
                self.reg_st()
            elif self.state_status == 'menu':
                self.draw_menu()
            elif self.state_status == 'play':
                self.play_st()
                if self.level and self.level.player.health <= 0:
                    self.state_status = 'game_over'
            elif self.state_status == 'pause':
                self.pause_st()
            elif self.state_status == 'game_over':
                self.game_over_st()
            elif self.state_status == 'win':
                self.win_st()

            pygame.display.flip()
            self.clock.tick(FPS)


    def handle_reg_events(self, event):
        """Обработка событий регистрации
        Args:
            event: Событие в игре.
        """
        if event.type == pygame.KEYDOWN and self.name_active:
            if event.key == pygame.K_RETURN and self.input_name.strip():
                self.username = self.input_name.strip()

                # Сначала проверяем соединение и уникальность
                if self.leaderboard.check_connection():
                    if self.leaderboard.check_unique_name(self.username):
                        # Имя занято — поднимаем флаг и сразу выходим (не пишем JSON и не идём в меню)
                        self.name_taken = True
                        return
                    else:
                        self.name_taken = False
                        # Сохраняем в БД
                        self.leaderboard.save_score(self.username, 0)

                # Если соединения нет — всё равно сохраняем локальный JSON
                # Только здесь, когда имя прошло проверку
                filename = "leaderboard.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump({"username": self.username, "time": 0},
                              f, ensure_ascii=False, indent=2)

                # Всё успешно — переходим в меню
                self.state_status = 'menu'

            elif event.key == pygame.K_BACKSPACE:
                self.input_name = self.input_name[:-1]
                self.name_taken = False  # сбрасываем предупреждение при любом изменении
            else:
                if len(self.input_name) < 12:
                    self.input_name += event.unicode
                    self.name_taken = False  # сбрасываем предупреждение


    def reg_st(self):
        """Отрисовка регистрации"""
        self.screen.fill((30, 30, 30))
        prompt = self.font_small.render("Введите имя:", True, WHITE)
        name_surf = self.font_small.render(self.input_name, True, YELLOW)
        self.screen.blit(prompt, PROMPT_POS)
        self.screen.blit(name_surf, NAME_SURF_POS)

        if self.name_taken:
            warn = self.font_small.render("Имя уже занято. Введите другое.", True, RED)
            self.screen.blit(warn, WARN_POS)


    def handle_menu_events(self, event):
        """Обработка событий и логики для меню
        Args:
            event: Событие в игре.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.play_rect.collidepoint(mouse_pos):
                # запускаем уровень и таймер
                self.level = self.create_level()
                self.timer = Timer()
                self.timer.start()
                self.state_status = 'play'
            elif self.quit_rect.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()


    def draw_menu(self):
        """Рисуем меню и его элементы"""
        self.screen.fill(OVERLAY_FILL)
        self.screen.blit(self.title_text, self.title_rect)
        self.play_image = pygame.transform.scale(self.play_image, BUTTON_SIZE)
        self.play_rect.center = (self.center_x -OFFSETXY, self.center_y + Y_OFFSET)
        self.screen.blit(self.play_image, self.play_rect)
        self.quit_image = pygame.transform.scale(self.quit_image, BUTTON_SIZE)
        self.quit_rect.center = (self.center_x -OFFSETXY, self.center_y + OFFSETXY)
        self.screen.blit(self.quit_image, self.quit_rect)

        #Leaderboard
        y = LEADERBOARD_POS[1]

        #Заголовок
        self.screen.blit(self.font_small.render("Best Time:", True, WHITE),
                         (LEADERBOARD_POS[0]-OFFSETXY, y))
        y += TOP_OFFSET

        #Свое время из JSON
        try:
            with open("leaderboard.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                user_ms = data.get("time", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            user_ms = 0

        sec = user_ms // 1000
        cs = (user_ms % 1000) // 10
        you_str = f"You: {sec:02d}.{cs:02d}" if user_ms > 0 else "You: --.--"
        self.screen.blit(self.font_small.render(you_str, True, WHITE),
                         (LEADERBOARD_POS[0]-OFFSETXY, y))
        y += LB_OFFSET

        #Топ‑5 из БД или прочерк
        if self.leaderboard.check_connection():
            if self.leaderboard.get_user_time(data['username']) > data['time']:
                self.leaderboard.update_score(data['username'], data['time'])
            top5 = self.leaderboard.get_top_scores()
            num = 1
            for name, t in top5:
                sec = t // 1000
                cs = (t % 1000) // 10
                line = f"{num}. {name} {sec:02d}.{cs:02d}"
                self.screen.blit(self.font_small.render(line, True, WHITE),
                                 (LEADERBOARD_POS[0]-OFFSETXY, y))
                y += TOP_OFFSET
                num+=1
        else:
            dash = self.font_small.render("——*——", True, WHITE)
            self.screen.blit(dash, (LEADERBOARD_POS[0], y))


    def create_level(self):
        """Создание таймера и старт уровня С САМОГО НАЧАЛА"""
        self.timer = Timer()
        self.timer.start()
        return Level()


    def play_st(self):
        """Запуск уровня (обычно после паузы) + Вывод таймера сверху справа + проверка победы"""
        self.screen.fill(WATER_COLOR)
        if self.level:
            self.level.run()

        # отрисовка таймера в play
        elapsed_ms = self.timer.get_elapsed()
        seconds = elapsed_ms // 1000
        millis = (elapsed_ms % 1000) // 10
        time_surf = self.font_small.render(f"{seconds:02d}.{millis:02d}", True, WHITE)
        self.screen.blit(time_surf, TIMER_POS)

        # проверка победы
        if self.finish_zone.colliderect(self.level.player.rect) and self.level.player.has_rune:
            self.win_sound.play()
            self.state_status = 'win'


    def pause_st(self):
        """Собственная обработка событий для паузы (для корректной работы) + Отрисовка паузы"""
        keys = pygame.key.get_pressed()
        # сохраняем экран и фон
        saved = self.screen.copy()
        while self.state_status == 'pause':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.resume_rect.collidepoint(event.pos):
                        self.timer.start()    # возобновляем таймер
                        self.state_status = 'play'
                    elif self.menu_rect.collidepoint(event.pos):
                        self.state_status = 'menu'
                elif keys[pygame.K_ESCAPE] and event.type == pygame.KEYDOWN:
                    self.timer.start()  # возобновляем таймер
                    self.state_status = 'play'

            self.screen.blit(saved, OVERLAY_POS)
            self.overlay()
            self.resume_image = pygame.transform.scale(self.resume_image, BUTTON_SIZE)
            self.resume_rect.center = (self.center_x + RMX_OFFSET, self.center_y)
            self.screen.blit(self.resume_image, self.resume_rect)
            self.menu_image = pygame.transform.scale(self.menu_image, BUTTON_SIZE)
            self.menu_rect.center = (self.center_x + RMX_OFFSET, self.center_y + MY_OFFSET)
            self.screen.blit(self.menu_image, self.menu_rect)
            pygame.display.flip()
            self.clock.tick(FPS_PAUSE)


    def overlay(self):
        """Затемнение для паузы, проигрыша и победы"""
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0,0,0,150))
        self.screen.blit(overlay, OVERLAY_POS)


    def win_st(self):
        """Отрисовка победы и запись времени для лидерборда"""
        if self.level:
            self.level.run(draw_only=True)

        # остановка таймера и сохранение результата
        elapsed = self.timer.stop()
        filename = "leaderboard.json"
        with open(filename, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            if data['time'] == 0:
                data['time'] = elapsed
                if self.leaderboard.check_connection():
                    self.leaderboard.update_score(data['username'], elapsed)
            elif elapsed < data['time']:
                data['time'] = elapsed
                if self.leaderboard.check_connection():
                    self.leaderboard.update_score(data['username'], elapsed)
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.truncate()

        # отрисовка окна победы
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, OVERLAY_POS)
        # ваши кнопки и текст
        text_surf = self.font_small.render("Mission completed!", True, (255, 255, 255))
        self.screen.blit(text_surf, (WIDTH // 3, HEIGHT // 2 - 150))
        # показать итоговое время
        sec = elapsed // 1000
        ms  = (elapsed % 1000) // 10
        time_surf = self.font_small.render(f"Time: {sec:02d}.{ms:02d}", True, (255, 255, 0))
        self.screen.blit(time_surf, (WIDTH // 3, HEIGHT // 2 - 100))

        # кнопки Replay / Menu
        self.replay_image = pygame.transform.scale(self.replay_image, (250, 64))
        self.replay_rect.center = (self.center_x + 35, self.center_y)
        self.screen.blit(self.replay_image, self.replay_rect)
        self.menu_image = pygame.transform.scale(self.menu_image, (250, 64))
        self.menu_rect.center = (self.center_x + 35, self.center_y + 100)
        self.screen.blit(self.menu_image, self.menu_rect)


    def handle_game_over_events(self, event):
        """Обработка событий для проигрыша/победы
        Args:
            event: Событие в игре.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.replay_rect.collidepoint(mouse_pos):
                # ПЕРЕЗАГРУЗКА: создаём заново LEVEL и переходим в состояние игры
                self.timer = Timer()  # Создаем новый таймер
                self.timer.start()
                self.level = self.create_level()
                self.state_status = 'play'
            elif self.menu_rect.collidepoint(mouse_pos):
                # Выходим в основное меню
                self.state_status = 'menu'


    def game_over_st(self):
        """Отрисовка проигрыша"""
        if self.level:
            self.level.run(draw_only=True)

        self.overlay()

        text_surface = self.font_small.render(
            """You're dead :(""",
            True, WHITE
        )
        self.screen.blit(text_surface, DEATH_POS)

        self.replay_image = pygame.transform.scale(self.replay_image, BUTTON_SIZE)
        self.replay_rect.center = (self.center_x + RMX_OFFSET, self.center_y)
        self.screen.blit(self.replay_image, self.replay_rect)

        self.menu_image = pygame.transform.scale(self.menu_image, BUTTON_SIZE)
        self.menu_rect.center = (self.center_x + RMX_OFFSET, self.center_y + MY_OFFSET)
        self.screen.blit(self.menu_image, self.menu_rect)


if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()