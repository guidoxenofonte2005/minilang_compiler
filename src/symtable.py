class Symbol:
  def __init__(self, variable, type):
    self.variable = variable
    self.type = type

class SymTable:
  def __init__(self, previousScope=None):
    self.table: dict = {}
    self.previous = previousScope

  def insert(self, stringValue, symbol):
    if stringValue in self.table:
      return False
    
    self.table[stringValue] = symbol
    return True
  
  def findSymbol(self, symbolStr):
    currentScope = self

    while currentScope is not None:
      if symbolStr in currentScope.table:
        return currentScope.table[symbolStr]
      
      currentScope = currentScope.previous
    
    return None