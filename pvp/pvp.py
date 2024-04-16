import pygame
import sys
import pymunk
import pymunk.pygame_util
import math


from define import *
from cue import Cue
from ai import *
from balls import *
from pvp.player import *
from pvp.score import *


class PVPGame:
    def __init__(self):
        pygame.init()
        self.window_color = COLOR_BACKGROUND
        self.WINDOW_GAME = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "board.png"), (BOARD_SIZE)).convert()

        # khai bao them
        self.space = pymunk.Space()
        self.static_body = self.space.static_body
        self.draw_options = pymunk.pygame_util.DrawOptions(self.WINDOW_GAME)
        pos = (self.WINDOW_GAME.get_width() // 2, 663)
        self.cue_ball = self.create_ball(38/2,pos)
        self.clock = pygame.time.Clock()
        self.balls = []
        self.striker_balls = []
        self.mouse_pressed = False
        self.key_down = False
        self.force_direction = 1
        self.powering_up = True
        self.playerturn = True

        new_size = (int(self.cue_ball.radius * 2), int(self.cue_ball.radius * 2))
        self.striker_ball = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "striker.png"),(BALL_SIZE)).convert_alpha()
        self.white_ball = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "white_new.png"),(WHITE_BALL_SIZE)).convert_alpha()
        self.black_ball = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "black_new.png"),(BLACK_BALL_SIZE)).convert_alpha()
        self.queen = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "queen.png"), (BALL_SIZE)).convert_alpha()


        # Define the pattern based on the shape file
        pattern = [
            ['', '', '0', '', ''],
            ['', '0', '*', '*', ''],
            ['*', '0', 'Q', '0', '*'],
            ['', '*', '*', '0', ''],
            ['', '', '0', '', '']
        ]

        for row in range(5):
            for col in range(5):

                pos = (BALL_POSITION[0] + (col * (DIA + 1)), BALL_POSITION[1] + (row * (DIA + 1)))

                if pattern[row][col] != '':
                    new_ball = self.create_ball(DIA/2, pos)
                    self.balls.append(new_ball)

                    if pattern[row][col] == '*':
                        self.striker_balls.append(self.black_ball)
                    elif pattern[row][col] == '0':
                        self.striker_balls.append(self.white_ball)
                    else:
                        self.striker_balls.append(self.queen)

        self.force = 0

        for i in range(0, 16):
            if i == 9:
                the_ball = self.queen
            elif i % 2 == 0:
                the_ball = self.black_ball
            else:
                the_ball = self.white_ball
            self.striker_balls.append(the_ball)
        self.cue = Cue(self.cue_ball.body.position)
        self.potted_ball = []
        self.black_ball_potted = False
    def create_ball(self, radius, pos):
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Circle(body, radius)
        shape.mass = 5
        shape.elasticity = 0.8
        # use pivot joint to add friction
        pivot = pymunk.PivotJoint(body, self.static_body, (0, 0), (0, 0))
        pivot.max_bias = 0
        pivot.max_force = 1000
        self.space.add(body, shape, pivot)
        return shape
    def create_cushion(self, polydim):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = ((0, 0))
        shape = pymunk.Poly(body, polydim)
        shape.elasticity = 0.8
        self.space.add(body, shape)

    def is_moving(self):
        velocity = self.cue_ball.body.velocity
        return velocity != (0, 0)

    def checkEvent(self, event, taking_shot):
        # Kiểm tra sự kiện khi nút chuột được nhấn
        if event.type == pygame.MOUSEBUTTONDOWN and taking_shot == True:
            if event.button == 1:  # Nút chuột trái
                self.powering_up = True
                self.mouse_pressed = True
        # Kiểm tra sự kiện khi nút chuột được thả
        if event.type == pygame.MOUSEBUTTONUP and taking_shot == True:
            self.powering_up = False
            self.key_down = True;
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                new_x = max(min(self.cue_ball.body.position[0] - 10, 1000), 380)
                self.cue_ball.body.position = (new_x, self.cue_ball.body.position[1])
                self.key_down = False
            elif event.key == pygame.K_RIGHT:
                new_x = max(min(self.cue_ball.body.position[0] + 10, 820), 380)
                self.cue_ball.body.position = (new_x, self.cue_ball.body.position[1])
                self.key_down = False

    def start_game(self):
        running = True
        for c in CUSHION:
            self.create_cushion(c)
        while running:
            taking_shot = True
            self.space.step(1 / 60)
            dt = self.clock.tick(60) / 1000
            self.WINDOW_GAME.fill(self.window_color)
            self.WINDOW_GAME.blit(self.bg, BOARD_POSITION)
            self.WINDOW_GAME.blit(self.striker_ball, (self.cue_ball.body.position[0] - self.cue_ball.radius,
                                                    self.cue_ball.body.position[1] - self.cue_ball.radius))

            for i, ball in enumerate(self.balls):
                for pocket in POCKETS:
                    ball_x_dist = abs(ball.body.position[0] - pocket[0])
                    ball_y_dist = abs(ball.body.position[1] - pocket[1])
                    ball_dist = math.sqrt(ball_x_dist ** 2 + ball_y_dist ** 2)
                    if ball_dist <= POCKET_DIA / 2:
                        self.space.remove(ball.body)
                        self.balls.remove(ball)
                        self.potted_ball.append(self.striker_balls[i])
                        self.striker_balls.pop(i)
                        if i % 2 ==0:
                            self.playerturn = False
                        elif i % 2 !=0:
                            self.playerturn = True
                    if self.playerturn == False:
                        self.playerturn = True

            # print(self.potted_ball)
            if self.is_moving() == False and self.playerturn == False:
                self.cue_ball.body.position = (self.WINDOW_GAME.get_width() // 2, 140)
                self.key_down = False
            if self.is_moving() == False and self.key_down == True and self.playerturn == True:
                self.cue_ball.body.position = (self.WINDOW_GAME.get_width() // 2, 663)
                self.key_down = False

            for i, ball in enumerate(self.balls):
                self.WINDOW_GAME.blit(self.striker_balls[i],(ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                self.checkEvent(event, taking_shot)

            for i, ball in enumerate(self.balls):
                for pocket in POCKETS:
                    ball_x_dist = abs(ball.body.position[0] - pocket[0])
                    ball_y_dist = abs(ball.body.position[1] - pocket[1])
                    ball_dist = math.sqrt(ball_x_dist ** 2 + ball_y_dist ** 2)
                    if ball_dist <= POCKET_DIA / 2:
                        self.space.remove(ball.body)
                        self.balls.remove(ball)
                        self.potted_ball.append(self.striker_balls[i])
                        self.striker_balls.pop(i)
                        if self.striker_balls[i] == self.current_player.ball_color:
                            continue
                        else:
                            if self.current_player == self.player1:
                                self.current_player = self.player2
                            else:
                                self.current_player = self.player1

            for ball in self.balls:
                if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0:
                    taking_shot = False
                if int(self.cue_ball.body.velocity[0]) != 0 or int(self.cue_ball.body.velocity[1]) != 0:
                    taking_shot = False

            if taking_shot == True:
                # calculate cue angle
                mouse_pos = pygame.mouse.get_pos()
                self.cue.rect.center = self.cue_ball.body.position
                x_dist = -(self.cue_ball.body.position[0] - mouse_pos[0])
                y_dist = self.cue_ball.body.position[1] - mouse_pos[1]
                cue_angle = math.degrees(math.atan2(y_dist, x_dist))
                self.cue.update(cue_angle)
                self.cue.draw(self.WINDOW_GAME)

            # Tăng lực nếu nút chuột được nhấn và giữ
            if self.mouse_pressed and self.powering_up == True:
                self.force += INCREASE_RATE * dt * self.force_direction
                if self.force >= MAXFORCE or self.force <= 0:
                    self.force_direction *= -1
            # Giảm lực nếu không có nút chuột nào được nhấn
            elif self.powering_up == False and taking_shot == True:
                x_impulse = self.force * math.cos(math.radians(self.cue.angle))
                y_impulse = self.force * math.sin(math.radians(self.cue.angle))
                self.cue_ball.body.apply_impulse_at_local_point((x_impulse * 100, -(y_impulse * 100)), (0, 0))
                self.force = 0
                mouse_pressed = False


            #print(self.cue_ball.body.position)
            #self.space.debug_draw(self.draw_options)

            pygame.draw.rect(self.WINDOW_GAME, COLOR_DARK_BROWN, (*POWER_BAR_POSITION, *POWER_BAR_SIZE))
            pygame.draw.rect(self.WINDOW_GAME, COLOR_WHITE, (
            POWER_BAR_POSITION[0], POWER_BAR_POSITION[1] + POWER_BAR_SIZE[1] - self.force * 5, POWER_BAR_SIZE[0],
            self.force * 5))

            pygame.display.flip()
        pygame.quit()
