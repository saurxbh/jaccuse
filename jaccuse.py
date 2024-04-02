import time, random, sys

# Set up the constants
SUSPECTS = ['DUKE HAUTDOG', 'MAXIMUM POWERS', 'BILL MONOPOLIS', 'SENATOR SCHMEAR', 'MRS. FEATHERTOSS', 'DR. JEAN SPLICER', 'RAFFLES THE CLOWN', 'ESPRESSA TOFFEEPOT', 'CECIL EDGAR VANDERTON']
ITEMS = ['FLASHLIGHT', 'CANDLESTICK', 'RAINBOW FLAG', 'HAMSTER WHEEL', 'ANIME VHS TAPE', 'JAR OF PICKLES', 'ONE COWBOY BOOT', 'CLEAN UNDERPANTS', '5 DOLLAR GIFT CARD']
PLACES = ['ZOO', 'OLD BARN', 'DUCK POND', 'CITY HALL', 'HIPSTER CAFE', 'BOWLING ALLEY', 'VIDEO GAME MUSEUM', 'UNIVERSITY LIBRARY', 'ALBINO ALLIGATOR PIT']
TIME_TO_SOLVE = 300 # 300 Seconds (5 minutes) to solve the game.

# First letters and longest length of places are needed for menu display
PLACE_FIRST_LETTERS = {}
LONGEST_PLACE_NAME_LENGTH = 0
for place in PLACES:
    PLACE_FIRST_LETTERS[place[0]] = place
    if len(place) > LONGEST_PLACE_NAME_LENGTH:
        LONGEST_PLACE_NAME_LENGTH = len(place)

# Basic sanity checks of the constants
assert len(SUSPECTS) == 9
assert len(ITEMS) == 9
assert len(PLACES) == 9
# First letter must be unique
assert len(PLACE_FIRST_LETTERS.keys()) == len(PLACES)

knownSuspectsAndItems = []
# visitedPlaces: Keys=places, values=strings of suspects and items there
visitedPlaces = {}
currentLocation = 'TAXI' # Start the game in the taxi
accusedSuspects = [] # Accused suspects won't offer clues
liars = random.sample(SUSPECTS, random.randint(3,4))
accusationsLeft = 3 # You can accuse up to 3 people
culprit = random.choice(SUSPECTS)

# Common indices link these, e.g. SUSPECTS[0] and ITEMS[0] are at PLACES[0]
random.shuffle(SUSPECTS)
random.shuffle(ITEMS)
random.shuffle(PLACES)


