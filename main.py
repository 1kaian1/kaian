import pygame
import random

pygame.init()

screen_width, screen_height = pygame.display.list_modes(0, pygame.FULLSCREEN, 0)[0]

if (screen_width, screen_height) < (1024, 768):
    raise Warning("Invalid screen scale.")

screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()
fps = 60

# fonts
base_font_50 = pygame.font.Font(None, 50)
base_font_100 = pygame.font.Font(None, 100)
base_font_200 = pygame.font.Font(None, 200)
base_font_1000 = pygame.font.Font(None, 1000)

# colors
color_light_blue = (0, 255, 255)
color_white = (255, 255, 255)
color_black = (0, 0, 0)
color_gray = (127, 127, 127)
color_red = (255, 0, 0)
color_blue = (0, 0, 255)
color_dark_gray = (15, 15, 15)

# load images
start_img = pygame.image.load("materials/start.png")
exit_img = pygame.image.load("materials/exit.png")
replay_img = pygame.image.load("materials/replay.png")

def draw_text(font, text, color, a, b):

    text_surface = font.render(text, True, color)
    x = a - text_surface.get_width() / 2
    y = b - text_surface.get_height() / 2
    screen.blit(text_surface, (x, y))


class Game:
    def __init__(self, p1_name, p2_name):

        self.ball_pos = [int(screen_width/2), int(screen_height/2)]
        self.ball_dir = random.randint(1, 360)
        self.ball_speed = 10
        self.arm_area = 150
        self.arm_speed = 10
        self.p1_pos = screen_height/2 - self.arm_area/2
        self.p2_pos = screen_height/2 - self.arm_area/2
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.ball_radius = 20
        self.line_width = 50
        self.arm_width = 10
        self.arm1_move = 0
        self.arm2_move = 0
        self.count_up = 0
        self.score_p1 = 0
        self.score_p2 = 0
        self.text = ""
        self.score_needed = 10

        game = True
        while game:

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.arm1_move = 1
                    elif event.key == pygame.K_s:
                        self.arm1_move = -1
                    if event.key == pygame.K_UP:
                        self.arm2_move = 1
                    elif event.key == pygame.K_DOWN:
                        self.arm2_move = -1

            screen.fill((0, 0, 0))

            """DRAWING"""

            # draw world
            line1 = pygame.draw.line(screen, color_white, (0, 0), (screen_width, 0), self.line_width)
            line2 = pygame.draw.line(screen, color_white, (0, screen_height), (screen_width, screen_height), self.line_width)
            line3 = pygame.draw.line(screen, color_white, (screen_width / 2, 0), (screen_width / 2, screen_height), 5)

            # draw arms
            arm1 = pygame.draw.rect(screen, color_white, (50, int(self.p1_pos), self.arm_width, self.arm_area))
            arm2 = pygame.draw.rect(screen, color_white, (screen_width - 50, int(self.p2_pos), self.arm_width, self.arm_area))

            # draw player 1 name
            draw_text(base_font_100, self.p1_name, color_dark_gray, screen_width/4, screen_height/8)

            # draw player 2 name
            draw_text(base_font_100, self.p2_name, color_dark_gray, screen_width/2*1.5, screen_height/8)

            # draw player 1 score
            draw_text(base_font_1000, str(self.score_p1), color_dark_gray, screen_width/4, screen_height/2*1.1)

            # draw player 2 score
            draw_text(base_font_1000, str(self.score_p2), color_dark_gray, screen_width/2*1.5, screen_height/2*1.1)

            # draw ball
            ball = pygame.draw.circle(screen, color_blue, self.ball_pos, self.ball_radius)

            """UPDATING"""

            if self.score_p1 == self.score_needed:
                game = False
                game_over(self.p1_name, self.p2_name, self.p1_name)

            elif self.score_p2 == self.score_needed:
                game = False
                game_over(self.p1_name, self.p2_name, self.p2_name)

            self.arms_position_update()

            self.score_update()

            # countdown
            if self.countdown_update():
                draw_text(base_font_200, self.text, color_light_blue, screen_width/2, screen_height/2)

            # ball update
            else:
                self.ball_position_update()
                self.ball_collision_and_direction_update(line1, line2, arm1, arm2)

            clock.tick(fps)
            self.count_up += 1

    def score_update(self):

        if self.ball_pos[0] < -self.ball_radius or self.ball_pos[0] > screen_width+self.ball_radius:

            if self.ball_pos[0] < -self.ball_radius:
                self.score_p2 += 1

            elif self.ball_pos[0] > screen_width+self.ball_radius:
                self.score_p1 += 1

            self.count_up = 0
            self.ball_pos = [int(screen_width / 2), int(screen_height / 2)]
            self.ball_dir = random.randint(1, 360)

    def countdown_update(self):

        if self.count_up <= 240:

            if self.count_up in range(61, 120):
                self.text = "3"
            elif self.count_up in range(121, 180):
                self.text = "2"
            elif self.count_up in range(181, 240):
                self.text = "1"
            return True

        elif self.count_up > 240:
            self.text = ""
            return False

    def ball_position_update(self):

        x = (self.ball_dir % 90)/100
        y = (90 - x)/100

        a = self.ball_pos[0]
        b = self.ball_pos[1]

        if self.ball_dir in range(1, 91):
            a = a - (x * self.ball_speed)
            b = b + (y * self.ball_speed)

        elif self.ball_dir in range(91, 181):
            a = a - (x * self.ball_speed)
            b = b - (y * self.ball_speed)

        elif self.ball_dir in range(181, 271):
            a = a + (x * self.ball_speed)
            b = b - (y * self.ball_speed)

        elif self.ball_dir in range(271, 361):
            a = a + (x * self.ball_speed)
            b = b + (y * self.ball_speed)

        else:
            raise Warning("Error0\nself.ball_dir: ", self.ball_dir)

        self.ball_pos[0] = int(a)
        self.ball_pos[1] = int(b)

    def ball_collision_and_direction_update(self, line1, line2, arm1, arm2):

        subjects = [line1, line2, arm1, arm2]
        test_rect = pygame.Rect(self.ball_pos[0]-self.ball_radius, self.ball_pos[1]-self.ball_radius, self.ball_radius*2, self.ball_radius*2)

        for subject in subjects:
            if test_rect.colliderect(subject):

                index = subjects.index(subject)

                if index == 0:
                    if self.ball_dir in range(91, 181):
                        self.ball_dir = random.randrange(1, 89)
                    elif self.ball_dir in range(181, 271):
                        self.ball_dir = random.randrange(271, 359)

                elif index == 1:
                    if self.ball_dir in range(1, 91):
                        self.ball_dir = random.randrange(91, 179)
                    elif self.ball_dir in range(271, 361):
                        self.ball_dir = random.randrange(181, 269)

                elif index == 2:
                    if self.ball_dir in range(1, 91):
                        self.ball_dir = random.randrange(271, 359)
                    elif self.ball_dir in range(91, 181):
                        self.ball_dir = random.randrange(181, 269)

                elif index == 3:
                    if self.ball_dir in range(181, 271):
                        self.ball_dir = random.randrange(91, 179)
                    elif self.ball_dir in range(271, 361):
                        self.ball_dir = random.randrange(1, 89)

                else:
                    raise Warning("Error1\nindex: ", index)

    def arms_position_update(self):

        if self.arm1_move == 1:
            if self.p1_pos - 5 < 25:
                self.p1_pos = self.p1_pos - (self.p1_pos - 25)
            else:
                self.p1_pos -= self.arm_speed

        elif self.arm1_move == -1:
            if self.p1_pos + self.arm_area + 5 > screen_height-25:
                self.p1_pos += (screen_height-24 - self.p1_pos-self.arm_area)
            else:
                self.p1_pos += self.arm_speed

        if self.arm2_move == 1:
            if self.p2_pos - 5 < 25:
                self.p2_pos = self.p2_pos - (self.p2_pos - 25)
            else:
                self.p2_pos -= self.arm_speed

        elif self.arm2_move == -1:
            if self.p2_pos + self.arm_area + 5 > screen_height - 25:
                self.p2_pos = self.p2_pos + (screen_height-24 - self.p2_pos-self.arm_area)
            else:
                self.p2_pos += self.arm_speed


