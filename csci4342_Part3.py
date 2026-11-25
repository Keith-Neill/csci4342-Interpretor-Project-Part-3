"""
Student Name: Keith Neill
Program Name: Interpreter Project Part 3
Description: This program reads a file with SFAscal code and displays the type of token associated with each lexeme. 
             This program displays the output as lexeme : token name. for example, the output “x : Identifier Token” tells the user that the lexeme, x, is an identifier token.  
"""

import sys
import re
from dataclasses import dataclass
from typing import Callable, NoReturn, Union


@dataclass(frozen=True)
class Variable:
    identifier: int | bool | str



@dataclass(frozen=True)
class BinaryOperation:
    """Twooperandsjoinedbyanoperatorsuchas+,divor<=."""

    operator:str
    left: Expression
    right: Expression
    #endofClass"BinaryOperation"


@dataclass(frozen=True)
class Assignment:
    """<variable>:=<expression>"""

    target: Variable
    value: Expression
    #line:int
    #endofClass"Assignment"


@dataclass(frozen=True)
class Compound:
    """begin<statement>{;<statement>}end"""

    statements: list[Statement]
    #line: int
    #endofClass"Compound"
 
@dataclass(frozen=True)
class IfStatement:
    

    condition: Expression
    then_part: Statement
    else_part: Statement
    #endofClass"IfStatement"

@dataclass(frozen=True)
class WhileStatement:
    
    condition: Expression
    inner_loop_part: Statement
    #endofClass"WhileStatement"

@dataclass(frozen=True)
class ProcedureBlock:
    
    variable_part: Variable
    statement_part: Statement
    #endofClass"ProcedureBlock"

@dataclass(frozen=True)
class ProcedureDeclaration:
    
    identifier: Variable
    procedure_block: ProcedureBlock
    #endofClass"ProcedureDeclaration"

@dataclass(frozen=True)
class VariableDeclaration:
    
    name: Variable
    type: str
    #endofClass"VariableDeclaration"

@dataclass(frozen=True)
class Block:
    
    variable: Variable
    procedure: ProcedureDeclaration
    statement: Statement
    #endofClass"Block"

@dataclass(frozen=True)
class Program:
    
    identifier: Variable
    block: Block
    #endofClass"VariableDeclaration"

@dataclass(frozen=True)
class WriteStatement:
    """write ( <output value> )"""

    value: Expression

@dataclass(frozen=True)
class ReadStatement:
    """Read ( <input value> )"""

    target: Variable 


# The kinds of node an expression can be.
Expression = Union[Variable, BinaryOperation]

Statement = Union[Assignment, ProcedureBlock, Compound, IfStatement,
                  WhileStatement, ReadStatement, WriteStatement]

# <identifier>
def identifier():
    global i
    if lexeme_tokens[i] == "Identifier Token":
        # if lexeme is an identifier, consume it by incrementing i by 1 and return i
        value = lexemes[i]
        i = i+1
        
        return Variable(value)
    else:
        print("Error: expected an identifier token, got", lexeme_tokens[i], "instead. '",lexemes[i],"' is not a valid identifier.")
        sys.exit(1)

# <factor>
def factor():
    global i

    # if "(<expression>)"
    if lexemes[i] == "(":
        i = i+1 # consume (
        ex = expression()
        if lexemes[i] == ")":
            i = i+1 # consume )
            return ex 
        else:
            print("Error: Expected ')' after expression.")
            sys.exit(1)

    if lexeme_tokens[i] == "Integer Token" or lexeme_tokens[i] == "Boolean Token":
        
        i = i+1 # <constant>
        return lexemes[i]
    
    elif lexemes[i] == "not":
        
        i = i+1 # consume "not"
        return factor()
    elif lexeme_tokens[i] == "Identifier Token":
        return identifier()
    else:
        print("Error: ", lexemes[i], "cannot be a factor")
        sys.exit(1)

    #return lexemes(i)

