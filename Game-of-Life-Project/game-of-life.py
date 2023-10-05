#to run the code, navigate to file in command line and then type
#python3 game-of-life.py --<still><travelling><oscillating><glidergun>
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time 
import argparse
##plt.imshow(map, ecoltent=[0,90,0,90])

##points =plt.ginput(1)
##plt.show()
##print(points[0].indecol(1))

def neighbors(map, row, col):
    sum = 0
    if col == 0 and (row!= 0 and row != size - 1):
        sum = map[row+1][col] + map[row-1][col] + map[row-1][col+1] + map[row+1][col+1] + map[row][col+1]
    elif col == 0 and (row == size - 1):
       sum =  map[row-1][col] + map[row-1][col+1] + map[row][col+1]
    elif (col != 0 and col != size-1)and row == size-1 :
        sum =  map[row-1][col-1] + map[row-1][col] + map[row-1][col+1] + map[row][col+1] + map[row][col-1]
    elif col == size - 1 and row == size-1:
        sum =  map[row-1][col-1] + map[row-1][col] + map[row][col-1]
    elif col == size - 1 and ( row!= size - 1 and row!= 0 ):
        sum =  map[row-1][col-1] + map[row-1][col] + map[row][col-1] + map[row+1][col-1] + map[row+1][col]
    elif col == size - 1 and row== 0:
        sum = map[row][col-1] + map[row+1][col-1] + map[row+1][col]
    elif  row== 0 and (col != 0 and col != size - 1):
       sum = map[row][col+1] + map[row][col-1] + map[row+1][col-1] + map[row+1][col] + map[row+1][col+1]
    elif col == 0 and row== 0:
        sum = map[row][col+1] + map[row+1][col] + map[row+1][col+1]
    else:
        sum = map[row-1][col-1] + map[row-1][col] + map[row-1][col+1] + map[row][col+1] + map[row][col-1] + map[row+1][col-1] + map[row+1][col] + map[row+1][col+1]
    return sum
def travelling(map):
    map[1][2] = 1
    map[3][1] = 1
    map[3][2] = 1
    map[2][3] = 1
    map[3][3] = 1
    return map
def glider_gun(map):
    map[6][5] = 1
    map[6][6] = 1
    map[7][5] = 1
    map[7][6] = 1
    map[6][15] = 1
    map[4][18] = 1
    map[4][17] = 1
    map[5][16] = 1
    map[6][15] = 1
    map[7][15] = 1
    map[8][15] = 1
    map[9][16] = 1
    map[10][17] = 1
    map[10][18] = 1

    map[7][19] = 1
    map[7][21] = 1
    map[7][22] = 1
    map[6][21] = 1
    map[8][21] = 1
    map[5][20] = 1
    map[9][20] = 1

    map[5][25] = 1
    map[5][26] = 1
    map[4][25] = 1
    map[4][26] = 1
    map[6][25] = 1
    map[6][26] = 1
    map[3][27] = 1
    map[7][27] = 1
    map[3][29] = 1
    map[2][29] = 1
    map[7][29] = 1
    map[8][29] = 1

    map[4][39] = 1
    map[4][40] = 1
    map[5][39] = 1
    map[5][40] = 1
    

    return map
def random(N):
    return np.random.randint(2, size = (N, N))
def still(map):
    map[3][1] = 1
    map[2][2] = 1
    map[2][3] = 1
    map[3][4] = 1
    map[4][2] = 1
    map[4][3] = 1
    return map
def oscillating(map):
    map[1][1] = 1
    map[1][2] = 1
    map [1][3] = 1
    return map
def update(frame, img, map):
    tmp = map.copy()
    for row in range(0, size - 1):
            for col in range(0, size - 1):
            #put neigth
                if (neighbors(map, row, col) == 1):
                    tmp[row][col] = 0
                elif neighbors(map, row, col) >= 4: 
                    tmp[row][col] = 0
                elif (neighbors(map, row, col) == 2 or neighbors(map, row, col) == 3) and map [row][col] == 1:
                    tmp[row][col] = 1
                elif neighbors(map, row, col) == 3 and map[row][col] == 0:
                    tmp[row][col] = 1
                else: 
                    tmp[row][col] = 0
    img.set_data(tmp)
    map[:] = tmp[:]
    return img,

def main():
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--map-size', dest='N', required=False)
    parser.add_argument('--still', action='store_true', required=False)
    parser.add_argument('--travelling', action='store_true', required=False)
    parser.add_argument('--oscillating', action='store_true', required=False)
    parser.add_argument('--glidergun', action='store_true', required=False)

    args = parser.parse_args()
    global map 
    global size 
    if args.N and int(args.N) > 0: 
        size = int(args.N)
    else: 
        size = 100
    iters = 10
    map = np.zeros((size, size))
    if args.still: 
        map = still(map)
    elif args.oscillating:
        map = oscillating(map)
    elif args.travelling: 
        map = travelling(map)
    elif args.glidergun: 
        map = glider_gun(map)
    else: 
        map = random(size)
    print(map)
    fig, ax = plt.subplots()
    img = ax.imshow(map, interpolation = 'nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, map),
                                  frames = 10,
                                  interval= 100,
                                  save_count=50)
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])
    plt.show()
    for i in range(0, iters):
        map = update(img, map)
        print(map)
if __name__ == "__main__":
    main()
