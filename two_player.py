import random

#Global Variables
#################################################################################

virtual_board = [['black    rook', 'black  knight', 'black  bishop', 'black   queen', 'black    king', 'black  bishop', 'black  knight', 'black    rook'], ['black    pawn', 'black    pawn', 'black    pawn', 'black    pawn', 'black    pawn', 'black    pawn', 'black    pawn', 'black    pawn'], ['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------'], ['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------'], ['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------'], ['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------'], ['white    pawn', 'white    pawn', 'white    pawn', 'white    pawn', 'white    pawn', 'white    pawn', 'white    pawn', 'white    pawn'], ['white    rook', 'white  knight', 'white  bishop', 'white   queen', 'white    king', 'white  bishop', 'white  knight', 'white    rook']]

player_turn = 'white'

promotion_row = {"black": 7, "white": 0}

black_castling_possible = True
white_castling_possible = True

red = "\033[31m"
bold = "\033[1m"
reset = "\u001b[0m"

#################################################################################
#Game & Movement Functions
#################################################################################

def check_checkmate(color):
  global virtual_board
  
  temp_virtual_board = [['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------'], ['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------'], ['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------'], ['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------'], ['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------'], ['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------'], ['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------'], ['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------']]

  is_checkmated = True

  for row in range(8): #This matches temp board with current board
    for col in range(8):
      temp_virtual_board[row][col] = virtual_board[row][col]
  
  piece_possible_moves = find_piece_possible_moves(find_pieces(color), color)
  
  for key_element in [*piece_possible_moves]:
    for move_element in piece_possible_moves[key_element]:
      virtual_board[move_element[0]][move_element[1]] = virtual_board[convert_to_index(key_element)[0]][convert_to_index(key_element)[1]] #This part moves the piece
      virtual_board[convert_to_index(key_element)[0]][convert_to_index(key_element)[1]] = '-------------'

      if check_check(color) == False:
        is_checkmated = False

      for row in range(8): #This resets board to equal temp board
        for col in range(8):
          virtual_board[row][col] = temp_virtual_board[row][col]

  return is_checkmated
      

def check_check(color):
  piece_positions = find_pieces(opposite_color(color))
  possible_moves = find_piece_possible_moves_list(piece_positions, opposite_color(color))
  king_position = find_king(color)
  if king_position in possible_moves:
    return True
  return False
  

def find_king(color):
  for row in range(8):
    for col in range(8):
      if color in virtual_board[row][col] and "king" in virtual_board[row][col]:
        king_location = [row, col]

  return king_location
  

def piece_is_guarded(position, color): #This function assumes the space isn't empty
  global virtual_board

  piece_is_guarded = False

  virtual_board[position[0]][position[1]] = opposite_color(color) + virtual_board[position[0]][position[1]][5:] #This temporarily switches the piece's color

  if position in find_piece_possible_moves_list(find_pieces(color), color): #This checks if the piece is now being threatened by its orignial color
    piece_is_guarded = True

  virtual_board[position[0]][position[1]] = color + virtual_board[position[0]][position[1]][5:] #This switches it back
    
  return piece_is_guarded
  

def promote_pawn(color):
  global virtual_board

  for col in range(8):
    if "pawn" in virtual_board[promotion_row[color]][col]:
      print_board()
      virtual_board[promotion_row[color]][col] = color + "   queen"
        

def print_board(old_position, new_move):
  if new_move == "No New Move": 
    for index in range(len(virtual_board)):
      print("\n")
      print(str(8 - index), end=" ")
      print(virtual_board[index])
    print("          a                b                c                d                e                f                g                h\n")
  else:
    for row in range(len(virtual_board)):
      print("\n")
      print(str(8 - row), end=" [")
      for col in range(len(virtual_board[0])):
        if [row, col] == old_position or [row, col] == new_move:
          print("'", end="")
          print(red + bold + virtual_board[row][col], end="")
          if col < 7:
            print(reset + "',", end=" ")
          else:
            print(reset + "'", end="]\n")
        elif col < 7:
          print("'" + virtual_board[row][col] + "',", end=" ")
        else:
          print("'" + virtual_board[row][col] + "'", end="]\n")
    print("          a                b                c                d                e                f                g                h\n")
  

