import ctypes

from game import Game, centerprint
from save import save_highscore

game = Game()

##set window title
ctypes.windll.kernel32.SetConsoleTitleW("DRAW - Made with Python")



##color coding   
RESET = "\033[0m"
RED = "\033[91m"
BLUE = "\033[94m"
ORANGE = "\033[38;5;208m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"

##print rules function
def rules():
    centerprint("RULES:")
    centerprint("Same suits add 1x to the combo.")
    centerprint("Same ranks add 2x to the combo.")
    centerprint("Sequential ranks add 3x to the combo.")
    centerprint("Drawing the same suit AND a sequential rank adds 6x to the combo.")
    centerprint("Every 10 combo reached, base combo is increased by 1x.")
    centerprint("If a drawn card does not add to the combo, the combo resets.")



##MAIN GAME LOOP
while True:
    centerprint("Welcome to Draw.")
    centerprint('At any point, type "Rules" or "R" for the rules.')
    centerprint('At any point, type "Stats" or "S" for the current run\'s stats.')
    centerprint('Type "Draw" or "D" to start.')
    centerprint(f'Highscore: {GREEN}{game.highscore}{RESET}')
    game.new_run()
    
    
    while True:
        
        userinput = input()
        if userinput.lower() == "draw" or userinput.lower() == "d":
            game.draw_card()
        ##rules
        elif userinput.lower() == "rules" or userinput.lower() == "r":
            rules()
        
        ##stats
        elif userinput.lower() == "stats" or userinput.lower() == "s":
            game.stats()
            
        ##for when game ends - writes high score to save if needed
        if len(game.deck) == 0:
            print()
            centerprint('No more cards in deck!')
            if game.score > game.highscore:
                centerprint(f"New highscore! {GREEN}{game.highscore}{RESET} {CYAN}->{RESET} {GREEN}{game.score}{RESET}")
                game.highscore = game.score
                save_highscore(game)
            else:
                centerprint(f'Total Points this run: {GREEN}{game.score}{RESET} (high: {GREEN}{game.highscore}{RESET})')
            centerprint(f'Max combo this run: {RED}{game.maxcombo}x{RESET}')
            break
        
    centerprint("Press ENTER to start new run")
    input()
    
    