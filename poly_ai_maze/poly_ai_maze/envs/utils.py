class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    RED = '\033[32m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m',
    BIGBOLD= '\033[97m'

# Dictionnary to convert the output into colours
CONVERT_COLORS = {0 : bcolors.BOLD + '👣'+ bcolors.ENDC,
               1: bcolors.OKBLUE + '⛹'+ bcolors.ENDC,
               2: bcolors.BIGBOLD + '⬜'+ bcolors.ENDC,
               3 : bcolors.HEADER + '💣'+ bcolors.ENDC,
               4: bcolors.OKGREEN + '🏠'+ bcolors.ENDC,
               5 : bcolors.RED + '➕' + bcolors.ENDC,
               6: bcolors.RED + '🟦' + bcolors.ENDC,
               7: bcolors.RED + '➖' + bcolors.ENDC,
               8: bcolors.RED + '➕' + bcolors.ENDC,
               }

ACTION_CONVERSION = {
    0 : "DOWN",
    1 : 'UP',
    2 : 'RIGHT',
    3 : 'LEFT'
}


POLY_AI = [bcolors.RED + '🟦'*12 + bcolors.ENDC ]

def convert_world(world) :
    """Class that convert the maze into colours"""
    # map = [CONVERT_COLORS[5] + CONVERT_COLORS[7]* (world.shape[0]) + CONVERT_COLORS[8]]
    map = [POLY_AI[0]]
    for i in range(world.shape[0]):
        current_map = CONVERT_COLORS[6]
        for j in range(world.shape[1]) :
            current_map+=CONVERT_COLORS[world[i,j]]
        current_map+=CONVERT_COLORS[6]
        map.append(current_map)
    # map.append(CONVERT_COLORS[5] + CONVERT_COLORS[7] * world.shape[0] + CONVERT_COLORS[8])
    map.append(POLY_AI[0])
    return map


def show_env(world, action):
    out = convert_world(world)
    for line in out:
        print(line)
    if action is not None :
        print(" "*7 +  "({})\n".format(ACTION_CONVERSION[action]))
    return out

def show(text):
    """Show an explicit text."""
    print(bcolors.BIGBOLD + text + bcolors.ENDC)