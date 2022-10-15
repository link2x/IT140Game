# Eden Simmons for IT140

if __name__ == '__main__':
    #
    # This is the full set of rooms before being placed within the map.
    # This space is used for descriptions, items, and flags.
    #
    # Flags:
    #   villain: Enables the villain check and win/lose condition.
    #   block_entry: Explicitly denies entry FROM directions.
    #   description: A description of the room that appears on entry or when the player inspects the room.
    #   inspect_text: Extra text that appears when the player inspects the room. (VERBOSE)
    #   items: A list of items within a room.
    #       item_name: The name of an item within the inventory, used in map description if there's no map_text.
    #       map_text: The description used when an item is in the world.
    #       require_all: Item can only be collected if all other items are in the inventory.
    #
    rooms = {
        'Dark Wizard\'s Chamber': {
            'villain': True
        },
        'Entryway': {
            'description': 'You stand in front of the Dark Wizard\'s hideout.\n'
                           'A large door stands before you, slightly ajar.'
        },
        'South Hall': {
            'description': 'A warm mahogany hallway almost invites you to this place.\n'
                           'There is a small door to the east, and the entryway to the south.\n'
                           'To the north, the hallway gives way to a massive room.',
            'items':
                [{
                    'item_name': 'Magenta Crystal',
                    'map_text': 'A Magenta Crystal glows gently as it floats in the '
                                'middle of the hall, almost welcoming you to this place.'
                 }]
        },
        'North Hall': {
            'description': 'The north hallway. This room feels heavier than the others.\n'
                           'You hear movement in the room to the north.\n'
                           'A glass doorway presents a greenhouse to the west.\n'
                           'In the south, the hallway gives way to a massive room.',
            'inspect_text': 'You feel a dangerous energy, perhaps you should tread lightly.',
            'items':
                [{
                    'item_name': 'Red Crystal',
                    'map_text': 'A deep Red Crystal illuminates the hall with a dark, foreboding energy.'
                }]
        },
        'Great Chamber': {
            'description': 'The great chamber is a massive space dominating the hideout.\n'
                           'A strange mechanism is built within the walls and floor, with a small door to the east.\n'
                           'The north and south are flanked by smaller hallways.',
            'items':
                [{
                    'item_name': 'Black Crystal',
                    'map_text': 'A large Black Crystal is lodged in the floor. It looks like it\'s been there forever.',
                    'requires_all': True,  # As a little bonus, the black crystal must be collected last.
                    'fail_text': 'The Black Crystal resists your grasp. Perhaps you need to be more powerful first?'
                }]
        },
        'Conservatory': {
            'description': 'You stand within a beautiful conservatory,'
                           'with every herb you could ever need around you.\n'
                           'A glass door sits to the east, showing the north hallway beyond.\n'
                           'To the south, there is a ramp upwards leading to some kind of workspace.',
            'items':
                [{
                    'item_name': 'Green Crystal',
                    'map_text': 'All the plants in the room face a vine-covered Green Crystal '
                                'that seems to fill the space with a humid warmth.'
                }]
        },
        'Workshop': {
            'description': 'Spartan work-surfaces make it apparent that you\'re in a workshop of sorts.\n'
                           'A ramp descends north into the conservatory.\n'
                           'To the east, a balcony overlooks the great chamber. You think you can jump down safely.',
            'block_entry': ['east'],
            'items':
                [{
                    'item_name': 'Blue Crystal',
                    'map_text': 'On a workbench you spot a Blue Crystal, waiting to be put to use.'
                }]
        },
        'Library': {
            'description': 'A tall but inviting library. The walls are coated in literature.\n'
                           'A small door is to the west, and an archway opens to the south.',
            'items':
                [{
                    'item_name': 'Cyan Crystal',
                    'map_text': 'A Cyan Crystal pulses slowly, illuminating the library in a soft light.'
                }]
        },
        'Alchemy Room': {
            'description': 'Colored fluids, glassware, flame. This is an alchemist\'s workspace.\n'
                           'To the north an archway opens to a library.\n'
                           'A small door sits on the west wall.',
            'items':
                [{
                    'item_name': 'Yellow Crystal',
                    'map_text': 'A Yellow Crystal blinks violently, it\'s chaotic energy '
                                'powering some kind of reaction unknown to you.'
                }]
        },
    }

    # I plan on implementing a simple 2D coordinate system using [x][y]
    # (0,0) is top left corner. X+ is east, Y+ is south.
    # Rooms will be retained and used to store items and flags.
    map_size_x = 3
    map_size_y = 5
    game_map = [[0 for y in range(map_size_y)] for x in range(map_size_x)]

    # Create room layout. These can/will reference the 'rooms' dictionary, they must match.
    # Pycharm isn't a fan of [][] syntax here, not sure why.
    game_map[1][0] = 'Dark Wizard\'s Chamber'
    game_map[1][1] = 'North Hall'
    game_map[1][2] = 'Great Chamber'
    game_map[1][3] = 'South Hall'
    game_map[1][4] = 'Entryway'
    game_map[0][1] = 'Conservatory'
    game_map[0][2] = 'Workshop'
    game_map[2][2] = 'Library'
    game_map[2][3] = 'Alchemy Room'

    # I want to allow some typical shorthand. I'm allowing up/down/etc. since the map is 2D
    synonyms = {
        # Commands
        'move': ('move', 'go', 'walk', 'run'),
        'quit_game': ('quit', 'exit', 'leave'),
        'look': ('look', 'explore', 'map', 'where', 'l'),
        'collect': ('collect', 'take', 'get'),
        'inventory': ('inventory', 'inv', 'i'),
        'help': ('help', 'commands', '?'),

        # Directions
        'north': ('north', 'n', 'up'),
        'south': ('south', 's', 'down'),
        'east': ('east', 'e', 'right'),
        'west': ('west', 'w', 'left'),

        # System
        'yes': ('yes', 'y'),
        'no': ('no', 'n')

    }

    # This is the descriptive text when the player calls help 'command'.
    help_text = {
        'move': 'Move around the world.',
        'quit_game': 'Quit the game.',
        'look': 'Inspect the current room.',
        'collect': 'Attempt to collect an item from the world.',
        'inventory': 'Check current inventory.',
        'help': 'Lists all available commands. Use help \'command\' to see details.'
    }

    # This is a direction -> x/y coordinate lookup. + sign is only there for clarity.
    # These can/will refer to synonyms, they must match.
    math_directions = {
        'north': (0, -1),
        'south': (0, +1),
        'east':  (+1, 0),
        'west':  (-1, 0)
    }

    # This is a semantic lookup.
    # Describes direction from the perspective of where we're looking instead of where we are.
    from_direction = {
        'north': 'south',
        'south': 'north',
        'east': 'west',
        'west': 'east'
    }

    # Player starting data
    player = {
        'x': 1,
        'y': 4,
        'inventory': []
    }

    def print_help(command='', verbose=False):
        # print_help() can either list all commands, or describe individual commands.
        if command:
            if command == 'quit':  # FIXME: help 'command' ignores synonyms, breaking quit_game
                command = 'quit_game'
            if command in synonyms:
                print(synonyms[command][0])
                print(help_text[command])
                print('Alternatives: {}'.format(synonyms[command][1:]))
                return
            else:
                print('{} is either not a valid command or is a shorthand.'.format(command))
                return
        if not verbose:
            print('Valid commands (type help \'command\' for details):')
            for command in ['move', 'quit_game', 'look', 'collect', 'inventory', 'help']:
                print(synonyms[command][0], end=' ')
            print()
            return
        for command in ['move', 'quit_game', 'look', 'collect', 'inventory', 'help']:
            print('{} - {}'.format(synonyms[command][0], help_text[command]))

    def get_input_lower():  # Forces input to lowercase to simplify comparisons
        return str(input().lower())

    def invalid_input(text):  # Simply prints invalid input. *text returns any .split() back into a full string
        print(*text, 'is not a valid input.')

    def get_current_room():
        return game_map[player['x']][player['y']]  # Returns current room name from the game map.

    def get_room_items(room):
        return rooms[room]['items']  # Returns a list of all items in a room.

    def check_room_items(verbose=False):  # Inspects the current room and lists all items.
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

    def check_room_blocked(direction, x, y):
        movement_tuple_x = math_directions[direction][0]
        movement_tuple_y = math_directions[direction][1]
        map_room_to_check = game_map[x + movement_tuple_x][y + movement_tuple_y]
        # Rooms block entry from the inside out. This function tests if there is a wall preventing movement.
        if 'block_entry' in rooms[map_room_to_check]:
            if from_direction[direction] in rooms[map_room_to_check]['block_entry']:
                return True
        return False

    #  This function iterates over all possible movement directions and presents them to the player as a nice string.
    def find_valid_directions(x, y):
        valid_directions = []
        for direction, math_tuple in math_directions.items():  # For each possible direction in math_directions
            if check_room_exists(x + math_tuple[0], y + math_tuple[1]):  # Check if there is a room
                if not check_room_blocked(direction, x, y):
                    # If there is a room, add it to the list of valid directions.
                    valid_directions.append(direction)
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

    def print_current_room(verbose=False):
        print('You are in the {}.'.format(
            get_current_room()
        ))
        if 'description' in rooms[get_current_room()]:
            print(rooms[get_current_room()]['description'])
        if verbose:  # There may be extra text for players who want to look closer.
            if 'inspect_text' in rooms[get_current_room()]:
                print(rooms[get_current_room()]['inspect_text'])
        check_room_items(verbose)
        find_valid_directions(player['x'], player['y'])  # Prints all available directions.

    def print_current_inventory():
        print('You check your pockets and see:')
        for position, item in enumerate(player['inventory']):
            if position < len(player['inventory']) - 2:
                print('{}, '.format(item['item_name']), end='')
            elif position < len(player['inventory']) - 1:
                print('{} '.format(item['item_name']), end='')
            else:
                print('{}.'.format(item['item_name']))
            if (position > len(player['inventory']) - 3) and (position < len(player['inventory']) - 1):
                print('and ', end='')
        if not len(player['inventory']):
            print('Absolutely nothing.')

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

    def check_villain():
        if 'villain' in rooms[get_current_room()]:
            print('-' * 32)
            print('You enter the dark wizard\'s lair.')
            print('He looks at you and scoffs, boasting that you will never be strong enough to defeat him.')
            if len(player['inventory']) > 6:  # Better: compare items to required items.
                print('It is then that he notices the energy of the crystals around you.\n',
                      'Melding them together, you cast a potent spell and banish the dark wizard from the land.\n',
                      'He attempts to put up a fight, but is no match to your power.\n',
                      'You win.')
                quit()
            else:
                print('It is then that you notice the door behind you is gone. There is no turning back.\n',
                      'The dark wizard rises from his throne, floating in the air in',
                      'front of you as a wind rushes through the room.\n',
                      'As the wind becomes heavy, the flames lighting the room',
                      'go out and you are plunged into darkness.\n',
                      'You lose.')
                quit()

    def attempt_move(player_input):
        # Iterate over all valid movement directions in math_directions
        x = player['x']
        y = player['y']
        for direction, math_tuple in math_directions.items():
            if player_input[0] in synonyms[direction]:  # Check if the player requested this direction
                # Check if there is a room and that this entryway is not blocked.
                if check_room_exists(x + math_tuple[0], y + math_tuple[1]) and not check_room_blocked(direction, x, y):
                    player['x'] = x + math_tuple[0]  # Move player
                    player['y'] = y + math_tuple[1]
                    print_current_room()  # Tell the player where they are.
                    check_villain()
                    return
                else:  # If there isn't a room in that direction, warn the player.
                    print('You can\'t go that way!')
                    return
        invalid_input(player_input)  # The function will return away from this warning if a valid direction occurs.

    def attempt_take(player_input):
        if 'items' not in rooms[get_current_room()]:
            print('There\'s nothing to take here.')
            return
        if not player_input:
            print('You grab the air. Nothing of value happens.')
            return
        for position, item in enumerate(rooms[get_current_room()]['items']):
            if player_input[0] in item['item_name'].lower():
                if 'requires_all' in item:
                    if ((item['requires_all']) and (len(player['inventory']) > 5)) or (not item['requires_all']):
                        player['inventory'].append(rooms[get_current_room()]['items'].pop(position))
                        print('You take the {}.'.format(item['item_name']))
                    else:
                        print(item['fail_text'])
                    return
                else:
                    player['inventory'].append(rooms[get_current_room()]['items'].pop(position))
                    print('You take the {}.'.format(item['item_name']))
                    return
        print('There is no {} to take.'.format(*player_input))
        return

    def show_instructions():
        print('The Dark Wizard\'s Stand')
        print('-' * 32)
        print('Objective: Collect the 7 magic crystals and use their power to defeat the dark wizard.')

    def main():  # Main player input loop
        print('-' * 32)
        print('What do you want to do?')
        player_input = get_input_lower().split(' ')
        if player_input[0] in synonyms['move']:
            attempt_move(player_input[1:])
        elif player_input[0] in synonyms['look']:
            print_current_room(True)
        elif player_input[0] in synonyms['collect']:
            attempt_take(player_input[1:])
        elif player_input[0] in synonyms['inventory']:
            print_current_inventory()
        elif player_input[0] in synonyms['help']:
            if len(player_input) > 1:
                print_help(command=player_input[1])
            else:
                print_help(verbose=True)
        elif player_input[0] in synonyms['quit_game']:
            offer_quit()
        else:
            invalid_input(player_input)

    #  The game loop is currently handled within the main() function, this triggers it.
    show_instructions()
    print_help()  # Tell the player all the basic commands
    print('-' * 32)
    print_current_room()  # Print the player location once to start.
    while True:
        main()
