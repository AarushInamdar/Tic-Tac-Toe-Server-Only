import socket
from gameboard import BoardClass


class NotAValidMove(Exception):
    pass

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Attempt to connect to the server side
def attemptConnection():

    IP = input('Please input the IP address that you want to connect to:\n')
    port_val = input('Please input the port that you want to connect to:\n')
    return IP, port_val

tryAgain = 'y'
while tryAgain == 'y':
    try:
        IP, port_val = attemptConnection()
        serverSocket.connect((IP, int(port_val)))
        tryAgain = 'n'
    except:
        tryAgain = input('Connection Failed: do you want to try again?(y/n)\n')
        if tryAgain == 'y':
            IP, port_val = attemptConnection()
            serverSocket.connect((IP, int(port_val)))
            tryAgain == 'n'
        if tryAgain == 'n':
            exit()


player1UserName = serverSocket.recv(1024)
player1UserName = player1UserName.decode()

BoardClass.userName = 'player2'

serverSocket.send('player2'.encode())


gameOn = True
latestGameBoard = [['1','2','3'],['4','5','6'],['7','8','9']]
currValidMoves = [1, 2, 3, 4, 5, 6, 7, 8, 9]

BoardClass.numGames, BoardClass.playerWins, BoardClass.playerLosses, BoardClass.playerTies = 0, 0, 0, 0

while gameOn:
    
    continueGame = True
    
    

    player1Placement = serverSocket.recv(1024)

    player1Placement = str(player1Placement, 'utf8')
    print('Player 1 placed at block number', player1Placement)
    
    
    BoardClass.updateGameBoard(player1Placement, latestGameBoard, 'X')
    BoardClass.lastPlayerTurn = player1UserName
    currValidMoves.remove(int(player1Placement))

    #here check if game is over, if it is start waiting for the signal from player 1 if they want to play again
    if BoardClass.isWinner(latestGameBoard) or BoardClass.boardIsFull(latestGameBoard):
        if BoardClass.isWinner(latestGameBoard):
            BoardClass.playerLosses += 1
            BoardClass.numGames += 1
            print('Error check: ', BoardClass.playerWins)
        elif BoardClass.boardIsFull(latestGameBoard):
            BoardClass.playerTies +=1    
            BoardClass.numGames += 1
        continueGame = False
        #get blocking, wait for signal from player one if they want to continue and determine break or not from there
        continueDecision = serverSocket.recv(1024)
        continueDecision = continueDecision.decode()
        
        print(BoardClass.numGames, BoardClass.playerWins, BoardClass.playerLosses, BoardClass.playerTies)
        
        if continueDecision == 'Play Again':
            latestGameBoard = BoardClass.resetGameBoard()
            currValidMoves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        elif continueDecision == 'Fun Times':
            BoardClass.printStats(BoardClass.userName, BoardClass.lastPlayerTurn, BoardClass.numGames, BoardClass.playerWins, BoardClass.playerLosses, BoardClass.playerTies)
            gameOn = False
            break
            

    
    if continueGame:
        placement = 0
        for row in latestGameBoard:
            print(row)
        print('')
        while placement not in currValidMoves:
                placement = input(f'Which block do you want to place your X in from valid move list:{currValidMoves}? \n')
                try:
                    placement = int(placement)
                    if placement not in currValidMoves:
                        raise NotAValidMove
                except(ValueError, NotAValidMove):
                    print('That is not a valid move please try again!')
    
        currValidMoves.remove(placement)
        BoardClass.updateGameBoard(placement, latestGameBoard, 'O')
        BoardClass.lastPlayerTurn = BoardClass.userName
        for row in latestGameBoard:
            print(row)
        print('')
        serverSocket.sendall(bytes(str(placement), 'utf-8'))
    
    #once again figure out if the game is over or not and if is wait for signal from player 1
    #figure out a way to break the loop here when the game is over (somebody wins or its a tie) - you can use the methods used in player1 or maybe receive a message from there.
    if BoardClass.isWinner(latestGameBoard) or BoardClass.boardIsFull(latestGameBoard):
        currGameBoard = BoardClass.reserGameBoard()
        if BoardClass.isWinner(latestGameBoard) and BoardClass.lastPlayerTurn == BoardClass.userName:
            BoardClass.playerWins += 1
            BoardClass.numGames += 1
        elif BoardClass.isWinner(latestGameBoard) and BoardClass.lastPlayerTurn == player1UserName:
            BoardClass.playerLosses += 1
            BoardClass.numGames += 1
        elif BoardClass.boardIsFull(latestGameBoard):
            BoardClass.playerTies +=1    
            BoardClass.numGames += 1
        
        gameOn = False
        #get blocking, wait for signal from player one if they want to continue and determine break or not from there
        continueDecision = serverSocket.recv(1024)
        continueDecision = continueDecision.decode()
        #print(continueDecision)
        if continueDecision == 'Play Again':
            latestGameBoard = BoardClass.resetGameBoard()
            pass

        elif continueDecision == 'Fun Times':
            gameOn = False
            BoardClass.printStats(BoardClass.userName, BoardClass.lastPlayerTurn, BoardClass.numGames, BoardClass.playerWins, BoardClass.playerLosses, BoardClass.playerTies)
            break
            