def check_king():
  black_king_present = False
  white_king_present = False

  for index in range(len(virtual_board)):
    if "black    king" in virtual_board[index]:
      black_king_present = True

    if "white    king" in virtual_board[index]:
      white_king_present = True

  if black_king_present and white_king_present:
    return "Both Present"
  elif (black_king_present) and (white_king_present == False):
    return "Black King Present"
  elif (black_king_present == False) and (white_king_present):
    return "White King Present"


def convert_to_index(position):
  possible_columns = "abcdefgh"
  
  return [8 - int(position[1]), possible_columns.find(position[0])]


def convert_to_chess_position(position):
  possible_columns = "abcdefgh"

  return str(possible_columns[position[1]]) + str(8 - position[0])


def user_move_choice(possible_moves):
  if len(possible_moves) > 0:
    print("Possible Moves:")
    for element in possible_moves:
      print(convert_to_chess_position(element))
  else:
    print("No Possible Moves\n")
    return "No Possible Moves"

  while True:
    user_move = input("Pick a Possible Move (Type 'back' to unselect piece): ")

    if "back" in user_move.lower():
      return user_move

    if len(user_move) != 2:
      print("That is not a valid move.")
      continue

    if user_move[0] in "abcdefgh" and user_move[1].isnumeric():
      user_move = convert_to_index(user_move)
    else:
      print("That is not a valid move.")
      continue
  
    if user_move in possible_moves:
      return user_move
    
    print("That is not a valid move.")


def move_piece(position, new_position):
  global virtual_board, black_castling_possible, white_castling_possible

  if ("black" in virtual_board[position[0]][position[1]]) and ((position == [0, 7] and "rook" in virtual_board[position[0]][position[1]]) or (position == [0, 4] and "king" in virtual_board[position[0]][position[1]])):
    black_castling_possible = False
    
    if "king" in virtual_board[position[0]][position[1]] and new_position == [0, 6]:
      virtual_board[0][5] = virtual_board[0][7]

      virtual_board[0][7] = '-------------'
    
  elif ("white" in virtual_board[position[0]][position[1]]) and ((position == [7, 7] and "rook" in virtual_board[position[0]][position[1]]) or (position == [7, 4] and "king" in virtual_board[position[0]][position[1]])):
    white_castling_possible = False

    if "king" in virtual_board[position[0]][position[1]] and new_position == [7, 6]:
      virtual_board[7][5] = virtual_board[7][7]

      virtual_board[7][7] = '-------------'
  
  virtual_board[new_position[0]][new_position[1]] = virtual_board[position[0]][position[1]]

  virtual_board[position[0]][position[1]] = '-------------'


def find_piece_type(position, color):
  if "pawn" in virtual_board[position[0]][position[1]]:
    return pawn_valid_moves(position, color)
  elif "knight" in virtual_board[position[0]][position[1]]:
    return knight_valid_moves(position, color)
  elif "rook" in virtual_board[position[0]][position[1]]:
    return rook_valid_moves(position, color)
  elif "bishop" in virtual_board[position[0]][position[1]]:
    return bishop_valid_moves(position, color)
  elif "queen" in virtual_board[position[0]][position[1]]:
    return queen_valid_moves(position, color)
  elif "king" in virtual_board[position[0]][position[1]]:
    return king_valid_moves(position, color)
  else:
    print("Error Piece Type")

#################################################################################
#Piece Rule Logic Functions
#################################################################################

def check_move_validity(row, col):
  try:
    virtual_board[row][col]
  except IndexError:
    return "Out of Index"

  if row < 0 or col < 0:
    return "Out of Index"
  
  if "black" in virtual_board[row][col]:
    return "black"
  elif "white" in virtual_board[row][col]:
    return "white"
    
  return "Clear"


def opposite_color(color):
  if color == "black":
    return "white"
  return "black"
  

