#import sys
#import copy

#%% DELETE THIS when moving to VEX V5 Code!!
class Brain:
    def __init__(self):
        pass
    class screen:
        def print(string):
            print(string)
        def clear_screen():
            pass
        def set_cursor(x, y):
            pass

brain = Brain()

class Human:
    def __init__(self, color):
        self.color = color

    def get_move(self):
        # Prompt the user to enter a move
        move_str = input("Enter a move (e.g. e2e4): ")

        # Parse the move string into a tuple of source and destination coordinates
        src_col = ord(move_str[0]) - ord("a")
        src_row = int(move_str[1]) - 1
        dst_col = ord(move_str[2]) - ord("a")
        dst_row = int(move_str[3]) - 1
        src = (src_row, src_col)
        dst = (dst_row, dst_col)

        return (src, dst)
class Computer:
    def evThread(self, move):
        return False
    def __init__(self, color):
        self.color = color
        self.opponent = "white" if self.color == "black" else "black"
    def make_move(self, board):
        # Create a copy of the board to simulate moves
        sim_board = board
        #copy.deepcopy(board)

        # Initialize the best move and score
        best_move = None
        best_score = None

        # Loop through all the possible moves
        for move in sim_board.get_all_moves(self.color):
            print('-', end='')
            # Make the move on the simulated board
            sim_board.make_move(((move[0], move[1]), (move[2], move[3])))

            # Recursively evaluate the score of the move
            score = self.minimax(sim_board, 2, self.color == "white")

            if not best_score and best_score != 0:
                best_score = score
                best_move = move
            # If the score is better than the current best score, update the best move and score
            if self.color == "white" and score > best_score:
                best_move = move
                best_score = score
            elif self.color == "black" and score < best_score:
                best_move = move
                best_score = score

            # Undo the move on the simulated board
            sim_board.undo_move()

        # Make the best move on the actual board
        board.make_move(((best_move[0], best_move[1]), (best_move[2], best_move[3])))

    

      
    def minimax(self, board, depth, maximizing_player):
        # If the depth is 0 or the game is over, return the score of the board
        if depth == 0 or board.game_over():
            score =  board.get_score()
            #brain.screen.print(score)
            return score

        # Initialize the best score
        best_score = None

        # Loop through all the possible moves
        for move in board.get_all_moves(self.color if maximizing_player else self.opponent):
            # Make the move on the simulated board
            board.make_move(((move[0], move[1]), (move[2], move[3])))

            # Recursively evaluate the score of the move
            score = self.minimax(board, depth - 1, not maximizing_player)
            
            if not best_score:
              best_score = score

            # If the score is better than the current best score, update the best score
            if maximizing_player and score < best_score:
                best_score = score
            elif not maximizing_player and score > best_score:
                best_score = score
            # Undo the move on the simulated board
            board.undo_move()
        return best_score       
def print_board(board):
    # Print the top row of brackets and separators
    print("   +--------+--------+--------+--------+--------+--------+--------+--------+")

    # Print each row of the board, starting from the top of the board
    for r in range(7, -1, -1):
        row = ""
        for c in range(8):
            row += " |   " + board.grid[r][c] + "   "
        print(str(r + 1) + " " + row + " |")

        # Print a row of brackets and separators
        if r > 0:
            print("   +--------+--------+--------+--------+--------+--------+--------+--------+")

    # Print the bottom row of brackets and separators
    print("   +--------+--------+--------+--------+--------+--------+--------+--------+")

    # Print the letter axis
    print("       a        b        c        d        e        f        g        h")