def game_over(p1_name, p2_name, winner):

    text = "Player " + winner + " win!"
    draw_text(base_font_100, text, color_light_blue, screen_width/2, screen_height/4)

    replay_btn = replay_img.get_rect()
    replay_btn.center = (screen_width/2, screen_height/2)
    exit_btn = exit_img.get_rect()
    exit_btn.center = (screen_width/2, screen_height/1.5)

    run = True
    while run:

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                if replay_btn.collidepoint(event.pos):  # if replay button clicked
                    screen.fill((0, 0, 0))
                    run = False
                    Game(p1_name, p2_name)

                elif exit_btn.collidepoint(event.pos):  # if exit button clicked
                    run = False
                    menu()

        screen.blit(replay_img, (replay_btn.x, replay_btn.y))
        screen.blit(exit_img, (exit_btn.x, exit_btn.y))

        clock.tick(fps)

def menu():

    user_text_p1 = "P1 name"
    user_text_p2 = "P2 name"

    input_rect_p1 = pygame.Rect(0, 0, 0, 50)
    input_rect_p2 = pygame.Rect(0, 0, 0, 50)

    start_btn = start_img.get_rect()
    start_btn.center = (screen_width/2, screen_height/2)
    exit_btn = exit_img.get_rect()
    exit_btn.center = (screen_width/2, screen_height/1.5)

    color_active = color_light_blue
    color_passive = color_gray
    color_p1 = color_passive
    color_p2 = color_passive

    active = 0

    run = True
    while run:

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                if input_rect_p1.collidepoint(event.pos):  # if p1 rect clicked
                    active = 1
                    color_p1, color_p2 = color_active, color_passive
                    user_text_p1 = ""
                    if user_text_p2 == "":
                        user_text_p2 = "P2 name"

                elif input_rect_p2.collidepoint(event.pos):  # if p2 rect clicked
                    active = 2
                    color_p1, color_p2 = color_passive, color_active
                    user_text_p2 = ""
                    if user_text_p1 == "":
                        user_text_p1 = "P1 name"

                elif start_btn.collidepoint(event.pos):  # if start button clicked
                    active = 0
                    color_p1 = color_passive
                    color_p2 = color_passive
                    if user_text_p1 == "" or user_text_p1 == "P1 name":
                        color_p1 = color_red
                        user_text_p1 = "P1 name"
                    if user_text_p2 == "" or user_text_p2 == "P2 name":
                        color_p2 = color_red
                        user_text_p2 = "P2 name"
                    if user_text_p1 != "" and user_text_p1 != "P1 name" and user_text_p2 != "" and user_text_p2 != "P2 name":
                        screen.fill((0, 0, 0))
                        run = False
                        Game(user_text_p1, user_text_p2)

                elif exit_btn.collidepoint(event.pos):  # if exit button clicked
                    run = False

                else:  # if clicked elsewhere
                    active = 0
                    color_p1 = color_passive
                    color_p2 = color_passive
                    if user_text_p1 == "":
                        user_text_p1 = "P1 name"
                    if user_text_p2 == "":
                        user_text_p2 = "P2 name"

            if event.type == pygame.KEYDOWN:

                if active == 1:
                    if event.key == pygame.K_BACKSPACE:
                        user_text_p1 = user_text_p1[:-1]
                    elif len(user_text_p1) <= 18:
                        user_text_p1 += event.unicode

                elif active == 2:
                    if event.key == pygame.K_BACKSPACE:
                        user_text_p2 = user_text_p2[:-1]
                    elif len(user_text_p2) <= 18:
                        user_text_p2 += event.unicode

        screen.fill((0, 0, 0))

        # player one
        text_surface = base_font_50.render(user_text_p1, True, color_p1)
        screen.blit(text_surface, (input_rect_p1.x + 10, input_rect_p1.y + 10))
        pygame.draw.rect(screen, color_p1, input_rect_p1, 2)
        input_rect_p1.w = max(175, text_surface.get_width() + 20)
        input_rect_p1.center = (screen_width / 2, screen_height / 3.3)

        # player two
        text_surface = base_font_50.render(user_text_p2, True, color_p2)
        screen.blit(text_surface, (input_rect_p2.x + 10, input_rect_p2.y + 10))
        pygame.draw.rect(screen, color_p2, input_rect_p2, 2)
        input_rect_p2.w = max(175, text_surface.get_width() + 20)
        input_rect_p2.center = (screen_width / 2, screen_height / 2.7)

        # other
        screen.blit(start_img, (start_btn.x, start_btn.y))
        screen.blit(exit_img, (exit_btn.x, exit_btn.y))

        clock.tick(fps)


menu()
