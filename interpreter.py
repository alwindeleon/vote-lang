IDENTIFIER = 0 #(variables and reserved words)
INTEGER = IDENTIFIER+1
FLOAT = INTEGER+1
BOOL = FLOAT+1
CHAR = BOOL+1
STRING = CHAR+1

ADD_OP = STRING+1
SUB_OP = ADD_OP+1
LEFT_P = SUB_OP+1
RIGHT_P = LEFT_P+1
MULT_OP = RIGHT_P+1 #10
DIV_OP = MULT_OP+1
MODULO = DIV_OP+1
EQ_ASSIGN = MODULO+1
NOT = EQ_ASSIGN+1
LOGICAL_EQ = NOT+1
NOT_EQ = LOGICAL_EQ+1
GREATER = NOT_EQ+1
GREATER_EQ = GREATER+1
LESS = GREATER_EQ+1
LESS_EQ = LESS+1 #20
ERROR = LESS_EQ+1

ASSIGN_BLOCK = ERROR+1
ASSIGN = ASSIGN_BLOCK+1
AS = ASSIGN+1
IF = AS+1
THEN = IF+1
DONE = THEN+1
ELSE_IF = DONE+1
ELSE = ELSE_IF+1
LOOP = ELSE+1 #30
F_DEC = LOOP+1
READ = F_DEC+1
PRINT = READ+1
RETURN = PRINT+1
BREAK = RETURN+1
CONTINUE = BREAK+1
TYPE_INT = CONTINUE+1
TYPE_FLOAT = TYPE_INT+1
TYPE_BOOL = TYPE_FLOAT+1
TYPE_CHAR = TYPE_BOOL+1 #40
TYPE_STR = TYPE_CHAR+1
NEWLINE = TYPE_STR+1
SEPARATOR = NEWLINE+1
EOF = SEPARATOR+1

