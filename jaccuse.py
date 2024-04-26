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

# Create data structures for clues the truth-tellers give about each item and suspect
# clues: Keys=Suspects being asked for a clue, value="clue dictionary".
clues = {}
for i, interviewee in enumerate(SUSPECTS):
    if interviewee in liars:
        continue # Skip the liars for now

    # This "clue dictionary" has keys=items & suspects, value=the clue given
    clues[interviewee] = {}
    clues[interviewee]['debug_liar'] = False # Useful for debugging
    for item in ITEMS: # Select clue about each item
        if random.randint(0, 1) == 0: # Tells where the item is
            clues[interviewee][item] = PLACES[ITEMS.index(item)]
        else: # tells who has the item
            clues[interviewee][item] = SUSPECTS[ITEMS.index(item)]
    for suspect in SUSPECTS: # Select clue about each suspect
        if random.randint(0, 1) == 0: # Tells where the suspect is
            clues[interviewee][suspect] = PLACES[SUSPECTS.index(suspect)]
        else: # tells what item the suspect has
            clues[interviewee][suspect] = ITEMS[SUSPECTS.index(suspect)]

# Create data structures about the clues the liars give about each item and suspect
for i, interviewee in enumerate(SUSPECTS):
    if interviewee not in liars:
        continue # We've already handled the truth-tellers

    # This 'clues dictionary' has keys=items & suspects, and values=the clue given
    clues[interviewee] = {}
    clues[interviewee]['debug_liar'] = True # Useful for debugging

    # This interviewee is a liar and gives wrong clues
    for item in ITEMS:
        if random.randint(0, 1) == 0: # Select a random (wrong) place clue
            while True: # Lies about the place
                clues[interviewee][item] = random.choice(PLACES)
                if clues[interviewee][item] != PLACES[ITEMS.index(item)]:
                    # break out of the loop when wrong clue is selected
                    break
        else: # Select a random (wrong) suspect clue
            while True:
                clues[interviewee][item] = random.choices(SUSPECTS)
                if clues[interviewee][item] != SUSPECTS[ITEMS.index(item)]:
                    # break out of the loop when wrong clue is selected
                    break
    for suspect in SUSPECTS:
        if random.randint(0, 1) == 0: # Select a random (wrong) place clue
            while True:
                clues[interviewee][suspect] = random.choice(PLACES)
                if clues[interviewee][suspect] != PLACES[SUSPECTS.index(suspect)]:
                    # break out of the loop when wrong clue is selected
                    break
        else: # Select a random (wrong) item clue
            while True:
                clues[interviewee][suspect] = random.choice(ITEMS)
                if clues[interviewee][suspect] != ITEMS[SUSPECTS.index(suspect)]:
                    # break out of the loop when wrong clue is selected
                    break

# Create the data structure for clues given when asked about Zophie:
zophieClues = {}
for interviewee in random.sample(SUSPECTS, random.randint(3, 4)):
    kindOfClue = random.randint(1, 3)
    if kindOfClue == 1:
        if interviewee not in liars:
            # They tell you who has Zophie
            zophieClues[interviewee] = culprit
        elif interviewee in liars:
            while True:
                # Select a (wrong) suspect clue
                zophieClues[interviewee] = random.choice(SUSPECTS)
                if zophieClues[interviewee] != culprit:
                    # Break out of the loop when wrong clue is selected
                    break

    elif kindOfClue == 2:
        if interviewee not in liars:
            # They tell you where Zophie is
            zophieClues[interviewee] = PLACES[SUSPECTS.index(culprit)]
        elif interviewee in liars:
            while True:
                # Select a (wrong) place clue
                zophieClues[interviewee] = random.choice(PLACES)
                if zophieClues[interviewee] != PLACES[SUSPECTS.index(culprit)]:
                    # Break out of the loop when wrong clue is selected
                    break

    elif kindOfClue == 3:
        if interviewee not in liars:
            # They tell you what item Zophie is near
            zophieClues[interviewee] = ITEMS[SUSPECTS.index(culprit)]
        elif interviewee in liars:
            while True:
                # Select a (wrong) item clue
                zophieClues[interviewee] = random.choice(ITEMS)
                if zophieClues[interviewee] != ITEMS[SUSPECTS.index(culprit)]:
                    # Break out of the loop when wrong clue is selected
                    break
            
# Uncomment to view the clue data structure
#import pprint
#pprint.pprint(clues)
#pprint.pprint(zophieClues)
#print("Culprit:", culprit)
# START OF THE GAME
print('''J'ACCUSE! (a mystery game)
You are the world-famous detective, Mathilde Camus.
ZOPHIE THE CAT has gone missing, and you must sift through the clues.
Suspects either always tell lies, or always tell the truth. Ask them
about other people, places, and items to see if the details they give are
truthful and consistent with your observations. Then you will know if
their clue about ZOPHIE THE CAT is true or not. Will you find ZOPHIE THE
CAT in time and accuse the guilty party?
''')
input('Press Enter to begin...')

startTime = time.time()
endTime = startTime + TIME_TO_SOLVE

# Main game loop
while True:
    if time.time() > endTime or accusationsLeft == 0:
        # Handle game over condtition
        if time.time() > endTime:
            print('You have run out of time!')
        elif accusationsLeft == 0:
            print('You have accused too many innocent people!')
        culpritIndex = SUSPECTS.index(culprit)
        print('It was {} with {} at {} who catnapped her!'.format(culprit, ITEMS[culpritIndex],PLACES[culpritIndex]))
        print('Better luck next time, Detective!')
        sys.exit()

    print()
    minutesLeft = int(endTime - time.time()) // 60
    secondsLeft = int(endTime - time.time()) % 60
    print('Time left: {} min, {} sec'.format(minutesLeft, secondsLeft))

    if currentLocation == 'TAXI':
        print('You are in your taxi, where do you want to go?')
        for place in sorted(PLACES):
            placeInfo = ''
            if place in visitedPlaces:
                placeInfo = visitedPlaces[place]
            nameLabel = '(' + place[0] + ')' + place[1:]
            spacing = " " * (LONGEST_PLACE_NAME_LENGTH - len(place))
            print('{} {}{}'.format(nameLabel, spacing, placeInfo))
        print('(Q)UIT GAME')
        while True: # Keep asking until a valid response is given
            response = input('> ').upper()
            if response == '':
                continue # ask again
            if response == 'Q':
                print('Thanks for playing!')
                sys.exit()
            if response in PLACE_FIRST_LETTERS.keys():
                break
        currentLocation = PLACE_FIRST_LETTERS[response]
        continue # Go back to the start of the main game loop

    # At a place, player can ask for clues
    print('You are at the {}.'.format(currentLocation))
    currentLocationIndex = PLACES.index(currentLocation)
    thePersonHere = SUSPECTS[currentLocationIndex]
    theItemHere = ITEMS[currentLocationIndex]
    print(' {} with the {} is here.'.format(thePersonHere, theItemHere))
