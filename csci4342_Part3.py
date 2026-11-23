"""
Student Name: Keith Neill
Program Name: Interpreter Project Part 3
Description: This program reads a file with SFAscal code and displays the type of token associated with each lexeme. 
             This program displays the output as lexeme : token name. for example, the output “x : Identifier Token” tells the user that the lexeme, x, is an identifier token.  
"""

import sys
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class BinaryOperation:
    """Twooperandsjoinedbyanoperatorsuchas+,divor<=."""

    operator:str
    left:Expression
    right:Expression
    #endofClass"BinaryOperation"


@dataclass(frozen=True)
class Assignment:
    """<variable>:=<expression>"""

    target:Variable
    value:Expression
    line:int
    #endofClass"Assignment"


@dataclass(frozen=True)
class Compound:
    """begin<statement>{;<statement>}end"""

    statements:list[Statement]
    line:int
    #endofClass"Compound"
 
# <identifier>
def identifier():
    global i
    if lexeme_tokens[i] == "Identifier Token":
        # if lexeme is an identifier, consume it by incrementing i by 1 and return i
        i = i+1
        return 
    else:
        print("Error: expected an identifier token, got", lexeme_tokens[i], "instead. '",lexemes[i],"' is not a valid identifier.")
        sys.exit(1)

# <factor>
def factor():
    global i

    # if "(<expression>)"
    if lexemes[i] == "(":
        i = i+1 # consume (
        expression()
        if lexemes[i] == ")":
            i = i+1 # consume )
            return 
        else:
            print("Error: Expected ')' after expression.")
            sys.exit(1)

    if lexeme_tokens[i] == "Integer Token" or lexeme_tokens[i] == "Boolean Token":
        
        i = i+1 # <constant>
    
    elif lexemes[i] == "not":
        
        i = i+1 # consume "not"
        factor()
    elif lexeme_tokens[i] == "Identifier Token":
        identifier()
    else:
        print("Error: ", lexemes[i], "cannot be a factor")
        sys.exit(1)

    return 

# <term>
def term():
    global i
    factor()
    if lexeme_tokens[i] == "Multiplication Token":
        multiply_more_factors = True
    else:
        multiply_more_factors = False
    
    while multiply_more_factors:
        i = i+1 # consume multiplication lexeme
        factor()
        if lexeme_tokens[i] != "Multiplication Token":
            multiply_more_factors = False
    
    return 

# <simple expression>
def simple_expression():
    global i
    term()
    if lexeme_tokens[i] == "Addition Token":
        add_more_terms = True
    else:
        add_more_terms = False
        
    while add_more_terms:
        i = i+1 # consume addition lexeme
        term()
        if lexeme_tokens[i] != "Addition Token":
            add_more_terms = False
        
    return 


# <expression>
def expression():
    global i
    simple_expression()
    if lexeme_tokens[i] == "Relation Token":
        i = i+1 # consume lexeme with relation token
        simple_expression()
    return 

# <assignment statement>
def assignment_statement():
    global i
    identifier()
    if lexeme_tokens[i] == "Assignment Token":
        i = i+1
    else:
        print("Error: Expected Assignment Token, got", lexeme_tokens[i], "instead.")
        sys.exit(1)

    expression()
    
    return 


# <read statement>
def read_statement():
    global i
    i = i+1 # consume "read"
    i = i+1 # consume (
    identifier()
    if lexemes[i] == ")":
        i = i+1 # consume )
    else:
        print("Error: ')' is expected after read statement")
        sys.exit(1)
    
    return 

# <write statement>
def write_statement():
    global i
    i = i+1 # consume "write"
    i = i+1 # consume (
    expression() # <output value>
    if lexemes[i] == ")":
        i = i+1 # consume )
    else:
        print("Error: ')' is expected after write statement")
        sys.exit()
    return 

# <simple statement>
def simple_statement():
    
    if lexeme_tokens[i] == "Identifier Token" and lexeme_tokens[i+1] == "Assignment Token":
       assignment_statement()
    elif lexeme_tokens[i] == "Identifier Token":
        identifier() # <procedure statement>
    elif lexemes[i] == "read":
        read_statement()
    elif lexemes[i] == "write":
        write_statement()
    else:
        print("Error: ",lexemes[i],"is not recognised as a statement.")
        sys.exit(1)
       
    return 


# <if statement>
def if_statement():
    global i
    i = i+1 # consume "if"
    expression()
    if lexemes[i] == "then":
        i = i+1 # consume then
    else:
        print("Error: Expected 'then' after if statenent.")
        sys.exit(1)
    statement()
    if lexemes[i] == "else":
        i = i+1 # consume else
        statement()
    return 

# <while statement>
def while_statement():
    global i
    i = i+1 # consume while
    expression()
    if lexemes[i] == "do":
        i = i+1 # consume do
    else:
        print("Error: Expected 'do' after exopression in while statement.")
        sys.exit(1)
    statement()
    return 

