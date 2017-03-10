import sys
from tkinter import *
import interpreter3 as intx
import better_lexer as lexer

class parser:
	def __init__(self,code):
		self.ofile=open('output.txt','w')
		self.commands={'equals-to','print','Return','function','assignment','less-than','greater-than','if','else','while','skip','semicolon','addition','subtraction','multiplication'}
		self.finallist=[]
		self.final=None
		for el in code:
			comm=el.strip()
			self.finallist.append(self.processit(comm))
		while len(self.finallist)!=1:
			j=0
			while j<len(self.finallist)/2:
				temp=intx.Seq(self.finallist[j],self.finallist[j+1])
				self.finallist.pop(j)
				self.finallist.pop(j)
				self.finallist.insert(j,temp)
				j+=1

	def getit(self):
		return self.finallist[0]
	
	def processit(self,command):
		print("processit: ",command)
		ll = lexer.lexer(command)
		lista, listb = ll.lexit()			#listb
		primary=None
		lx=[]

		for j in range(len(lista)):
			if listb[j] in self.commands:
				lx.append(listb[j])
		
		primr=self.find_primary(lx)
		if primr=='assignment':
			return self.process_assignment(lista,listb)
		elif primr=='if':
			return self.process_ifelse(lista,listb)
		elif primr=='print':
			return self.process_print(lista,listb)
		elif primr=='while':
			return self.process_while(lista,listb)
		elif primr=='function':
			if command.count('{')==1:
				print("function definition")
				return self.process_function_def(lista,listb)
			else:
				print("function call")
				return self.process_function_call(lista,listb)

	def process_ifelse(self,listx,listy):						#complete the ifelse and write process_cexp,
		pos_do=0
		pos_else=0
		for j in range(len(listy)):
			if listy[j]=='do':
				pos_do=j
			if listy[j]=='else':
				pos_else=j
		bx1 = self.process_bexp(listx[1:pos_do],listy[1:pos_do])
		cx1 = self.process_cexp(listx[pos_do+1:pos_else],listy[pos_do+1:pos_else])
		cx2 = self.process_cexp(listx[pos_else+1:],listy[pos_else+1:])
		rex = intx.IfElse(bx1,cx1,cx2)
		return rex

	def process_while(self,listx,listy):
		pos_do=0
		for j in range(len(listy)):
			if listy[j]=='do':
				pos_do=j
		bx1 = self.process_bexp(listx[1:pos_do],listy[1:pos_do])
		cx1 = self.process_cexp(listx[pos_do+1:],listy[pos_do+1:])
		rex = intx.While(bx1,cx1)
		return rex

	def process_function_def(self,lista,listb):
		fname=lista[1]
		variablex=intx.Var(lista[3])
		cx1=self.process_cexp(lista[6:-1],listb[6:-1])
		rex = intx.FuncDef(fname,variablex,cx1)
		return rex

	def process_function_call(self,lista,listb):
		fname=lista[1]
		print("lista3=",lista[3])
		variablex=intx.Aexp(int(lista[3]))
		rex = intx.FuncCall(fname,variablex)
		return rex

	def process_print(self,lista,listb):
		k=0
		deleted=0	
		while k<len(listb)-deleted:
			if listb[k]=='comma':
				listb.pop(k)
				lista.pop(k)
				deleted+=1
			else:
				k+=1
		elx=intx.Print(lista[1:])
		return elx

	def find_primary(self,listx):
		return listx[0]

	def process_cexp(self,lista,listb):
		sems=listb.count('semicolon')
		if sems==0:
			if listb[1]=='assignment':
				return self.process_assignment(lista,listb)
			elif listb[0]=='print':
				return self.process_print(lista,listb)
		else:
			slist=[]
			flist=[]
			for j in range(len(listb)):
				if listb[j]=='semicolon':
					slist.append(j)
			prevpoint=0
			scount=0
			while(scount<sems):
				flist.append(self.process_cexp(lista[prevpoint:slist[scount]],listb[prevpoint:slist[scount]]))
				prevpoint=slist[scount]+1
				scount+=1
			flist.append(self.process_cexp(lista[prevpoint:],listb[prevpoint:]))
			while len(flist)!=1:
				j=0
				while j<len(flist)/2:
					temp=intx.Seq(flist[j],flist[j+1])
					flist.pop(j)
					flist.pop(j)
					flist.insert(j,temp)
					j+=1
			return flist[0]

	def process_assignment(self,lista,listb):		#for assignment operations!
		print("process assignment!")
		a=self.process_variable(lista[0])
		if listb[2]=='function':
			b=self.process_function_call(lista[2:],listb[2:])
		else:
			b=self.process_aexp(lista[2:],listb[2:])
		c=intx.Assign(a,b)
		return c

	def process_variable(self,itemx):
		var1=intx.Var(itemx)
		return var1	

	def process_bexp(self,lista,listb):
		v1=intx.Var(lista[0])
		v2=intx.Var(lista[2])	
		if listb[1]=='less-than':
			lt=intx.LessThan(v1,v2)
		elif listb[1]=='and':
			lt=intx.OpAnd(v1,v2)
		elif listb[1]=='or':
			lt=intx.OpOr(v1,v2)
		return lt

	def process_aexp(self,listx,listy):
		if len(listx)==1:
			if listy[0]=='number':
				aexp1=intx.Aexp(int(listx[0]))
			elif listy[0]=='variable':
				aexp1=intx.Var(listx[0])
			return aexp1
		else:
			if listy[0]=='variable':
				if listy[1]=='addition':
					aexp1=intx.Var(listx[0])
					aexp2=self.process_aexp(listx[2:],listy[2:])
					aexp3=intx.Add(aexp1,aexp2)
				elif listy[1]=='subtraction':
					aexp1=intx.Var(listx[0])
					aexp2=self.process_aexp(listx[2:],listy[2:])
					aexp3=intx.Sub(aexp1,aexp2)
				elif listy[1]=='multiplication':
					aexp1=intx.Var(listx[0])
					aexp2=self.process_aexp(listx[2:],listy[2:])
					aexp3=intx.Mul(aexp1,aexp2)
			return aexp3

