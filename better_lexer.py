import sys
import re
from tkinter import *
import interpreter3 as intx

class lexer:
	def __init__(self,expr):
		self.initexpr=expr
		self.lx=[]
		self.tokens=['<','>',',','::=','-',';','{','}']
		self.newtokens=[' < ',' > ',' , ',' ::= ',' - ',' ; ',' { ',' } ']
		#print(len(self.tokens),len(self.newtokens))
		self.separateit()
		#print(self.expr)

	def lexit(self):
		lexed=self.expr.split()
		rtypes=[]
		for el in lexed:
			rtypes.append(self.findtype(el))
		
		if rtypes[-1]=='semicolon':
			rtypes.pop()
			lexed.pop()
		return lexed,rtypes	

	def separateit(self):
		codex=self.initexpr
		for p in range(len(self.tokens)):
			codex=re.sub(self.tokens[p],self.newtokens[p],codex.rstrip())
			#print(self.tokens[p],codex)
		lenx=len(codex)
		rept=0
		j=0
		while j < lenx+rept:
			if codex[j]=='+':
				codex=codex[:j]+' + '+codex[j+1:]
				rept+=2
				j+=3
			elif codex[j]=='(':
				codex=codex[:j]+' ( '+codex[j+1:]
				rept+=2
				j+=3		
			elif codex[j]==')':
				codex=codex[:j]+' ) '+codex[j+1:]
				rept+=2
				j+=3
			else:
				j+=1			
		self.expr=codex

	def findtype(self,stx):
		if stx.isdigit()==True:
			return 'number'
		elif stx=='::=':
			return 'assignment'
		elif stx=='=':
			return 'equals-to'
		elif stx=='+':
			return 'addition'
		elif stx=='-':
			return 'subtraction'
		elif stx=='*':
			return 'multiplication'
		elif stx=='/':
			return 'division'
		elif stx==';':
			return 'semicolon'
		elif stx=='<':
			return 'less-than'
		elif stx=='>':
			return 'greater-than'
		elif stx==',':
			return 'comma'
		elif stx=='(':
			return 'open_bracket'
		elif stx==')':
			return 'close_bracket'
		elif stx=='{':
			return 'open_curly'
		elif stx=='}':
			return 'close_curly'
		elif stx[0]=='"' and stx[-1]=='"':
			return 'string'
		elif stx=='print':
			return 'print'
		elif stx=='skip':
			return 'skip'
		elif stx=='while':
			return 'while'
		elif stx=='do':
			return 'do'
		elif stx=='if':
			return 'if'
		elif stx=='else':
			return 'else'
		elif stx=='func':
			return 'function'
		elif stx=='Return':
			return 'Return'
		elif stx.isalpha()==True:
			return 'variable'

if __name__=='__main__':
	intext1 = "while a<b do a::=a"
	intext2 = "func add3(x) {x::=x+3; Return x}"
	l1 = lexer(intext2)
	l2 = l1.lexit()
	for j in range(len(l2[0])):
		print(l2[0][j],l2[1][j])