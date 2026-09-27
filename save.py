import os

script_dir = os.path.dirname(os.path.abspath(__file__))
savefile = os.path.join(script_dir, "DRAW_SaveFile.txt")


def load_highscore():
    try:
        with open(savefile, "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0  
    
def save_highscore(game):
    with open(savefile, "w") as file:
        file.write(str(game.highscore))    
    
    