class Piece:
    def __init__(self, symbol, color, position):
        self.symbol = symbol
        self.color = color
        self.position = position
        if symbol == 'P' or symbol == 'p':
          self.value = 1
        if symbol == 'N' or symbol == 'n':
          self.value = 3
        if symbol == 'B' or symbol == 'b':
          self.value = 3
        if symbol == 'R' or symbol == 'r':
          self.value = 5
        if symbol == 'Q' or symbol == 'q':
          self.value = 9
        if symbol == 'K' or symbol == 'k':
          self.value = float('inf')
          
          
          
          
          

    def __repr__(self):
        return f"{self.color}{self.__class__.__name__} at {self.position}"

    def is_white(self):
        return self.color == "white"

    def move(self, destination):
        raise NotImplementedError
class Pawn(Piece):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.symbol = "P" if self.color == "white" else "p"
        self.value = 1
    
    def get_valid_moves(self, board):
        valid_moves = []

        r, c = self.position
        forward = 1 if self.color == "white" else -1

        # Check if the square in front is empty
        if board.grid[r + forward][c] == " ":
            valid_moves.append((r, c, r + forward, c))

            # Check if the pawn can move two squares from its starting position
            if (self.color == "white" and r == 1) or (self.color == "black" and r == 6):
                if board.grid[r + 2 * forward][c] == " ":
                    valid_moves.append((r, c, r + 2 * forward, c))

        # Check for captures
        for dc in [-1, 1]:
            if 0 <= c + dc < 8:
                if board.grid[r + forward][c + dc].islower() == self.is_white() and board.grid[r + forward][c + dc] != " ":
                    valid_moves.append((r, c, r + forward, c + dc))

        return valid_moves
      
    def move(self, destination, board):
        for move in self.get_valid_moves(board):
            if (move[2], move[3]) == destination:
                return True
        return False
class Knight(Piece):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.symbol = "N" if self.color == "white" else "n"
        self.value = 3

    def get_valid_moves(self, board):
        valid_moves = []

        r, c = self.position
        offsets = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]

        for dr, dc in offsets:
            rr, cc = r + dr, c + dc
            if 0 <= rr < 8 and 0 <= cc < 8:
                if board.grid[rr][cc] == " " or board.grid[rr][cc].islower() == self.is_white():
                    valid_moves.append((r, c, rr, cc))

        return valid_moves
      
    def move(self, destination, board):
        for move in self.get_valid_moves(board):
            if (move[2], move[3]) == destination:
                return True
        return False
class Bishop(Piece):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.symbol = "B" if self.color == "white" else "b"
        self.value = 3

    def get_valid_moves(self, board):
        valid_moves = []

        r, c = self.position
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in directions:
            rr, cc = r + dr, c + dc
            while 0 <= rr < 8 and 0 <= cc < 8:
                if board.grid[rr][cc] == " ":
                    valid_moves.append((r, c, rr, cc))
                    rr, cc = rr + dr, cc + dc
                else:
                    if board.grid[rr][cc].islower() == self.is_white():
                        valid_moves.append((r, c, rr, cc))
                    break

        return valid_moves
      
    def move(self, destination, board):
        for move in self.get_valid_moves(board):
            if (move[2], move[3]) == destination:
                return True
        return False
class Rook(Piece):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.symbol = "R" if self.color == "white" else "r"
        self.value = 5

    def get_valid_moves(self, board):
        valid_moves = []

        r, c = self.position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dr, dc in directions:
            rr, cc = r + dr, c + dc
            while 0 <= rr < 8 and 0 <= cc < 8:
                if board.grid[rr][cc] == " ":
                    valid_moves.append((r, c, rr, cc))
                    rr, cc = rr + dr, cc + dc
                else:
                    if board.grid[rr][cc].islower() == self.is_white():
                        valid_moves.append((r, c, rr, cc))
                    break

        return valid_moves
      
    def move(self, destination, board):
        for move in self.get_valid_moves(board):
            if (move[2], move[3]) == destination:
                return True
        return False
