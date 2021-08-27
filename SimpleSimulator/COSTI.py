from sys import stdin
import random
import sys
import matplotlib.pyplot as plt
j=0
def tracesplot(cycles,address):
    j=random.randint(0,100)
    plt.plot(cycles,address)
    plt.ylabel("ADDRESS")
    plt.xlabel("CYCLES")
    s="output"+ str(j)+".jpg"
    plt.savefig(s)
    

################################################ change binary to integer #####################################################
def intfrbin(x):
    return int(x,2)

################################################ change binary to integer #####################################################
def binfrbin(x):
    return int(x)

################################################ change to binary 8 bits #####################################################
def binto8(x):
    return str("{0:08b}".format(x))

################################################ change to binary 16 bits ####################################################
def binto16(x):
    return str("{0:016b}".format(x))

def binto32(x):
    return str("{0:032b}".format(x))    


################################################  FLAGS bits #####################################################
changebit={"V":8,"L":4,"G":2,"E":1}

################################################ Store cyclevalue ############################################################
CycleNO=[]

################################################ Store PC value ############################################################
PCNO=[]

################################################ ALL Instruvtion ############################################################
memory=[]
for i in range(256):
    memory.append("0000000000000000")

################################################ load  Instruvtion ############################################################
variables={}

################################################ REGISTER NAMES ############################################################
Regnames={"000":"R0","001":"R1","010":"R2","011":"R3","100":"R4","101":"R5","110":"R6","111":"FLAGS"}

################################################ REGISTER VALUES ############################################################
Regvalues={"R0":0,"R1":0,"R2":0,"R3":0,"R4":0,"R5":0,"R6":0,"FLAGS":0,}

################################################ TAKING INPUT ############################################################
i=0
for line in stdin:
    if line == '': # If empty string is read then stop the loop
        break
    line=line.replace('\n','')   
    memory[i]=line
    i+=1



################################################ halted ############################################################
halted=False


################################################ SET FLAGS VALUES #####################################################
def setflag(konsa,yesNo): #######konsa matlab konsa bit change karna ha   ################yesNo mean value 1 karni ha ya na
    value=Regvalues.get("FLAGS")
    if (not yesNo):
        Regvalues["FLAGS"]=0
    else:
        Regvalues["FLAGS"]=changebit[konsa]

################################################ compare STATENMENTS #####################################################
def comparereg(r1,r2):
    if r1==r2:
        return 'E'
    elif r1>r2:
        return 'G'
    else:
        return 'L'
    
################################################ bitwise operator STATENMENTS #####################################################
def xorreg(a, b):                             ########################### XOR FUNCTION
    return (a and (notreg(b))) or ((notreg(a)) and b)  

def andreg(a,b):                                ######################## AND
    return (a and b)

def orreg(a,b):                                ######################## OR
    return (a or b)
 
def notreg(a):                                ##########################NOT
    return intfrbin(str(1111111111111111-int(binto16(a)))) 

################################################ shift  STATENMENTS #####################################################
def rshift(x,a):
    return int(x/pow(2,a))

def lshift(x,a):
    va=int(x*pow(2,a))
    ta=binto32(va)[16:]
    ta=intfrbin(ta)
    return ta
################################################ PRINT STATENMENTS #####################################################        
def PRINTSTATENMENT():
    global PC
    STRING=binto8(PC) + " " + str(binto16(Regvalues["R0"])) + " " + str(binto16(Regvalues["R1"])) + " " + str(binto16(Regvalues["R2"])) 
    STRING=STRING + " " + str(binto16(Regvalues["R3"])) + " " + str(binto16(Regvalues["R4"])) + " " + str(binto16(Regvalues["R5"])) 
    STRING=STRING + " " + str(binto16(Regvalues["R6"])) + " " + str(binto16(Regvalues["FLAGS"])) 
    sys.stdout.write(STRING +"\n")
    
    
