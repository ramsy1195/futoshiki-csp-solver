"""
Each futoshiki board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8

Empty values in the board are represented by 0

An * after the letter indicates the inequality between the row represented
by the letter and the next row.
e.g. my_board['A*1'] = '<' 
means the value at A1 must be less than the value
at B1

Similarly, an * after the number indicates the inequality between the
column represented by the number and the next column.
e.g. my_board['A1*'] = '>' 
means the value at A1 is greater than the value
at A2

Empty inequalities in the board are represented as '-'

"""
import sys

#======================================================================#
#*#*#*# Optional: Import any allowed libraries you may need here #*#*#*#
#======================================================================#

import copy
import numpy as np
import time

#=================================#
#*#*#*# Your code ends here #*#*#*#
#=================================#

ROW = "ABCDEFGHI"
COL = "123456789"

class Board:
    '''
    Class to represent a board, including its configuration, dimensions, and domains
    '''
    
    def get_board_dim(self, str_len):
        '''
        Returns the side length of the board given a particular input string length
        '''
        d = 4 + 12 * str_len
        n = (2+np.sqrt(4+12*str_len))/6
        if(int(n) != n):
            raise Exception("Invalid configuration string length")
        
        return int(n)
        
    def get_config_str(self):
        '''
        Returns the configuration string
        '''
        return self.config_str
        
    def get_config(self):
        '''
        Returns the configuration dictionary
        '''
        return self.config
        
    def get_variables(self):
        '''
        Returns a list containing the names of all variables in the futoshiki board
        '''
        variables = []
        for i in range(0, self.n):
            for j in range(0, self.n):
                variables.append(ROW[i] + COL[j])
        return variables
    
    def convert_string_to_dict(self, config_string):
        '''
        Parses an input configuration string, retuns a dictionary to represent the board configuration
        as described above
        '''
        config_dict = {}
        
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_string[0]
                config_string = config_string[1:]
                
                config_dict[ROW[i] + COL[j]] = int(cur)
                
                if(j != self.n - 1):
                    cur = config_string[0]
                    config_string = config_string[1:]
                    config_dict[ROW[i] + COL[j] + '*'] = cur
                    
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_string[0]
                    config_string = config_string[1:]
                    config_dict[ROW[i] + '*' + COL[j]] = cur
                    
        return config_dict
        
    def print_board(self):
        '''
        Prints the current board to stdout
        '''
        config_dict = self.config
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_dict[ROW[i] + COL[j]]
                if(cur == 0):
                    print('_', end=' ')
                else:
                    print(str(cur), end=' ')
                
                if(j != self.n - 1):
                    cur = config_dict[ROW[i] + COL[j] + '*']
                    if(cur == '-'):
                        print(' ', end=' ')
                    else:
                        print(cur, end=' ')
            print('')
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_dict[ROW[i] + '*' + COL[j]]
                    if(cur == '-'):
                        print(' ', end='   ')
                    else:
                        print(cur, end='   ')
            print('')
    
    def __init__(self, config_string):
        '''
        Initialising the board
        '''
        self.config_str = config_string
        self.n = self.get_board_dim(len(config_string))
        if(self.n > 9):
            raise Exception("Board too big")
            
        self.config = self.convert_string_to_dict(config_string)
        self.domains = self.reset_domains()
        
        self.forward_checking(self.get_variables())
        
        
    def __str__(self):
        '''
        Returns a string displaying the board in a visual format. Same format as print_board()
        '''
        output = ''
        config_dict = self.config
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_dict[ROW[i] + COL[j]]
                if(cur == 0):
                    output += '_ '
                else:
                    output += str(cur)+ ' '
                
                if(j != self.n - 1):
                    cur = config_dict[ROW[i] + COL[j] + '*']
                    if(cur == '-'):
                        output += '  '
                    else:
                        output += cur + ' '
            output += '\n'
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_dict[ROW[i] + '*' + COL[j]]
                    if(cur == '-'):
                        output += '    '
                    else:
                        output += cur + '   '
            output += '\n'
        return output
        
    def reset_domains(self):
        '''
        Resets the domains of the board assuming no enforcement of constraints
        '''
        domains = {}
        variables = self.get_variables()
        for var in variables:
            if(self.config[var] == 0):
                domains[var] = [i for i in range(1,self.n+1)]
            else:
                domains[var] = [self.config[var]]
                
        self.domains = domains
                
        return domains
        
    def forward_checking(self, reassigned_variables):
        '''
        Runs the forward checking algorithm to restrict the domains of all variables based on the values
        of reassigned variables
        '''
        #======================================================================#
		#*#*#*# TODO: Write your implementation of forward checking here #*#*#*#
		#======================================================================#
        
        domains = copy.deepcopy(self.domains)
        for var in reassigned_variables:
            assigned_value = self.config[var]
            row, col = ROW.index(var[0]), int(var[1]) - 1
            
            # Check neighbors in all directions
            directions = {
                'up': (row > 0, ROW[row - 1] + COL[col], ROW[row - 1] + "*" + COL[col], lambda d: d < assigned_value, lambda d: d > assigned_value),
                'down': (row < self.n - 1, ROW[row + 1] + COL[col], ROW[row] + "*" + COL[col], lambda d: d > assigned_value, lambda d: d < assigned_value),
                'left': (col > 0, ROW[row] + COL[col - 1], ROW[row] + COL[col - 1] + "*", lambda d: d < assigned_value, lambda d: d > assigned_value),
                'right': (col < self.n - 1, ROW[row] + COL[col + 1], ROW[row] + COL[col] + "*", lambda d: d > assigned_value, lambda d: d < assigned_value)
            }
    
            for direction in directions.values():
                valid, neighbor, temp, condition1, condition2 = direction
                if valid:
                    # Inequality checks
                    if self.config[temp] == "<":
                        domains[neighbor] = [d for d in domains[neighbor] if condition1(d)]
                    elif self.config[temp] == ">":
                        domains[neighbor] = [d for d in domains[neighbor] if condition2(d)]
                    
                    # Check if any domain becomes empty
                    if not domains[neighbor]:
                        return False
    
            # Check entire row and column for the assigned value
            for i in range(self.n):
                if i != row:
                    neighbor_row = ROW[i] + COL[col]
                    if assigned_value in domains[neighbor_row]:
                        domains[neighbor_row].remove(assigned_value)
                        if not domains[neighbor_row]:
                            return False
    
                if i != col:
                    neighbor_col = ROW[row] + COL[i]
                    if assigned_value in domains[neighbor_col]:
                        domains[neighbor_col].remove(assigned_value)
                        if not domains[neighbor_col]:
                            return False
                        
        self.domains = domains
        return True
        
        #=================================#
		#*#*#*# Your code ends here #*#*#*#
		#=================================#
        
    #=================================================================================#
	#*#*#*# Optional: Write any other functions you may need in the Board Class #*#*#*#
	#=================================================================================#
    
    #=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#