#import sys and traceback for exception handling (to find info on exceptions)
from lex import get_tokens
import sys
import traceback
#python.py is the default name for the python file we will create from interpreting the input file
def interpret():
  output = open("python.py", "w")
  #dictionary is where lexemes and tokens from the input file are stored
  dictionary = get_tokens("test.vote")
  lexe = dictionary["lexemes"]
  token = dictionary["tokens"]
  #index is our iterator through the tokens
  index = 0
  #two arrays are initialized, this is where we will store the declared variables and their types (indexes are also synchronized)
  nom_variables = []
  nom_types = []
  #the area variable will differentiate which area of the code we are in (whether declaration, or the code proper)
  area = 0
  #errornumber is the variable we use to know what error has occured (0 means no error)
  errornumber = 0
  #end is our condition variable to see if the interpretation should continue
  end = 0
  #line_number tracks the line number
  line_number = 1
  #tabcounter tracks the number of tabs we need to print onto our python code
  tabcounter = 0
  #the beginning of our interpretation loop, it should only stop once we reach end of file or there is an error
  while end==0:
    #Making sure the code begins with 'ballot', errors here are handled by the parser
    if(token[0] == ASSIGN_BLOCK):
      index+=1
      if(token[1] == NEWLINE):
        index+=1
        area = 1
        output.write("\n")
    #Moving on to the declaration block
    while area < 2:
      line_number+=1
      #If the next token is a declaration token, we check if the variable has already been declared, if not, we add the variable and its tye to our lists, and we print its declaration in the python code for formality
      #If it has already been declared, this will cause an error
      if(token[index] == ASSIGN):
        index+=1
        if (nom_variables.count(lexe[index]) == 0):
          nom_variables.append(lexe[index])
          output.write(lexe[index])
          output.write("=None")
        else:
          errornumber = 4 #ERROR VARIABLE ALREADY DECLARED
          end = 1
          area = 3
          break
        index+=1
        index+=1
        if (errornumber == 0):
          nom_types.append(token[index])
        index+=1
      #If the next token is a variable, we check if it has already been declared, if it has not, we raise error 3
      #If it has been declared, we check its type and compare it to every term that it is being assigned to to make sure it is of the same type
      elif(token[index] == IDENTIFIER):
        if (nom_variables.count(lexe[index]) > 0):
          nom_location = nom_variables.index(lexe[index])
          temp_type = nom_types[nom_location]
          output.write(lexe[index])
          output.write("=")
          index+=1
          index+=1
          while (token[index] != NEWLINE):
            #checking if is is being assigned to a constant (or if there is a constant in the expression)
            if (INTEGER <= token[index] <= STRING):
              #if the constant is not equal to the type of the variable, error 5 will be raised
              if (token[index] != temp_type-36):
                errornumber = 5 #ERROR: WRONG TYPE
                end = 1
                area = 3
                break
            #checking if it is being assigned to another variable (or if there is another variable in the expression)
            elif (token[index] == IDENTIFIER):
              #checking to see if the other variable is already declared
              if (nom_variables.count(lexe[index]) == 0):
                errornumber = 3 #ERROR: VAR NOT DECLARED YET
                end = 1
                area = 3
                break
              else:
                new_nom_location = nom_variables.index(lexe[index])
                new_temp_type = nom_types[new_nom_location]
                #Checking to see if the two variables have the same type, if not, error 5 will be raised
                if (temp_type != new_temp_type):
                  errornumber = 5 #ERROR: WRONG TYPE
                  end = 1
                  area = 3
                  break
            #If the token is any other character, we write it on to the output file
            output.write(str(lexe[index]))
            index+=1
        else:
          errornumber = 3 #ERROR: VARIABLE NOT DECLARED YET
          end = 1
          area = 3
          break
      #If there is a newline, we write it and move on
      if(token[index] == NEWLINE):
        index+=1
        output.write("\n")
      #If the next token is 'done', then this signals the end of the declaration block
      if(token[index] == DONE):
        area = 2
        index+=1
    #This is the loop for interpreting the code proper
    while area < 3:
      line_number+=1
      #y is our count variable for printing tabs
      y = 0
      #if the next token is 'print', we write the current number of tabs and then the print statement followed by any number of terms
      #every if statement from here on will include printing the current number of tabs
      if(token[index] == PRINT):
        while (y < tabcounter):
          output.write("\t")
          y+=1
        output.write("print ")
        #left par
        index+=1
        index+=1
        while (token[index] != RIGHT_P):
          if(token[index] == SEPARATOR):
            output.write(",")
          else:
            output.write(lexe[index])
          index+=1
        index+=1
      #if the next token is 'read', we simply write the built in read function into our python file
      elif(token[index] == READ):
        while (y < tabcounter):
          output.write("\t")
          y+=1
        index+=1
        #left par
        index+=1
        #if it has not been declared, we raise error 3
        if (nom_variables.count(lexe[index]) == 0):
          errornumber = 3
          end = 1
          area = 3
          break
        output.write(lexe[index])
        nom_location = nom_variables.index(lexe[index])
        temp_type = nom_types[nom_location]
        if (temp_type >= 40):
          output.write(" = raw_input()")
        else:
          output.write(" = int(raw_input())")
        #right par
        index+=1
        index+=1
      #if the next token is a function declaration, we do several things
      elif(token[index] == F_DEC):
        #we first write the keyword def into our python code
        output.write("def ")
        index+=1
        index+= 1
        #we write the function name
        output.write(lexe[index])
        index+=1
        #we write the left par
        output.write(lexe[index])
        index+=1
        while (token[index] != NEWLINE):
          #if the next token is a variable, we write it into our file, if it is a type, we skip it
          if (token[index] == IDENTIFIER):
            output.write(lexe[index])
          else:
            index+=1
            continue
          index+=1
          #if the next token is a right par, we write it and break the loop
          if (token[index] == RIGHT_P):
            output.write(lexe[index])
            index+=1
            break
          output.write(", ")
        output.write(":")
        #we increase the tab count by one
        tabcounter+=1
      #if the next token is return, we write it and any succeeding terms
      elif(token[index] == RETURN):
        while (y < tabcounter):
          output.write("\t")
          y+=1
        output.write("return ")
        index+=1
        while (token[index] != NEWLINE):
          output.write(str(lexe[index]))
          index+=1
      #if the next token is a loop declaration, we write while into our output code and any condition that comes after
      elif(token[index] == LOOP):
        while (y < tabcounter):
          output.write("\t")
          y+=1
        output.write("while ")
        index+=1
        check_then = 0
        while (token[index] != NEWLINE):
          if (token[index] == THEN):
            check_then = 1
          else:
            output.write(str(lexe[index]))
          index+=1
        output.write(":")
        if (check_then == 0):
          errornumber = 6 #ERROR: FORGOT 'THEN'
          end = 1
          area = 3
          break
        tabcounter+=1
      #if the next token is a variable (which means there will be an assignment statement), we first check if the variable has been declared
      elif(token[index] == IDENTIFIER):
        #if it has not been declared, we raise error 3
        if (nom_variables.count(lexe[index]) == 0):
          errornumber = 3
          end = 1
          area = 3
          break
        while (y < tabcounter):
          output.write("\t")
          y+=1
        #we write everything else afterwards
        while (token[index] != NEWLINE):
          output.write(str(lexe[index]))
          index+=1
      #if the next token is an if declaration, we do several things
      elif(token[index] == IF):
        while (y < tabcounter):
          output.write("\t")
          y+=1
        #we write 'if' into our file, and initialize check_then which will be our variable to check if a 'then' keyword had been written
        output.write("if ")
        index+=1
        check_then = 0
        #we write anything afterwards
        while (token[index] != NEWLINE):
          if (token[index] == THEN):
            check_then = 1
          else:
            output.write(str(lexe[index]))
          index+=1
        #we write ':' to match python syntax
        output.write(":")
        #we check now to see if a 'then' was written, if not we raise error 6
        if (check_then == 0):
          errornumber = 6 #ERROR: FORGOT 'THEN'
          end = 1
          area = 3
          break
        #we increase the tab count
        tabcounter+=1
      #if the next token is an else if, we do the same thing as above, but replacing the 'if' with 'elif'
      elif(token[index] == ELSE_IF):
        y=1
        while (y < tabcounter):
          output.write("\t")
          y+=1
        output.write("elif ")
        index+=1
        check_then = 0
        while (token[index] != NEWLINE):
          if (token[index] == THEN):
            check_then = 1
          else:
            output.write(str(lexe[index]))
          index+=1
        output.write(":")
        if (check_then == 0):
          errornumber = 6 #ERROR: FORGOT 'THEN'
          end = 1
          area = 3
          break
      #if the next token is 'else', we simply write 'else:' into our file
      elif(token[index] == ELSE):
        y=1
        while (y < tabcounter):
          output.write("\t")
          y+=1
        output.write("else ")
        index+=1
        output.write(":")
      #if the next token is 'done', we simply print skip it and decrease the tab count
      elif(token[index] == DONE):
        index+=1
        tabcounter-=1
      #if the next token is a break statement, we just write it into our python code
      elif(token[index] == BREAK):
        output.write("break")
        index+=1
      #after every iteration, we check to see if we print a newline
      if(token[index] == NEWLINE):
        index+=1
        output.write("\n")
      #if we have reached te end of file, we exit the loop
      if(token[index] == EOF):
        area = 3
        end = 1
        index+=1
    

  #we stop reading the file and close it
  output.close()


  #Reference: http://stackoverflow.com/questions/28836078/how-to-get-the-line-number-of-an-error-from-exec-or-execfile-in-python
  class InterpreterError(Exception): pass

  #This function runs 'exec' on our newly made file, and catches the exceptions and tracks them to a line number corresponding to the line number in our input file
  def my_exec(cmd, description):
    #we try executing our file (with our scope being declared to be the scope of the file we are executing)
      try:
          exec cmd in dict()
    #we try to catch any syntax errors we may have missed in the parser, and then get its details and line number
      except SyntaxError as err:
          error_class = err.__class__.__name__
          detail = err.args[0]
          line_number = err.lineno
    #we catch other exceptions and its details and line numbers
      except Exception as err:
          error_class = err.__class__.__name__
          detail = err.args[0]
          cl, exc, tb = sys.exc_info()
          line_number = traceback.extract_tb(tb)[-1][1]
      else:
          return
    #we print our formatted details of the exception
      raise InterpreterError("\n\n%s at line %d of %s: %s" % (error_class, line_number, description, detail))

  #the name of our input file
  file_name = "test.vote"

  #if we have no errors, we call the my_exec function and run it to see if there are no errors again!
  #if there are errors, we print the error to terminal
  #ERROR LIST:
  # 3 - Undeclared Variable
  # 4 - Variable Already Declared
  # 5 - Type Error
  # 6 - Lack of 'then' Error
  # More to come!
  if (errornumber == 0):
    code= open("python.py", "r").read().split("raw_input()")
    code = "tkSimpleDialog.askstring('INPUT', '')".join(code)
    code = "import tkSimpleDialog\n" + code 
    my_exec(code, file_name)
  elif (errornumber == 3):
    print "NameError at line", line_number, "of", file_name, ": Undeclared Variable"
  elif (errornumber == 4):
    print "NameError at line", line_number, "of", file_name, ": Variable already declared"
  elif (errornumber == 5):
    print "TypeError at line", line_number, "of", file_name, ": Wrong Type Assignment"
  elif (errornumber == 6):
    print "SyntaxError at line", line_number, "of", file_name, ": Forgot 'then'"





