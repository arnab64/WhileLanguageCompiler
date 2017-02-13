'''
How it works?
Its the same as homework2 except that every eval function (of the Cexp classes) returns the next command to be executed and the current state.


How it prints the command?
By an INORDER traversal of the tree recursively. Every class has a printx() function, that calls the printx() function of its children. 
'''

class State:
	def __init__(self):
		self.dictx={}
	
	def read(self,x):
		a=self.dictx.get(x,-1)
		return a
		
	def write(self,x,val):
		self.dictx[x]=val
		
	def getall(self):
		return self.dictx.keys()
		
	def printstate(self):
		statestack=['{']
		for el in self.dictx:
			statestack.append(str(el))
			statestack.append(':')
			statestack.append(str(self.dictx[el]))
			statestack.append(',')
		if len(statestack)>1:
			statestack.pop()
		statestack.append('}')
		return "".join(statestack)
		
class Aexp:
	def __init__(self,a1):
		self.left=a1

	def eval(self,sx):
		if type(self.left)==int:
			return self.left
		elif type(self.left)==Var:
			return sx.read(self.left.varname())
		else:
			return self.left.eval(sx)
			
	def printx(self,stck):
		if type(self.left)==int:
			stck.append(str(self.left))
		elif type(self.left)==Var:
			stck.append(self.left.varname())
		else:
			stck.extend(self.left.printx([]))
		return stck

class Add:	
	def __init__(self,left,right):			#left is Aexp and right is Aexp
		self.left=left
		self.right=right
		
	def eval(self,sx):
		return self.left.eval(sx)+self.right.eval(sx)
		
	def printx(self,stck):
		# self.left.printx()
		# print('+')
		# self.right.printx()
		stck.extend(self.left.printx([]))
		stck.append("+")
		stck.extend(self.right.printx([]))	
		return stck
		

class Sub:	
	def __init__(self,left,right):			#left is Aexp and right is Aexp
		self.left=left
		self.right=right
		
	def eval(self,sx):
		return self.left.eval(sx)-self.right.eval(sx)		
		
	def printx(self,stck):
		stck.extend(self.left.printx([]))
		stck.append("-")
		stck.extend(self.right.printx([]))		
		return stck
		
class Mul:	
	def __init__(self,left,right):
		self.left=left
		self.right=right
		
	def eval(self,sx):
		return self.left.eval(sx)*self.right.eval(sx)		
		
	def printx(self,stck):
		stck.extend(self.left.printx([]))
		stck.append("*")
		stck.extend(self.right.printx([]))		
	
#Boolean expressions and their derived classes	
	
class Bexp:
	def __init__(self,a1):
		self.left=a1

	def eval(self,sx):
		if type(self.left)==bool:
			return self.left
		else:
			return self.left.eval(sx)
			
	def printx(self,stck):
		#self.left.printx()
		stck.extend(self.left.printx([]))
		return stck
	
class OpAnd:
	def __init__(self,a,b):
		self.a=a
		self.b=b
	
	def eval(self,sx):
		return self.a.eval(sx) and self.b.eval(sx)
		
	def printx(self,stck):
		# self.a.printx()
		# print('AND')
		# self.b.printx()
		stck.extend(self.a.printx([]))
		stck.append("<")
		stck.extend(self.b.printx([]))
		return stck

class OpOr:
	def __init__(self,a,b):
		self.a=a
		self.b=b
	
	def eval(self,sx):
		return self.a.eval(sx) or self.b.eval(sx)	

	def printx(self,stck):
		stck.extend(self.a.printx([]))
		stck.append("<")
		stck.extend(self.b.printx([]))
		return stck		

class Equalto:
	def __init__(self,a,b):
		self.a=a
		self.b=b
		
	def eval(self,sx):
		if self.a.eval(sx)==self.b.eval(sx):
			return True
		else:
			return False
	
	def printx(self,stck):
		stck.extend(self.a.printx([]))
		stck.append("==")
		stck.extend(self.b.printx([]))
		return stck

	
class LessThan:
	def __init__(self,a,b):
		self.a=a
		self.b=b
		
	def eval(self,sx):
		if self.a.eval(sx)<self.b.eval(sx):
			return True
		else:
			return False
	
	def printx(self,stck):
		stck.extend(self.a.printx([]))
		stck.append("<")
		stck.extend(self.b.printx([]))
		return stck