class Queen(Piece):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.symbol = "Q" if self.color == "white" else "q"
        self.value = 9

    def get_valid_moves(self, board):
        valid_moves = []

        r, c = self.position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in directions:
            rr, cc = r + dr, c + dc
            while 0 <= rr < 8 and 0 <= cc < 8:
                if board.grid[rr][cc] == " ":
                    valid_moves.append((r, c, rr, cc))
                    rr, cc = rr + dr, cc + dc
                else:
                    if board.grid[rr][cc].islower() == self.is_white():
                        valid_moves.append((r, c, rr, cc))
                    break

        return valid_moves
    def move(self, destination, board):
        for move in self.get_valid_moves(board):
            if (move[2], move[3]) == destination:
                return True
        return False
class King(Piece):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.symbol = "K" if self.color == "white" else "k"
        self.value = 1100
    def get_valid_moves(self, board):
        valid_moves = []

        r, c = self.position
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in offsets:
            rr, cc = r + dr, c + dc
            if 0 <= rr < 8 and 0 <= cc < 8:
                if board.grid[rr][cc] == " " or board.grid[rr][cc].islower() == self.is_white():
                    valid_moves.append((r, c, rr, cc))

        return valid_moves
      
    def move(self, destination, board):
        for move in self.get_valid_moves(board):
            if (move[2], move[3]) == destination:
                return True
        return False
