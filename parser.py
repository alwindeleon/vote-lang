import lex as l
import sys
import inspect

from collections import deque

global dictionary,code
class Node:
  """what is this thing"""
  def __init__(self):
    self.token = None
    self.lexeme = None
    self.lineno = None
    self.offset = None

  def fetch(self, arg1):
    self.token = arg1['tokens'].popleft()
    self.lexeme = arg1['lexemes'].popleft()
    self.lineno = arg1['lineno'].popleft()
    self.offset = arg1['offset'].popleft()

  def peek(self, arg1, arg2):
    self.token = arg1['tokens'][arg2]
    self.lexeme = arg1['lexemes'][arg2]
    self.lineno = arg1['lineno'][arg2]
    self.offset = arg1['offset'][arg2]

  def printall(self):
    print str(self.token) + " '" + str(self.lexeme) + "' " + str(self.lineno) + " " + str(self.offset)

  def comp(self, arg1):
    for y in arg1:
      if self.token == y:
        return True
    return False
  
  def getToken(self):
    return self.token
  
  def getLex(self):
    return self.lexeme

  def getLine(self):
    return self.lineno

  def getOffset(self):
    return self.offset


class ParserError(SyntaxError):
  def __init__(self, node, expected):
    self.token = node.getToken()
    self.lexeme = node.getLex()
    self.lineno = node.getLine()
    self.offset = node.getOffset()
    self.expected = expected


Ident = 0
Int = 1
Float = 2
Bool = 3
Char = 4
String = 5
Plus = 6
Minus = 7
LP = 8
RP = 9
Mult = 10
Div = 11
Mod = 12
Eq = 13
LNot = 14 
LEq = 15
NEq = 16
Greater = 17
GreatEq = 18
Lesser = 19
LessEq = 20
Error = 21
Ballot = 22
Nominate = 23
As = 24
Pork = 25 
Then = 26
Done = 27
Saln = 28
Else = 29
Rally = 30
Campaign = 31 
Vote = 32
Elect = 33
Return = 34
Break = 35
Continue = 36
TInt = 37
TFloat = 38
TBool = 39
TChar = 40
TString = 41
NL = 42
Comma = 43 
Eof = 44

filename = "test.vote"
tabs = 0
i = 0

ctoken = None
ntoken = None
node = Node()

def tabulate():
  global tabs
  for i in xrange(tabs):
    sys.stdout.write('\t')
  sys.stdout.flush()

# def enter(string):
#   global tabs
#   tabulate()
#   print "<" + string + ">"
#   tabs = tabs+1

# def getnext(lis):
#   global i
#   tabulate()
#   sys.stdout.write("Expected ")
#   found = tokens['lexemes'][i]
#   if found == "\n":
#     found = "\\n"
#   for x in lis:
#     if x != lis[-1]:
#       sys.stdout.write("'" + l.actual[x] + "', ")
#     else:
#       sys.stdout.write("'" + l.actual[x] + "', found \"" + found + "\"\n")
#   sys.stdout.flush()
#   i = i+1

def fetch():
  global node, dictionary
  node.fetch(dictionary)
  # print "node"
  # node.printall()
  # print ""

def peek(arg1):
  global dictionary
  node = Node()
  node.peek(dictionary, arg1-1)
  # print "peeknode" + str(arg1)
  # node.printall()
  # print ""
  return node

def error(e,code):
  global filename, tabs, node
  toprint = "Error in file!!!!!! '" + filename + "', line " + str(e.lineno) + "\n"
  # fp = open(filename,'r')
  tmp = tabs
  tabs = 1
  # indent = tabulate()
  # string = ''
  for i in xrange(tabs):
    toprint = toprint + "\t"
  # line = "lmao may bug"
  # print str(e.lineno())
  data = code.split('\n')
  # for i in xrange(int(e.lineno)):
  #   line = fp.readline().splitlines()
  for j in list(data[int(e.lineno)-1]):
    if (j == '\t'):
      toprint = toprint + "\t"
    else:
      break

def start():
  declarationblock()

  fetch()
  if not(node.comp([NL])):
    raise ParserError(node, NL)

  block()

  fetch()
  if not(node.comp([Eof])):
    raise ParserError(node, Eof)