def pawn_valid_moves(position, color):
  valid_moves = []
  
  if color == "black":
    if check_move_validity(position[0] + 1, position[1]) == "Clear": #This part checks in front of the pawn
      valid_moves.append([position[0] + 1, position[1]])

      if (check_move_validity(position[0] + 2, position[1]) == "Clear") and (position[0] == 1):
        valid_moves.append([position[0] + 2, position[1]])

    if check_move_validity(position[0] + 1, position[1] - 1) == "white": #This part checks left of the pawn
      valid_moves.append([position[0] + 1, position[1] - 1])

    if check_move_validity(position[0] + 1, position[1] + 1) == "white": #This part checks right of the pawn
      valid_moves.append([position[0] + 1, position[1] + 1])

  elif color == "white":
    if check_move_validity(position[0] - 1, position[1]) == "Clear": #This part checks in front of the pawn
      valid_moves.append([position[0] - 1, position[1]])

      if (check_move_validity(position[0] - 2, position[1]) == "Clear") and (position[0] == 6):
        valid_moves.append([position[0] - 2, position[1]])

    if check_move_validity(position[0] - 1, position[1] - 1) == "black": #This part checks left of the pawn
      valid_moves.append([position[0] - 1, position[1] - 1])

    if check_move_validity(position[0] - 1, position[1] + 1) == "black": #This part checks right of the pawn
      valid_moves.append([position[0] - 1, position[1] + 1])

  return valid_moves
  

def rook_valid_moves(position, color):
  valid_moves = []
  check_position = ["", ""]
  check_position[0] = position[0]
  check_position[1] = position[1]

  while check_move_validity(check_position[0] + 1, check_position[1]) == "Clear": #This moves it down a row
    check_position[0] += 1
    valid_moves.append([check_position[0], check_position[1]])

  if check_move_validity(check_position[0] + 1, check_position[1]) == opposite_color(color):
    check_position[0] += 1
    valid_moves.append([check_position[0], check_position[1]])

  check_position[0] = position[0]
  check_position[1] = position[1]

  while check_move_validity(check_position[0] - 1, check_position[1]) == "Clear": #This moves it up a row
    check_position[0] -= 1
    valid_moves.append([check_position[0], check_position[1]])

  if check_move_validity(check_position[0] - 1, check_position[1]) == opposite_color(color):
    check_position[0] -= 1
    valid_moves.append([check_position[0], check_position[1]])

  check_position[0] = position[0]
  check_position[1] = position[1]

  while check_move_validity(check_position[0], check_position[1] + 1) == "Clear": #This moves it right a column
    check_position[1] += 1
    valid_moves.append([check_position[0], check_position[1]])

  if check_move_validity(check_position[0], check_position[1] + 1) == opposite_color(color):
    check_position[1] += 1
    valid_moves.append([check_position[0], check_position[1]])

  check_position[0] = position[0]
  check_position[1] = position[1]

  while check_move_validity(check_position[0], check_position[1] - 1) == "Clear": #This moves it left a column
    check_position[1] -= 1
    valid_moves.append([check_position[0], check_position[1]])

  if check_move_validity(check_position[0], check_position[1] - 1) == opposite_color(color):
    check_position[1] -= 1
    valid_moves.append([check_position[0], check_position[1]])

  check_position[0] = position[0]
  check_position[1] = position[1]
    
  return valid_moves
  

