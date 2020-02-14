from token_class import Token

class Lexer:
    """
       MulSymb:
       SingleSymb:
       StopSymb:
       ConSymb:
    """
    def __init__(self,str):
        self.str = str
        self.str_len = len(str)
        self.cur_pos = 0
        self.MulSymb = dict()
        MulSymb_file = open("../input/multi_symbol.txt","r")
        for line in MulSymb_file:
            line = line.strip().split("\t")
            self.MulSymb[line[1]]=line[0]
        MulSymb_file.close()
        SingleSymb_file = open("../input/single_symbol.txt","r") 
        for line in SingleSymb_file:
            line = line.strip().split("\t")
            self.SingleSymb = set(line) 
        SingleSymb_file.close()
        self.delimer = self.SingleSymb
        Stop_file = open("../input/stop.txt","r")
        for line in Stop_file:
            line = line.strip().split("\t")
            self.StopSymb = set(line)
        Stop_file.close()                
        self.ConSymb = self.StopSymb - self.SingleSymb

    def type_check(self,input,type_record):
        if type_record["alpha"] == 0:
            if type_record["dot"] == 0:
                return "NUM"
            elif type_record["dot"] == 1:
                return "REAL"

        if type_record["number"] == 0:
            if type_record["dot"] == 0:
                if input in self.MulSymb:
                    return self.MulSymb[input]
                else:
                    return "ID"
        
        if type_record["dot"] == 0:
            return "ID"
        else:
            return "INCORRECT TYPE"

    def getNextToken(self):
        #remove space
        while self.cur_pos < self.str_len and self.str[self.cur_pos] == ' ':
            self.cur_pos += 1
        self.cur_token = Token("","")
        #check for end of file
        if self.cur_pos >= self.str_len:
            self.cur_token = Token("","EOF")
            return self.cur_token
        
        #if the first char in stopsymb: &,=><!|;(){}+-*/
        if self.str[self.cur_pos] in self.StopSymb:
            #if the char belong to consymb: & = > < | !, tell if str[cur_pos,cur_pos+1] in consymb
            if self.cur_pos+1 < self.str_len and self.str[self.cur_pos:self.cur_pos+2] in self.MulSymb:
                self.cur_token = Token(self.str[self.cur_pos:self.cur_pos+1],self.MulSymb[self.str[self.cur_pos:self.cur_pos+2]])
                self.cur_pos += 2
                 
            #or a real stopsymb: if it's not a consymb, then it's a real stopsymb
            else:
                self.cur_token = Token(self.str[self.cur_pos],self.str[self.cur_pos])
                self.cur_pos += 1
        #else count the continues string to tell if it belongs to NUM OR REAL OR MULTI-symbol 
        else:
            pos = self.cur_pos
            type_record = {"alpha": 0,
                           "number": 0,
                           "dot": 0}
            while pos < self.str_len and self.str[pos] != ' ' and self.str[pos] not in self.StopSymb:
                if self.str[pos].isalpha():
                    type_record["alpha"] += 1
                if self.str[pos] == '.':
                    type_record["dot"] += 1
                if self.str[pos].isdigit():
                    type_record["number"] += 1
                pos += 1 
           
            self.cur_token = Token(self.str[self.cur_pos:pos],self.type_check(self.str[self.cur_pos:pos],type_record)) 
            self.cur_pos = pos
        return self.cur_token 
        
