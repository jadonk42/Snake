#snake_logic
#the logic for the game. both interfaces use this to represent the game, and board

from random import randint
#state and directions
EMPTY = 'EMPTY'
FILLED = 'FILLED'
FOOD = 'FOOD'
FROZEN = 'FROZEN'
MOVING = 'MOVING'
RIGHT = 'RIGHT'
LEFT = 'LEFT'
DOWN = 'DOWN'
UP = 'UP'

class Gamestate:
    def __init__(self, rows, cols):
        self.board = []
        self.rows = rows
        self.cols = cols
        
        self.game_over = False
        self.snake = Snake()
        self.food = None
        self.change_food()
        self.freeze_counter = 0
        self.score = 0
        for row in range(self.rows):
            self.board.append([])
            for col in range(self.cols):
                self.board[-1].append( EMPTY )
        self.update_board()

    def print_board(self):
        for row in range(self.rows):
            print('|', end = '')
            for col in range(self.cols):
                if self.board[row][col] == EMPTY:
                    print('   ', end = '')
                elif self.board[row][col] == FILLED:
                    print('[O]', end = '')
                elif self.board[row][col] == FOOD:
                    print('[F]', end = '')
            print('|')


    def update_board(self):
        self.clear_board()
        for block in self.snake.body:
            row = block.row
            col = block.col
            self.board[row][col] = FILLED
        self.board[self.food.row][self.food.col] = FOOD

 
    def clear_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.board[row][col] = EMPTY


    def move_snake(self):
        if self.can_move_snake():
            self.snake.move()
            if self.can_eat():
                self.eat_food()
                
            if self.freeze_counter != 0 and self.freeze_counter < 6:
                self.freeze_counter += 1
                if self.freeze_counter == 6:
                    self.freeze_counter = 0
                    self.snake.unfreeze()
        else:
            self.game_over = True
                    

    def can_move_snake(self) -> bool:
        head_row = self.snake.body[0].row
        head_col = self.snake.body[0].col
        if self.snake.direction == UP:
            return head_row != 0 and (self.board[head_row-1][head_col] == EMPTY or self.board[head_row-1][head_col] == FOOD)
        if self.snake.direction == DOWN:
            return head_row != self.rows-1 and (self.board[head_row+1][head_col] == EMPTY or self.board[head_row+1][head_col] == FOOD)
        if self.snake.direction == LEFT:
            return head_col != 0 and (self.board[head_row][head_col-1] == EMPTY or self.board[head_row][head_col-1] == FOOD)
        if self.snake.direction == RIGHT:
            return head_col != self.cols-1 and (self.board[head_row][head_col+1] == EMPTY or self.board[head_row][head_col+1] == FOOD)


    def can_eat(self) -> bool:
        head_row = self.snake.body[0].row
        head_col = self.snake.body[0].col
        return head_row == self.food.row and head_col == self.food.col


    def eat_food(self):
        if self.can_eat():
            self.snake.freeze()
            self.freeze_counter = 1
            self.change_food()
            self.score += 1


    def change_food(self):
        not_valid = True
        while not_valid:
            food_row = randint(0, self.rows-1)
            food_col = randint(0, self.cols-1)
            not_valid = self.food_not_valid(food_row, food_col)
        self.food = Block(food_row, food_col)


    def food_not_valid(self, food_row, food_col) -> bool:
        is_same = False
        for block in self.snake.body:
            if block.row == food_row and block.col == food_col:
                is_same = True
        return is_same


    def game_not_over(self) -> bool:
        return not self.game_over


    def turn_snake(self, new_direction: str):
        self.snake.turn(new_direction)

        

class Snake:
    def __init__(self):
        self.body = []
        self.state = MOVING
        self.direction = RIGHT
        self.body.append( Block( 5,5 ) )


    def freeze(self) -> None:
        self.state = FROZEN


    def unfreeze(self) -> None:
        self.state = MOVING
        

    def move(self):
        if self.state == FROZEN:
            row = self.body[0].row
            col = self.body[0].col
            if self.direction == RIGHT:
                new_block = Block(row, col+1)
                self.body.insert(0, new_block)
            if self.direction == LEFT:
                new_block = Block(row, col-1)
                self.body.insert(0, new_block)
            if self.direction == UP:
                new_block = Block(row-1, col)
                self.body.insert(0, new_block)
            if self.direction == DOWN:
                new_block = Block(row+1, col)
                self.body.insert(0, new_block)
                
                
        if self.state == MOVING:
            row = self.body[0].row
            col = self.body[0].col
            if self.direction == RIGHT:
                new_block = Block(row, col+1)
                self.body.insert(0, new_block)
                self.body.pop(-1)
            if self.direction == LEFT:
                new_block = Block(row, col-1)
                self.body.insert(0, new_block)
                self.body.pop(-1)
            if self.direction == UP:
                new_block = Block(row-1, col)
                self.body.insert(0, new_block)
                self.body.pop(-1)
            if self.direction == DOWN:
                new_block = Block(row+1, col)
                self.body.insert(0, new_block)
                self.body.pop(-1)


    def turn(self, new_direction: str):
        if self.can_turn(new_direction):
            self.direction = new_direction


    def can_turn(self, new_direction: str) -> bool:
        if self.direction == UP:
            return new_direction != DOWN
        if self.direction == LEFT:
            return new_direction != RIGHT
        if self.direction == DOWN:
            return new_direction != UP
        if self.direction == RIGHT:
            return new_direction != LEFT



class Block:
    def __init__(self, row, col):
        self.row = row
        self.col = col



