#!/usr/bin/env python3
import pygame, sys, json, os
from settings import *
from level import Level
from timer import Timer                 # добавили импорт таймера
from leaderboard import Leaderboard


class Game:
    def __init__(self, state_status = 'reg'):  # по умолчанию — режим регистрации
        pygame.init()
        pygame.display.set_caption("SCAVENGERS")
        logo = pygame.image.load('../graphics/runes/6-32x32.png')
        pygame.display.set_icon(logo)
        self.state_status = state_status
        if os.path.exists('leaderboard.json'):
            self.state_status = 'menu'

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = None
        self.finish_zone = pygame.Rect(1280, 640, 128, 128)

        # ——— НОВЫЕ ПОЛЯ ДЛЯ РЕГИСТРАЦИИ ———
        self.username = None
        self.name_taken = False
        self.input_name = ''
        self.name_active = True

        # Шрифты
        font = pygame.font.Font('../graphics/font/alagard-12px-unicode.ttf', 120)
        self.font_small = pygame.font.Font('../graphics/font/joystix.ttf', 30)
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 2

        # ——— НОВЫЙ ТАЙМЕР ———
        self.timer = Timer()

        # ——— ЛИДЕРБОРД ———
        self.leaderboard = Leaderboard()
        # позиции для leaderboard
        self.lb_x = 800
        self.lb_y = 300
        self.lb_width = 300
        self.lb_line_h = self.font_small.get_linesize()

        # Звуки
        pygame.mixer.init(channels=16)
        self.game_over_channel = pygame.mixer.Channel(7)
        self.main_sound = pygame.mixer.Sound('../audio/main.ogg')
        self.main_sound.set_volume(0.05)
        self.main_sound.play(loops=-1)
        self.win_sound = pygame.mixer.Sound('../audio/win.wav')
        self.win_sound.set_volume(0.2)
        self.game_over_sound = pygame.mixer.Sound('../audio/death.wav')
        self.game_over_sound.set_volume(0.4)

        # Кнопки и картинки
        self.title_text = font.render("SCAVENGERS", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(self.center_x, self.center_y - 120))
        self.play_image   = pygame.image.load('../graphics/buttons/Play.png').convert_alpha()
        self.quit_image   = pygame.image.load('../graphics/buttons/Quit.png').convert_alpha()
        self.resume_image = pygame.image.load('../graphics/buttons/Resume.png').convert_alpha()
        self.replay_image = pygame.image.load('../graphics/buttons/Replay.png').convert_alpha()
        self.menu_image   = pygame.image.load('../graphics/buttons/Menu.png').convert_alpha()
        self.play_rect    = self.play_image.get_rect()
        self.quit_rect    = self.quit_image.get_rect()
        self.resume_rect  = self.resume_image.get_rect()
        self.replay_rect  = self.replay_image.get_rect()
        self.menu_rect    = self.menu_image.get_rect()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Регистрация
                if self.state_status == 'reg':
                    self.handle_reg_events(event)
                # Общая проверка ESC для паузы (как было)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.state_status == 'play':
                        self.timer.pause()           # ставим таймер на паузу
                        self.state_status = 'pause'

                # Обычные состояния
                if self.state_status == 'menu':
                    self.handle_menu_events(event)
                elif self.state_status == 'play':
                    self.handle_play_events(event)
                elif self.state_status == 'pause':
                    # в pause_st() мы уже вешаем свой цикл
                    pass
                elif self.state_status in ('game_over', 'win'):
                    self.handle_game_over_events(event)

            # Отрисовка / логика
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


    # === РЕГИСТРАЦИЯ ===
    def handle_reg_events(self, event):
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
        self.screen.fill((30, 30, 30))
        prompt = self.font_small.render("Введите имя:", True, (255, 255, 255))
        name_surf = self.font_small.render(self.input_name, True, (255, 255, 0))
        self.screen.blit(prompt, (100, 100))
        self.screen.blit(name_surf, (100, 150))

        if self.name_taken:
            warn = self.font_small.render("Имя уже занято. Введите другое.", True, (255, 0, 0))
            self.screen.blit(warn, (100, 200))


    # === МЕНЮ (ВАШЕ СОХРАНЁННОЕ) ===
    def handle_menu_events(self, event):
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
        self.screen.fill((50, 50, 50))
        self.screen.blit(self.title_text, self.title_rect)
        self.play_image = pygame.transform.scale(self.play_image, (250, 64))
        self.play_rect.center = (self.center_x -130, self.center_y + 30)
        self.screen.blit(self.play_image, self.play_rect)
        self.quit_image = pygame.transform.scale(self.quit_image, (250, 64))
        self.quit_rect.center = (self.center_x -130, self.center_y + 130)
        self.screen.blit(self.quit_image, self.quit_rect)

        # === Leaderboard ===
        y = self.lb_y+40
        white = (255, 255, 255)

        # Заголовок
        self.screen.blit(self.font_small.render("Best Time:", True, white),
                         (self.lb_x-130, y))
        y += 50

        # — Свое время из JSON —
        try:
            with open("leaderboard.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                user_ms = data.get("time", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            user_ms = 0

        sec = user_ms // 1000
        cs = (user_ms % 1000) // 10
        you_str = f"You: {sec:02d}.{cs:02d}" if user_ms > 0 else "You: --.--"
        self.screen.blit(self.font_small.render(you_str, True, white),
                         (self.lb_x-130, y))
        y += 60

        # — Топ‑5 из БД или прочерк —
        if self.leaderboard.check_connection():
            if self.leaderboard.get_user_time(data['username']) > data['time']:
                self.leaderboard.update_score(data['username'], data['time'])
            top5 = self.leaderboard.get_top_scores()
            num = 1
            for name, t in top5:
                sec = t // 1000
                cs = (t % 1000) // 10
                line = f"{num}. {name} {sec:02d}.{cs:02d}"
                self.screen.blit(self.font_small.render(line, True, white),
                                 (self.lb_x-130, y))
                y += 50
                num+=1
        else:
            dash = self.font_small.render("——*——", True, white)
            self.screen.blit(dash, (self.lb_x, y))


    def create_level(self):
        self.timer = Timer()
        self.timer.start()
        return Level()


    # === ИГРА ===
    def handle_play_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            # ваш existing logic, например атаки
            pass  # оставляем без изменений


    def play_st(self):
        self.screen.fill(WATER_COLOR)
        if self.level:
            self.level.run()

        # отрисовка таймера в play
        elapsed_ms = self.timer.get_elapsed()
        seconds = elapsed_ms // 1000
        millis = (elapsed_ms % 1000) // 10
        time_surf = self.font_small.render(f"{seconds:02d}.{millis:02d}", True, (255, 255, 255))
        self.screen.blit(time_surf, (WIDTH - 150, 10))

        # проверка победы
        if self.finish_zone.colliderect(self.level.player.rect) and self.level.player.has_rune:
            self.win_sound.play()
            self.state_status = 'win'


    # === ПАУЗА ===
    def pause_st(self):
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

            self.screen.blit(saved, (0, 0))
            self.overlay()
            self.resume_image = pygame.transform.scale(self.resume_image, (250, 64))
            self.resume_rect.center = (self.center_x + 35, self.center_y)
            self.screen.blit(self.resume_image, self.resume_rect)
            self.menu_image = pygame.transform.scale(self.menu_image, (250, 64))
            self.menu_rect.center = (self.center_x + 35, self.center_y + 100)
            self.screen.blit(self.menu_image, self.menu_rect)
            pygame.display.flip()
            self.clock.tick(10)


    def overlay(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

    # === ПОБЕДА ===
    def win_st(self):
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
        self.screen.blit(overlay, (0, 0))
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
        """Обработка кликов в режиме 'game_over'"""
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
        """Создание кнопок после проигрыша"""
        if self.level:
            self.level.run(draw_only=True)

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        text_surface = self.font_small.render(
            """You're dead :(""",
            True, (255, 255, 255)
        )
        self.screen.blit(text_surface, (WIDTH // 3 + 55, HEIGHT // 2 - 110))

        self.replay_image = pygame.transform.scale(self.replay_image, (250, 64))
        self.replay_rect.center = (self.center_x + 35, self.center_y)
        self.screen.blit(self.replay_image, self.replay_rect)

        self.menu_image = pygame.transform.scale(self.menu_image, (250, 64))
        self.menu_rect.center = (self.center_x + 35, self.center_y + 100)
        self.screen.blit(self.menu_image, self.menu_rect)


if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()
