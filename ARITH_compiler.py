'''
Assignment CMPS203
Submitted by: Arnab Borah
Language: Python

1.

class expression contains the final data in integer format
class num is inherited from class exp and contains the expression
class mul is inherited from class exp and returns the sum of two numbers
class add is inherited from class exp and returns the product of two numbers

2. 

the eval function is the interpreter which takes in the expression of the Abstract Syntax Tree in the form of a string and returns
the result in the form of integer. The abstract syntax tree is not an actual tree, but is represented in the form of an expression 
string. Like for eg: mul(add(num(1),num(2)),add(num(3),num(4)))
The eval function returns the result of the tree, for eg, the result of the above expression is: 

3.

The test cases have been provided inside this code itself, they are available in line 193.

4. 
Extra feature: I implemented the additional feature for division, which is the class div.
'''

class exp:							#class for expressions
	def __init__(self,data):
		self.data = data
	
	def getdata(self):			 
		return self.data

class num(exp):						#class num is inherited from exp
	def __init__(self,expr):
		self.expr=expr
		exp.__init__(self,int(expr))
	
	def getdata(self):
		return exp.getdata(self)
	
class mul(exp):						#class mul is inherited from exp
	def __init__(self,a,b):
		n1=num(a)
		n2=num(b)
		exp.__init__(self,n1.getdata()*n2.getdata())

	def getdata(self):
		return exp.getdata(self)
	
		
class add(exp):						#class add is inherited from exp
	def __init__(self,a,b):
		n1=num(a)
		n2=num(b)
		exp.__init__(self,n1.getdata()+n2.getdata())		

	def getdata(self):
		return exp.getdata(self)
		
		
class add():
	def __init__(self, l, r):
		left = l;
		right = r;
		
	def eval(self):
		left.eval() + right.eval();

class div(exp):						#class div is inherited from exp
	def __init__(self,a,b):
		n1=num(a)
		n2=num(b)
		divx=n1.getdata()/n2.getdata()
		exp.__init__(self,divx)
		
	def getdata(self):
		return exp.getdata(self)
		
'''
This function getexpr() takes an expression and returns the operation name 
and the operands.
For eg: 	
mul(num(3),num(6))		returns 	operation: mul, 	operands: num(3),num(6)
num(3)					returns		operation: num,		operands: 3	
'''	
def getexpr(expr):
	lol=expr.split('(')
	keyw=lol[0]
	notlol=expr[len(keyw):]
	openbr=0
	closebr=0
	temp=[]
	for el in notlol:
		if el=='(':
			openbr+=1
		elif el==')':
			closebr+=1
		temp.append(el)
		if openbr==closebr and openbr!=0:
			temp=temp[1:-1]
			lx="".join(temp)
			return keyw,lx
	
'''
This function splits the expression if the two operands are compound expressions. 
For eg. 		if the operands are mul(num(3),num(4)),mul(num(2),num(5)) it splits them and separates them.
This is not trivial because one has to know which comma to split on.
'''		

def splitit(expr):
	op=0		#openbracket count
	cl=0		#closebracket count
	res=[]
	temp=[]
	ct=0
	for el in expr:
		if el=='(':
			op+=1
		elif el==')':
			cl+=1
		temp.append(el)
		if op==cl and op!=0:
			if ct==1:
				xxx="".join(temp[1:])
			else:
				xxx="".join(temp)
			res.append(xxx)
			del temp[:]
			op=0
			cl=0
			ct+=1
	return res

	
'''
the eval function takes in input as string of type: add(num(2),mul(num(3),num(5))) and parses it in order to find the
operations and operands in the proper sequence. Because it parses the input string, it uses the functions getexpr() and 
splitit(). 
'''	
def eval(expr):						
	if expr.isdigit()==True:		#if expression is a number, return the value
		return int(expr)
	arx=getexpr(expr)
	oper=arx[0]
	if arx[0]=='num':				#if the operation is num, return the value of the num
		numx=num(arx[1])
		return numx.getdata()
		
	newexp=arx[1]
	splitbycomma=newexp.split(',')
	front=splitbycomma[0]
	back=splitbycomma[-1]

	if front.isdigit()==True and back.isdigit()==True:		#if both the operands are numbers
		if oper=='add':
			a1 = add(eval(front),eval(back))
			return a1.getdata()
		elif oper=='mul':
			m1=mul(eval(front),eval(back))
			return m1.getdata()
		else:
			d1=div(eval(front),eval(back))
			return d1.getdata()
			
	elif front.isdigit()==True:						#if one of the operands is a number and the other is an expression
		nexpr=newexp[len(front)+1:]
		if oper=='add':
			a1=add(eval(front),eval(nexpr))
			return a1.getdata()
		elif oper=='mul':
			m1=mul(eval(front),eval(nexpr))
			return m1.getdata()
		else:
			d1=mul(eval(front),eval(nexpr))
			return d1.getdata()
	
	elif back.isdigit()==True:
		nexpr=newexp[:-len(back)-1]
		if oper=='add':
			a1=add(eval(nexpr),eval(back))
			return a1.getdata()
		elif oper=='mul':
			m1=mul(eval(nexpr),eval(back))
			return m1.getdata()
		else:
			d1=div(eval(nexpr),eval(back))
			return d1.getdata()
	
	else:											#if both the operands are complex expression
		a,b=splitit(newexp)
		if oper=='add':
			a1=add(eval(a),eval(b))
			return a1.getdata()
		elif oper=='mul':
			m1=mul(eval(a),eval(b))
			return m1.getdata()
		else:
			d1=div(eval(a),eval(back))
			return d1.getdata()		
		
'''
All the test cases. 
5
2+3*5
2*3+5
2*3+4*6
2+3+4
2*3*4
(1+2)*(3+4)
7/3
(6/2)/2

test cases represented in ARITH expressions below:
'''		

test_cases = [
'num(5)',
'add(num(2),mul(num(3),num(5)))',
'add(mul(num(2),num(3)),num(5))',
'add(mul(num(2),num(3)),mul(num(4),num(6)))',
'add(add(num(2),num(3)),num(4))',
'mul(mul(num(2),num(3)),num(4))',
'mul(num(5),add(num(4),add(num(2),num(3))))',
'mul(add(num(1),num(2)),add(num(3),num(4)))',
'div(num(7),num(3))',
'div(div(num(6),num(2)),num(2))']
			
#correct results of the test cases: [5,17,11,30,9,24,45,21,2.33,1.5]			

'''
Passing every test case to the eval function and getting back the result.
'''
results = []
for tcase in test_cases:
	res=eval(tcase)					#calling the eval function
	results.append(res)
			
'''
Printing out the result.
'''			
print("\n\n")
for j in range(len(test_cases)):
	#print(test_cases[j],"------>",results[j])
	print('{0} \n {1}\n'.format(test_cases[j],results[j]))
