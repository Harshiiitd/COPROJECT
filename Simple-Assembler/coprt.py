from sys import stdin
import sys
opcode={"add":("00000",'A'),"sub":("00001",'A'),"mov1":["00010",'B'],"mov2":("00011",'C'),"ld":("00100",'D'),
        "st":("00101",'D'),"mul":("00110",'A'),"div":("00111",'C'),"rs":("01000",'B'),"ls":("01001",'B'),
        "xor":("01010",'A'),"or":("01011",'A'),"and":("01100",'A'),"not":("01101",'C'),"cmp":("01110",'C'),
        "jmp":("01111",'E'),"jlt":("10000",'E'),"jgt":("10001",'E'),"je":("10010",'E'),"hlt":("10011",'F')}



reg={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"    }
integer=['1','2','3','4','5','6','7','8','9','0']
labelindex={}
varindex={} 
errorno=0
simple=[]
variable=[]
count=0
 #opcode, r1,r2,r0ss
def process(line):
    global count
    if line=='':
        count+=1
        return
    while line[0]==" ":  
        line=line[1:]
    Str=line.split()
    if Str[0]=="var": 
        if len(variable)!=count:
            lk="error VAR is not defined in begning line no of error " + str(count)
            sys.stdout.write(lk+"\n")                                                                         # print
            errordetect=True
        count+=1
        variable.append(line)
    else:
        simple.append(line)
        count+=1
        

for line in stdin:
    if line == '': # If empty string is read then stop the loop
        break
    process(line.replace('\n',''))
#while True:
 #   line=input()
  #  if line=='':
   #     break
    #process(line)    

errordetect=False
n=len(simple)
if errordetect==False:
    for i in variable:
        while i[0]==" ":  # VAR X
            i=i[1:]
        Str=i.split() # VAR ,X
        if len(Str)!=2:
            lk="error WORNG VAR INSTRUCTION AT NUMBER "+ str(errorno)
            sys.stdout.write(lk+"\n")                                                                    #print line
            errordetect=True
            break
        elif (Str[1]=="var" or Str[1]=="hlt"or (Str[1] in opcode) or Str[1]=="mov"):
            lk="error WORNG VAR INSTRUCTION AT NUMBER "+ str(errorno)
            sys.stdout.write(lk+"\n")                                                                    #print line
            errordetect=True
            break    
        else:
            if Str[1].isidentifier()==False:
                lk="Error wrong variable name and at number " + str(errorno)
                sys.stdout.write(lk+"\n")                                                                  #print line
                errordetect=True                          
                break  
            varindex[Str[1]]=n     # 'x'=n
            n+=1
        errorno+=1    
        
        

if errordetect==False:
    for i in range(len(simple)):
        ins=simple[i]
        while ins[0]==" ": 
            ins=ins[1:]
        Str=ins.split()    ####  ek instruction pa 2 label ho 
        ved=Str[0]
        if(ved[-1]==':'):
            ved=ved[:-1]
            if ved in labelindex:                                                
                lk="Error same name of label again and at number " +str((i+len(variable)))
                sys.stdout.write(lk+"\n")                                                                  #print line
                errordetect=True                          
                break
            if (ved=="var" or ved=="hlt" or ved=="mov" or (ved in opcode)):
                lk="Error no such label name allowed and at number " +str((i+len(variable)))
                sys.stdout.write(lk+"\n")                                                                  #print line
                errordetect=True                          
                break    
            else:
                if len(Str)==1:
                    lk="Error nothing after label and at number " +str((i+len(variable)))
                    sys.stdout.write(lk+"\n")                                                                  #print line
                    errordetect=True                          
                    break
                elif  ved.isidentifier()==False:
                    lk="Error wrong label name and at number " +str((i+len(variable)))
                    sys.stdout.write(lk+"\n")                                                                  #print line
                    errordetect=True                          
                    break    
                labelindex[ved]=i                       ###############changes
                simple[i]=ins[len(ved)+1:]              ##############changes
 
while simple[-1]=="":
    simple.pop(-1)
    
cdsa=simple[-1]
while cdsa[0]==" ":
    cdsa=cdsa[1:]

while cdsa[-1]==" ":
    cdsa=cdsa[:-1]
                                                             ###################################3changes
simple[-1]=cdsa
if simple[-1]!="hlt":
    lk="error  HLT is not used at last at line number " +str((len(variable)+len(simple)))     
    sys.stdout.write(lk +"\n")                                                                                     # print line
    errordetect=True

if simple.count("hlt")>1:
    lk="error related to multiple  HLT at line number " +str((len(variable)+len(simple)))     
    sys.stdout.write(lk+"\n")                                                                                     # print line
    errordetect=True   

def machinecode(t):
    global errorline
    global numberinstruction
    if t=='':
        return
    
    
    while t[0]==" ":
        t=t[1:]
    arr=t.split()
    s=""
    if arr[0]=="mov":
        if len(arr)!=3:
            lk="error in line no "+str(numberinstruction)
            sys.stdout.write(lk+"\n")                                              # print line                            
            errorline=True
            return
        xc=arr[2]
        if xc[0]=='$':
            arr[0]="mov1"
        else :
            arr[0]="mov2"
            
    d=opcode.get(arr[0],"errors")
    if d=="errors":
      sys.stdout.write("wrong statenment at line no"+str(numberinstruction) +"\n")
      errorline=True
      return
    if  d[1]=='A':
        if len(arr)!=4:
            lk="error of wrong instruction A and at line no " +str(numberinstruction)
            sys.stdout.write(lk+"\n")                                                       # print line  
            errorline=True
            return 
        if arr[1]=="FLAGS" or  arr[2]=="FLAGS" or arr[3]=="FLAGS":
            lk="cannot use FLAG resister for this instruction  line no "+str(numberinstruction)
            sys.stdout.write(lk+"\n")                                                       #print line
            errorline=True

        labelno1=reg.get(arr[1],"error")
        if labelno1=="error":
            lk=" no label name like this  line no "+str(numberinstruction)
            sys.stdout.write(lk+"\n")                                                       #print line
            errorline=True
            return
        labelno2=reg.get(arr[2],"error")
        if labelno2=="error":
            lk=" no label name like this  line no "+str(numberinstruction)
            sys.stdout.write(lk+"\n")                                                  # printline
            errorline=True
            return    
        labelno3=reg.get(arr[3],"error")
        if labelno3=="error":
            lk=" no label name like this  line no "+str(numberinstruction)
            sys.stdout.write(lk+"\n")                                                     #print
            errorline=True
            return  
        s=s+d[0]+"00"+labelno1 +labelno2 +labelno3
        sys.stdout.write(s)                                                                          # print

###### B TYPE
    elif d[1]=='B':
        if len(arr)!=3:
            lk="error of wrong instruction B and at line no "+str(numberinstruction)
            sys.stdout.write(lk+"\n")                                                                       #print
            errorline=True
            return
        if arr[1]=="FLAGS":
            lk="cannot use FLAG resister for this instruction  line no "+str(numberinstruction)
            sys.stdout.write(lk+"\n")                                                       #print line
            errorline=True

        dc=reg.get(arr[1],"error")
        if dc=="error":
            lk="error"+str(numberinstruction)
            sys.stdout.write(lk+"\n")                                                                 #print 
            errorline=True
            return
        
        s2=arr[2]
        s2=s2[1:]
        z=False
        for i in s2:
            if i not in integer:
                lk="immediate is not integer and line no"+str(numberinstruction)
                sys.stdout.write(lk+"\n")                                                                  #prnt
                z=True
                errorline=True
                break
        if z:
            return
        tre=int(s2)
        if tre>255:
            lk="error immediate is greater than 255 and line no "+str(numberinstruction)
            sys.stdout.write(lk+"\n")  # overflow bit set karni ha               #prt
            errorline=True
            return
        binary="{0:08b}".format(tre)
        s=s+d[0]
        s=s+dc+binary
        sys.stdout.write(s)                                                                                     #prt



###### C   TYPE
    elif d[1]=='C':
        if len(arr)!=3:
            lk="error of wrong instruction c and at line no "+str(numberinstruction)
            sys.stdout.write(lk+"\n")                                                       #prt
            errorline=True 
            return
        if arr[1]=="FLAGS" :
            lk="cannot use FLAG resister for this instruction  line no "+str(numberinstruction)
            sys.stdout.write(lk+"\n")                                                       #print line
            errorline=True

        labelno1=reg.get(arr[1],"error")
        if labelno1=="error":
            lk=" no label name like this  line no "+str(numberinstruction)
            sys.stdout.write(lk+"\n")                                                               #prt
            errorline=True
            return
        
        labelno2=reg.get(arr[2],"error")
        if labelno2=="error":
            lk=" no label name like this  line no "+str(numberinstruction)
            sys.stdout.write(lk+"\n")                                                                 #prt
            errorline=True
            return
        
        s=s+d[0]+"00000"+labelno1+labelno2
        sys.stdout.write(s)                                                                                #  prt



###### F TYPE
    elif d[1]=='F':
        if len(arr)!=1:
            lk="error of wrong instruction B and at line no " +str(numberinstruction)
            sys.stdout.write(lk+"\n")                                                                          #prt
            errorline=True
            return
        s=s+d[0]+"00000000000"
        sys.stdout.write(s)                                                                                     #prt 


#######   E TYPE    
    elif d[1]=='E':
        if len(arr)!=2:
            lk="error of wrong instruction E and at line no "+str(numberinstruction)
            sys.stdout.write(lk+"\n")                                                       #prt
            errorline=True
            return
        
        labelno=labelindex.get(arr[1],"error")
        if labelno=="error":
            lk=" no label name like this  line no " +str(numberinstruction)
            sys.stdout.write(lk+"\n")                                                                  #prt
            errorline=True
            return
        s=s+d[0]+"000" + "{0:08b}".format(labelno)                             ##############changes   
        sys.stdout.write(s)                                                                             #prt
        
    
    
###### D TYPE    
    elif d[1]=='D':
        if len(arr)!=3:
            lk="error of wrong instruction D and at line no "+str(numberinstruction)
            sys.stdout.write(lk)                                                         #prt
            errorline=True
            return

        if arr[1]=="FLAGS":
            lk="cannot use FLAG resister for this instruction  line no "+str(numberinstruction)
            sys.stdout.write(lk+"\n")                                                       #print line
            errorline=True    
        s=s+d[0]
        dc=reg.get(arr[1],"error")
        if dc=="error":
            lk="error wrong resister name and at line number "+str(numberinstruction)
            sys.stdout.write(lk+"\n")                                                                 #prt
            errorline=True
            return
        memadd=varindex.get(arr[2],"error")
        if memadd=="error":
            lk="error no variable name  and at line number " +str(numberinstruction)
            sys.stdout.write(lk+"\n")                                                           #prt
            errorline=True
            return
        s=s+dc+"{0:08b}".format(memadd)    
        sys.stdout.write(s)                                                                           #prt       
        
    
    else:
        lk="eror   NO SUCH TYPE OF INSTRUCTION or error more space in instruction than expected and line no " +str(numberinstruction)
        sys.stdout.write(lk+"\n")                                                  
        errorline=True
        return                                                                                           #prt
        # for the instruction with wrong name
    numberinstruction+=1
    sys.stdout.write("\n")

    
numberinstruction=len(variable)    
errorline=False
for i in simple: 
    if errorline==False and errordetect==False:
        machinecode(i)             