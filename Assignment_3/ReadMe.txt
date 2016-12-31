####################### ASSIGNMENT 3 ####################### 
# Courses - CS 8803 Big Data - Fall 2016
# Yann RAVEL-SIBILLOT
# 10/21/2016

## Implementation of the Apriori Algorithm

# Folder SourceCode
You will find one python file, whish contains the Apriori Algorithm.
Below there is also a folder named Data, which contains dataset, and after launching the program, also outputFile.

# Folder Output:
Give some explain of subset we found with a support above 80% of the number of transaction wrote on the database.


# Start:
You can launch the file main.py, without modification, it will generate all subsets with a support upper 
than 80% of the total number of line of the dataset "Data/chess.dat" 
Then the result is stored on the file "Data/chess_output.dat"

# Modify the input
You just have to modify:
 - the InputFileName with a String
 - the OutputFileName with a String
 - the Threshold with an Integer