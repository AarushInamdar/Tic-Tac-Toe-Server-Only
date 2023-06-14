import socket
from gameboard import BoardClass

class NotAValidMove(Exception):
    pass

'''Taking input values for the IP and Port'''

def takeHostInputs():
    IP = input('Please input the IP address that you want to connect to:\n')
    port_val = input('Please input the port that you want to connect to:\n')

    IP_val = IP
    port = int(port_val)
    return IP_val, port

IP, port = takeHostInputs()

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

'''send player2 player1s user name, make sure to implement the try again loop'''

try:
    serverSocket.bind((IP, int(port)))
    serverSocket.listen(2)
    conn, address = serverSocket.accept()
    BoardClass.userName = input('Please input your user name:\n')
    conn.sendall(BoardClass.userName.encode())
except:
    tryAgain = input('Connection Failed: do you want to try again?(y/n)\n')
    if tryAgain == 'y':
        IP, port = takeHostInputs()
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((IP, int(port)))
        serverSocket.listen(2)
        conn, address = serverSocket.accept()
        BoardClass.userName = input('Please input your user name:\n')
        conn.sendall(BoardClass.userName.encode())
    elif tryAgain == 'n':
        exit()
        

player2UserName = conn.recv(1024) #trying to receive player 2 username and if they want to play again
player2UserName = player2UserName.decode()

'''User name of the last player to have a turn'''
BoardClass.lastPlayerTurn = player2UserName
'''Number of wins for the current player'''
BoardClass.playerWins = 0
'''Number of ties for the current player'''
BoardClass.playerTies = 0
'''Number of losses for the current player'''
BoardClass.playerLosses = 0
'''Number of games'''
BoardClass.numGames = 0


currGameBoard = [['1','2','3'],['4','5','6'],['7','8','9']]
wantPlay = True
validMoves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
while wantPlay:
    gameOver = False
    placement = 0
    for row in currGameBoard:
        print(row)
    print('')
    while placement not in validMoves:
            placement = input(f'Which block do you want to place your X in from valid move list:{validMoves}? \n')
            try:
                placement = int(placement)
                if placement not in validMoves:
                    raise NotAValidMove
            except(ValueError, NotAValidMove):
                print('That is not a valid move please try again.')

    validMoves.remove(placement)
    '''update current gameboard based on input variable placement'''
    
    BoardClass.updateGameBoard(placement, currGameBoard, 'X')
    for row in currGameBoard:
        print(row)
    print('')
    BoardClass.lastPlayerTurn = BoardClass.userName

    conn.sendall(bytes(str(placement), 'utf8'))

    if BoardClass.isWinner(currGameBoard) == True:
        print(f'{BoardClass.lastPlayerTurn} Won!')
        currGameBoard = BoardClass.resetGameBoard()
        if BoardClass.lastPlayerTurn == BoardClass.userName:
            BoardClass.playerWins += 1
            BoardClass.numGames += 1
            gameOver = True
        else:
            BoardClass.playerLosses += 1
            BoardClass.numGames += 1
            gameOver = True
    else:
        #might be here lol
        if BoardClass.boardIsFull(currGameBoard):
            print('The game tied!')
            BoardClass.playerTies +=1
            currGameBoard = BoardClass.resetGameBoard()    
            BoardClass.numGames += 1
            gameOver = True
    
    '''send updates to player 2 in the form of list of lists and also send current valid moves possible'''
    if not gameOver:
        #conn.sendall(bytes(str(placement), 'utf8'))
        
        '''receive move and validMoves from player 2'''
        Player2Placement = conn.recv(1024)
        Player2Placement = str(Player2Placement, 'utf-8')
        validMoves.remove(int(Player2Placement))
        print('Player 2 placed at block number', Player2Placement)
        BoardClass.updateGameBoard(Player2Placement, currGameBoard, 'O')

        BoardClass.lastPlayerTurn = player2UserName

        '''check for winner or tie, if neither and board is full it is a loss'''
        #probably check if somebody won even after having a move from only player 1
        if BoardClass.isWinner(currGameBoard) == True:
            print(f'{BoardClass.lastPlayerTurn} Won!')
            currGameBoard = BoardClass.resetGameBoard()
            if BoardClass.lastPlayerTurn == BoardClass.userName:
                BoardClass.playerWins += 1
                BoardClass.numGames += 1
                gameOver = True
            else:
                BoardClass.playerLosses += 1
                BoardClass.numGames += 1
                gameOver = True
        # else:
        #     if BoardClass.boardIsFull(currGameBoard):
        #         print('The game tied!')
        #         BoardClass.playerTies +=1
        #         currGameBoard = BoardClass.resetGameBoard()    
        #         BoardClass.numGames += 1
        #         gameOver = True

    '''checking if they want to play again (if not send 'Fun Times')'''

    if gameOver:
        continuePlaying = input('Do you want to continue playing?(y/n)\n')
        if continuePlaying.lower() == 'y':
            conn.sendall('Play Again'.encode())
            validMoves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        elif continuePlaying.lower() == 'n':
            conn.sendall('Fun Times'.encode())
            BoardClass.printStats(BoardClass.userName, BoardClass.lastPlayerTurn, BoardClass.numGames, BoardClass.playerWins, BoardClass.playerLosses, BoardClass.playerTies)
            wantPlay = False