class Board:
    def copy(board):
        brd = Board()
        brd.setGrid(board.grid, board.history)
        return brd
    def __init__(self):
        self.grid = [
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["r", "n", "b", "q", "k", "b", "n", "r"]
        ]
        self.pieces = {}
        for r in range(8):
            for c in range(8):
                symbol = self.grid[r][c]
                if symbol != " ":
                    color = "white" if symbol.isupper() else "black"
                    position = (r, c)
                    if symbol == "P" or symbol == "p":
                        piece = Pawn(color, position)
                    elif symbol == "N" or symbol == "n":
                        piece = Knight(color, position)
                    elif symbol == "B" or symbol == "b":
                        piece = Bishop(color, position)
                    elif symbol == "R" or symbol == "r":
                        piece = Rook(color, position)
                    elif symbol == "Q" or symbol == "q":
                        piece = Queen(color, position)
                    elif symbol == "K" or symbol == "k":
                        piece = King(color, position)
                    self.pieces[position] = piece
        self.history = []
    def setGrid(self, grid, history):
        self.grid =  [row[:] for row in grid]
        self.pieces = {}
        for r in range(8):
            for c in range(8):
                symbol = self.grid[r][c]
                if symbol != " ":
                    color = "white" if symbol.isupper() else "black"
                    position = (r, c)
                    if symbol == "P" or symbol == "p":
                        piece = Pawn(color, position)
                    elif symbol == "N" or symbol == "n":
                        piece = Knight(color, position)
                    elif symbol == "B" or symbol == "b":
                        piece = Bishop(color, position)
                    elif symbol == "R" or symbol == "r":
                        piece = Rook(color, position)
                    elif symbol == "Q" or symbol == "q":
                        piece = Queen(color, position)
                    elif symbol == "K" or symbol == "k":
                        piece = King(color, position)
                    self.pieces[position] = piece
        self.history = history
    def get_score(self):
        if self.game_over():
          if self.is_in_check("white"):
            return float("-inf")
          else:
            return float("inf")
        score = 0
        for piece in self.pieces.values():
            if piece.color == "white":
                score += piece.value
            else:
                score -= piece.value
        return score
    def undo_move(self):
        # Check if there is a move to undo
        if len(self.history) == 0:
            return

        # Get the last move from the history
        src_r, src_c, dest_r, dest_c, captured_piece = self.history.pop()

        # Move the piece back to its original position
        piece = self.pieces.get((dest_r, dest_c))
        self.pieces[(src_r, src_c)] = piece
        del self.pieces[(dest_r, dest_c)]
        piece.position = (src_r, src_c)

        # Put the captured piece back on the board
        if captured_piece is not None:
            self.pieces[(dest_r, dest_c)] = captured_piece
            captured_piece.position = (dest_r, dest_c)

        # Update the board grid
        self.grid[src_r][src_c] = piece.symbol
        self.grid[dest_r][dest_c] = captured_piece.symbol if captured_piece is not None else " "

    def make_move(self, move):
        src, dest = move
        src_r, src_c = src
        dest_r, dest_c = dest

        # Check if the source position is on the board
        if not (0 <= src_r < 8 and 0 <= src_c < 8):
            raise ValueError("Invalid source position")

        # Check if the destination position is on the board
        if not (0 <= dest_r < 8 and 0 <= dest_c < 8):
            raise ValueError("Invalid destination position")

        # Get the piece at the source position
        piece = self.pieces.get((src_r, src_c))

        # Check if there is a piece at the source position
        if piece is None:
            raise ValueError("No piece at source position")

        # Get the valid moves for the piece
        valid_moves = piece.get_valid_moves(self)

        # Check if the destination position is in the list of valid moves
        if (src_r, src_c, dest_r, dest_c) not in valid_moves:
            #brain.screen.print((src_r, src_c, dest_r, dest_c))
            raise ValueError("Invalid move for piece")

        # Remove the piece from its original position
        del self.pieces[(src_r, src_c)]

        # Check if there is a piece at the destination position
        captured_piece = self.pieces.get((dest_r, dest_c))
        if captured_piece is not None:
            # Remove the captured piece from the board
            del self.pieces[(dest_r, dest_c)]

        # Place the piece at the destination position
        self.pieces[(dest_r, dest_c)] = piece
        piece.position = (dest_r, dest_c)

        # Update the board grid
        self.grid[src_r][src_c] = " "
        self.grid[dest_r][dest_c] = piece.symbol

        # Add the move to the history
        self.history.append((src_r, src_c, dest_r, dest_c, captured_piece))


    def is_in_check(self, color):
      # Initialize the position of the king to a default value
      king_position = None

      # Find the position of the king
      for position, piece in self.pieces.items():
        if isinstance(piece, King) and piece.color == color:
          king_position = position
          break
      # Check if any enemy pieces can attack the king
      if king_position is not None:
        for position, piece in self.pieces.items():
          if piece.color != color and piece.move(king_position, self):
            return True
      return False
    def game_over(self):
        # Check if white king is in check
        white_king_in_check = self.is_in_check("white")

        # Check if black king is in check
        
        black_king_in_check = self.is_in_check("black")

        if white_king_in_check and self.get_all_moves("white") == []:
            return True
        if black_king_in_check and self.get_all_moves("black") == []:
            return True

        # TODO: Check for other conditions that would end the game, such as
        # stalemate or threefold repetition

        return False
    def get_all_moves(self, color):
        valid_moves = []
        simBoard = Board.copy(board)
        
        # Iterate through the pieces dictionary
        for position, piece in self.pieces.items():
            if piece.color == color:
                # Get the valid moves for this piece
                piece_valid_moves = piece.get_valid_moves(self)

                # Add the valid moves to the list
                for move in piece_valid_moves:
                    simBoard.make_move(((move[0], move[1]), (move[2], move[3])))
                    if not simBoard.is_in_check(color):
                        valid_moves.append(move)
                    simBoard.undo_move()
                #valid_moves.extend(piece_valid_moves)

        return valid_moves

# Create the board and players
board = Board()
white_player = Human("white")
black_player = Computer("black")
# Initialize the current player and game over flag
current_player = white_player
game_over = False

while not game_over:
    # brain.screen.print the board
    brain.screen.print("\n\n\n\n\n")
    print_board(board)

    # Check if the current player is a computer
    if isinstance(current_player, Computer):
        # Have the computer make a move
        current_player.make_move(board)
    else:
        #Get the move from the human player

        move = current_player.get_move()
        
        # Make the move on the board
        board.make_move(move)

    # Check if the game is over
    game_over = board.game_over()

    # Switch the current player
    current_player = black_player if current_player == white_player else white_player
    

# brain.screen.print the final board
print_board(board)
