from connectfour.agents.computer_player import RandomAgent
import random

class StudentAgent(RandomAgent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 3
        self.opponent = -1


    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """
        self.opponent = (self.id % 2) + 1
        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            next_state = board.next_state(self.id, move[1])
            moves.append( move )
            vals.append( self.dfMiniMax(next_state, 1) )

        bestMove = moves[vals.index( max(vals) )]
        return bestMove

    def dfMiniMax(self, board, depth):
        # Goal return column with maximized scores of all possible next states
        
        if depth == self.MaxDepth:
            return self.evaluateBoardState(board)
        winner = board.winner()
        if winner == self.id:
            return 1
        if winner == self.opponent:
            return -1
        
        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            if depth % 2 == 1:
                next_state = board.next_state(self.opponent, move[1])
            else:
                next_state = board.next_state(self.id, move[1])
                
            moves.append( move )
            vals.append( self.dfMiniMax(next_state, depth + 1) )

        
        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)

        return bestVal

    def evaluateBoardState(self, board):
        """
        Your evaluation function should look at the current state and return a score for it. 
        As an example, the random agent provided works as follows:
            If the opponent has won this game, return -1.
            If we have won the game, return 1.
            If neither of the players has won, return a random number.
        """
        
        """
        These are the variables and functions for board objects which may be helpful when creating your Agent.
        Look into board.py for more information/descriptions of each, or to look for any other definitions which may help you.

        Board Variables:
            board.width 
            board.height
            board.last_move
            board.num_to_connect
            board.winning_zones
            board.score_array 
            board.current_player_score

        Board Functions:
            get_cell_value(row, col)
            try_move(col)
            valid_move(row, col)
            valid_moves()
            terminal(self)
            legal_moves()
            next_state(turn)
            winner()
        """
        
        values = []
        for direction in range(1,5): # 1, 2, 3, 4 refers to down, down-right, right, up
            for i in range(0, board.width):
                for j in range(0, board.height):
                    tokens = self.get_tokens(board, direction, i, j)
                    if tokens:
                        values.append(self.check_tokens(tokens))
        value = 0.0
        for v in values:
            if v == board.num_to_connect:
                return 1
            if v == -board.num_to_connect:
                return -1
            if v < 0:
                value -= (0.001**(1.0*(board.num_to_connect + v)))
            if v > 0:
                value += (0.001**(1.0*(board.num_to_connect - v)))
        return value

    def get_tokens(self, board, direction, x, y):
        # check if the set is within the board
        num_to_connect = board.num_to_connect
        tokens = []
        if direction == 1:
            if y + num_to_connect > board.height:
                return []
            else:
                for j in range(y, y + num_to_connect):
                    tokens.append(board.get_cell_value(j, x))
        elif direction == 2:
            if x + num_to_connect > board.width or\
               y + num_to_connect > board.height:
               return []
            else:
                for i in range(0, num_to_connect):
                    tokens.append(board.get_cell_value(y + i, x + i))
        elif direction == 3:
            if x + num_to_connect > board.width:
               return []
            else:
                for i in range(x, x + num_to_connect):
                    tokens.append(board.get_cell_value(y, i))
        elif direction == 4:
            if x + num_to_connect > board.width or\
               y - num_to_connect <= -1:
               return []
            else:
                for j in range(0, num_to_connect):
                    tokens.append(board.get_cell_value(y - j, x + j))
        return tokens

    def check_tokens(self, tokens):
        """
        Counts the number of tokens in a row, ignoring spaces.
        Returns 0 if there's an opponent's piece.
        """
        value = 0
        allied = False
        enemy = False
        for token in tokens:
            if token == self.id:
                allied = True
                if enemy:
                    return 0
                else:
                    value += 1
            elif token == self.opponent:
                enemy = True
                if allied:
                    return 0
                else:
                    value -= 1
        return value

