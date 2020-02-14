from lexer_class import Lexer

input = "{   int b; b = 1; { int a; a = 2; do a = a + 1; while(a<100);} float kk2 = 24.67  }"
lex = Lexer(input)
while True:
    t1 = lex.getNextToken()
    if t1.tag == "EOF":
        break
    print(t1.tag + " " + t1.name)