#Cexp and derived classes
			
class Var:
	def __init__(self,x):
		self.x=x

	def eval(self,sx):
		return sx.read(self.x)
		
	def varname(self):
		return self.x
		
	def printx(self,stck):
		stck.append(self.x)
		return stck

class Assign:
	def __init__(self,varx,valx):	#varx is of type Var and valx is of type Aexp	
		self.varx=varx
		self.valx=valx
	
	def eval(self,sx):
		p=self.varx.varname()
		q=self.valx.eval(sx)
		sx.write(p,q)
		s1=Skip()
		return s1,sx
		
	def printx(self,stck):
		stck.extend(self.varx.printx([]))
		stck.append(":=")
		stck.extend(self.valx.printx([]))
		return stck
		
class Cexp:
	def __init__(self,a):
		self.a=a
	
	def eval(self,sx):
		return self.a.eval(sx)
	
	def printx(self,stck):
		stck.extend(self.a.printx([]))
		return stck		
				
class Skip:
	def __init__(self):
		sopos=0
	def eval(self):
		return None
	def printx(self,stck):
		stck.append('Skip')
		return stck
		
class IfElse:
	def __init__(self,a,b,c):
		self.a=a
		self.b=b
		self.c=c
	
	def eval(self,sx):
		stat=self.a.eval(sx)
		if stat==True:
			return self.b,sx
		else:
			return self.c,sx
			
	def printx(self,stck):
		stck.append('If ')
		stck.extend(self.a.printx([]))
		stck.append(' Then ')
		stck.extend(self.b.printx([]))
		stck.append(' Else ')
		stck.extend(self.c.printx([]))
		return stck

class While:
	def __init__(self,a,b):
		self.a=a
		self.b=b

	def eval(self,sx):
		stat=self.a.eval(sx)
		if stat==True:
			s1=Seq(self.b,self)
			return s1,sx
		else:
			return Skip(),sx

	def printx(self,stck):
		stck.append('While ')
		stck.extend(self.a.printx([]))
		stck.append(' Do ')
		stck.extend(self.b.printx([]))
		return stck

class Seq:			
	def __init__(self,a,b):			#a is a Cexp and b is a Cexp
		self.a=a
		self.b=b
	
	def eval(self,sx):
		if type(self.a)==Assign:
			temp=self.a.eval(sx)
			ax=Seq(temp[0],self.b)
			return ax, temp[1]	#returned the state
		elif type(self.a)==Seq:
			rexx=self.a.eval(sx)				#returns the state after executing the first command of the left
			x1=Seq(rexx[0],self.b)
			return x1,rexx[1]
		elif type(self.a)==Skip:
			#print(type(self.b))
			return self.b,sx
		elif type(self.a)==IfElse:
			rex=self.a.eval(sx)
			s1=Seq(rex[0],self.b)
			return s1,rex[1]
		elif type(self.a)==While:
			rex=self.a.eval(sx)
			s1=Seq(rex[0],self.b)
			return s1,rex[1]
		elif type(self.a)==Cexp:
			rex=self.a.eval(sx)
			s1=Seq(rex[0],self.b)
			return s1,rex[1]	

	def printx(self,stck):
		stck.extend(self.a.printx([]))
		stck.append('; ')
		stck.extend(self.b.printx([]))
		return stck

#--------------------------------------------------------------THE MAIN FUNCTION-------------------------------------------------
def run_this_system(p1):				#the main function that executes and prints
	s1=State()
	structx=[p1,s1]
	res0=structx[0].printx([])
	print("<","".join(res0),s1.printstate(),">")
	while type(structx[0])!=Skip:
		resx=structx[0].eval(structx[1])
		res1=resx[0].printx([])
		print("<","".join(res1),resx[1].printstate(),">")
		del structx[:]
		structx.extend(resx)
#----------------------------------------------------------------------TEST CASES-------------------------------------------------