def king_valid_moves(position, color):
  valid_moves = []

  if (check_move_validity(position[0] + 1, position[1]) == opposite_color(color)) or (check_move_validity(position[0] + 1, position[1]) == "Clear"):
    valid_moves.append([position[0] + 1, position[1]])

  if (check_move_validity(position[0] + 1, position[1] + 1) == opposite_color(color)) or (check_move_validity(position[0] + 1, position[1] + 1) == "Clear"):
    valid_moves.append([position[0] + 1, position[1] + 1])

  if (check_move_validity(position[0], position[1] + 1) == opposite_color(color)) or (check_move_validity(position[0], position[1] + 1) == "Clear"):
    valid_moves.append([position[0], position[1] + 1])

  if (check_move_validity(position[0] - 1, position[1] + 1) == opposite_color(color)) or (check_move_validity(position[0] - 1, position[1] + 1) == "Clear"):
    valid_moves.append([position[0] - 1, position[1] + 1])

  if (check_move_validity(position[0] - 1, position[1]) == opposite_color(color)) or (check_move_validity(position[0] - 1, position[1]) == "Clear"):
    valid_moves.append([position[0] - 1, position[1]])

  if (check_move_validity(position[0] - 1, position[1] - 1) == opposite_color(color)) or (check_move_validity(position[0] - 1, position[1] - 1) == "Clear"):
    valid_moves.append([position[0] - 1, position[1] - 1])

  if (check_move_validity(position[0], position[1] - 1) == opposite_color(color)) or (check_move_validity(position[0], position[1] - 1) == "Clear"):
    valid_moves.append([position[0], position[1] - 1])

  if (check_move_validity(position[0] + 1, position[1] - 1) == opposite_color(color)) or (check_move_validity(position[0] + 1, position[1] - 1) == "Clear"):
    valid_moves.append([position[0] + 1, position[1] - 1])

  if color == "black" and check_move_validity(0, 5) == "Clear" and check_move_validity(0, 6) == "Clear" and black_castling_possible:
    valid_moves.append([0, 6])
  elif color == "white" and check_move_validity(7, 5) == "Clear" and check_move_validity(7, 6) == "Clear" and white_castling_possible:
    valid_moves.append([7, 6])
  
  return valid_moves
  

def knight_valid_moves(position, color):
  valid_moves = []
  
  if check_move_validity(position[0] + 2, position[1] + 1) == "Clear" or check_move_validity(position[0] + 2, position[1] + 1) == opposite_color(color): 
    valid_moves.append([position[0] + 2, position[1] + 1])

  if check_move_validity(position[0] + 2, position[1] - 1) == "Clear" or check_move_validity(position[0] + 2, position[1] - 1) == opposite_color(color): 
    valid_moves.append([position[0] + 2, position[1] - 1])
    
  if check_move_validity(position[0] + 1, position[1] + 2) == "Clear" or check_move_validity(position[0] + 1, position[1] + 2) == opposite_color(color):
    valid_moves.append([position[0] + 1, position[1] + 2])
  
  if check_move_validity(position[0] + 1, position[1] - 2) == "Clear" or check_move_validity(position[0] + 1, position[1] - 2) == opposite_color(color): 
    valid_moves.append([position[0] + 1, position[1] - 2])
    
  if check_move_validity(position[0] - 1, position[1] + 2) == "Clear" or check_move_validity(position[0] - 1, position[1] + 2) == opposite_color(color): 
    valid_moves.append([position[0] - 1, position[1] + 2])

  if check_move_validity(position[0] - 1, position[1] - 2) == "Clear" or check_move_validity(position[0] - 1, position[1] - 2) == opposite_color(color):
    valid_moves.append([position[0] - 1, position[1] - 2])
    
  if check_move_validity(position[0] - 2, position[1] + 1) == "Clear" or check_move_validity(position[0] - 2, position[1] + 1) == opposite_color(color):
    valid_moves.append([position[0] - 2, position[1] + 1])
    
  if check_move_validity(position[0] - 2, position[1] - 1) == "Clear" or     check_move_validity(position[0] - 2, position[1] - 1) == opposite_color(color):  
    valid_moves.append([position[0] - 2, position[1] - 1])

  return valid_moves
    
      
