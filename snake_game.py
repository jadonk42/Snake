#snake_game.py
#CODE FOR GRAPHICAL INTERFACE FOR USER TO PLAY GAME.


import snake_logic
import pygame

RED = pygame.Color(249, 36, 11)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
BLUE = pygame.Color(3, 99, 255)

class Game:

    def __init__(self):
        self.running = True
        self.gamestate = snake_logic.Gamestate(30, 30)
        self.size = (750, 750)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Snake')
        self.delayed_move = None
        self.ignore_next = False


    def start(self):
        pygame.init()
        pygame.font.init()
        clock = pygame.time.Clock()
        self.draw_screen()
        ticks = 0

        while self.running:
            clock.tick(30)
            self.running = self.gamestate.game_not_over()
            self.draw_screen()
            self.handle_events()
            ticks += 1
            if ticks%3 == 0:
                if self.delayed_move == None:
                    self.gamestate.move_snake()
                    self.gamestate.update_board()
                    self.ignore_next = False
                if self.delayed_move != None:
                    self.gamestate.move_snake()
                    self.gamestate.turn_snake(self.delayed_move)
                    self.gamestate.update_board()
                    self.delayed_move = None
                    self.ignore_next = False
            if ticks == 30:
                ticks = 0
        self.game_over()
        pygame.quit()


    def draw_screen(self):
        for row in range(self.gamestate.rows):
            for col in range(self.gamestate.cols):
                self.draw_block( self.gamestate.board[col][row], col, row)
        pygame.display.flip()


    def draw_block(self, state: str, col, row):
        if state == snake_logic.EMPTY:
            block_rectangle = pygame.Rect( (row/30) * self.size[0], (col/30)*(self.size[1]), self.size[0]/30, self.size[1]/30)          
            pygame.draw.rect( self.screen, WHITE, block_rectangle )
        elif state == snake_logic.FILLED:
            border = pygame.Rect( (row/30) * self.size[0], (col/30)*(self.size[1]), self.size[0]/30, self.size[1]/30  )
            pygame.draw.rect( self.screen, WHITE, border, 1 )
            block_rectangle = pygame.Rect( (row/30) * self.size[0], (col/30)*(self.size[1]), self.size[0]/30-1, self.size[1]/30 -1 )          
            pygame.draw.rect( self.screen, BLACK, block_rectangle )
        elif state == snake_logic.FOOD:
            block_rectangle = pygame.Rect( (row/30) * self.size[0], (col/30)*(self.size[1]), self.size[0]/30, self.size[1]/30  )          
            pygame.draw.rect( self.screen, RED, block_rectangle )


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type ==pygame.KEYDOWN and self.delayed_move == None:
                self.handle_keypresses(event.key)
                    

    def handle_keypresses(self, key):
        if key == pygame.K_q:
            self.running = False
            
        elif key == pygame.K_RIGHT:
            if not self.ignore_next:
                self.gamestate.turn_snake(snake_logic.RIGHT)
                self.ignore_next = True
            else:
                self.delayed_move = snake_logic.RIGHT
                
        elif key == pygame.K_UP:
            if not self.ignore_next:
                self.gamestate.turn_snake(snake_logic.UP)
                self.ignore_next = True
            else:
                self.delayed_move = snake_logic.UP
                
        elif key == pygame.K_LEFT:
            if not self.ignore_next:
                self.gamestate.turn_snake(snake_logic.LEFT)
                self.ignore_next = True
            else:
                self.delayed_move =  snake_logic.LEFT
                
        elif key == pygame.K_DOWN:
            if not self.ignore_next:
                self.gamestate.turn_snake(snake_logic.DOWN)
                self.ignore_next = True
            else:
                self.delayed_move = snake_logic.DOWN


    def game_over(self):
        not_closed = True
        while not_closed:
            score_font = pygame.font.SysFont('Comic Sans MS', 60)
            score = str(len( self.gamestate.snake.body))
            text = score_font.render( ('SCORE: ' + score), False, BLUE)
            self.screen.blit( text, (375, 375))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    not_closed = False

            


if __name__ == '__main__':
    Game().start()