#================================================================================#
#*#*#*# Optional: You may write helper functions in this space if required #*#*#*#
#================================================================================#        

#=================================#
#*#*#*# Your code ends here #*#*#*#
#=================================#

def backtracking(board):
    '''
    Performs the backtracking algorithm to solve the board
    Returns only a solved board
    '''
    #==========================================================#
	#*#*#*# TODO: Write your backtracking algorithm here #*#*#*#
	#==========================================================#
    
    var = board.get_variables()
        
    if all(board.config[v] !=0 for v in var):
        config_str = ''.join(
            str(board.config[key]) 
            for key in board.config.keys()
        )
        board.config_str = config_str
        return board
        
    remaining_var = [v for v in var if board.config[v] == 0]
    remaining_var.sort(key = lambda v: len(board.domains[v]))
        
    assign_var = remaining_var[0]
        
    for value in board.domains[assign_var]:
        original_domains = copy.deepcopy(board.domains)
        board.config[assign_var] = value
        if board.forward_checking([assign_var]):
            result = backtracking(board)
            if result is not None:
                return result
                
        board.config[assign_var] = 0
        
        board.domains = original_domains
     
    return None

    #=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#
    
def solve_board(board):
    '''
    Runs the backtrack helper and times its performance.
    Returns the solved board and the runtime
    '''
    #================================================================#
	#*#*#*# TODO: Call your backtracking algorithm and time it #*#*#*#
	#================================================================#
    
    start_time = time.time()
    solved_board = backtracking(board)
    runtime = time.time() - start_time
    return solved_board, runtime

    #=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#

def print_stats(runtimes):
    '''
    Prints a statistical summary of the runtimes of all the boards
    '''
    min = 100000000000
    max = 0
    sum = 0
    n = len(runtimes)

    for runtime in runtimes:
        sum += runtime
        if(runtime < min):
            min = runtime
        if(runtime > max):
            max = runtime

    mean = sum/n

    sum_diff_squared = 0

    for runtime in runtimes:
        sum_diff_squared += (runtime-mean)*(runtime-mean)

    std_dev = np.sqrt(sum_diff_squared/n)

    print("\nRuntime Statistics:")
    print("Number of Boards = {:d}".format(n))
    print("Min Runtime = {:.8f}".format(min))
    print("Max Runtime = {:.8f}".format(max))
    print("Mean Runtime = {:.8f}".format(mean))
    print("Standard Deviation of Runtime = {:.8f}".format(std_dev))
    print("Total Runtime = {:.8f}".format(sum))


if __name__ == '__main__':
    if len(sys.argv) > 1:

        # Running futoshiki solver with one board $python3 futoshiki.py <input_string>.
        print("\nInput String:")
        print(sys.argv[1])
        
        print("\nFormatted Input Board:")
        board = Board(sys.argv[1])
        board.print_board()
        
        solved_board, runtime = solve_board(board)
        
        print("\nSolved String:")
        print(solved_board.get_config_str())
        
        print("\nFormatted Solved Board:")
        solved_board.print_board()
        
        print_stats([runtime])

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(solved_board.get_config_str())
        outfile.write('\n')
        outfile.close()

    else:
        # Running futoshiki solver for boards in futoshiki_start.txt $python3 futoshiki.py

        #  Read boards from source.
        src_filename = 'futoshiki_start.txt'
        try:
            srcfile = open(src_filename, "r")
            futoshiki_list = srcfile.read()
            srcfile.close()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        
        runtimes = []

        # Solve each board using backtracking
        for line in futoshiki_list.split("\n"):
            
            print("\nInput String:")
            print(line)
            
            print("\nFormatted Input Board:")
            board = Board(line)
            board.print_board()
            
            solved_board, runtime = solve_board(board)
            runtimes.append(runtime)
            
            print("\nSolved String:")
            print(solved_board.get_config_str())
            
            print("\nFormatted Solved Board:")
            solved_board.print_board()

            # Write board to file
            outfile.write(solved_board.get_config_str())
            outfile.write('\n')

        # Timing Runs
        print_stats(runtimes)
        
        outfile.close()
        print("\nFinished all boards in file.\n")
