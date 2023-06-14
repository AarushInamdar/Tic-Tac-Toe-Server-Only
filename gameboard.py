class BoardClass():
    '''How should we generate the Tic Tac Toe board?'''
    def __init__(self) -> None: #, username, lastPerson, numWins, numLosses, numTies
        # self.username = username
        # self.lastPerson = lastPerson
        # self.numWins = numWins
        # self.numLosses = numLosses
        # self.numTies = numTies
        '''Attributes defined later in file'''
        pass 

    def updateGamesPlayed(GamesPlayed:int) -> int:
        GamesPlayed += 1
        return GamesPlayed
    
    def resetGameBoard() -> list[list]:
        '''Resets the game board to the original values by taking a list object from the class'''
        originalGameBoard = [['1','2','3'],['4','5','6'],['7','8','9']]
        #Clear all the moves from game board
        return originalGameBoard
    
    def updateGameBoard(placementArg:str, currGameBoard:list, playerXorO:str) -> list[list]:
        '''Updates the game board with the player's move'''
        placementArg = int(placementArg)
        if 1 <= placementArg <= 3:
            currGameBoard[0][placementArg-1] = playerXorO
        elif 4 <= placementArg <= 6:
            currGameBoard[1][placementArg-4] = playerXorO
        elif 7 <= placementArg <= 9:
            currGameBoard[2][placementArg-7] = playerXorO
        return currGameBoard
    
    def isWinner(gameBoard:list) -> bool:
        ''' Checks if the latest move resulted in a win. Updates the wins and losses count. Goes over every possible combination of win criteria for the game board and checks if the players have won or not.'''
        Flag = False
        for lists in gameBoard:
            if lists[0] == lists[1] == lists[2]:
                return True
        if (gameBoard[0][0].lower() == 'x' and gameBoard[1][0].lower() == 'x' and gameBoard[2][0].lower() == 'x') or (gameBoard[0][0].lower() == 'o' and gameBoard[1][0].lower() == 'o' and gameBoard[2][0].lower() == 'o'):
            Flag = True
        elif (gameBoard[0][1].lower() == 'x' and gameBoard[1][1].lower() == 'x' and gameBoard[2][1].lower() == 'x') or (gameBoard[0][1].lower() == 'o' and gameBoard[1][1].lower() == 'o' and gameBoard[2][1].lower() == 'o'):
            Flag = True
        elif (gameBoard[0][2].lower() == 'x' and gameBoard[1][2].lower() == 'x' and gameBoard[2][2].lower() == 'x') or (gameBoard[0][2].lower() == 'o' and gameBoard[1][2].lower() == 'o' and gameBoard[2][2].lower() == 'o'):
            Flag = True
        elif (gameBoard[0][0].lower() == 'x' and gameBoard[1][1].lower() == 'x' and gameBoard[2][2].lower() == 'x') or (gameBoard[0][0].lower() == 'o' and gameBoard[1][1].lower() == 'o' and gameBoard[2][2].lower() == 'o'):
            Flag = True
        elif (gameBoard[0][2].lower() == 'x' and gameBoard[1][1].lower() == 'x' and gameBoard[2][0].lower() == 'x') or (gameBoard[0][2].lower() == 'o' and gameBoard[1][1].lower() == 'o' and gameBoard[2][0].lower() == 'o'):
            Flag = True
        return Flag            


    def boardIsFull(gameBoard:list) -> bool:
        '''Goes over every piece on the board to see if a valid move has been played, if so the board is full'''
        movesPlayable = ['x', 'X', 'o', 'O']
        Flag = True
        for list in gameBoard:
            for variable in list:
                if variable not in movesPlayable:
                    Flag = False
        return Flag

    def printStats(userName:str, lastPerson:str, numGames:int, numWins:int, numLosses:int, numTies:int) -> str:
        '''Prints all the stats based on arguments fed in from previous functions'''
        print('User Name:', userName)
        print('Last Player to have a turn: ', lastPerson)
        print('Total Games Played: ', numGames)
        print(f'Number of wins for {userName}: {numWins}')
        print(f'Number of losses for {userName}: {numLosses}')
        print(f'Number of ties for {userName}: {numTies}')
