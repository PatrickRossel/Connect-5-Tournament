import os
import signal
import sys
import time
import matplotlib
matplotlib.use('Agg')
from matplotlib.transforms import ScaledTranslation
import matplotlib.pyplot as plt

MAX_MOVES = 100
NUM_ROWS = 8
NUM_COLS = 11
WIN_SIZE = 5
PLAYER_A = 'A'
PLAYER_B = 'B'
SPACE = 'e'


# Kill a process
def check_kill_process(pstring):
    for line in os.popen(f"ps ax | grep {pstring} | grep -v grep"):
        fields = line.split()
        pid = fields[0]
        try:
            os.kill(int(pid), signal.SIGKILL)
        except (PermissionError, ProcessLookupError):
            # Already finished
            pass

# Add a coin
def addCoin(state, pos, player):
    pos = pos - 1
    if pos < 0:
        print(f"E1: Not allowed move by {player} at position {pos}")
        return False
    if pos >= NUM_COLS:
        print(f"E2: Not allowed move by {player} at position {pos}")
        return False
    if state[pos][0] != SPACE:
        print(f"E3: Not allowed move by  move by {player} at position {pos} since board was full")
        return False

    for y in range(NUM_ROWS - 1, -1, -1):
        if state[pos][y] == SPACE:
            state[pos][y] = player
            return True
    print(f"Not allowed move by {player}")
    return False


# Flips the board
def flip(state):
    oldState = [[SPACE for _ in range(NUM_ROWS)] for _ in range(NUM_COLS)]
    for y in range(NUM_ROWS):
        for x in range(NUM_COLS):
            oldState[x][y] = state[x][y]
            state[x][y] = SPACE
    for x in range(NUM_COLS):
        flag = False
        yPos = NUM_ROWS - 1
        for y in range(NUM_ROWS):
            if oldState[x][y] != SPACE:
                flag = True
            if flag:
                state[x][yPos] = oldState[x][y]
                yPos = yPos - 1
    return True


# test if there is a 5er in down-direction starting from x,y
def testPositionDown(state, x, y):
    player = state[x][y]
    if y > NUM_ROWS - WIN_SIZE:
        return ''
    for ny in range(y + 1, y + WIN_SIZE):
        if player != state[x][ny]:
            return ''
    return player


# test if there is a 5er in right-direction starting from x,y
def testPositionRight(state, x, y):
    player = state[x][y]
    if x > NUM_COLS - WIN_SIZE:
        return ''
    for nx in range(x + 1, x + WIN_SIZE):
        if player != state[nx][y]:
            return ''
    return player


# test if there is a 5er down-right-diagonal starting from x,y
def testPositionDownRight(state, x, y):
    player = state[x][y]
    if x > NUM_COLS - WIN_SIZE or y > NUM_ROWS - WIN_SIZE:
        return ''
    ny = y + 1
    for nx in range(x + 1, x + WIN_SIZE):
        if player != state[nx][ny]:
            return ''
        ny = ny + 1
    return player


# test if there is a 5er up-right-diagonal starting from x,y
def testPositionUpRight(state, x, y):
    player = state[x][y]
    if x > NUM_COLS - WIN_SIZE or y < 4:
        return ''
    ny = y - 1
    for nx in range(x + 1, x + WIN_SIZE):
        if player != state[nx][ny]:
            return ''
        ny = ny - 1
    return player


# test if there is a 5er starting from a given x,y
def testPosition(state, x, y):
    player = state[x][y]
    # x=0,y=0 is upper left corner
    if player == SPACE:
        return ''
    if testPositionDown(state, x, y) != '':
        return player
    if testPositionRight(state, x, y) != '':
        return player
    if testPositionDownRight(state, x, y) != '':
        return player
    if testPositionUpRight(state, x, y) != '':
        return player
    return ''


# Test is somebody has one, by testing each position
def hasWon(state):
    for x in range(NUM_COLS):
        for y in range(NUM_ROWS):
            player = testPosition(state, x, y)
            if player != '':
                return player
    return ''


# Test if there is a draw in the game
def isDraw(state):
    winners = set()
    for x in range(NUM_COLS):
        for y in range(NUM_ROWS):
            player = testPosition(state, x, y)
            winners.add(player)
    if PLAYER_A in winners and PLAYER_B in winners:
        return True
    for x in range(NUM_COLS):
        for y in range(NUM_ROWS):
            if state[x][y] == SPACE:
                return False
    return True


# Read Move From File
def readMove(filename):
    try:
        file = open(filename, "r")
        move = file.readline()
        file.close()
        return str(move)
    except FileNotFoundError:
        return '-999'


# Read State-File to disk
def readStateSpace(filename):
    state = [[SPACE for _ in range(NUM_ROWS)] for _ in range(NUM_COLS)]
    with open(filename, 'r') as file:
        bflag = False
        nY = 0
        for line in file:
            if bflag:
                nX = 0
                for c in line:
                    if nX < NUM_COLS:
                        state[nX][nY] = c
                    nX = nX + 1
                nY = nY + 1
            if line.find("Current-State") != -1:
                bflag = True
    return state


# Save State-File to disk
def writeStateSpace(filename, nMove, sPlayer, sMove, state):
    with open(filename, 'w') as file:
        file.write(f"Moves-Played: {nMove}\n")
        file.write(f"Last-Move: {sPlayer} {sMove}\n")
        file.write("\n")
        file.write("Current-State:\n")
        for y in range(NUM_ROWS):
            for x in range(NUM_COLS):
                file.write(str(state[x][y]))
            file.write("\n")


