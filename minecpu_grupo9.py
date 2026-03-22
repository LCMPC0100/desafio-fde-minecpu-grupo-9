class MiniCPU:
    def __init__(self):
        self.mem = [0] * 256
        self.reg = [0, 0, 0, 0]  # R0-R3
        self.pc = 0
        self.zf = 0
        self.running = True
        self.ciclo = 0
        
    def fetch(self):
        op = self.mem[self.pc]
        a = self.mem[self.pc + 1]
        b = self.mem[self.pc + 2]
        self.pc += 3
        return op, a, b
    
    def reg_ok(self, r):
        return 0 <= r < len(self.reg)
    
    def decode_execute(self, op, a, b):

        if op == 0x01:  # LOAD
            if self.reg_ok(a):
                self.reg[a] = self.mem[b]

        elif op == 0x02:  # STORE
            if self.reg_ok(a):
                self.mem[b] = self.reg[a]

        elif op == 0x03:  # ADD
            if self.reg_ok(a) and self.reg_ok(b):
                self.reg[a] = (self.reg[a] + self.reg[b]) & 0xFF

        elif op == 0x04:  # SUB
            if self.reg_ok(a) and self.reg_ok(b):
                self.reg[a] = (self.reg[a] - self.reg[b]) & 0xFF

        elif op == 0x05:  # MOV
            if self.reg_ok(a):
                self.reg[a] = b

        elif op == 0x06:  # CMP
            if self.reg_ok(a) and self.reg_ok(b):
                self.zf = 1 if self.reg[a] == self.reg[b] else 0

        elif op == 0x07:  # JMP
            self.pc = a

        elif op == 0x08:  # JZ
            if self.zf:
                self.pc = a

        elif op == 0x09:  # JNZ
            if not self.zf:
                self.pc = a

        elif op == 0x0A:  # HALT
            self.running = False
            
    def trace(self, op, a, b):
        nomes = {
            1:'LOAD',2:'STORE',3:'ADD',4:'SUB',
            5:'MOV',6:'CMP',7:'JMP',8:'JZ',9:'JNZ',10:'HALT'
        }

        nome = nomes.get(op, '???')
        print(f'Ciclo {self.ciclo}: {nome:5s} {a},{b} |'
              f' R0={self.reg[0]:3d} R1={self.reg[1]:3d}'
              f' R2={self.reg[2]:3d} R3={self.reg[3]:3d}'
              f' | PC={self.pc:3d} ZF={self.zf}')

    def run(self):
        while self.running and self.pc < 256:
            self.ciclo += 1
            op, a, b = self.fetch()
            self.decode_execute(op, a, b)
            self.trace(op, a, b)


cpu = MiniCPU()

# -----------------------------
# Programa
# -----------------------------

program = [

0x05,0,0,
0x01,2,0x30,
0x05,3,1,

# 10
0x01,1,0x10,
0x04,1,2,
0x06,1,0,
0x08,24,0,
0x03,0,3,

# 25
0x01,1,0x11,
0x04,1,2,
0x06,1,0,
0x08,39,0,
0x03,0,3,

# 5
0x01,1,0x12,
0x04,1,2,
0x06,1,0,
0x08,54,0,
0x03,0,3,

# 30
0x01,1,0x13,
0x04,1,2,
0x06,1,0,
0x08,69,0,
0x03,0,3,

# 15
0x01,1,0x14,
0x04,1,2,
0x06,1,0,
0x08,84,0,
0x03,0,3,

# 40
0x01,1,0x15,
0x04,1,2,
0x06,1,0,
0x08,99,0,
0x03,0,3,

# 8
0x01,1,0x16,
0x04,1,2,
0x06,1,0,
0x08,114,0,
0x03,0,3,

# 22
0x01,1,0x17,
0x04,1,2,
0x06,1,0,
0x08,129,0,
0x03,0,3,

0x02,0,0x20,
0x0A,0,0
]

for i in range(len(program)):
    cpu.mem[i] = program[i]

# -----------------------------
# Dados
# -----------------------------

cpu.mem[0x30] = 20

valores = [10,25,5,30,15,40,8,22]

for i in range(len(valores)):
    cpu.mem[0x10+i] = valores[i]

# -----------------------------
# Executar
# -----------------------------

cpu.run()

print("\nResultado final em 0x20 =", cpu.mem[0x20])