import random

SIZE = 4

room = [[random.randint(0, 1) for _ in range(SIZE)] for _ in range(SIZE)]

memory = [[False for _ in range(SIZE)] for _ in range(SIZE)]

x, y = 0, 0

moves = []


def print_room():
    for i in range(SIZE):
        for j in range(SIZE):

            if i == x and j == y:
                print("A", end=" ")

            elif room[i][j] == 1:
                print("D", end=" ")  

            else:
                print("C", end=" ")  
        print()

    print("-" * 25)


def is_clean():
    for row in room:
        if 1 in row:
            return False
    return True


# Hàm di chuyển
def P_move(direction):
    global x, y

    if direction == "RIGHT" and y < SIZE - 1:
        y += 1
        moves.append("RIGHT")

    elif direction == "LEFT" and y > 0:
        y -= 1
        moves.append("LEFT")

    elif direction == "UP" and x > 0:
        x -= 1
        moves.append("UP")

    elif direction == "DOWN" and x < SIZE - 1:
        x += 1
        moves.append("DOWN")


def is_valid(nx, ny):
    return 0 <= nx < SIZE and 0 <= ny < SIZE


def find_unvisited_neighbor():

    directions = [
        ("RIGHT", x, y + 1),
        ("DOWN", x + 1, y),
        ("LEFT", x, y - 1),
        ("UP", x - 1, y)
    ]

    for direction, nx, ny in directions:

        if is_valid(nx, ny) and not memory[nx][ny]:
            return direction

    return None


print("TRẠNG THÁI BAN ĐẦU")
print_room()


while not is_clean():

    memory[x][y] = True

    if room[x][y] == 1:

        print(f"SUCK at ({x},{y})")

        room[x][y] = 0
        moves.append("SUCK")

    else:

        direction = find_unvisited_neighbor()

        if direction:
            P_move(direction)

        else:

            moved = False

            for i in range(SIZE):
                for j in range(SIZE):

                    if not memory[i][j]:

                        while x < i:
                            P_move("DOWN")

                        while x > i:
                            P_move("UP")

                        while y < j:
                            P_move("RIGHT")

                        while y > j:
                            P_move("LEFT")

                        moved = True
                        break

                if moved:
                    break

    print_room()


print("HOÀN THÀNH LÀM SẠCH!")

print("\nMEMORY:")
for row in memory:
    print(row)

print("\nMOVES:")
print(moves)