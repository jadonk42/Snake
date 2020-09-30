#snake_console_ui.py
import snake_logic
def run():
    gamestate = snake_logic.Gamestate(10,10)
    gamestate.print_board()
    running = True
    while running:
        action = input()
        if action == '':
            gamestate.move_snake()
            gamestate.eat_food()
            running = gamestate.game_not_over()
        if action == 'Q':
            running = False
            break
        if action == 'W':
            gamestate.snake.turn(snake_logic.UP)
        if action == 'A':
            gamestate.snake.turn(snake_logic.LEFT)
        if action == 'S':
            gamestate.snake.turn(snake_logic.DOWN)
        if action == 'D':
            gamestate.snake.turn(snake_logic.RIGHT)

        gamestate.update_board()
        gamestate.print_board()
            
        
    

if __name__ == '__main__':
    run()


