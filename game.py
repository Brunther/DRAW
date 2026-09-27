import random
import re
import shutil

from save import load_highscore

##color coding
RESET = "\033[0m"
RED = "\033[91m"
BLUE = "\033[94m"
ORANGE = "\033[38;5;208m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"

suitcolors = {
    "Spades": "\033[94m\u2660 ",
    "Hearts": "\033[91m\u2665 ",
    "Clubs": "\u2663 ",
    "Diamonds": "\033[38;5;208m\u2666 "
}


##centerprint function
ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
terminal_width = shutil.get_terminal_size().columns

def centerprint(text=""):
    clean_text = ANSI_ESCAPE.sub("", str(text))

    padding = max(0, (terminal_width - len(clean_text)) // 2)

    print(" " * padding + str(text))
    
    

##initialize ranks and suits
ranklist = ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"]
suitlist = ["Spades", "Hearts", "Clubs", "Diamonds"]


## lists of points and values for ranks
points = {
    "Ace": 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10 
    }
rankvalues = {
    "Ace": 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    "Jack": 11,
    "Queen": 12,
    "King": 13 
    }


##convert sequential multipliers to words (double, triple, quad, etc)
seqtoword = {
    2: "Double",
    3: "Triple",
    4: "Quadruple",
    5: "Quintuple",
    6: "Sextuple",
    7: "Septuple",
    8: "Octuple"
}


##rules function
def rules():
    centerprint("RULES:")
    centerprint("Same suits add 1x to the self.combo.")
    centerprint("Same ranks add 2x to the self.combo.")
    centerprint("Sequential ranks add 3x to the self.combo.")
    centerprint("Drawing the same suit AND a sequential rank adds 6x to the self.combo.")
    centerprint("Every 10 self.combo reached, base combo is increased by 1x.")
    centerprint("If a drawn card does not add to the self.combo, the self.combo resets.")






class Game:
    
    def __init__(self):
        self.highscore = load_highscore()
        self.new_run()
    
    ##new run initialization
    def new_run(self):
        self.deck = [(rank, suit) for rank in ranklist for suit in suitlist]
        
        
        self.lastrank = None
        self.lastsuit = None
        self.lastmult = None
        self.combo = 1
        self.basecombo = 1
        self.maxcombo = 1
        self.comboreq = 10
        self.score = 0
        self.suitpaircounter = 0
        self.sequencecounter = 0
        self.spscounter = 0

            
        
        
    def draw_card(self):
        card = random.choice(self.deck)
        self.deck.remove(card)
                    
        rank = card[0]
        suit = card[1]
        
        suitdisplay = f"{suitcolors[suit]}{suit}{RESET}"
        
        ##turns "drew a" into "drew an" for aces and 8s
        if rankvalues[rank] == 1 or rankvalues[rank] == 8:
            aorn = "an"
        else:
            aorn = "a"
            
        ##reset suit pair and sequence counter
        if self.lastmult != "suit pair":
            self.suitpaircounter = 0
        if self.lastmult != "sequence":
            self.sequencecounter = 0
        if self.lastmult != "sps":
            self.spscounter = 0
            
        ##pairs
        if self.lastrank == rank:
            if self.lastmult == "pair":
                self.combo += 4
                self.lastmult = "3oak"
                centerprint(f'drew {aorn} {YELLOW}{rank}{RESET} of {suitdisplay}. {CYAN}Three of a kind!!{RESET} combo: {RED}{self.combo}x{RESET}')
            elif self.lastmult == "3oak":
                self.combo += 8
                self.lastmult = "4oak"
                centerprint(f'drew {aorn} {YELLOW}{rank}{RESET} of {suitdisplay}. {CYAN}Four of a kind!!!{RESET} combo: {RED}{self.combo}x{RESET}')
            else:
                self.combo += 2
                self.lastmult = "pair"
                centerprint(f'drew {aorn} {YELLOW}{rank}{RESET} of {suitdisplay}. {CYAN}Pair!{RESET} combo: {RED}{self.combo}x{RESET}')
                
        ##suit pair sequence
        elif self.lastrank is not None and (rankvalues[rank] == rankvalues[self.lastrank] + 1) and self.lastsuit is not None and self.lastsuit == suit:
            if self.spscounter > 0:
                self.combo += self.spscounter * 6
                self.spscounter += 1
                centerprint(f'drew {aorn} {YELLOW}{rank}{RESET} of {suitdisplay}. {CYAN}{seqtoword[self.spscounter]} Suit Pair Sequence!!{RESET} combo: {RED}{self.combo}x{RESET}')
            else:
                self.combo += 6
                self.lastmult = "sps"
                self.spscounter += 1
                centerprint(f'drew {aorn} {YELLOW}{rank}{RESET} of {suitdisplay}. {CYAN}Suit Pair Sequence!!{RESET} combo: {RED}{self.combo}x{RESET}')
        
        ##sequences
        elif self.lastrank is not None and ((rankvalues[rank] == rankvalues[self.lastrank] + 1) or (rankvalues[rank] == 1 and rankvalues[self.lastrank] == 13)):
            if self.sequencecounter > 0:
                self.combo += self.sequencecounter * 3
                self.sequencecounter += 1
                centerprint(f'drew {aorn} {YELLOW}{rank}{RESET} of {suitdisplay}. {CYAN}{seqtoword[self.sequencecounter]} Sequence!{RESET} combo: {RED}{self.combo}x{RESET}')
            else:
                self.combo += 3
                self.lastmult = "sequence"
                self.sequencecounter += 1
                centerprint(f'drew {aorn} {YELLOW}{rank}{RESET} of {suitdisplay}. {CYAN}Sequence!{RESET} combo: {RED}{self.combo}x{RESET}')
            
        ##suit pairs
        elif self.lastsuit is not None and self.lastsuit == suit:
            if self.suitpaircounter > 0:
                self.combo += self.suitpaircounter * 2
                self.suitpaircounter += 1
                centerprint(f'drew {aorn} {YELLOW}{rank}{RESET} of {suitdisplay}. {CYAN}{seqtoword[self.suitpaircounter]} Suit Pair!{RESET} combo: {RED}{self.combo}x{RESET}')
            else:
                self.combo += 1
                self.lastmult = "suit pair"
                self.suitpaircounter += 1
                centerprint(f'drew {aorn} {YELLOW}{rank}{RESET} of {suitdisplay}. {CYAN}Suit Pair!{RESET} combo: {RED}{self.combo}x{RESET}')
            
        else:
            centerprint(f'drew {aorn} {YELLOW}{rank}{RESET} of {suitdisplay}.')
            self.combo = self.basecombo
            self.lastmult = None
        
        ##sets basecombo/combo requirement for next base combo
        if self.combo >= self.comboreq:
            self.basecombo += 1
            centerprint(f'Combo has reached {RED}{self.comboreq}x{RESET}! base combo is now {RED}{self.basecombo}x{RESET}.')
            self.comboreq += 10
        self.score += self.combo * points[rank]
        
        ##sets max combo for stats
        self.maxcombo = max(self.maxcombo, self.combo)
        
        
        self.lastrank = rank
        self.lastsuit = suit
        
        centerprint(f'points: {GREEN}{self.score}{RESET}')    
        
        
        
        
        
        
        
        
        
    ##stats function
    def stats(self):
        centerprint('STATS:')
        centerprint(f'Cards drawn: {52 - len(self.deck)} ({len(self.deck)} cards left)')
        centerprint(f'Current combo: {RED}{self.combo}x{RESET}')
        centerprint(f'base combo: {RED}{self.basecombo}x{RESET}')
        centerprint(f'Max combo: {RED}{self.maxcombo}x{RESET}')
        centerprint(f'Total score: {GREEN}{self.score}{RESET}')
        if self.score > self.highscore:
            centerprint(f'Highscore: {GREEN}{self.score}{RESET}')
        else:
            centerprint(f'Highscore: {GREEN}{self.highscore}{RESET}')
        
        
        
        
        
    