def bishop_valid_moves(position, color):
  valid_moves = []
  check_position = ["", ""]
  check_position[0] = position[0]
  check_position[1] = position[1]
  
  while check_move_validity(check_position[0] + 1, check_position[1] + 1) == "Clear": #This moves it down a row and right a column
    check_position[0] += 1
    check_position[1] += 1
    valid_moves.append([check_position[0], check_position[1]])

  if check_move_validity(check_position[0] + 1, check_position[1] + 1) == opposite_color(color):
    check_position[0] += 1
    check_position[1] += 1
    valid_moves.append([check_position[0], check_position[1]])

  check_position[0] = position[0]
  check_position[1] = position[1]

  while check_move_validity(check_position[0] + 1, check_position[1] - 1) == "Clear": #This moves it down a row and left a column
    check_position[0] += 1
    check_position[1] -= 1
    valid_moves.append([check_position[0], check_position[1]])

  if check_move_validity(check_position[0] + 1, check_position[1] - 1) == opposite_color(color):
    check_position[0] += 1
    check_position[1] -= 1
    valid_moves.append([check_position[0], check_position[1]])

  check_position[0] = position[0]
  check_position[1] = position[1]

  while check_move_validity(check_position[0] - 1, check_position[1] + 1) == "Clear": #This moves it up a row and right a column
    check_position[0] -= 1
    check_position[1] += 1
    valid_moves.append([check_position[0], check_position[1]])

  if check_move_validity(check_position[0] - 1, check_position[1] + 1) == opposite_color(color):
    check_position[0] -= 1
    check_position[1] += 1
    valid_moves.append([check_position[0], check_position[1]])

  check_position[0] = position[0]
  check_position[1] = position[1]

  while check_move_validity(check_position[0] - 1, check_position[1] - 1) == "Clear": #This moves it up a row and left a column
    check_position[0] -= 1
    check_position[1] -= 1
    valid_moves.append([check_position[0], check_position[1]])

  if check_move_validity(check_position[0] - 1, check_position[1] - 1) == opposite_color(color):
    check_position[0] -= 1
    check_position[1] -= 1
    valid_moves.append([check_position[0], check_position[1]])

  check_position[0] = position[0]
  check_position[1] = position[1]
    
  return valid_moves
  

def queen_valid_moves(position, color):
  valid_moves = []

  for element in rook_valid_moves(position, color):
    valid_moves.append(element)

  for element in bishop_valid_moves(position, color):
    valid_moves.append(element)

  return valid_moves

#################################################################################
#AI Functions
#################################################################################

def find_pieces(color):
  piece_positions = []
  
  for row in range(8):
    for col in range(8):
      if color in virtual_board[row][col]:
        piece_positions.append([row, col])

  return piece_positions
  

def find_piece_possible_moves(piece_positions, color): #Plan to change this is to have the starting position as the key and then have the possible moves of that piece be the element. We can go through all of the moves and keep adding a slot for dictionary for each piece position
  piece_possible_moves = {}
  
  for position_element in piece_positions:
    piece_possible_moves[convert_to_chess_position(position_element)] = find_piece_type(position_element, color)

  return piece_possible_moves


def move_value(position): #This looks at the board position given and returns a value bases on what is there
  if "-" in virtual_board[position[0]][position[1]]:
    return 0
  if "pawn" in virtual_board[position[0]][position[1]]:
    return 10
  elif "knight" in virtual_board[position[0]][position[1]]:
    return 30
  elif "bishop" in virtual_board[position[0]][position[1]]:
    return 30
  elif "rook" in virtual_board[position[0]][position[1]]:
    return 50
  elif "queen" in virtual_board[position[0]][position[1]]:
    return 90
  elif "king" in virtual_board[position[0]][position[1]]:
    return 900


def piece_value(piece_type):
  if piece_type == "pawn":
    return 10
  elif piece_type == "knight":
    return 30
  elif piece_type == "bishop":
    return 30
  elif piece_type == "rook":
    return 50
  elif piece_type == "queen":
    return 90
  elif piece_type == "king":
    return 900