# <structured statenebt>
def structured_statement():
    if lexemes[i] == "begin":
        compound_statement()
    elif lexemes[i] == "if":
        if_statement()
    elif lexemes[i] == "while":
        while_statement()
    else:
        print("Error: ",lexemes[i], " is not recognised as a structured statement.")
    return 

# <statement>
def statement():
    
    if lexeme_tokens[i] == "Identifier Token" or lexemes[i] == "read" or lexemes[i] == "write":
        simple_statement()
    elif lexemes[i] == "begin" or lexemes[i] == "if" or lexemes[i] == "while":
        structured_statement()
    elif lexemes[i] == "end" or lexemes[i] == ";":
        return  # <empty statement>
    else:
        print("Error: ", lexemes[i], "is not the start of a valid statement.")
        sys.exit(i)

    return 

# <compound statement>
def compound_statement():
    global i
    if lexemes[i] == "begin":
        i = i+1 # consume "begin"
        
    else:
        print("Error: Expected lexene 'begin', got", lexemes[i], "instead")
        sys.exit(1)

    statement()
    
    if lexemes[i] == ";":
       more_statements = True
    else:
        more_statements = False

    while more_statements:
        i = i+1 # consume ;
        statement()
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

    return 

# <statement part>
def statement_part():
    compound_statement()
    return 

#  <procedure block>
def procedure_block():
    variable_declarition_part()
    statement_part()

    return 

# <procedure declaration>
def procedure_declaration():
    global i
    i = i+1 # consume "procedure"
    identifier()
    if lexemes[i] == ";":
        i = i+1 # consume ";"
    else:
        print("Error: Expected a ';', got", lexemes[i], "instead")
        sys.exit(1)

    procedure_block()

    return 

# <procedure declaration part>
def procedure_declaration_part():
    global i
    if lexemes[i] == "procedure":
        more_procedure_declarations = True
    else:
        more_procedure_declarations = False

    while more_procedure_declarations:
        procedure_declaration()
        if lexemes[i] == ";":
            i = i+1 # consume ";"
        else:
            print("Error: Expected a ';', got", lexemes[i], "instead")
            sys.exit(1)
        if lexemes[i] != "procedure":
            more_procedure_declarations = False
    return 
        

# <simple type>
def simple_type():
    global i
    if lexeme_tokens[i] == "Data Type Token":
        i = i+1 # consume data type
    else:
        print("Error: Expected a Data Type Token, got a ", lexeme_tokens[i], " instead. Lexeme ", lexemes[i], " is not a Data Type Token.")
        sys.exit(1)
    return 

# <type>
def type():
    simple_type()
    return 

#<variable declaration>
def variable_declaration():
    global i
       
    identifier()

    if lexemes[i] == "," and lexeme_tokens[i+1] == "Identifier Token":
        more_identifiers = True
    else:
        more_identifiers = False
    
    while more_identifiers:
        if lexemes[i] != ",":
            print("Error: A ',' is expected, got lexeme ", lexemes[i], "instead.")
            sys.exit(1)
        
        i = i+1 # consume ","
        identifier()

        if lexemes[i] != "," and lexeme_tokens[i+1] != "Identifier Token":
            more_identifiers = False
    
    if lexemes[i] == ":":
        i = i+1 # consume the ":" lexeme
    else:
        print("Error: Expect a ':', got",lexemes[i], "instead.")
        sys.exit(1)

    type()
    
    return

# <variable declaration part>
def variable_declarition_part():
    global i
    if lexemes[i] == "var":
        i = i+1 # consume "var"
    else:
        # if the current lexeme isn't i, go back to block() function. <variable declaration part> -> empty string
        return 
    
    variable_declaration()

    if lexemes[i] == ";":
        i = i+1 # consume ";"
    else:
        print("Error: Expected a ';', got", lexeme[i], "instead")
        sys.exit(1)

    if lexeme_tokens[i] == "Identifier Token":
        more_variable_declaritions = True
    else:
        more_variable_declaritions = False
    
    while more_variable_declaritions:
        
        variable_declaration()
        if lexemes[i] == ";":
            i = i+1 # consume ";"
        else:
            print("Error: Expected a ';', got", lexeme[i], "instead")
            sys.exit(1)
        if lexeme_tokens[i] != "Identifier Token":
            more_variable_declaritions = False
        
    return 
    

# <block>
def block():
    
    variable_declarition_part()
    procedure_declaration_part()
    statement_part()
    return


# <program>
def program():
    global i
    if lexemes[i] == "program":
        i = i+1 # consumed input "program" increment i by 1
        identifier()
        if lexemes[i] == ";":
            i = i+1
        else:
            print("Error: ';' is expected. Fornd'", lexemes[i], "'instead.")
            sys.exit(1)
        
        block()

        if i > len(lexemes) - 1:
            print("Error: Expect '.' after last 'end'.")
        elif lexemes[i] != "." or i < len(lexemes) - 1:
            print("Error: There cannot be anything after the last 'end' in the program.")
        else:
            print("Parse successful.")

    else:
        print("Error: expected 'program', found'" ,lexemes[i], "'instead")
        sys.exit(1)

# classes      

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
program()
