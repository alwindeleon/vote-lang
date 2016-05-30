from collections import deque

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

lexemes = ['identifier', #0
        'integer',
        'float',
        'bool',
        'char',
        'string',
        'add_op',
        'sub_op',
        'left_p',
        'right_p',
        'mult_op', #10
        'div_op',
        'mod_op',
        'eq_assign',
        'not',
        'logical_eq', 
        'not_eq',
        'greater',
        'greater_eq',
        'less',
        'less_eq', #20
        'error',
        'assign_block',
        'assign',
        'as',
        'if',
        'then',
        'done',
        'else_if',
        'else',
        'loop', #30
        'f_dec',
        'read',
        'print',
        'return',
        'break',
        'continue',
        'type_int',
        'type_float',
        'type_bool',
        'type_char', #40
        'type_str',
        'newline',
        'separator',
        'eof']

actual = ['identifier', #0
        'integer',
        'float',
        'bool',
        'char',
        'string',
        '+',
        '-',
        '(',
        ')',
        '*', #10
        '/', 
        '%',
        '=',
        '!',
        '==', 
        '!=',
        '>',
        '>=',
        '<',
        '<=', #20
        'a valid token',
        'ballot',
        'nominate',
        'as',
        'pork',
        'then',
        'done',
        'saln',
        'else',
        'rally', #30
        'campaign',
        'vote',
        'elect',
        'return',
        'break',
        'continue',
        'type integer',
        'type float',
        'type boolean',
        'type char', #40
        'type string',
        '\\n',
        ',',
        'eof'] #40

line = 1
offset = -1

class TokenError(SyntaxError):
    def __init__(self, lineno, lexeme, expected):
        self.lineno = lineno
        self.lexeme = lexeme
        self.expected = expected

def peek(f):                            #returns the next char, but doesn't shift to it
        pos = f.tell()
        data = f.read(1)
        f.seek(pos)
        return data

def lexical_analyzer(f):                             #returns a dictionary containing the lexeme and its token
        global offset, line
        array = []                      #contains the lexeme
        nextToken = -1
        nextChar = ""            #get the next char to be read
        curOffset = offset
        curLine = line
        while True:
                nextChar = f.read(1)     #incase it got a whitespace
                offset = offset+1
                curOffset = offset
                if nextChar != ' ' and nextChar != '\t':
                    break
        if not nextChar:
                nextToken == EOF
                array.append('E')
                array.append('O')
                array.append('F')
        elif nextChar == "\n":
                nextToken = NEWLINE
                array.append('\n')
                offset = -1
                line = line + 1
                # array.append('n')
        elif nextChar.isalpha() and nextChar != '"':              #a variable: it starts with a letter
                array.append(nextChar)      #add the char to the lexeme
                while peek(f).isalpha() or peek(f).isdigit():
                        nextChar = f.read(1)
                        offset = offset+1
                        array.append(nextChar)

                if ''.join(array) == "true" or ''.join(array) == "false" :
                    nextToken = BOOL

                if nextToken < 0 :
                    nextToken = IDENTIFIER
                
        elif nextChar.isdigit():            #an integer: it starts with a digit
                array.append(nextChar)
                nextToken = INTEGER
                while peek(f).isdigit() or peek(f) == '.':
                        nextChar = f.read(1)
                        offset = offset+1
                        # print nextChar    #get the next digit to be read
                        if nextChar == '.':
                                nextToken = FLOAT
                        array.append(nextChar)
                
                
        elif not nextChar.isalpha():        #a symbol
                if nextChar == '"':        #a string: it starts with doublequote
                        array.append(nextChar)
                        nextChar = f.read(1)
                        offset = offset+1
                        while nextChar != '"' and nextChar != '\n':     #ends if it reaches the next doublequote
                                array.append(nextChar)
                                nextChar = f.read(1)
                                offset = offset+1
                        if nextChar == '"':
                            array.append(nextChar)
                            nextToken = STRING
                        else:
                            nextToken = ERROR
                            raise TokenError(curLine, ''.join(array), STRING)

                elif nextChar == '\'':
                        array.append(nextChar)
                        nextChar = f.read(1)
                        offset = offset+1
                        array.append(nextChar)
                        nextChar = f.read(1)
                        offset = offset+1
                        if nextChar == "'":
                            array.append(nextChar)
                            nextToken = CHAR
                        else:
                            nextToken = ERROR
                            raise TokenError(curLine, ''.join(array), CHAR)
                        
                elif nextChar == '+':
                        array.append(nextChar)
                        nextToken = ADD_OP
                        
                elif nextChar == '-':
                        array.append(nextChar)
                        nextToken = SUB_OP
                        
                elif nextChar == '(':
                        array.append(nextChar)
                        nextToken = LEFT_P
                        
                elif nextChar == ')':
                        array.append(nextChar)
                        nextToken = RIGHT_P
                        
                elif nextChar == '*':
                        array.append(nextChar)
                        nextToken = MULT_OP
                        
                elif nextChar == '/':
                        array.append(nextChar)
                        nextToken = DIV_OP
                        
                elif nextChar == '%':
                        array.append(nextChar)
                        nextToken = MODULO
                        
                elif nextChar == '=':
                        array.append(nextChar)
                        if peek(f) == '=':
                                nextChar = f.read(1)
                                offset = offset+1
                                array.append(nextChar)
                                nextToken = LOGICAL_EQ
                        else:
                                nextToken = EQ_ASSIGN
                                
                elif nextChar == '!':
                        array.append(nextChar)
                        if peek(f) == '=':
                            nextChar = f.read(1)
                            offset = offset+1
                            array.append(nextChar)
                            nextToken = NOT_EQ
                        else:
                            nextToken = NOT
                        
                elif nextChar == '<':
                        array.append(nextChar)
                        if peek(f) == '=':
                                nextChar = f.read(1)
                                offset = offset+1
                                array.append(nextChar)
                                nextToken = LESS_EQ
                        else:
                                nextToken = LESS
                                
                elif nextChar == '>':
                        array.append(nextChar)
                        if peek(f) == '=':
                                nextChar = f.read(1)
                                offset = offset+1
                                array.append(nextChar)
                                nextToken = GREATER_EQ
                        else:
                                nextToken = GREATER

                elif nextChar == ',':
                        array.append(nextChar)
                        nextToken = SEPARATOR

                else:
                        array.append(nextChar)
                        nextToken = ERROR
                        raise TokenError(curLine, ''.join(array), ERROR)

        return {'lexeme':array, 'token':nextToken, 'lineno': curLine, 'offset': curOffset}


