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
		for el in self.dictx:
			print(el,self.dictx[el])
		
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


class Add:	
	def __init__(self,left,right):			#left is Aexp and right is Aexp
		self.left=left
		self.right=right
		
	def eval(self,sx):
		#print(">>>>",self.left.eval(sx),self.right.eval(sx))
		return self.left.eval(sx)+self.right.eval(sx)		

class Sub:	
	def __init__(self,left,right):			#left is Aexp and right is Aexp
		self.left=left
		self.right=right
		
	def eval(self,sx):
		return self.left.eval(sx)-self.right.eval(sx)		
		
class Mul:	
	def __init__(self,left,right):
		self.left=left
		self.right=right
		
	def eval(self,sx):
		return self.left.eval(sx)*self.right.eval(sx)		
	
#Boolean expressions and their derived classes	
	
class Bexp:
	def __init__(self,a1):
		self.left=a1

	def eval(self,sx):
		if type(self.left)==bool:
			return self.left
		else:
			return self.left.eval(sx)
			
class OpAnd:
	def __init__(self,a,b):
		self.a=a
		self.b=b
	
	def eval(self,sx):
		return self.a.eval(sx) and self.b.eval(sx)

class OpOr:
	def __init__(self,a,b):
		self.a=a
		self.b=b
	
	def eval(self,sx):
		return self.a.eval(sx) or self.b.eval(sx)	

class Equalto:
	def __init__(self,a,b):
		self.a=a
		self.b=b
		
	def eval(self,sx):
		if self.a.eval(sx)==self.b.eval(sx):
			return True
		else:
			return False
	
class LessThan:
	def __init__(self,a,b):
		self.a=a
		self.b=b
		
	def eval(self,sx):
		if self.a.eval(sx)<self.b.eval(sx):
			return True
		else:
			return False
			
class Var:
	def __init__(self,x):
		self.x=x

	def eval(self,sx):
		return sx.read(self.x)
		
	def varname(self):
		return self.x
		
class Assign:
	def __init__(self,varx,valx):	#varx is of type Var and valx is of type Aexp	
		self.varx=varx
		self.valx=valx
	
	def eval(self,sx):
		p=self.varx.varname()
		q=self.valx.eval(sx)
		#print(p,'assigned',q)
		sx.write(p,q)
		return sx 						#may need modification
		
class Cexp:
	def __init__(self,a):
		self.a=a
	
	def eval(self,sx):
		return self.a.eval(sx)
				
class Skip:
	def __init__(self):
		sopos=0

	def eval(self):
		return None
		
class IfElse:
	def __init__(self,a,b,c):
		self.a=a
		self.b=b
		self.c=c
	
	def eval(self,sx):
		stat=self.a.eval(sx)
		if stat==True:
			return self.b.eval(sx)
		else:
			return self.c.eval(sx)
			
class While:
	def __init__(self,a,b):
		self.a=a 			#bexp
		self.b=b  			#cexp

	def eval(self,sx):
		stat=self.a.eval(sx)
		while stat==True:
			sx=self.b.eval(sx)
			stat=self.a.eval(sx)
		return sx

class Print:
	def __init__(self,a):
		self.a=a

	def eval(self,sx): 				
		#print(sx.read(p))
		ofile=open('output.txt','a+')
		#if len(self.a)==1:
		tempstr=''
		for el in self.a:	
			p=el.strip()
			if p[0]=='"' and p[-1]=='"':			#if it is a string
				#ofile.write(p[1:-1])
				tempstr+=p[1:-1]
				tempstr+=" "
			else:									#if it is a variable
				value=sx.read(p)
				if value==-1:
					#ofile.write('Error: Undefined symbol a referenced\n')
					ofile.write('Error: Undefined symbol ')
					ofile.write(str(p))
					ofile.write(' referenced\n')
					break;
				else:
					tempstr+=str(value)
					tempstr+=" "
					#ofile.write(str(value)+'\n')
		ofile.write(tempstr+'\n')
		ofile.close()
		return sx			