#--------------------------------------------------------------- FRONTEND ----------------------------------------------------
					
class frontend:
	def __init__(self):
		self.ofile=open("code.txt",'w')
		self.mGui=Tk()
		self.ment = Text(self.mGui)
		self.ment.pack()
		self.mbutton2=Button(self.mGui,text='Compile!',command=self.closefile).pack()
		self.mentry=Entry(self.mGui,textvariable=self.ment).pack()
		self.mGui.mainloop()
	
	def mhello(self):
		self.mtext=self.ment.get("1.0","end-1c")
		print(self.mtext)
		self.ofile.write(self.mtext)

	def closefile(self):
		self.mtext=self.ment.get("1.0","end-1c")
		self.ofile.write(self.mtext)
		self.ofile.close()
		self.ment.insert("end-1c","\n-------------------------------------------------------------------------\nCompiling........\n\n")
		codex=get_the_code()
		p1=parser(codex)
		p2=p1.getit()
		run_this_system(p2)
		txtxtx=get_output()
		self.ment.insert("end-1c",txtxtx)	

	def putitin(self,textx):
		self.ment.insert("end-1c","\n"+textx)


#------------------------------------------------------------READ THE CODE------------------------------------------------------
def get_the_code():
	c1=open('code.txt','r')
	c2=c1.readlines()
	c3=[]
	for el in c2:
		c3.append(el.strip())
	return c3

def get_output():
	inf=open('output.txt','r')
	txtx=inf.read()
	return txtx
#--------------------------------------------------------------THE MAIN FUNCTION(S)-------------------------------------------------

def run_this_system(p1):				#the main function that executes and prints
	s0=intx.State()
	p1.eval(s0)


fr = frontend()