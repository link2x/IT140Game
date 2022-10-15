# Eden Simmons for IT140 @ Southern New Hampshire University

print_line = ('-' * 32)  # Just a handy decorative line preformatted for output.

# Typical shorthand for text-based adventures.
synonyms = {
        # Commands
        'move': ('move', 'go', 'walk', 'run'),
        'quit_game': ('quit', 'exit', 'leave'),
        'collect': ('collect', 'take', 'get'),
        # Directions
        'north': ('north', 'n', 'up'),
        'south': ('south', 's', 'down'),
        'east': ('east', 'e', 'right'),
        'west': ('west', 'w', 'left'),
    }


def show_instructions():
    print()
    print('The Dark Wizard\'s Stand')
    print(print_line)
    print('Objective: Collect the 7 magic crystals and use their power to defeat the dark wizard.')
    print('To move: go North, go South, go East, go West')
    print('To get items: get \'item name\'')
    print()


def main():
    # Player variables
    player_room = 'Entryway'
    player_items = []

    # Game rooms
    rooms = {
        'Dark Wizard\'s Chamber': {
            'South': 'North Hall',
            'villain': True
        },
        'North Hall': {
            'North': 'Dark Wizard\'s Chamber',
            'West': 'Conservatory',
            'South': 'Great Chamber',
            'item': 'Green Crystal'
        },
        'Great Chamber': {
            'North': 'North Hall',
            'West': 'Workshop',
            'East': 'Library',
            'South': 'South Hall',
            'item': 'Black Crystal'
        },
        'South Hall': {
            'North': 'Great Chamber',
            'East': 'Alchemy Room',
            'South': 'Entryway',
            'item': 'Magenta Crystal'
        },
        'Entryway': {
            'North': 'South Hall'
        },
        'Conservatory': {
            'East': 'North Hall',
            'South': 'Workshop',
            'item': 'Red Crystal'
        },
        'Workshop': {
            'North': 'Conservatory',
            'East': 'Great Chamber',
            'item': 'Blue Crystal'
        },
        'Library': {
            'West': 'Great Chamber',
            'South': 'Alchemy Room',
            'item': 'Cyan Crystal'
        },
        'Alchemy Room': {
            'North': 'Library',
            'West': 'South Hall',
            'item': 'Yellow Crystal'
        }
    }

    def print_status():
        print('You are in the {}.'.format(player_room))  # Display current room
        print('Inventory: {}'.format(player_items))  # Display inventory
        if 'item' in rooms[player_room]:
            print('You see a {}.'.format(rooms[player_room]['item']))  # Display room items if there are any
        print(print_line)

    # Main Gameplay Loop
    show_instructions()
    while True:
        print_status()
        print('What will you do next?')
        player_input = str(input()).lower().split(' ')  # Force player input to lowercase and split words

        # Player Movement
        if player_input[0] in synonyms['move'] and (len(player_input) > 1):
            move_direction = ''

            # I didn't want to lose the 'synonyms' functionality.
            # These convert player input back to valid map directions.
            if player_input[1] in synonyms['north']:
                move_direction = 'North'
            if player_input[1] in synonyms['south']:
                move_direction = 'South'
            if player_input[1] in synonyms['east']:
                move_direction = 'East'
            if player_input[1] in synonyms['west']:
                move_direction = 'West'

            if move_direction:  # Invalid input = '' = false
                if move_direction in rooms[player_room]:  # Check if valid direction
                    player_room = rooms[player_room][move_direction]  # Move player
                else:
                    print('There is no room in that direction!')
            else:
                print('You can\'t move that way!')

        # Player Item Collection
        elif player_input[0] in synonyms['collect'] and (len(player_input) > 1):
            if 'item' in rooms[player_room]:  # If room contains an item
                # And player input matches the item in the room
                if ' '.join(player_input[1:]) == rooms[player_room]['item'].lower():
                    player_items.append(rooms[player_room].pop('item'))  # Move item from room to inventory
                else:
                    print('That item isn\'t here.')
            else:
                print('There are no items here.')

        # Quit Game
        elif player_input[0] in synonyms['quit_game']:
            player_room = 'exit'  # Retains exit code from Module 6 Milestone

        # Invalid Input
        else:
            print('\'{}\' is not a valid input.'.format(' '.join(player_input)))

        print()  # Extra line for spacing between player inputs.

        # Quit if player is in exit room
        if player_room == 'exit':
            quit()

        # If room contains a villain, run win/lose tests
        if 'villain' in rooms[player_room]:  # If villain is defined, check if true
            if rooms[player_room]['villain']:  # The way I implemented the villain flag, this could technically be false
                if len(player_items) >= 7:  # If the player collected the items first, they win
                    print('Congratulations! You have collected all items and defeated the dark wizard!')
                else:
                    print('The dark wizard is too powerful for you! You lose.')  # Otherwise, they lose!
                print('Thanks for playing my game. I hope you enjoyed it.')
                quit()


if __name__ == '__main__':
    main()