# <term>
def term():
    global i
    tree = factor()
    if lexeme_tokens[i] == "Multiplication Token":
        multiply_more_factors = True
    else:
        multiply_more_factors = False
    
    while multiply_more_factors:
        operation = lexemes[i]
        i = i+1 # consume multiplication lexeme
        right = factor()
        tree = BinaryOperation(operation, tree, right)
        if lexeme_tokens[i] != "Multiplication Token":
            multiply_more_factors = False
    
    return tree

# <simple expression>
def simple_expression():
    global i
    tree = term()
    if lexeme_tokens[i] == "Addition Token":
        add_more_terms = True
    else:
        add_more_terms = False
        
    while add_more_terms:
        operation = lexemes[i]
        i = i+1 # consume addition lexeme
        right = term()
        tree = BinaryOperation(operation, tree, right)
        if lexeme_tokens[i] != "Addition Token":
            add_more_terms = False
        
    return tree


# <expression>
def expression():
    global i
    left = simple_expression()
    if lexeme_tokens[i] == "Relation Token":
        operation = lexemes[i]
        i = i+1 # consume lexeme with relation token
        right = simple_expression()
        return BinaryOperation(operation, left, right)
    
    return left 

# <assignment statement>
def assignment_statement():
    global i
    target = identifier()
    if lexeme_tokens[i] == "Assignment Token":
        i = i+1
    else:
        print("Error: Expected Assignment Token, got", lexeme_tokens[i], "instead.")
        sys.exit(1)

    value = expression()
    
    return Assignment(target, value)


# <read statement>
def read_statement():
    global i
    i = i+1 # consume "read"
    i = i+1 # consume (
    id = identifier()
    if lexemes[i] == ")":
        i = i+1 # consume )
    else:
        print("Error: ')' is expected after read statement")
        sys.exit(1)
    
    return ReadStatement(id)

# <write statement>
def write_statement():
    global i
    i = i+1 # consume "write"
    i = i+1 # consume (
    wr = expression() # <output value>
    if lexemes[i] == ")":
        i = i+1 # consume )
    else:
        print("Error: ')' is expected after write statement")
        sys.exit()
    return WriteStatement(wr)

# <simple statement>
def simple_statement():
    
    if lexeme_tokens[i] == "Identifier Token" and lexeme_tokens[i+1] == "Assignment Token":
      return assignment_statement()
    elif lexeme_tokens[i] == "Identifier Token":
        return identifier() # <procedure statement>
    elif lexemes[i] == "read":
        return read_statement()
    elif lexemes[i] == "write":
        return write_statement()
    else:
        print("Error: ",lexemes[i],"is not recognised as a statement.")
        sys.exit(1)
       


# <if statement>
def if_statement():
    global i
    i = i+1 # consume "if"
    condition = expression()
    if lexemes[i] == "then":
        i = i+1 # consume then
    else:
        print("Error: Expected 'then' after if statenent.")
        sys.exit(1)
    then_part = statement()
    if lexemes[i] == "else":
        i = i+1 # consume else
        else_part = statement()
    return IfStatement(condition, then_part, else_part)

# <while statement>
def while_statement():
    global i
    i = i+1 # consume while
    condition = expression()
    if lexemes[i] == "do":
        i = i+1 # consume do
    else:
        print("Error: Expected 'do' after exopression in while statement.")
        sys.exit(1)
    inner_loop_part = statement()
    return WhileStatement(condition, inner_loop_part) 

# <structured statenebt>
def structured_statement():
    if lexemes[i] == "begin":
        return compound_statement()
    elif lexemes[i] == "if":
        return if_statement()
    elif lexemes[i] == "while":
        return while_statement()
    else:
        print("Error: ",lexemes[i], " is not recognised as a structured statement.")
        return


# <statement>
def statement():
    
    if lexeme_tokens[i] == "Identifier Token" or lexemes[i] == "read" or lexemes[i] == "write":
       return simple_statement()
    elif lexemes[i] == "begin" or lexemes[i] == "if" or lexemes[i] == "while":
        return structured_statement()
    elif lexemes[i] == "end" or lexemes[i] == ";":
        return  # <empty statement>
    else:
        print("Error: ", lexemes[i], "is not the start of a valid statement.")
        sys.exit(i)