# Print State on Screen
def printState(state):
    print("State")
    for y in range(NUM_ROWS):
        for x in range(NUM_COLS):
            print(state[x][y] if state[x][y] != SPACE else '.', end="")
        print('')


def drawState(state):
    global fig
    global ax
    global TEAM_XX
    global TEAM_YY
    ax.cla()
    circle = plt.Circle((6, 5), 40, color='b')
    ax.add_artist(circle)
    for y in range(NUM_ROWS):
        for x in range(NUM_COLS):
            scol = 'w'
            if state[x][y] == PLAYER_A:
                scol = 'r'
            if state[x][y] == PLAYER_B:
                scol = 'y'
            circle1 = plt.Circle((x + 1, NUM_ROWS - y), 0.4, color=scol)
            ax.add_artist(circle1)
    plt.axis([0, NUM_COLS + 1, 0, NUM_ROWS + 1])
    plt.yticks([i + 1 for i in range(NUM_ROWS)])
    plt.xticks([i + 1 for i in range(NUM_COLS)])
    # Create offset transform by 5 points in x direction
    ax.set_xticklabels([str(i + 1) for i in range(NUM_COLS)])
    ax.set_yticklabels([str(i + 1) for i in range(NUM_ROWS)])
    dx = 28 / 72.
    dy = 0 / 72.
    # apply offset transform to all x ticklabels.
    for label in ax.xaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + ScaledTranslation(dx, dy, fig.dpi_scale_trans))
    for label in ax.yaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + ScaledTranslation(dy, dx, fig.dpi_scale_trans))
    ax.tick_params(axis=u'both', which=u'both', length=0)
    plt.tight_layout()
    fig.savefig(f'./5GewinntState_{TEAM_XX}_{TEAM_YY}.png')


# Lets Player X do its Move
def movePlayer(programname, player, state):
    global nMOVES
    global lMOVES
    global bFlippedPlayerA
    global bFlippedPlayerB
    global draw
    file_name = f"LastAction_Player{player}.txt"
    os.system(programname + f" 5GewinntState.txt {file_name} &")
    time.sleep(1.1)
    check_kill_process(file_name)
    move = readMove(file_name)
    if move == '-999':
        return f"Player {player} did not provide information on its next move in time - disqualified"
    os.remove(file_name)
    nMOVES = nMOVES + 1
    if move.lower() == 'flip':
        if (player == PLAYER_A and bFlippedPlayerA) or (player == PLAYER_B and bFlippedPlayerB):
            return f"Player {player} tried to flip board a second time - disqualified"
        print(f"Player {player} flips board")
        flip(state)
        lMOVES.append(f"Player {player}: flipped")
        if player == PLAYER_A:
            bFlippedPlayerA = True
        if player == PLAYER_B:
            bFlippedPlayerB = True
    else:
        print(f"Player {player} puts coin to row {move}")
        lMOVES.append(f"Player {player}: {move}")
        try:
            if not addCoin(state, int(move), player):
                return f"Player {player} tried to put a coin where one should not - disqualified"
        except ValueError:
            return f"Player {player} tried to put a coin where one should not - disqualified"
    writeStateSpace("5GewinntState.txt", nMOVES, player, move, state)
    printState(state)
    if draw:
        drawState(state)
    return ''


##########################################
# Main Program
# Usage: python 5Gewinnt.py PROGRAM_PLAYER_A PROGRAM_PLAYER_B
##########################################
if len(sys.argv) != 3 and len(sys.argv) != 5:
    print("Invalid usage:")
    print("Usage: python 5Gewinnt.py PROGRAM_PLAYER_A PROGRAM_PLAYER_B")
    print("Usage: python 5Gewinnt.py PROGRAM_PLAYER_A PROGRAM_PLAYER_B TEAM_XX TEAM_YY")
    exit(0)
PROGRAM_PLAYER_A = f'{sys.argv[1]}'
PROGRAM_PLAYER_B = f'{sys.argv[2]}'
draw = len(sys.argv) == 5
if draw:
    TEAM_XX = f'{sys.argv[3]}'
    TEAM_YY = f'{sys.argv[4]}'

nMOVES = 0
lMOVES = []
bFlippedPlayerA = False
bFlippedPlayerB = False

fig, ax = plt.subplots()  # note we must use plt.subplots, not plt.subplot


def makeMove(program, player, state):
    result = movePlayer(program, player, state)
    if result != '':
        print(result)
        # A or B were disqualified
        if "Player A" in result:
            win_file.write(PLAYER_B)
        else:
            win_file.write(PLAYER_A)
        sys.exit()
    if isDraw(state):
        print("Draw Game")
        win_file.write("Draw")
        sys.exit()
    winner = hasWon(state)
    if winner == PLAYER_A:
        print(f"Player {PLAYER_A} won")
        win_file.write(PLAYER_A)
        sys.exit()
    if winner == PLAYER_B:
        print(f"Player {PLAYER_B} won")
        win_file.write(PLAYER_B)
        sys.exit()


# Create Empty Board
current_state = [[SPACE for y in range(NUM_ROWS)] for x in range(NUM_COLS)]
writeStateSpace("5GewinntState.txt", nMOVES, 'nobody', -1, current_state)

with open("Win.txt", 'w') as win_file:
    for _ in range(MAX_MOVES // 2):
        # Player A
        makeMove(PROGRAM_PLAYER_A, PLAYER_A, current_state)
        # Player B
        makeMove(PROGRAM_PLAYER_B, PLAYER_B, current_state)

sys.exit()