#test case1
'''
x=5;
y=25;
while x<y:
	x=x+2
	y=y-2	
'''
s1=State()
incr1=Aexp(Add(Var('x'),Aexp(2)))
decr1=Aexp(Sub(Var('x'),Aexp(2)))
x1=Cexp(Assign(Var('x'),Aexp(5)))
y1=Cexp(Assign(Var('y'),Aexp(25)))
xy1=Seq(incr1,decr1)
b1=Bexp(LessThan(Var('x'),Var('y')))
wh1=While(b1,xy1)
p1=Seq(x1,y1)
p2=Seq(p1,wh1)

#testcase2:
'''
x=5;
if x<6:
	x=x+1
else:
	x=x-1
'''
xx1=Cexp(Assign(Var('x'),Aexp(5)))
bb1=Bexp(LessThan(Var('x'),Aexp(6)))
xplus=Cexp(Assign(Var('x'),incr1))
xminus=Cexp(Assign(Var('x'),decr1))
ie=Cexp(IfElse(bb1,xplus,xminus))
finalx=Seq(xx1,ie)
#res0=finalx.printx([])
#print("<","".join(res0),s1.printstate(),">")

#test_case3: 
#this test case includes a while, an if-else, a comparison, 
'''
a=5;
b=11;
while a<b:
	a=a+1; b=b-1;
if a==b:
	a=a+b; b=0;	
else:
	b=a+b; a=0
'''
a1=Cexp(Assign(Var('a'),Aexp(5)))
b1=Cexp(Assign(Var('b'),Aexp(11)))
seq1=Seq(a1,b1)
cond1=Bexp(LessThan(Var('a'),Var('b')))
add1=Cexp(Assign(Var('a'),Aexp(Add(Var('a'),Aexp(1)))))
sub1=Cexp(Assign(Var('b'),Aexp(Sub(Var('b'),Aexp(1)))))
seq2=Seq(add1,sub1)
wh1=Cexp(While(cond1,seq2))					#while statement
cond2=Bexp(Equalto(Var('a'),Var('b')))
add2=Cexp(Assign(Var('a'),Aexp(Add(Var('a'),Var('b')))))
b0=Cexp(Assign(Var('b'),Aexp(0)))
seq3=Seq(add2,b0)
add3=Cexp(Assign(Var('b'),Aexp(Add(Var('a'),Var('b')))))
a0=Cexp(Assign(Var('a'),Aexp(0)))
seq4=Seq(add3,a0)
ifel1=Cexp(IfElse(cond2,seq3,seq4))					#ifelse
seq5=Seq(wh1,ifel1)
seq6=Seq(seq1,seq5)

#------------------------------------------------------RUN THE TEST CASES--------------------------------------------------------

print("\n")
run_this_system(seq6)				#pass 'finalx' in place of 'seq6' if you want to run test case 2, and 'p2' if you want to run test case 1

#The output of the above test case is as follows
'''
< a:=5; b:=11; While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {} >
< Skip; b:=11; While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {a:5} >
< b:=11; While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {a:5} >
< Skip; While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {b:11,a:5} >
< While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {b:11,a:5} >
< a:=a+1; b:=b-1; While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {b:11,a:5} >
< Skip; b:=b-1; While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {b:11,a:6} >
< b:=b-1; While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {b:11,a:6} >
< Skip; While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {b:10,a:6} >
< While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {b:10,a:6} >
< a:=a+1; b:=b-1; While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {b:10,a:6} >
< Skip; b:=b-1; While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {b:10,a:7} >
< b:=b-1; While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {b:10,a:7} >
< Skip; While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {b:9,a:7} >
< While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {b:9,a:7} >
< a:=a+1; b:=b-1; While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {b:9,a:7} >
< Skip; b:=b-1; While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {b:9,a:8} >
< b:=b-1; While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {b:9,a:8} >
< Skip; While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {b:8,a:8} >
< While a<b Do a:=a+1; b:=b-1; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {b:8,a:8} >
< Skip; If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {b:8,a:8} >
< If a==b Then a:=a+b; b:=0 Else b:=a+b; a:=0 {b:8,a:8} >
< a:=a+b; b:=0 {b:8,a:8} >
< Skip; b:=0 {b:8,a:16} >
< b:=0 {b:8,a:16} >
< Skip {b:0,a:16} >
'''