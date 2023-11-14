__author__ = "Ricky Yoder, Justin Verhosek, Thomas Kmetich"
__Copyright__ = "Copyright @2022"


class circuit(object):

  def __init__(self, in1, in2):
    self.in1_ = in1
    self.in2_ = in2


class andgate(circuit):

  def getCircuitOutput(self):
    if self.in1_ == 1 and self.in2_ == 1:
      return 1
    else:
      return 0


class orgate(circuit):

  def getCircuitOutput(self):
    if self.in1_ == 0 and self.in2_ == 0:
      return 0
    else:
      return 1


class notgate(circuit):

  def __init__(self, in1):
    self.in1_ = in1

  def getCircuitOutput(self):
    if self.in1_ == 1:
      return 0
    elif self.in1_ == 0:
      return 1


#Hint: you may implement some multi-input logic gates to help you build the circuit,
#for example, below is a 3-input andgate3 boolean algebra: Y=ABC
class andgate3(circuit):

  def __init__(self, in1, in2, in3):
    self.in1_ = in1
    self.in2_ = in2
    self.in3_ = in3

  def getCircuitOutput(self):
    andg0 = andgate(self.in1_, self.in2_)
    out_andg0 = andg0.getCircuitOutput()

    andg1 = andgate(out_andg0, self.in3_)
    out_andg1 = andg1.getCircuitOutput()

    return out_andg1


class orgate3(circuit):

  def __init__(self, in1, in2, in3):
    self.in1_ = in1
    self.in2_ = in2
    self.in3_ = in3

  def getCircuitOutput(self):
    org0 = orgate(self.in1_, self.in2_)
    out_org0 = org0.getCircuitOutput()

    org1 = orgate(out_org0, self.in3_)
    out_org1 = org1.getCircuitOutput()

    return out_org1


class andgate6(circuit):

  def __init__(self, in1, in2, in3, in4, in5, in6):
    self.in1 = in1
    self.in2 = in2
    self.in3 = in3
    self.in4 = in4
    self.in5 = in5
    self.in6 = in6

  def getCircuitOutput(self):
    return andgate(
      andgate3(self.in1, self.in2, self.in3).getCircuitOutput(),
      andgate3(self.in4, self.in5,
               self.in6).getCircuitOutput()).getCircuitOutput()


#2to1 mux implemented by notgate, andgates and orgates
class mux_2to1(circuit):
  '''
    Implement a 2to1 multiplexer by using the notgate, andgate and orgate
    '''

  def __init__(self, in1, in2, sel):
    self.in1 = in1
    self.in2 = in2
    self.sel = sel

  def getCircuitOutput(self):
    return orgate(
      andgate(self.in2, self.sel).getCircuitOutput(),
      andgate(notgate(self.sel).getCircuitOutput(),
              self.in1).getCircuitOutput()).getCircuitOutput()


#4to1 mux implemented by 2to1 muxes
class mux_4to1(circuit):
  '''
    Implement a 4to1 multiplexer by using the mux_2to1
    '''

  def __init__(self, in1, in2, in3, in4, sel1, sel2):
    self.in1 = in1
    self.in2 = in2
    self.in3 = in3
    self.in4 = in4
    self.sel1 = sel1
    self.sel2 = sel2

  def getCircuitOutput(self):
    return mux_2to1(
      mux_2to1(self.in1, self.in3, self.sel1).getCircuitOutput(),
      mux_2to1(self.in2, self.in4, self.sel1).getCircuitOutput(),
      self.sel2).getCircuitOutput()


#fulladder implemented with logic gates
class fulladder(circuit):

  def __init__(self, cin, in1, in2):
    self.cin = cin
    self.in1 = in1
    self.in2 = in2

  def getCircuitOutput(self):
    return [
      orgate3(
        andgate(self.in1, self.in2).getCircuitOutput(),
        andgate(self.in2, self.cin).getCircuitOutput(),
        andgate(self.in1, self.cin).getCircuitOutput()).getCircuitOutput(),
      orgate(
        orgate(
          andgate3(self.in1, self.in2, self.cin).getCircuitOutput(),
          andgate3(self.in1,
                   notgate(self.in2).getCircuitOutput(),
                   notgate(self.cin).getCircuitOutput()).getCircuitOutput()).
        getCircuitOutput(),
        orgate(
          andgate3(
            notgate(self.in1).getCircuitOutput(), self.in2,
            notgate(self.cin).getCircuitOutput()).getCircuitOutput(),
          andgate3(
            notgate(self.in1).getCircuitOutput(),
            notgate(self.in2).getCircuitOutput(),
            self.cin).getCircuitOutput()).getCircuitOutput()).getCircuitOutput(
            )
    ]
    #[in1*in2 + in2*cin + in1*cin, in1*in2*carryin + in1*!in2*!cin + !in1*in2+!cin + !in1*!in2*cin] [Carryout, sum]

  '''
  Implement a full adder by using the above circuits, e.g.,  andgate, orgate3, etc.
  '''


