from game import Game

game = Game()

while not game.over:
    game.update()
    game.draw()
game.exit()
