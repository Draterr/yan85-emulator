from collections import deque
from typing import *

#first opcode,second arg2,third arg1
vm_code = [ 0x20, 0xb9, 0x20, 0x04, 0x20, 0x08, 0x04, 0x10, 0x00, 0x04, 0x40, 0x00, 0x04, 0x20, 0x00, 0x04, 0x00, 0x20, 0x04, 0x00, 0x40, 0x04, 0x00, 0x10, 0x20, 0x96, 0x08, 0x20, 0x01, 0x40, 0x02, 0x04, 0x40, 0x20, 0x43, 0x01, 0x04, 0x01, 0x00, 0x20, 0x4f, 0x01, 0x04, 0x01, 0x00, 0x20, 0x52, 0x01, 0x04, 0x01, 0x00, 0x20, 0x52, 0x01, 0x04, 0x01, 0x00, 0x20, 0x45, 0x01, 0x04, 0x01, 0x00, 0x20, 0x43, 0x01, 0x04, 0x01, 0x00, 0x20, 0x54, 0x01, 0x04, 0x01, 0x00, 0x20, 0x21, 0x01, 0x04, 0x01, 0x00, 0x20, 0x20, 0x01, 0x04, 0x01, 0x00, 0x20, 0x59, 0x01, 0x04, 0x01, 0x00, 0x20, 0x6f, 0x01, 0x04, 0x01, 0x00, 0x20, 0x75, 0x01, 0x04, 0x01, 0x00, 0x20, 0x72, 0x01, 0x04, 0x01, 0x00, 0x20, 0x20, 0x01, 0x04, 0x01, 0x00, 0x20, 0x66, 0x01, 0x04, 0x01, 0x00, 0x20, 0x6c, 0x01, 0x04, 0x01, 0x00, 0x20, 0x61, 0x01, 0x04, 0x01, 0x00, 0x20, 0x67, 0x01, 0x04, 0x01, 0x00, 0x20, 0x3a, 0x01, 0x04, 0x01, 0x00, 0x20, 0x0a, 0x01, 0x04, 0x01, 0x00, 0x20, 0x14, 0x20, 0x20, 0x01, 0x10, 0x08, 0x01, 0x01, 0x20, 0x2f, 0x01, 0x20, 0x80, 0x20, 0x01, 0x01, 0x20, 0x20, 0x66, 0x01, 0x20, 0x81, 0x20, 0x01, 0x01, 0x20, 0x20, 0x6c, 0x01, 0x20, 0x82, 0x20, 0x01, 0x01, 0x20, 0x20, 0x61, 0x01, 0x20, 0x83, 0x20, 0x01, 0x01, 0x20, 0x20, 0x67, 0x01, 0x20, 0x84, 0x20, 0x01, 0x01, 0x20, 0x20, 0x00, 0x01, 0x20, 0x85, 0x20, 0x01, 0x01, 0x20, 0x20, 0x80, 0x10, 0x20, 0x00, 0x40, 0x08, 0x01, 0x02, 0x20, 0x00, 0x40, 0x02, 0x04, 0x40, 0x20, 0xff, 0x20, 0x20, 0x00, 0x10, 0x02, 0x01, 0x10, 0x08, 0x01, 0x10, 0x20, 0x00, 0x40, 0x02, 0x04, 0x40, 0x20, 0x00, 0x20, 0x02, 0x01, 0x20, 0x20, 0x01, 0x10, 0x08, 0x01, 0x01, 0x20, 0x00, 0x10, 0x08, 0x00, 0x20, 0x04, 0x10, 0x00, 0x04, 0x40, 0x00, 0x04, 0x20, 0x00, 0x20, 0x01, 0x40, 0x02, 0x04, 0x40, 0x20, 0x4b, 0x01, 0x04, 0x01, 0x00, 0x20, 0x45, 0x01, 0x04, 0x01, 0x00, 0x20, 0x59, 0x01, 0x04, 0x01, 0x00, 0x20, 0x3a, 0x01, 0x04, 0x01, 0x00, 0x20, 0x20, 0x01, 0x04, 0x01, 0x00, 0x20, 0x05, 0x20, 0x20, 0x01, 0x10, 0x08, 0x01, 0x01, 0x04, 0x00, 0x20, 0x04, 0x00, 0x40, 0x04, 0x00, 0x10, 0x04, 0x10, 0x00, 0x04, 0x40, 0x00, 0x04, 0x20, 0x00, 0x20, 0x30, 0x40, 0x20, 0x0b, 0x20, 0x20, 0x00, 0x10, 0x08, 0x01, 0x10, 0x04, 0x00, 0x20, 0x04, 0x00, 0x40, 0x04, 0x00, 0x10, 0x20, 0x02, 0x08, 0x20, 0x01, 0x40, 0x02, 0x04, 0x40, 0x20, 0x49, 0x01, 0x04, 0x01, 0x00, 0x20, 0x4e, 0x01, 0x04, 0x01, 0x00, 0x20, 0x43, 0x01, 0x04, 0x01, 0x00, 0x20, 0x4f, 0x01, 0x04, 0x01, 0x00, 0x20, 0x52, 0x01, 0x04, 0x01, 0x00, 0x20, 0x52, 0x01, 0x04, 0x01, 0x00, 0x20, 0x45, 0x01, 0x04, 0x01, 0x00, 0x20, 0x43, 0x01, 0x04, 0x01, 0x00, 0x20, 0x54, 0x01, 0x04, 0x01, 0x00, 0x20, 0x21, 0x01, 0x04, 0x01, 0x00, 0x20, 0x0a, 0x01, 0x04, 0x01, 0x00, 0x20, 0x0b, 0x20, 0x20, 0x01, 0x10, 0x08, 0x01, 0x01, 0x20, 0x01, 0x10, 0x08, 0x00, 0x20, 0x20, 0x30, 0x10, 0x20, 0x75, 0x40, 0x20, 0x09, 0x20, 0x20, 0x02, 0x01, 0x02, 0x08, 0x01, 0x04, 0x01, 0x00, 0x20, 0xa3, 0x08, 0x20, 0x00, 0x20, 0x10, 0x20, 0x01, 0x20, 0x09, 0x01, 0x80, 0x01, 0x04, 0x20, 0x79, 0x01, 0x80, 0x01, 0x03, 0x02, 0x20, 0x10, 0x02, 0x20, 0x40, 0x20, 0xff, 0x01, 0x02, 0x01, 0x10, 0x02, 0x01, 0x40, 0x04, 0x10, 0x00, 0x04, 0x40, 0x00, 0x40, 0x10, 0x10, 0x40, 0x40, 0x40, 0x10, 0x40, 0x10, 0x04, 0x00, 0x40, 0x04, 0x00, 0x10, 0x20, 0xb7, 0x01, 0x80, 0x01, 0x08, 0x20, 0xff, 0x01, 0x02, 0x01, 0x20, 0x20, 0x00, 0x01, 0x10, 0x01, 0x20, 0x20, 0xa5, 0x01, 0x80, 0x01, 0x08, 0x04, 0x20, 0x01, 0x04, 0x00, 0x08, 0x20, 0x8d, 0x01, 0x20, 0x73, 0x20, 0x01, 0x01, 0x20, 0x20, 0x23, 0x01, 0x20, 0x74, 0x20, 0x01, 0x01, 0x20, 0x20, 0x16, 0x01, 0x20, 0x75, 0x20, 0x01, 0x01, 0x20, 0x20, 0xd2, 0x01, 0x20, 0x76, 0x20, 0x01, 0x01, 0x20, 0x20, 0x77, 0x01, 0x20, 0x77, 0x20, 0x01, 0x01, 0x20, 0x20, 0x4f, 0x01, 0x20, 0x78, 0x20, 0x01, 0x01, 0x20, 0x20, 0x6a, 0x01, 0x20, 0x79, 0x20, 0x01, 0x01, 0x20, 0x20, 0x73, 0x01, 0x20, 0x7a, 0x20, 0x01, 0x01, 0x20, 0x20, 0x93, 0x01, 0x20, 0x7b, 0x20, 0x01, 0x01, 0x20, 0x20, 0x7f, 0x01, 0x20, 0x7c, 0x20, 0x01, 0x01, 0x20, 0x20, 0x79, 0x01, 0x20, 0x7d, 0x20, 0x01, 0x01, 0x20, 0x20, 0x59, 0x08 ]