def execute(ins):                             ##################################return new programm counter####################
    global PC
    new_PC=PC
    global halted
    opcode=ins[:5]
    
    if opcode=="10011":                     #####################################UPDATE Hallted to end the program #############
        halted=True
        setflag('V',False)                                                                                                      ################FLAG set
        return -1
    
    if opcode[0]!='1' and opcode!="01111":   #####################################UPDATE PC IF NO BRANCH ######################
        new_PC+=1
        
    elif opcode=="01111":
        new_PC=intfrbin(ins[8:].replace('\r',''))            ##################################### cinvert last 8 bit address into integer#######
        setflag('V',False)                                                                                                    ################FLAG set
        return new_PC
    
    elif opcode=="10000":                  ##################################### branch if less than ##########################
        if Regvalues["FLAGS"]==4:
            new_PC=intfrbin(ins[8:].replace('\r',''))       ##################################### cinvert last 8 bit address into integer#######
        else:
            new_PC+=1
        setflag('V',False)                                                                                                   ################FLAG set
        return new_PC
        
    elif opcode=="10001" :                   ##################################### branch if greater than #######################
        if Regvalues["FLAGS"]==2:
            new_PC=intfrbin(ins[8:].replace('\r',''))          ##################################### cinvert last 8 bit address into integer####### 
        else:
            new_PC+=1
        setflag('V',False)                                                                                                    ################FLAG set    
        return new_PC
        
    else:                                  ##################################### branch if equal  ############################
        if Regvalues["FLAGS"]==1:
            new_PC=intfrbin(ins[8:].replace('\r',''))       ##################################### cinvert last 8 bit address into integer#######
        else:
            new_PC+=1
        setflag('V',False)                                                                                                    ################FLAG set    
        return new_PC
######################################## MOVE instruction #####################################
    if opcode=="00010":
        reg=Regnames[ins[5:8]]
        value=intfrbin(ins[8:].replace('\r',''))
        Regvalues[reg]=value
        setflag('V',False)                                                                                    ################FLAG set
        return new_PC
    elif opcode=="00011":
        reg1=Regnames[ins[10:13]]
        reg2=Regnames[ins[13:].replace('\r','')]
        Regvalues[reg1]=Regvalues[reg2]
        setflag('V',False)                                                                                     ################FLAG set
        return new_PC

######################################## LOAD and STORE  instruction #####################################
    if opcode=="00100":                        #########################   LOAD
        reg=Regnames[ins[5:8]]
        value=ins[8:].replace('\r','')        ## binary value
        Regvalues[reg]=variables[value]
        setflag('V',False)                                                                                       ################FLAG set 
        return new_PC

    elif opcode=="00101":                      #########################   STORE
        reg=Regnames[ins[5:8]]
        value=ins[8:].replace('\r','')        ## binary value
        variables[value]=Regvalues[reg]
        memory[intfrbin(value)]=binto16(Regvalues[reg])
        setflag('V',False)                                                                                  ################FLAG set
        return new_PC
        
        
######################################## compare   instruction #####################################
    if opcode=="01110":
        reg1=Regnames[ins[10:13]]
        reg2=Regnames[ins[13:].replace('\r','')]
        stre=comparereg(Regvalues[reg1],Regvalues[reg2])       #############################return g,e,l
        setflag(stre,True)                                      ###############################set flag according to g,e,l
        return new_PC
    
######################################## bit wise operator   instruction #####################################
    if opcode=="01101":                             ##################### invert
        reg1=Regnames[ins[10:13]]
        reg2=Regnames[ins[13:].replace('\r','')]
        Regvalues[reg1]=notreg(Regvalues[reg2])
        setflag('V',False)                                                                                        ################FLAG set
        return new_PC
    
    elif opcode=="01100":                                             ######################## AnD
        reg1=Regnames[ins[7:10]]
        reg2=Regnames[ins[10:13]]
        reg3=Regnames[ins[13:].replace('\r','')]
        Regvalues[reg1]=andreg(Regvalues[reg2],Regvalues[reg3])
        setflag('V',False)                                                                                         ################FLAG set
        return new_PC
        
    elif opcode=="01011":                                  ######################## Or
        reg1=Regnames[ins[7:10]]
        reg2=Regnames[ins[10:13]]
        reg3=Regnames[ins[13:].replace('\r','')]
        Regvalues[reg1]=orreg(Regvalues[reg2],Regvalues[reg3])
        setflag('V',False)                                                                                         ################FLAG set
        return new_PC
            
    elif opcode=="01010":                                  ######################## XOR            
        reg1=Regnames[7:10]
        reg2=Regnames[10:13]
        reg3=Regnames[13:].replace('\r','')
        Regvalues[reg1]=orreg(Regvalues[reg2],Regvalues[reg3])
        setflag('V',False)                                                                                          ################FLAG set
        return new_PC
        
