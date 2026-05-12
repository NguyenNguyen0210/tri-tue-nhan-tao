goal = [
    [1, 2, 3],
    [6, 5, 4],
    [7, 8, 0]
]

state = [
    [1, 3, 5],
    [4, 6, 8],
    [2, 7, 0]
]

MAX_STEPS = 1000

model_memory = {}

moves = []


def print_board(board):
    print("+-------+")

    for row in board:
        cells = " ".join(str(n) if n != 0 else "_" for n in row)
        print(f"| {cells} |")

    print("+-------+")


def find_zero(board):

    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return i, j


def copy_board(board):
    return [row[:] for row in board]


def board_to_key(board):
    return tuple(tuple(row) for row in board)


def move(board, dx, dy):

    x, y = find_zero(board)

    nx, ny = x + dx, y + dy

    if 0 <= nx < 3 and 0 <= ny < 3:

        new_board = copy_board(board)

        new_board[x][y], new_board[nx][ny] = (
            new_board[nx][ny],
            new_board[x][y]
        )

        return new_board

    return None


def score(board):

    count = 0

    for i in range(3):
        for j in range(3):

            if board[i][j] == goal[i][j]:
                count += 1

    return count


DIRECTIONS = [
    (-1,  0, "UP"),
    ( 1,  0, "DOWN"),
    ( 0, -1, "LEFT"),
    ( 0,  1, "RIGHT"),
]


def model_based_agent(board, visited):

    current_key = board_to_key(board)

    # Cập nhật model
    model_memory[current_key] = {
        "score": score(board),
        "visited": True
    }

    best_board = None
    best_score = -1
    best_action = ""

    for dx, dy, action in DIRECTIONS:

        new_board = move(board, dx, dy)

        if new_board is None:
            continue

        new_key = board_to_key(new_board)

        if new_key in visited:
            continue

        s = score(new_board)

        if (
            new_key not in model_memory
            or s > best_score
        ):

            best_score = s
            best_board = new_board
            best_action = action

    return best_board, best_action


def main():

    global state

    print("=" * 40)
    print("   8-PUZZLE — MODEL-BASED REFLEX AGENT")
    print("=" * 40)

    print("\nGOAL STATE:")
    print_board(goal)

    visited = set()

    visited.add(board_to_key(state))

    step = 0
    solved = False

    while step < MAX_STEPS:

        print(f"\n--- STEP {step} ---")

        print_board(state)

        if state == goal:
            solved = True
            break

        new_board, action = model_based_agent(
            state,
            visited
        )

        if new_board is None:

            print("⚠ Agent bị kẹt!")
            break

        print(f"→ ACTION: {action}")

        moves.append(action)

        state = new_board

        visited.add(board_to_key(state))

        step += 1


    print("\n" + "=" * 40)
    print("            FINAL RESULT")
    print("=" * 40)

    print_board(state)

    if solved:
        print(f"✔ Giải thành công sau {step} bước")

    elif step >= MAX_STEPS:
        print("⚠ Vượt quá số bước cho phép")

    else:
        print("✘ Không tìm được lời giải")

    print("\nMOVES:")
    print(moves)

    print("\nMEMORY STATES:")
    print(len(model_memory))


if __name__ == "__main__":
    main()