def declarationblock():
  fetch()
  if not(node.comp([Ballot])):
    raise ParserError(node, Ballot)

  fetch()
  if not(node.comp([NL])):
    raise ParserError(node, NL)

  assignblock()

  fetch()
  if not(node.comp([Done])):
    raise ParserError(node, Done)

def assignblock():
  peeknode = peek(1)

  if peeknode.comp([Nominate, Ident]):

    if peeknode.comp([Nominate]):
      declarestatement()
    else:
      assignstatement()

    assignblock()

  elif peeknode.comp([Done]):
    pass
  else:
    raise ParserError(peeknode, Error)

def declarestatement():
  fetch()
  if not(node.comp([Nominate])):
    raise ParserError(node, Nominate)

  fetch()
  if not(node.comp([Ident])):
    raise ParserError(node, Ident)

  fetch()
  if not(node.comp([As])):
    raise ParserError(node, As)

  fetch()
  if not(node.comp([TInt, TFloat, TBool, TChar, TString])):
    raise ParserError(node, Error)

  fetch()
  if not(node.comp([NL])):
    raise ParserError(node, NL)

def assignstatement():
  fetch()
  if not(node.comp([Ident])):
    raise ParserError(node, Ident)

  fetch()
  if not(node.comp([Eq])):
    raise ParserError(node, Eq)

  peeknode = peek(1)
  if (peeknode.comp([Ident])):
    peeknode = peek(2)

    if (peeknode.comp([LP])):
      fcall()

    else:
      expr()

  elif (peeknode.comp([Vote, Elect])):
    fcall()

  else:
    expr()
  
  fetch()
  if not(node.comp([NL])):
    raise ParserError(node, NL)

def block():
  peeknode = peek(1)
  i = 1

  while((peeknode.comp([Ident, Campaign, Vote, Elect, Pork, Rally, NL]))):
    block_()
    peeknode = peek(1)
    i = i + 1

def block_():
  peeknode = peek(1)

  if (peeknode.comp([NL])): #get newline
    fetch()

  elif (peeknode.comp([Ident, Vote, Elect])):

    if (peeknode.comp([Vote, Elect])):

      fcall()

      fetch()
      if not(node.comp([NL])):
        raise ParserError(node, NL)

    else:
      peeknode = peek(2)

      if (peeknode.comp([Eq])):
        assignstatement()

      else:
        fcall()

  elif (peeknode.comp([Campaign])):
    fdec()

  elif (peeknode.comp([Pork])):
    ifblock()

  elif (peeknode.comp([Rally])):
    loopblock()

def fdec():
  fetch()
  if not(node.comp([Campaign])):
    raise ParserError(node, Campaign)

  fetch()
  if not(node.comp([TInt, TFloat, TBool, TChar, TString])):
    raise ParserError(node, Error)

  fetch()
  if not(node.comp([Ident])):
    raise ParserError(node, Ident)

  fetch()
  if not(node.comp([LP])):
    raise ParserError(node, LP)

  decargs()

  fetch()
  if not(node.comp([RP])):
    raise ParserError(node, RP)

  fetch()
  if not(node.comp([NL])):
    raise ParserError(node, NL)

  funcstatement()

  fetch()
  if not(node.comp([Done])):
    raise ParserError(node, Done)

  fetch()
  if not(node.comp([NL])):
    raise ParserError(node, NL)
def decargs():
  peeknode = peek(1)

  if (peeknode.comp([TInt, TFloat, TBool, TChar, TString])):
    fetch() # get type

    fetch()
    if not(node.comp([Ident])):
      raise ParserError(node, Ident)

    decargs_()

def decargs_():
  peeknode = peek(1)

  while((peeknode.comp([Comma]))):
    fetch() # get comma


    fetch() # get type
    if not(node.comp([TInt, TFloat, TBool, TChar, TString])):
      raise ParserError(node, Error)

    fetch()
    if not(node.comp([Ident])):
      raise ParserError(node, Ident)

    peeknode = peek(1)

def funcstatement():
  peeknode = peek(1)

  while (peeknode.comp([Ident, Campaign, Vote, Elect, Pork, Rally, NL, Return])):
    if (peeknode.comp([Return])):
      fetch() # get break or continue

      fetch()
      if not(node.comp([NL])):
        raise ParserError(node, NL)

    else:
      block_()

    peeknode = peek(1)