######################################## ALL FOR updating FLAGS (V) bit mean FLAGS=8 #####################################
    if opcode=="00000":                           ################################# simple ADD
        reg1=Regnames[ins[7:10]]
        reg2=Regnames[ins[10:13]]
        reg3=Regnames[ins[13:].replace('\r','')]
        a=Regvalues[reg2]
        b=Regvalues[reg3]
        c=a+b
        if c>65535:
            ta=binto32(c)[16:]
            c=intfrbin(ta)
            setflag('V',True)                                           ################FLAG set
        else:
            setflag('V',False)
        Regvalues[reg1]=c    
        return new_PC
        
    if opcode=="00001":                           ################################# simple sub
        reg1=Regnames[ins[7:10]]
        reg2=Regnames[ins[10:13]]
        reg3=Regnames[ins[13:].replace('\r','')]
        a=Regvalues[reg2]
        b=Regvalues[reg3]
        c=a-b
        if c<0:
            c=0
            setflag('V',True)                                   ################FLAG set
        else:
            setflag('V',False)
        Regvalues[reg1]=c    
        return new_PC

    if opcode=="00110":                           ################################# simple multiply
        reg1=Regnames[ins[7:10]]
        reg2=Regnames[ins[10:13]]
        reg3=Regnames[ins[13:].replace('\r','')]
        a=Regvalues[reg2]
        b=Regvalues[reg3]
        c=a*b
        if c>65535:
            ta=binto32(c)[16:]
            c=intfrbin(ta)
            setflag('V',True)                                           ################FLAG set
        else:
            setflag('V',False)
        Regvalues[reg1]=c
        return new_PC
    
    if opcode=="00111":                           ################################# simple divide
        reg1=Regnames[ins[10:13]]
        reg2=Regnames[ins[13:].replace('\r','')]
        a=Regvalues[reg1]
        b=Regvalues[reg2]
        c=a/b
        d=a%b
        Regvalues["R0"]=c
        Regvalues["R1"]=d
        setflag('V',False)                                     ################FLAG set
        return new_PC
    
######################################## Shift  operator   instruction #####################################

    if opcode=="01000":                                   ############################# right shift
        reg=Regnames[ins[5:8]]
        value=intfrbin(ins[8:].replace('\r',''))                ##int value
        rs=rshift(Regvalues[reg],value)
        Regvalues[reg]=rs
        setflag('V',False)                                        ################FLAG set
        return new_PC
    
    if opcode=="01001":                                   ############################ left shift
        reg=Regnames[5:8]
        value=intfrbin(ins[8:].replace('\r','')) ## int value
        ls=lshift(Regvalues[reg],value)
        Regvalues[reg]=ls
        setflag('V',False)                                         ################FLAG set
        return new_PC   

################################################ PROGRAMM COUNTER  ############################################################    
PC=0

################################################ FOR GRAPH ############################################################

############## programm counter is appended in PC no array ##################

################################################ cycleno ############################################################
Cycle=0

################################################ FOR GRAPH ############################################################

############## programm counter is appended in PC no array ##################

################################################ Main code  ############################################################
while (not halted):
    CycleNO.append(Cycle)                 ########################################## append value for graph cycle
    Cycle+=1
    PCNO.append(PC)                      ########################################## append value for graph PC
    
    
    Instruction = memory[PC]                          ################################# Get current instructionhalted
    
    new_PC=execute(Instruction)                       #################################Update Program Counter
    
    PRINTSTATENMENT()                                 ############################################# Print the ALL things
    
    PC=new_PC                                       #################################### UPDATE VALUE IN PC 

    
################################################ Print all MEMORY ############################################################
dsa=0 
for i in memory:
    dsa+=1
    sys.stdout.write(i+"\n")


    
tracesplot(CycleNO,PCNO)    