class registerFile(circuit):

  def __init__(self, reg_initial_value):
    self.registers = []
    for i in range(32):
      self.registers.append(reg_initial_value)

  def setRegValue(self, valueToSet, fiveBitBinList = [0,0,0,0,0]): #sets the register corresponding to the decimal value of the list which depicts binary
    o_regDecoder = decoderReg(fiveBitBinList)
    self.registers[o_regDecoder.getCircuitOutput()] = valueToSet 

  def getRegValue(self, fiveBitBinList = [0,0,0,0,0]): #gets the value of the register in the position corresponding to the decmial value of the list
    o_regDecoder = decoderReg(fiveBitBinList)
    return self.registers[o_regDecoder.getCircuitOutput()]

  def getAllRegValues(self):
    return self.registers
    

class decoderReg(circuit):

  def __init__(self, fiveBitBinList): #list of 5 bits e.g. [0,0,1,0,1] with a decimal value of 5 corresponding to register 5
    self.binaryList = fiveBitBinList
    
  def getCircuitOutput(self):
    binaryString = []
    for bit in self.binaryList:
      binaryString.append(str(bit))
    binaryString = ''.join(binaryString)
    return int(binaryString, 2)
    

class mainControl(circuit):

  def __init__(self, sixBitBinList):
    self.op_0 = sixBitBinList[5]
    self.op_1 = sixBitBinList[4]
    self.op_2 = sixBitBinList[3]
    self.op_3 = sixBitBinList[2]
    self.op_4 = sixBitBinList[1]
    self.op_5 = sixBitBinList[0]

  def getCircuitOutput(self):
    andg3 = andgate6(
      notgate(self.op_0).getCircuitOutput(),
      notgate(self.op_1).getCircuitOutput(),
      notgate(self.op_2).getCircuitOutput(),
      notgate(self.op_3).getCircuitOutput(),
      notgate(self.op_4).getCircuitOutput(),
      notgate(self.op_5).getCircuitOutput()).getCircuitOutput()
    andg2 = andgate6(self.op_0, self.op_1,
                     notgate(self.op_2).getCircuitOutput(),
                     notgate(self.op_3).getCircuitOutput(),
                     notgate(self.op_4).getCircuitOutput(),
                     self.op_5).getCircuitOutput()
    andg1 = andgate6(self.op_0, self.op_1,
                     notgate(self.op_2).getCircuitOutput(), self.op_3,
                     notgate(self.op_4).getCircuitOutput(),
                     self.op_5).getCircuitOutput()
    andg0 = andgate6(
      notgate(self.op_0).getCircuitOutput(),
      notgate(self.op_1).getCircuitOutput(), self.op_2,
      notgate(self.op_3).getCircuitOutput(),
      notgate(self.op_4).getCircuitOutput(),
      notgate(self.op_5).getCircuitOutput()).getCircuitOutput()
    if andg3 == 1:  #R-Type
      return [1, 0, 0, 1, 0, 0, 0, 1, 0]  
      #regDst, ALUSrc, MemtoReg, RegWrite, MemRead, MemWrite, Branch, ALUOp1, ALUOp0
    elif andg2 == 1:  #load word
      return [0, 1, 1, 1, 1, 0, 0, 0, 0]
    elif andg1 == 1:  #store word
      return [0, 1, 0, 0, 0, 1, 0, 0, 0]
    elif andg0 == 1:  #Branch if equal
      return [0, 0, 0, 0, 0, 0, 1, 0, 1]
    else:
      return [0, 0, 0, 0, 0, 0, 0, 0, 0]


#1 bit ALU implemented with logic gates
class ALU_1bit(object):

  def __init__(self, a, b, aInvCode, bInvCode, op1, op2, carryIn):
    self.a = a
    self.b = b
    self.aInvCode = aInvCode
    self.bInvCode = bInvCode
    self.op1 = op1
    self.op2 = op2
    self.carryIn = carryIn

  def getCircuitOutput(self):
    aInverse = notgate(self.a).getCircuitOutput()
    bInverse = notgate(self.b).getCircuitOutput()
    
    aMux = mux_2to1(self.a, aInverse, self.aInvCode).getCircuitOutput() # 0-selects a / 1-selects aInverse
    bMux = mux_2to1(self.b, bInverse, self.bInvCode).getCircuitOutput()
    
    AND = andgate(aMux, bMux).getCircuitOutput()
    OR = orgate(aMux, bMux).getCircuitOutput()
    adder = fulladder(self.carryIn, aMux, bMux).getCircuitOutput()  # fulladder returns [carryout, sum]
    SUM = adder[1]
    carryout = adder[0]
    LESS = adder[1] 

    MUX4 = mux_4to1(AND, OR, SUM, LESS, self.op1, self.op2).getCircuitOutput()

    result = [MUX4, carryout]

    return result

  '''
    Implement a 1-bit ALU by using the above circuits, e.g.,  mux_2to1, fulladder and mux_4to1, etc.
    '''