def fcall():
  fname()

  fetch()
  if not(node.comp([LP])):
    raise ParserError(node, LP)

  callargs()

  fetch()
  if not(node.comp([RP])):
    raise ParserError(node, RP)

def fname():
  fetch()
  if not(node.comp([Ident, Vote, Elect])):
    raise ParserError(node, Error)

def callargs():
  peeknode = peek(1)

  if (peeknode.comp([LP, Ident, Int, Float, Bool, Char, String])):
    expr()
    callargs_()

def callargs_():
  peeknode = peek(1)

  while((peeknode.comp([Comma]))):
    fetch() # get comma

    expr()

    peeknode = peek(1)

def expr():
  term()

  peeknode = peek(1)
  while (peeknode.comp([Plus, Minus])):
    fetch()
    term()
    peeknode = peek(1)

def term():
  factor()

  peeknode = peek(1)
  while (peeknode.comp([Mult, Div, Mod])):
    fetch()
    factor()
    peeknode = peek(1)

def factor():
  peeknode = peek(1)

  if (peeknode.comp([LP])): #branch to ( <factor> )
    fetch() # already is (

    expr()

    fetch()
    if not(node.comp([RP])):
      raise ParserError(node, RP)

  elif (peeknode.comp([Ident, Int, Float, Bool, Char, String])): #branch to <val>
    fetch()

  else:
    raise ParserError(peeknode, Error)

def cond():
  peeknode = peek(1)

  if (peeknode.comp([Bool, Ident])): #it could go to factor or bool
    
    peeknode = peek(2)

    if (peeknode.comp([LEq, NEq, Greater, GreatEq, Lesser, LessEq])): # factor eop factor
      factor() # get bool or ident

      fetch() # get eop

      factor() # get bool or ident

    else:
      fetch() # get bool or ident which is not factor

  elif (peeknode.comp([LP, Int, Float, Char, String])): # sure na factor eop factor
    factor() # get factor

    fetch() # get eop
    if not(node.comp([LEq, NEq, Greater, GreatEq, Lesser, LessEq])):
      raise ParserError(node, Error)

    factor()

def ifblock():
  fetch()
  if not(node.comp([Pork])):
    raise ParserError(node, Pork)

  cond()

  fetch()
  if not(node.comp([Then])):
    raise ParserError(node, Then)

  fetch()
  if not(node.comp([NL])):
    raise ParserError(node, NL)

  block()

  elifblock()

  fetch()
  if not(node.comp([Done])):
    raise ParserError(node, Done)

  fetch()
  if not(node.comp([NL])):
    raise ParserError(node, NL)

def elifblock():
  peeknode = peek(1)

  while (peeknode.comp([Saln])):
    fetch() # got saln

    cond()

    fetch()
    if not(node.comp([Then])):
      raise ParserError(node, Then)

    fetch()
    if not(node.comp([NL])):
      raise ParserError(node, NL)

    block()

  elseblock()

def elseblock():
  peeknode = peek(1)

  if (peeknode.comp([Else])):
    fetch() # get else

    fetch()
    if not(node.comp([NL])):
      raise ParserError(node, NL)

    block()

def loopblock():
  fetch()
  if not(node.comp([Rally])):
    raise ParserError(node, Rally)

  cond()

  fetch()
  if not(node.comp([Then])):
    raise ParserError(node, Then)

  fetch()
  if not(node.comp([NL])):
    raise ParserError(node, NL)

  loopstatement()

  fetch()
  if not(node.comp([Done])):
    raise ParserError(node, Done)

  fetch()
  if not(node.comp([NL])):
    raise ParserError(node, NL)

def loopstatement():
  peeknode = peek(1)

  while (peeknode.comp([Ident, Campaign, Vote, Elect, Pork, Rally, NL, Break, Continue])):
    if (peeknode.comp([Break, Continue])):
      fetch() # get break or continue

      fetch()
      if not(node.comp([NL])):
        raise ParserError(node, NL)

    else:
      block_()

    peeknode = peek(1)

def parse():
  global dictionary
  dictionary = l.get_tokens(filename)

  if (dictionary):
    try:
      start()
    except ParserError as e:
      error(e)