from circuits import fulladder, mux_2to1, mux_4to1, decoderReg, mainControl, registerFile, aluControl, ALU_1bit, ALU_32bit, simpleMIPS
'''
Adder = fulladder(cin=0, in1=1, in2=1)
print(Adder.getCircuitOutput())

MUX = mux_2to1(in1=0, in2=1, sel=0)
print(MUX.getCircuitOutput())

MUX2 = mux_4to1(in1=0, in2=0, in3=0, in4=1, sel1=1, sel2=0) # Problem: in2 & in3 are reversed (Thomas's note)
print(MUX2.getCircuitOutput())

decoder = decoderReg([0, 0, 1, 1, 0])
print(decoder.getCircuitOutput())

mainCntrol = mainControl([1,0,0,0,1,1])
print(mainCntrol.getCircuitOutput())

registers = registerFile([
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 1, 0
])

values = registers.getAllRegValues()
for row in values:
  print(row)

registers.setRegValue([1,1,1,0,0,0,0,0], [0,0,1,1,0])
print(registers.getRegValue([0,0,1,1,0]))
print(registers.getRegValue())

values = registers.getAllRegValues()
for row in values:
  print(row)

alucontrol = aluControl(1,0,1,0,1,0,1,0)
print(alucontrol.getCircuitOutput())

alu_1bit = ALU_1bit(a=0, b=0, aInvCode=0, bInvCode=0, op1=0, op2=0, carryIn=0, less=0)
print(alu_1bit.getCircuitOutput())

first = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0] # 36
second = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1] # 47

alu_32bit = ALU_32bit(A=second, B=first, aluControlCode=[0,1,1,1])
print(alu_32bit.getCircuitOutput())


reg_file = registerFile([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0])

instruction = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]

results = simpleMIPS(reg_file).getCircuitOutput(instruction)

for row in results:
  print(row)
'''
test_instruction_sequence = [
  [
    0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0
  ],  #add $8, $6, $7
  [
    0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1
  ],  #or $9, $8, $7
  [
    0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0
  ],  #add $10, $9, $9
  [
    0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0
  ],  #and $11, $9, $10
  [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 0, 1, 0, 1, 0
  ],  #slt $2, $3, $10
]

reg_initial_value = [
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 1, 0
]

reg_file = registerFile(reg_initial_value)

simpleMIPSCPU = simpleMIPS(reg_file)

for instru in test_instruction_sequence:
  results = simpleMIPSCPU.getCircuitOutput(instru)
  print("After excute instruciton: ",
        instru)
  for i in range(32):
    print("Register ", i, ": ", results[i])
  print(" ")

