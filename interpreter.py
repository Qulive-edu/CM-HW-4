import csv
import argparse
import math

class UVM:
    def __init__(self, memory_size=1024):
        self.memory = [0] * memory_size

    def load_constant(self, b, c):
        self.memory[b] = c

    def read_memory(self, b, c):
        self.memory[b] = self.memory[c]

    def write_memory(self, b, c, d):
        addr = self.memory[b] + c
        self.memory[addr] = self.memory[d]

    def sqrt_operation(self, b, c):
        self.memory[b] = int(math.sqrt(self.memory[c]))

    def execute(self, binary_file, result_file, memory_range):
        with open(binary_file, 'rb') as bf:
            while command := bf.read(9):
                a, b, c = command[0], (command[1] << 16) + (command[2] << 8) + command[3], \
                          (command[4] << 16) + (command[5] << 8) + command[6]
                if a == 2:
                    self.load_constant(b, c)
                elif a == 5:
                    self.read_memory(b, c)
                elif a == 13:
                    d = (command[7] << 16) + (command[8] << 8) + command[9]
                    self.write_memory(b, c, d)
                elif a == 18:
                    self.sqrt_operation(b, c)
        
        # Сохранение диапазона памяти в CSV
        with open(result_file, 'w', newline='') as rf:
            writer = csv.writer(rf)
            writer.writerow(["Address", "Value"])
            for i in range(*memory_range):
                writer.writerow([i, self.memory[i]])

def main():
    parser = argparse.ArgumentParser(description="Интерпретатор для учебной виртуальной машины.")
    parser.add_argument("binary_file", help="Путь к бинарному файлу для интерпретации.")
    parser.add_argument("result_file", help="Путь к файлу для сохранения результата в формате CSV.")
    parser.add_argument("memory_start", type=int, help="Начальный адрес диапазона памяти для записи результата.")
    parser.add_argument("memory_end", type=int, help="Конечный адрес диапазона памяти для записи результата.")
    
    args = parser.parse_args()
    
    uvm = UVM()
    uvm.execute(args.binary_file, args.result_file, (args.memory_start, args.memory_end))

if __name__ == "__main__":
    main()