class FuncDef:
	def __init__(self,fname,arguments,defn):
		self.fname=fname
		self.arguments=arguments
		self.defn=defn

	def eval(self,sx):
		sx.write(self.fname,[self.arguments,self.defn])
		return sx

class FuncCall:
	def __init__(self,fname,arguments):
		self.fname=fname
		self.arguments=arguments

	def eval(self,sx):
		parent=sx.read(self.fname)
		varx1=parent[0]					#the variable
		fdefn=parent[1]					#the function
		s1=State()
		if type(varx1)==Var:
			s1.write(varx1.varname(),self.arguments.eval(s1))
		else:
			s1.write(varx1,self.arguments.eval(s1))	
		s1dash=fdefn.eval(s1)
		print("s1dash=",s1dash)
		s1x=s1dash.read(varx1)
		s1dash.printstate()
		#print("the value of",varx1.varname()," is",s1x)
		return s1dash.read(varx1.varname())

class Return:
	def __init__(self,c):
		self.c=c

	def eval(self,sx):
		if type(self.c)==int:
			return self.c
		elif type(self.c)==Var:
			vari=self.c.varname()
			return sx.read(vari)

class Seq:			
	def __init__(self,a,b):			#a is a Cexp and b is a Cexp
		self.a=a
		self.b=b
	
	def eval(self,sx):
		#print("sx is of type",type(sx))
		if type(self.a)==Assign:
			temp=self.a.eval(sx)
			if self.b:
				return self.b.eval(temp)
			else:
				return sx
		elif type(self.a)==Seq:
			rexx=self.a.eval(sx)				#returns the state after executing the first command of the left
			return self.b.eval(rexx)
		elif type(self.a)==Skip:
			return self.b.eval()
		elif type(self.a)==IfElse:
			rex=self.a.eval(sx)
			return self.b.eval(rex)
		elif type(self.a)==While:
			rex=self.a.eval(sx)
			return self.b.eval(rex)
		elif type(self.a)==Cexp:
			rex=self.a.eval(sx)
			return self.b.eval(rex)	
		elif type(self.a)==Print:
			self.a.eval(sx)
			return self.b.eval(sx)
		elif type(self.a)==FuncDef:
			so=self.a.eval(sx)
			return self.b.eval(so)

	def printx(self,stck):
		stck.extend(self.a.printx([]))
		stck.append('; ')
		stck.extend(self.b.printx([]))
		return stck

if __name__=='__main__':
	sp = State()
	g1 = Assign(Var('z'),Aexp(34))
	a1 = Assign(Var('x'),Add(Var('x'),Aexp(3)))
	r1 = Return(Var('x'))
	s1 = Seq(a1,r1)
	f1 = FuncDef('add3',Var('x'),s1)
	f2 = FuncCall('add3',Aexp(5))
	v1 = Assign(Var('y'),f2)
	s2 = Seq(f1,v1)
	s3 = Seq(g1,s2)
	p1 = Print(Var('y'))
	s4 = Seq(s3,p1)

	sz = s4.eval(sp)


#test_case0
'''
x1=Cexp(Assign(Var('a'),Add(Var('a'),Aexp(3))))
funcit = FuncDef('add','a',x1)
FuncCall('add',Aexp(5))
run_this_system(funcit)
'''
'''
sp=State()
x1 = Assign(Var('x'),Aexp(19))
x2 = Assign(Var('y'),Aexp(7))
b1 = Bexp(LessThan(Var('x'),Var('y')))
incr1=Aexp(Add(Var('x'),Aexp(2)))
incr2=Aexp(Add(Var('y'),Aexp(2)))
cx1 = Assign(Var('x'),incr1)
cx2 = Assign(Var('y'),incr2)
x3 = IfElse(b1,cx1,cx2)
x4 = Print(Var('x'))
x5 = Print(Var('y'))
s1=Seq(x1,x2)
s2=Seq(s1,x3)
s3=Seq(x4,x5)
s4=Seq(s2,s3)
s4.eval(sp)
'''

#test case1
'''
x=5;
y=25;
while x<y:
	x=x+2
	y=y-2	
'''
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
p2=Seq(p1,wh1)'''