# <compound statement>
def compound_statement():
    global i
    if lexemes[i] == "begin":
        i = i+1 # consume "begin"
        
    else:
        print("Error: Expected lexene 'begin', got", lexemes[i], "instead")
        sys.exit(1)

    statements = [statement()]
    
    if lexemes[i] == ";":
       more_statements = True
    else:
        more_statements = False

    while more_statements:
        i = i+1 # consume ;
        statements.append(statement())
        if lexemes[i] == "end" or lexemes[i] != ";":
            more_statements = False

    if lexemes[i] != "end" and (lexeme_tokens[i] == "Identifier Token" or lexeme_tokens[i] == "Reserved Token"):
        print("Error: Expected ';' in between statements")
        sys.exit(1)
    elif lexemes[i] != "end":
        print("Expected 'end' after compound statement.")
        sys.exit(1)
    else:
        i = i + 1 # consume end

    return Compound([statement for statement in statements if statement is not None])

# <statement part>
def statement_part():
    return compound_statement()

#  <procedure block>
def procedure_block():
    variable_declaration = variable_declarition_part()
    statement_declaration = statement_part()

    return ProcedureBlock(variable_declaration, statement_declaration)

# <procedure declaration>
def procedure_declaration():
    global i
    i = i+1 # consume "procedure"
    id = identifier()
    if lexemes[i] == ";":
        i = i+1 # consume ";"
    else:
        print("Error: Expected a ';', got", lexemes[i], "instead")
        sys.exit(1)

    block = procedure_block()

    return ProcedureDeclaration(id, block)

# <procedure declaration part>
def procedure_declaration_part():
    global i
    if lexemes[i] == "procedure":
        more_procedure_declarations = True
    else:
        more_procedure_declarations = False

    procedures = []
    while more_procedure_declarations:
        procedures.append(procedure_declaration())
        if lexemes[i] == ";":
            i = i+1 # consume ";"
        else:
            print("Error: Expected a ';', got", lexemes[i], "instead")
            sys.exit(1)
        if lexemes[i] != "procedure":
            more_procedure_declarations = False
    return procedures
        

# <simple type>
def simple_type():
    global i
    if lexeme_tokens[i] == "Data Type Token":
        type = lexemes[i]
        i = i+1 # consume data type
    else:
        print("Error: Expected a Data Type Token, got a ", lexeme_tokens[i], " instead. Lexeme ", lexemes[i], " is not a Data Type Token.")
        sys.exit(1)
    return type

# <type>
def type():
    return simple_type()
    

#<variable declaration>
def variable_declaration():
    global i
       
    names = [identifier()]

    if lexemes[i] == "," and lexeme_tokens[i+1] == "Identifier Token":
        more_identifiers = True
    else:
        more_identifiers = False
    
    while more_identifiers:
        
        if lexemes[i] != ",":
            print("Error: A ',' is expected, got lexeme ", lexemes[i], "instead.")
            sys.exit(1)
        
        i = i+1 # consume ","
        names.append(identifier())

        if lexemes[i] != "," and lexeme_tokens[i+1] != "Identifier Token":
            more_identifiers = False
    
    if lexemes[i] == ":":
        i = i+1 # consume the ":" lexeme
    else:
        print("Error: Expect a ':', got",lexemes[i], "instead.")
        sys.exit(1)

    type_name = type()
    
    return [ VariableDeclaration(name, type_name)
            for name in names]

