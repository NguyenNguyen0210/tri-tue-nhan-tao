import random

n = 4
room = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
x, y = 1,1

moves = []


def print_room():
    for i in range(n):
        for j in range(n):
            if i == x and j == y:
                print("A", end=" ")
            else:
                print(room[i][j], end=" ")
        print()
    print("-" * 20)


def is_clean():
    for row in room:
        if 1 in row:
            return False
    return True


def P_move(direction):
    global x, y

    if direction == "RIGHT":
        if y < n - 1:
            y += 1
            moves.append("RIGHT")

    elif direction == "LEFT":
        if y > 0:
            y -= 1
            moves.append("LEFT")

    elif direction == "UP":
        if x > 0:
            x -= 1
            moves.append("UP")

    elif direction == "DOWN":
        if x < n - 1:
            x += 1
            moves.append("DOWN")


print("TRẠNG THÁI BAN ĐẦU")
print_room()

while not is_clean():

    if room[x][y] == 1:
        room[x][y] = 0
        moves.append("SUCK")
        print(f"Hút bụi tại ({x},{y})")

    else:
        if y < n - 1:
            P_move("RIGHT")

        else:
            if x < n - 1:
                P_move("DOWN")

                while y > 0:
                    P_move("LEFT")

    print_room()

print("HOÀN THÀNH!")

print("\nDanh sách moves:")
print(moves)