def ai_choose_move(possible_moves, color): #Third AI  -  Right now the AI is selecting the first possible move from left to right top to bottom 
  global virtual_board
  
  temp_virtual_board = [['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------'], ['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------'], ['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------'], ['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------'], ['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------'], ['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------'], ['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------'], ['-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------', '-------------']]

  for row in range(8): #This matches temp board with current board
    for col in range(8):
      temp_virtual_board[row][col] = virtual_board[row][col]

  while True: #This part loops until it finds a piece that has more than 0 possible moves
    selected_piece_position = [*possible_moves][random.randint(0, len([*possible_moves]) - 1)]

    if len(possible_moves[selected_piece_position]) > 0:
      break
    
  selected_move = possible_moves[selected_piece_position][random.randint(0, len(possible_moves[selected_piece_position]) - 1)]
  
  virtual_board[selected_move[0]][selected_move[1]] = virtual_board[convert_to_index(selected_piece_position)[0]][convert_to_index(selected_piece_position)[1]] #This part moves the piece
  virtual_board[convert_to_index(selected_piece_position)[0]][convert_to_index(selected_piece_position)[1]] = '-------------'
  
  selected_move_value = evaluate_board_value(selected_move, color)

  for row in range(8): #This resets board to equal temp board
    for col in range(8):
      virtual_board[row][col] = temp_virtual_board[row][col]

  #At this point, there is a temp virtual board and a selected move value

  for key_element in [*possible_moves]:
    for move_element in possible_moves[key_element]: #These two for loops look through every possible move the AI has
      virtual_board[move_element[0]][move_element[1]] = virtual_board[convert_to_index(key_element)[0]][convert_to_index(key_element)[1]] #This part moves the piece
      virtual_board[convert_to_index(key_element)[0]][convert_to_index(key_element)[1]] = '-------------'

      board_value = evaluate_board_value(move_element, color)

      if board_value > selected_move_value:
        selected_piece_position = key_element
        selected_move = move_element
        selected_move_value = board_value

      for row in range(8):
        for col in range(8):
          virtual_board[row][col] = temp_virtual_board[row][col]

  return [convert_to_index(selected_piece_position), selected_move]
      

def find_old_position(black_pieces, new_position):
  for element in black_pieces:
    if new_position in find_piece_type([element[0], element[1]], "black"):
      return [element[0], element[1]]


def find_piece_possible_moves_list(piece_positions, color): #This creates a list instead of a dictionary
  possible_moves = []
  
  for position_element in piece_positions:
    for move_element in find_piece_type(position_element, color):
      possible_moves.append(move_element)

  return possible_moves


def ai_choose_move_easy(possible_moves):
  selected_move = possible_moves[random.randint(0, len(possible_moves) - 1)]

  for element in possible_moves:
    if move_value(element) > move_value(selected_move):
      selected_move = element
      
  return selected_move


def evaluate_board_value(move, color):
  board_value = 1290
  
  piece_positions = find_pieces(color)
  possible_moves_list = find_piece_possible_moves_list(piece_positions, color)
  enemy_piece_positions = find_pieces(opposite_color(color))
  enemy_possible_moves = find_piece_possible_moves(enemy_piece_positions, opposite_color(color))
  enemy_possible_moves_list = find_piece_possible_moves_list(enemy_piece_positions, opposite_color(color))

  for opponent_piece in enemy_piece_positions: #This part looks through every opponent piece and subtracts its value from the board value
    board_value -= move_value(opponent_piece)
    
  for position_element in piece_positions:
    for opponent_piece in enemy_piece_positions:
      if (opponent_piece in find_piece_type(position_element, color)) and (position_element not in enemy_possible_moves_list) and ((piece_is_guarded(opponent_piece, opposite_color(color)) == False) or ("king" in virtual_board[opponent_piece[0]][opponent_piece[1]])): #This adds the opponent's value if it is being threatened, AI's piece isn't getting threatened, and the opponent piece isn't guarded
        board_value += move_value(opponent_piece)/2
      elif (opponent_piece in find_piece_type(position_element, color)) and (piece_is_guarded(position_element, color)) and (move_value(position_element) < move_value(opponent_piece)): #This adds the opponent's value if it is being threatened, the AI's piece is guarded, and the opponent's value is greater than the AI's
        board_value += move_value(opponent_piece)/2
        board_value -= move_value(position_element)/2
  
  for position_element in piece_positions:
    for key_element in [*enemy_possible_moves]: #This looks through every piece it has and subtracts the pieces value if it is being threatened
      if position_element in enemy_possible_moves[key_element]:
        board_value -= move_value(position_element)
        
        if (piece_is_guarded(position_element, color)) and (move_value(position_element) < move_value(convert_to_index(key_element))):
          board_value += move_value(position_element)
          
        break

    if piece_is_guarded(position_element, color): #Might need to modify how many points are given here
      board_value += move_value(position_element)/50

  board_value += len(possible_moves_list)/2

  return board_value
  

#################################################################################
#Board Setup
#################################################################################

print_board("No Old Position", "No New Move")

#################################################################################
#Start of Game
#################################################################################

