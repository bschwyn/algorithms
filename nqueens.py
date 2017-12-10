

def createboard(n):
    b = []
    for i in range(n):
        b.append([0]*n)
    return b

def printboard(b):
    print('')
    for row in b:
        print(''.join(map(str, row)))


def nqueens(n, row, board):
    if sum(board[n-1]) == 1:
        print(board)
        return True

    #check and see if i, j is a spot that works for a queen
    #check i

    #try all columns in current row. For each tried column do the following:
        #a) if the queen can be safely placed in this column, then mark [row, column]
        # as part of the solution and recursively check if placing the queen leads
        # to a soln
        # figure out what "recursively check soln means"
        #b) if placing queen in [row, column] leads to a solution then return true
            # how is this different from the first all queens placed?
        #c if placing queen doesn't lead to a solution, then unmark this [row [column]
        # backtrack and go to step a to try other columns
    # if all rows have been tried and nothing worked, return false to triger backtracking

    for j in range(n): #try all columns
        locationOk = True
        #check if row, column ok
        for i in range(0,row):
            if board[i][j] == 1:
                locationOk = False
            #5,7 check 4,6, 2,4 1,3, 0,2

            if i + j - row > -1 and board[i][i + j- row] == 1:
                locationOk = False
            #5,7 check 4,8, 3, 10 4 (8 - 2
            if j + row - i < n and board[i][j + row -i] == 1:
                locationOk = False
        if locationOk:
            board[row][j] = 1
            printboard(board)
            soln_ok = nqueens(n, row+1, board)
            if not soln_ok:
                board[row][j] = 0
                printboard(board)
        if sum(board[n-1]) == 1:
            print(".................................")
            print("..............")
            printboard(board)
            return True
    return False

b = createboard(8)
nqueens(8,0,b)