lexeme = "foo"  #string or integer representation of the lexeme
token = -1      #the token of the lexeme, list of tokens is at the top of the file

def lex(f):     #returns a dictionary
        result = lexical_analyzer(f)
        list_r = result['lexeme']
        token = result['token']
        lineno = result['lineno']
        offset = result['offset']
        if token == INTEGER:
                lexeme = int(''.join(map(str,list_r)))
        else:   #a string or a symbol
                lexeme = ''.join(map(str,list_r))
                if lexeme == "ballot":
                        token = ASSIGN_BLOCK
                elif lexeme == "nominate":
                        token = ASSIGN
                elif lexeme == "as":
                        token = AS
                elif lexeme == "pork":
                        token = IF
                elif lexeme == "then":
                        token = THEN
                elif lexeme == "done":
                        token = DONE
                elif lexeme == "saln":
                        token = ELSE_IF
                elif lexeme == "else":
                        token = ELSE
                elif lexeme == "rally":
                        token = LOOP
                elif lexeme == "end":
                        token = LOOP_DONE
                elif lexeme == "campaign":
                        token = F_DEC
                elif lexeme == "vote":
                        token = READ
                elif lexeme == "elect":
                        token = PRINT
                elif lexeme == "return":
                        token = RETURN
                elif lexeme == "break":
                        token = BREAK
                elif lexeme == "continue":
                        token = CONTINUE
                elif lexeme == "int":
                        token = TYPE_INT
                elif lexeme == "float":
                        token = TYPE_FLOAT
                elif lexeme == "char":
                        token = TYPE_CHAR
                elif lexeme == "string":
                        token = TYPE_STR
                elif lexeme == "\n":
                        token = NEWLINE
                elif lexeme == "EOF":
                        token = EOF
        # if token != 17:
        return {'lexeme':lexeme, 'token':token, 'lineno': lineno, 'offset': offset}

def get_tokens(string):
        fp = open(string, "r")      #open the file
        tokens = deque()
        lexemes = deque()
        lineno = deque()
        offset = deque()
        i = 0
        try:
            while True:                 #make sure that the next char that can be read is not the end of file
                    result = lex(fp)        #read the next lexeme
                    lexemes.append(result['lexeme'])      #set the lexeme
                    tokens.append(result['token'])        #set the token
                    lineno.append(result['lineno'])
                    offset.append(result['offset'])
                    # if lexemes[i] == "\n":
                    #     print "\\n:" + str(tokens[i]) + " at (" + str(lineno[i]) + "," + str(offset[i]) + ")"
                    # else :
                    #     print str(lexemes[i]) + ":" + str(tokens[i]) + " at (" + str(lineno[i]) + "," + str(offset[i]) + ")"
                    if tokens[i] == EOF :
                        break
                    i = i + 1
            fp.close()                      #close the file
            dicto = {'lexemes':lexemes, 'tokens':tokens, 'lineno':lineno, 'offset':offset}
            return dicto
        except TokenError as e:
            print "Lexical Error at line " + str(e.lineno) + ": got '" + e.lexeme + "' but expected '" + actual[e.expected] + "'"

# get_tokens(raw_input())