while True:
  if check_checkmate(player_turn):
    print(opposite_color(player_turn)[0].upper() + opposite_color(player_turn)[1:] + " Player Wins by Checkmate!")
    break
    
  if player_turn == "white":
    print("White Player's Turn")
    
    while True:
      user_move = input("Please select which piece you would like to move (Ex: a1): ")
  
      if len(user_move) != 2:
        print("That is not a valid piece.")
        continue
  
      if (user_move[0].isnumeric()) or (user_move[1].isnumeric() == False):
        print("That is not a valid piece or the incorrect format.")
        continue

      if user_move[0] not in "abcdefgh" or int(user_move[1]) < 1 or int(user_move[1]) > 8:
        print("The letter or number in your desired move is not in the given range.")
        continue

      user_move = convert_to_index(user_move)

      if opposite_color(player_turn) in virtual_board[user_move[0]][user_move[1]]:
        print("That is not your piece!")
        continue
      elif '-' in virtual_board[user_move[0]][user_move[1]]:
        print("You do not have a piece there.")
        continue

      new_user_move = user_move_choice(find_piece_type(user_move, player_turn))

      if new_user_move == "No Possible Moves" or new_user_move == "back":
        continue

      break
        
    move_piece(user_move, new_user_move)

    print("You moved your piece to " + convert_to_chess_position(new_user_move) + ".")

    for col in range(8):
      if "pawn" in virtual_board[promotion_row[player_turn]][col]:
        print_board(user_move, new_user_move)
        pawn_promotion = input("Which piece would you like to promote your pawn to (queen, rook, bishop, or horse)? ")
        
        if "queen" in pawn_promotion.lower():
          virtual_board[promotion_row[player_turn]][col] = player_turn + "   queen"
        elif "rook" in pawn_promotion.lower():
          virtual_board[promotion_row[player_turn]][col] = player_turn + "    rook"
        elif "bishop" in pawn_promotion.lower():
          virtual_board[promotion_row[player_turn]][col] = player_turn + "  bishop"
        elif "horse" in pawn_promotion.lower():
          virtual_board[promotion_row[player_turn]][col] = player_turn + "   horse"

    print_board(user_move, new_user_move)

    player_turn = "black"

  elif player_turn == "black":
    print("Black Player's Turn")
    
    while True:
      user_move = input("Please select which piece you would like to move (Ex: a1): ")
  
      if len(user_move) != 2:
        print("That is not a valid piece.")
        continue
  
      if (user_move[0].isnumeric()) or (user_move[1].isnumeric() == False):
        print("That is not a valid piece or the incorrect format.")
        continue

      if user_move[0] not in "abcdefgh" or int(user_move[1]) < 1 or int(user_move[1]) > 8:
        print("The letter or number in your desired move is not in the given range.")
        continue

      user_move = convert_to_index(user_move)

      if opposite_color(player_turn) in virtual_board[user_move[0]][user_move[1]]:
        print("That is not your piece!")
        continue
      elif '-' in virtual_board[user_move[0]][user_move[1]]:
        print("You do not have a piece there.")
        continue

      new_user_move = user_move_choice(find_piece_type(user_move, player_turn))

      if new_user_move == "No Possible Moves" or new_user_move == "back":
        continue

      break
        
    move_piece(user_move, new_user_move)

    print("You moved your piece to " + convert_to_chess_position(new_user_move) + ".")

    for col in range(8):
      if "pawn" in virtual_board[promotion_row[player_turn]][col]:
        print_board(user_move, new_user_move)
        pawn_promotion = input("Which piece would you like to promote your pawn to (queen, rook, bishop, or horse)? ")
        
        if "queen" in pawn_promotion.lower():
          virtual_board[promotion_row[player_turn]][col] = player_turn + "   queen"
        elif "rook" in pawn_promotion.lower():
          virtual_board[promotion_row[player_turn]][col] = player_turn + "    rook"
        elif "bishop" in pawn_promotion.lower():
          virtual_board[promotion_row[player_turn]][col] = player_turn + "  bishop"
        elif "horse" in pawn_promotion.lower():
          virtual_board[promotion_row[player_turn]][col] = player_turn + "   horse"

    print_board(user_move, new_user_move)

    player_turn = "white"
      
  else:
    print("Error")