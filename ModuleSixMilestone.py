#  Eden Simmons for IT140 @ SNHU

if __name__ == '__main__':
    # A dictionary for the simplified dragon text game
    # The dictionary links a room to other rooms.
    rooms = {
        'Dark Wizard\'s Chamber': {
            'villain': True
        },
        'Entryway': {},
        'South Hall': {
            'items': {
                0: {
                    'item_name': 'Magenta Crystal',
                    'map_text': 'A magenta crystal glows gently as it floats in the '
                                'middle of the hall, almost welcoming you to this place.'
                 }
            }
        },
        'North Hall': {
            'inspect_text': 'You feel a dangerous energy, perhaps you should tread lightly.',
            'items': {
                0: {
                    'item_name': 'Red Crystal'
                }
            }
        },
        'Great Chamber': {
            'items': {
                0: {
                    'item_name': 'Black Crystal',
                    'requires_all': True  # As a little bonus, the black crystal must be collected last.
                }
            }
        },
        'Conservatory': {
            'items': {
                0: {
                    'item_name': 'Green Crystal'
                }
            }
        },
        'Workshop': {
            'items': {
                0: {
                    'item_name': 'Blue Crystal'
                }
            }
        },
        'Library': {
            'items': {
                0: {
                    'item_name': 'Cyan Crystal'
                }
            }
        },
        'Alchemy Room': {
            'items': {
                0: {
                    'item_name': 'Yellow Crystal'
                }
            }
        },
    }

    #  I plan on implementing a simple 2D coordinate system using [x][y]
    #  (0,0) is top left corner. X+ is east, Y+ is south.
    #  Rooms will be retained and used to store items
    map_size_x = 3
    map_size_y = 5
    game_map = [[0 for y in range(map_size_y)] for x in range(map_size_x)]

    #  Create room layout. These can/will reference the rooms dictionary, they must match.
    #  Pycharm isn't a fan of [][] syntax here, not sure why.
    game_map[1][0] = 'Dark Wizard\'s Chamber'
    game_map[1][1] = 'North Hall'
    game_map[1][2] = 'Great Chamber'
    game_map[1][3] = 'South Hall'
    game_map[1][4] = 'Entryway'
    game_map[0][1] = 'Conservatory'
    game_map[0][2] = 'Workshop'
    game_map[2][2] = 'Library'
    game_map[2][3] = 'Alchemy Room'

    #  I want to allow some typical shorthand. I'm allowing up/down/etc. since the map is 2D
    synonyms = {
        #  Commands
        'move': ('move', 'go', 'walk', 'run'),
        'quit_game': ('quit', 'exit'),
        'look': ('explore', 'map', 'look', 'where'),
        'collect': ('collect', 'take', 'get'),

        #  Directions
        'north': ('north', 'n', 'up'),
        'south': ('south', 's', 'down'),
        'east': ('east', 'e', 'right'),
        'west': ('west', 'w', 'left'),

        # System
        'yes': ('yes', 'y'),
        'no': ('no', 'n')

    }

    #  This is a direction -> x/y coordinate lookup. + sign is only there for clarity.
    #  These can/will refer to synonyms, they must match.
    math_directions = {
        'north': (0, -1),
        'south': (0, +1),
        'east':  (+1, 0),
        'west':  (-1, 0)
    }

    #  Player starting data
    player = {
        'x': 1,
        'y': 4,
        'inventory': []
    }

    def get_input_lower():  # Forces input to lowercase to simplify comparisons
        return str(input().lower())

    def invalid_input(text):  # Simply prints invalid input. *text returns any .split() back into a full string
        print(*text, 'is not a valid input.')

    def get_current_room():
        return game_map[player['x']][player['y']]  # Returns current room name from the game map.

    def get_room_items(room):
        return rooms[room]['items'].values()  # Returns a list of all items in a room.

    def check_room_items(verbose = False):
        if 'items' in rooms[get_current_room()].keys():
            for item in get_room_items(get_current_room()):
                if 'map_text' in item:
                    print(item['map_text'])
                else:
                    print(item['item_name'])
        elif verbose:
            print('You see nothing of value here.')

    def check_room_exists(x, y):  # Tests if a room exists given an x,y coordinate
        if (x < 0) or (x > map_size_x-1) or (y < 0) or (y > map_size_y-1):  # Python lists wrap, this cancels that out.
            return False
        else:
            try:
                return bool(game_map[x][y])
            except IndexError:  # This error shouldn't happen, but it means there isn't a room in that location.
                return False

    #  This function iterates over all possible movement directions and presents them to the player as a nice string.
    def find_valid_directions(x, y):
        valid_directions = []
        for direction, math_tuple in math_directions.items():  # For each possible direction in math_directions
            if check_room_exists(x + math_tuple[0], y + math_tuple[1]):  # Check if there is a room
                valid_directions.append(direction)  # If there is a room, add it to the list of valid directions.
        if not valid_directions:
            print('There\'s nowhere to go!')  # This shouldn't be possible, but let the player know they're stuck.
            return
        elif len(valid_directions) > 1:  # If there's more than one possible direction,
            print('There are exits to the', end=' ')
            for index, direction in enumerate(valid_directions):
                if index < len(valid_directions)-1:  # Print almost all directions
                    print('{}{}'.format(
                        direction,
                        (index < len(valid_directions)-1) * ','),  # This adds commas to long direction lists.
                        end=' ')
                    if index == len(valid_directions)-2:
                        print('and', end=' ')  # Proper grammar before the last direction.
                else:
                    print('{}.'.format(direction))
        else:
            print('There is an exit to the {}.'.format(valid_directions[0]))  # If there's only one option it's free.

    def print_current_room(verbose = False):
        print('You are in the {}.'.format(
            get_current_room()
        ))
        if 'inspect_text' in rooms[get_current_room()]:
            print(rooms[get_current_room()]['inspect_text'])
        # if verbose:
            # FIXME: Define verbosity
        check_room_items(verbose)
        find_valid_directions(player['x'], player['y'])  # Prints all available directions.

    def offer_quit():  # Gives the player a chance to cancel quitting with a yes/no prompt.
        print('Your journey isn\'t over yet!')
        while True:
            print('Are you sure you want to quit? (y/n)')
            quit_input = get_input_lower().split(' ')
            if quit_input[0] in synonyms['yes']:  # If yes, quit.
                quit()
            elif quit_input[0] in synonyms['no']:  # If no, leave the offer_quit prompt.
                return
            else:  # If invalid, warn the player and stay in the offer_quit prompt
                invalid_input(quit_input)

    def attempt_move(player_input):
        # Iterate over all valid movement directions in math_directions
        for direction, math_tuple in math_directions.items():
            if player_input[0] in synonyms[direction]:  # Check if the player requested this direction
                if check_room_exists(player['x'] + math_tuple[0], player['y'] + math_tuple[1]):  # Is there a room?
                    player['x'] = player['x'] + math_tuple[0]  # Move player
                    player['y'] = player['y'] + math_tuple[1]
                    print_current_room()  # Tell the player where they are.
                    return
                else:  # If there isn't a room in that direction, warn the player.
                    print('You can\'t go that way!')
                    return
        invalid_input(player_input)  # The function will return away from this warning if a valid direction occurs.

    def input_loop():  # Main player input loop
        print('What do you want to do?')
        player_input = get_input_lower().split(' ')
        if player_input[0] in synonyms['move']:
            attempt_move(player_input[1:])
        elif player_input[0] in synonyms['look']:
            print_current_room(True)
        elif player_input[0] in synonyms['collect']:
            print('What are you, a thief?')
        elif player_input[0] in synonyms['quit_game']:
            offer_quit()
        elif player_input[0] in ['debug']:  # FIXME: This is for debugging.
            print(game_map)
            print(player)
        else:
            invalid_input(player_input)

    #  The game loop is currently handled within the input_loop() function, this triggers it.
    print_current_room()  # Print the player location once to start.
    while True:
        input_loop()