# a = 0
# b = 0
# c = 0
# d = 0
# s = 0
# i = 1
# f = 0
#                a      b      c     d     s     i     f
# register = {0x10:0,0x40:0,0x20:0,0x1:0,0x4:0,0x8:1,0x2:0}
reverse_register = {0x10:'a',0x40:'b',0x20:'c',0x1:'d',0x4:'s',0x8:'i',0x2:'f',0x0:None}
op_code = {0x20:'IMM',0x02:'ADD',0x04:'STK',0x01:'STM',0x40:'LDM',0x10:'CMP',0x08:'SYS',0x80:'JMP'}


# class vm_memory:
#    def __init__(self,vm_mem_size: int) -> None:
#       self.vm_memory: List[int] = [0] * vm_mem_size 
#
#    def write_vm_memory(self,position: int,data: int) -> None:
#       self.vm_memory[position] = data
#
#    def read_vm_memory(self,position: int)->int:
#       return self.vm_memory[position]
#    
#    def read_entire_vm_memory(self) -> List[int]:
#       return self.vm_memory


print("""[+] Welcome to ./babyrev_level19.0!                                                   
[+] This challenge is an custom emulator. It emulates a completely custom             
[+] architecture that we call "Yan85"! You'll have to understand the                  
[+] emulator to understand the architecture, and you'll have to understand            
[+] the architecture to understand the code being emulated, and you will              
[+] have to understand that code to get the flag. Good luck!                          
[+]                                                                                   
[+] This level is a full Yan85 emulator. You'll have to reason about yancode,         
[+] and the implications of how the emulator interprets it!                           
[+] Starting interpreter loop! Good luck!""")
class vm_register:
   def __init__(self,a: int,b: int,c: int,d: int,s: int,i: int,f: int):
      self.a_hex = a
      self.b_hex = b
      self.c_hex = c
      self.d_hex = d
      self.s_hex = s
      self.i_hex = i
      self.f_hex = f
      self.register: dict[int,int]= {self.a_hex:0,self.b_hex:0,self.c_hex: 0, self.d_hex: 0, self.s_hex: 0, self.i_hex: 1,self.f_hex: 0}
      self.reverse_register = {self.a_hex: "a",self.b_hex: "b",self.c_hex: "c",self.d_hex: "d",self.s_hex: "s",self.i_hex: "i",self.f_hex:"f",0x0:None}
   
   def write_register(self,register: int,value: int) -> None:
      self.register[register] = value
      return

   def read_register(self,register: int) -> int:
      reg_value = self.register[register]
      return reg_value