class aluControl(circuit):

  def __init__(self, aluOp1, aluOp0, f5, f4, f3, f2, f1, f0):
    self.aluOp1 = aluOp1
    self.aluOp0 = aluOp0
    self.f5 = f5
    self.f4 = f4
    self.f3 = f3
    self.f2 = f2
    self.f1 = f1
    self.f0 = f0

  def getCircuitOutput(self):
    or1 = orgate(self.f3, self.f0).getCircuitOutput()
    and1 = andgate(self.f1, self.aluOp1).getCircuitOutput()
    op0 = andgate(or1, self.aluOp1).getCircuitOutput()
    op1 = orgate(notgate(self.f2).getCircuitOutput(),notgate(self.aluOp1).getCircuitOutput()).getCircuitOutput()
    op2 = orgate(and1, self.aluOp0).getCircuitOutput()
    op3 = andgate(self.aluOp0,
                  notgate(self.aluOp0).getCircuitOutput()).getCircuitOutput()

    return [op3, op2, op1, op0] #AluControlCode

  '''
    Implement the ALU control circuit shown in Figure D.2.2 on page 7 of the slides 10_ALU_Control.pdf.
    There are eight inputs: aluOp1, aluOp2, f5, f4, f3, f2, f1, f0.
    There are four outputs of the circuit, you may put them in a python list and return as a whole.
    '''


class ALU_32bit(object):

  def __init__(self, A, B, aluControlCode):
    self.A = A
    self.B = B
    self.aluControlCode = aluControlCode

  def getCircuitOutput(self):

    result = []
    aMuxControl = self.aluControlCode[0]
    bMuxControl = self.aluControlCode[1]
    aluOp1 = self.aluControlCode[2]
    aluOp2 = self.aluControlCode[3]
    if self.aluControlCode == [0,1,1,0] or self.aluControlCode == [0,1,1,1]: 
      carryIn = 1
    else:
      carryIn = 0

    for x in range(31, -1, -1):
      output = ALU_1bit(self.A[x], self.B[x], aMuxControl, bMuxControl, aluOp1, aluOp2, carryIn).getCircuitOutput() 
            # output is [x, carryout] where x is (AND, OR, SUM, less) depending on mux4

      if aluOp1 == 0 and (aluOp2 == 0 or aluOp2 == 1):  # AND or OR
        result.append(output[0])
      elif aluOp1 == 1 and aluOp2 == 0:                 # Fulladder, ADD and SUBTRACT
        carryIn = output[1]
        result.append(output[0])
      else:                                             # LESS
        carryIn = output[1]
        if x == 0:
          result.append(output[0])
        else:
          result.append(0)

    if not(aluOp1 == 1 and aluOp2 == 1):
      result.reverse()

    return result
         
        

  '''
    Implement a 32 bit ALU by using the 1 bit ALU.
    Your 32-bit ALU should be able to compute 32-bit AND, OR, addition, subtraction, slt(set on if less than).
    The inputs are:

    two python lists with lenth 32, e.g.:
         0, 1, 2, 3, 4, 5, 6, 7, ...                                                          29, 30, 31
    A = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1]
    B = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    please note that bit 0 is at the end of the list, which means that bit 0 of A is A[31], bit 31 of A is A[0], bit 0 of B is B[31] and bit 31 of B is B[0].

    carryIn for the 0th 1-bit ALU, which take care of the bit 0.

    aluctrs, which could be a list of alu control signals:
    aluctrs[0] controls the all the 2to1 mux in each 1-bit ALU for bits of input A,
    aluctrs[1] controls the all the 2to1 mux in each 1-bit ALU for bits of input B.
    aluctrs[2] and aluctrs[3] controls all the 4to1 mux in each 1-bit ALU for choose what as output, 00 choose out from AND, 01 choose out from OR, 10 choose out from adder, 11 choose the less.

    Please note that the carryOut output of each 1-bit ALU except the 31th one should be the carryIn the next 1 bit ALU, you may use for loop here for the computation of the sequential 1-bit ALU.

    And please also note that in order to make slt work, we need to use the sum output from the adder of the 31th 1-bit ALU and make it as the less input of the 0th 1bit ALU.
    '''


  '''
    Implement a simpleMIPS class to process R-Type instructions, e.g.: add, sub, or, and, slt.
To get credit for the final project, you need to use the mainCtrol class, aluControl Class,
ALU32bit class, and registerFile class.
    '''
  
class simpleMIPS(circuit):

  def __init__(self, registers):
    self.registers = registers

  def getCircuitOutput(self, instru):
    #breaks apart instruction
    opcode = instru[0:6]
    rs = instru[6:11]
    rt = instru[11:16]
    rd = instru[16:21]
    shamt = instru[21:26]
    funct = instru[26:32]
    #uses all needed classes
    ALUOp = mainControl(opcode).getCircuitOutput()
    acOutput = aluControl(ALUOp[7], ALUOp[8], funct[0], funct[1], funct[2], funct[3], funct[4], funct[5]).getCircuitOutput()

    A = self.registers.getRegValue(rs) 
    B = self.registers.getRegValue(rt)

    result = ALU_32bit(A, B, acOutput).getCircuitOutput()

    self.registers.setRegValue(result, rd)

    return self.registers.getAllRegValues()

  

    