# <variable declaration part>
def variable_declarition_part():
    global i
    if lexemes[i] == "var":
        i = i+1 # consume "var"
    else:
        # if the current lexeme isn't i, go back to block() function. <variable declaration part> -> empty string
        return 
    
    """
    if lexemes[i] == ";":
        i = i+1 # consume ";"
    else:
        print("Error: Expected a ';', got", lexemes[i], "instead")
        sys.exit(1)
    """
    declarations = []

    if lexeme_tokens[i] == "Identifier Token":
        more_variable_declaritions = True
    else:
        more_variable_declaritions = False
    
    while more_variable_declaritions:
        
        declarations.append(variable_declaration())
        if lexemes[i] == ";":
            i = i+1 # consume ";"
        else:
            print("Error: Expected a ';', got", lexemes[i], "instead")
            sys.exit(1)
        if lexeme_tokens[i] != "Identifier Token":
            more_variable_declaritions = False
        
    return declarations
    
    

# <block>
def block():
    
    variable = variable_declarition_part()
    procedure = procedure_declaration_part()
    statement = statement_part()
    return Block(variable, procedure, statement)


# <program>
def program():
    global i
    if lexemes[i] == "program":
        i = i+1 # consumed input "program" increment i by 1
        id = identifier()
        if lexemes[i] == ";":
            i = i+1
        else:
            print("Error: ';' is expected. Fornd'", lexemes[i], "'instead.")
            sys.exit(1)
        
        b = block()

        if i > len(lexemes) - 1:
            print("Error: Expect '.' after last 'end'.")
        elif lexemes[i] != "." or i < len(lexemes) - 1:
            print("Error: There cannot be anything after the last 'end' in the program.")
        else:
            print("Parse successful.")
        return Program(id, block)

    else:
        print("Error: expected 'program', found'" ,lexemes[i], "'instead")
        sys.exit(1)

     

if len(sys.argv) != 2:
    print("Invalid number of arguments. You must specify a file for the input.")
    sys.exit(1)

input_file_name = sys.argv[1]

# read lexeams from the file into a list
try:
    with open(input_file_name, 'r') as f:
        lexemes = f.read().split()
# when the file does not exist or is not in the directory of the program file
except:
    print("Error: The input file does not exist in the same directory as this program.")
    sys.exit(1)

# define each type of tokens
reserved_tokens_list = {"program" , "var", "procedure", "begin", "end", "if", "then", "else", "while", "do", "read", "write", "not", "array", "of"}
data_type_tokens_list = {"integer", "boolean"}
boolean_tokens_list = {"true", "false"}
special_tokens_list = {"(", ")", "[", "]", ".", ",", ";", ":", ".."}
relation_tokens_list = {"=", "<>", "<", "<=", ">=", ">"}
addition_tokens_list = {"+", "-", "or"}
multiplication_tokens_list = {"*", "div", "and"}
integer_type_token = re.compile("[0-9]+") # any number at any length with digits from 0 - 9
identifier_token = re.compile("^[A-Za-z]([A-Za-z]|[0-9])*") # must begin with a capital or lower case letter. Can end with letter or digit. Can be as long as needed
lexeme_tokens = []

# determine what type of token each lexeme is
for lexeme in lexemes:
    if lexeme in reserved_tokens_list:
        lexeme_tokens.append("Reserved Token")
    elif lexeme in data_type_tokens_list:
        lexeme_tokens.append("Data Type Token")
    elif lexeme in boolean_tokens_list:
        lexeme_tokens.append("Boolean Token")
    elif lexeme in special_tokens_list:
        lexeme_tokens.append("Special Token")
    elif lexeme == ":=":
        lexeme_tokens.append("Assignment Token")
    elif lexeme in relation_tokens_list:
        lexeme_tokens.append("Relation Token")
    elif lexeme in addition_tokens_list:
        lexeme_tokens.append("Addition Token")
    elif lexeme in multiplication_tokens_list:
        lexeme_tokens.append("Multiplication Token")
    elif integer_type_token.fullmatch(lexeme):
        lexeme_tokens.append("Integer Token")
    elif identifier_token.fullmatch(lexeme):
        lexeme_tokens.append("Identifier Token")
    else:
        print(lexeme, "is not associated with a valid token.")
        sys.exit(1)

# time to put the input through the grammar using the tokens and the lexemes list
i = 0 # start at position 0 in the lists
pr = program()
pid = pr.identifier.identifier
print("", pid)