class vm_stack:
   def  __init__(self,register: vm_register,size: int):
      self.stack: list[int] = [0] * size
      self.register = register

   def push_stack(self,register:int) -> None:
      self.stack.append(register)

   def pop_stack(self,register:int) -> None:
      self.register.write_register(register,self.stack.pop())
   
   def write_vm_stack(self,position: int,data: int) -> None:
      self.stack[position] = data

   def read_vm_stack(self,position: int)->int:
      return self.stack[position]

   def read_stack_len(self,amount: int) -> list[int]:
      len_stack = len(self.stack)
      return self.stack[len_stack - amount:len_stack]
   def read_entire_virtual_stack(self) -> list [int]:
      return self.stack

class disassemble_yan_85:
   """
   Get all the hex code for yan_85 instructions for that respective binary
   """
   def __init__(self,imm: int,add: int,stk: int,stm: int,ldm: int,cmp: int,jmp: int,sys :int,byte_code: list[int],registers: vm_register,virtual_memory: vm_stack):
      self.instructions = {"IMM":imm,"ADD":add,"STK":stk,"STM":stm,"LDM":ldm,"CMP":cmp,"JMP":jmp,"SYS":sys}
      self.byte_code = byte_code
      self.register = registers
      # self.vm_mem = virtual_memory
      self.vm_stack = virtual_memory

   def translate(self) -> None:
      #while True
      for _ in range(205):
         three_bytes = self.byte_code[self.register.register[self.register.i_hex]*3-3:self.register.register[self.register.i_hex]*3]
         three_translated = []
         for i in range(len(three_bytes)):
            match i:
               case 0:
                  current = list(self.instructions.keys())[list(self.instructions.values()).index(three_bytes[i])]
               case 1: 
                  current = hex(three_bytes[i])
               case 2:
                  current = hex(three_bytes[i])
            three_translated.append(current)
         tmp = three_translated[1]
         three_translated[1] = three_translated[2]
         three_translated[2] = tmp

         print(f"[V] a:{hex(self.register.register[self.register.a_hex])} b:{hex(self.register.register[self.register.b_hex])} c:{hex(self.register.register[self.register.c_hex])} d:{hex(self.register.register[self.register.d_hex])} s:{hex(self.register.register[self.register.s_hex])} i:{hex(self.register.register[self.register.i_hex])} f:{hex(self.register.register[self.register.f_hex])}")
         print(f"[I] op:{hex(three_bytes[0])} arg1:{hex(three_bytes[2])} arg2:{hex(three_bytes[1])}")

         match three_translated[0]:
            case "IMM":
               self.register.write_register(three_bytes[2],three_bytes[1])
               print(f"[s] {three_translated[0]} {self.register.reverse_register.get(three_bytes[2])} = {three_translated[2]}")
            case "ADD":
               add_res = self.register.register[three_bytes[2]] + self.register.register[three_bytes[1]]
               if add_res > 0xFF:
                  add_res = add_res & 0xff
               self.register.write_register(three_bytes[2],add_res)
               print(f"[s] {three_translated[0]} {self.register.reverse_register.get(three_bytes[2])} {self.register.reverse_register[three_bytes[1]]}")
            case "STK":
               print(f"[s] {three_translated[0]} {self.register.reverse_register.get(three_bytes[2])} {self.register.reverse_register.get(three_bytes[1])}")
               current_stack_val = self.register.read_register(0x4)
               if three_bytes[1] != 0x0:
                  reg_value = self.register.register[three_bytes[1]]
                  self.vm_stack.push_stack(reg_value)
                  print(f"[s] ... pushing {self.register.reverse_register[three_bytes[1]]}")
                  current_stack_val += 1
                  self.register.write_register(0x4,current_stack_val)
               if three_bytes[2] != 0x0:
                  reg_value = self.register.register[three_bytes[2]]
                  self.vm_stack.pop_stack(three_bytes[2])
                  print(f"[s] ... popping {self.register.reverse_register[three_bytes[2]]}")
                  current_stack_val -= 1
                  self.register.write_register(0x4,current_stack_val)
            case "STM":
               print(f"[s] {three_translated[0]} *{self.register.reverse_register[three_bytes[2]]} = {self.register.reverse_register[three_bytes[1]]}")
               self.vm_stack.write_vm_stack(self.register.register[three_bytes[2]],self.register.register[three_bytes[1]])
               # print(f"[s] current memory layout: {self.vm_mem.read_entire_vm_memory()}")
            case "LDM":
               print(f"[s] {three_translated[0]} {self.register.reverse_register[three_bytes[2]]} = *{self.register.reverse_register[three_bytes[1]]}")
               val_in_reg = self.register.read_register(three_bytes[1])
               self.register.write_register(three_bytes[2],self.vm_stack.read_vm_stack(val_in_reg))
            case "JMP":
               flags = three_bytes[2] 
               flag_description = ""
               current_f = self.register.read_register(0x2)
               if (flags & 1) != 0:
                  flag_description += "L"
               if flags & 2 != 0:
                  flag_description += "G"
               if flags & 4 != 0:
                  flag_description += "E"
               if flags & 8 != 0:
                  flag_description += "N"
               if flags & 0x10 != 0:
                  flag_description += "Z"
               if flags & 0x10 != 0:
                  flag_description += "*"
         
               print(f"[j] {three_translated[0]} {flag_description}  {self.register.reverse_register[three_bytes[1]]}")
               if flag_description == 0 or three_bytes[2] & current_f != 0:
                  print(f"[j] ... TAKEN")
                  register_val_to_jump_to = self.register.read_register(three_bytes[1])
                  self.register.write_register(0x8,register_val_to_jump_to)
               else:
                  print("[j] ... NOT TAKEN")
            case "SYS":
               print(f"[s] SYS {hex(three_bytes[2])} {self.register.reverse_register[three_bytes[1]]}")
               if three_bytes[2] & 0x2 != 0:
                  print(f"[s] ... open")
               if three_bytes[2] & 0x4 != 0:
                  print(f"[s] ... read_code")
               if three_bytes[2] & 0x10 != 0:
                  print(f"[s] ... read_memory")
                  user_input = input("")
                  len_input = len(user_input)
                  user_input = list(user_input)
                  write_address = self.register.read_register(self.register.b_hex)
                  for position in range(len_input):
                     self.vm_stack.write_vm_stack(write_address+position,ord(user_input[position]))
                  print(f"[s] ... return value (in register {self.register.reverse_register[three_bytes[1]]}): {len_input+1}")
                  self.register.write_register(three_bytes[1],len_input+1)
               if three_bytes[2] & 0x1 != 0:
                  print(f"[s] ... write")
                  txt_to_be_printed = self.vm_stack.read_stack_len(self.register.read_register(0x20))
                  txt_to_be_printed = [chr(k) for k in txt_to_be_printed]
                  txt_to_be_printed = "".join(txt_to_be_printed)
                  print(txt_to_be_printed,end="")
                  print(f"[s] ... return value (in register {self.register.reverse_register[three_bytes[1]]}): {self.register.read_register(0x20)}")
                  self.register.write_register(three_bytes[1],self.register.read_register(0x20))
               if three_bytes[2] & 0x8 != 0:
                  print(f"[s] ... sleep")
               if three_bytes[2] & 0x20 != 0:
                  print(f"[s] ... exit")
                  exit(1)
            case "CMP":
               print(f"[s] CMP {self.register.reverse_register[three_bytes[2]]} {self.register.reverse_register[three_bytes[1]]}")
               print(f"[s] resetting the f register to 0")
               self.register.write_register(0x2,0)
               f_new = self.register.read_register(0x2)
               if three_bytes[2] > three_bytes[1]:
                  f_new = f_new | 1
               if three_bytes[1] > three_bytes[2]:
                  f_new = f_new | 2
               if three_bytes[2] == three_bytes[1]:
                  f_new = f_new | 4
               else:
                  f_new = f_new | 8
               if three_bytes[1] == 0 and three_bytes[2] == 0:
                  f_new = f_new | 10
               self.register.write_register(0x2,f_new)




         self.register.register[self.register.i_hex] += 1


reg_class = vm_register(0x10,0x40,0x20,0x1,0x4,0x8,0x2)
# virutal_mem = vm_memory(1000)
virutal_stack = vm_stack(reg_class,1000)
yan_85_dis = disassemble_yan_85(0x20,0x02,0x04,0x01,0x40,0x10,0x80,0x8,vm_code,reg_class,virutal_stack)

yan_85_dis.translate()

#Todo: figure out read_memory syscall
