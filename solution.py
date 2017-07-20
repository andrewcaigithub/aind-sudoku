def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
unit_list = [cross(r, cols) for r in rows] \
            + [cross(rows, c) for c in cols] \
            + [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')] \
            + [[rows[i]+c for i, c in enumerate(cols)], [rows[i]+c for i, c in enumerate(reversed(cols))]]
units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unit_list:
        # Find all instances of naked twins of every unit
        twins = [values[box] for box in unit if len(values[box]) == 2]
        twins = list(set(t for t in twins if twins.count(t) == 2))
        if len(twins) < 1:
            continue
        for twin in twins:
            for box in unit:
                value = values[box]
                if value == twin:
                    continue
                assign_value(values, box, value.replace(twin[0], '').replace(twin[1], ''))
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1' Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    grids = []
    digits = cols
    for c in grid:
        if c in digits:
            grids.append(c)
        elif c == '.':
            grids.append(digits)
    assert(len(grids) == 81)
    return dict(zip(boxes, grids))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in rows:
        print(''.join(values[row + col].center(width) + ('|' if col in '36' else '')
                      for col in cols))
        if row in 'CF':
            print(line)
    print()


def eliminate(values):
    solved_values = [box for box in boxes if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit, ''))
    return values


def only_choice(values):
    for unit in unit_list:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values

    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    print('n: ' + n)
    print('s: ' + s)

    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attemp = search(new_sudoku)
        if attemp:
            return attemp


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    return search(grid_values(grid))
 
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    sudoku = solve(diag_sudoku_grid)
    if sudoku is False:
        print('This sudoku has no solutions.')
    else:
        display(sudoku)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
