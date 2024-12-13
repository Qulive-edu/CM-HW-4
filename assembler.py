import csv
import argparse


def parse_command(line):
    """Разбирает текстовую строку команды УВМ."""
    parts = line.strip().split()
    opcode = int(parts[0])  # A
    b = int(parts[1])  # B
    c = int(parts[2])  # C (или смещение, если C в другой интерпретации)
    d = int(parts[3]) if len(parts) > 3 else 0  # D (не всегда используется)
    if opcode in {2, 5, 18}:
        return [opcode, 
                (b >> 16) & 0xFF, (b >> 8) & 0xFF, b & 0xFF, 
                (c >> 16) & 0xFF, (c >> 8) & 0xFF, c & 0xFF, 
                0x00, 0x00]
    elif opcode == 13:
        return [opcode, 
                (b >> 16) & 0xFF, (b >> 8) & 0xFF, b & 0xFF, 
                c & 0xFF, 
                (d >> 16) & 0xFF, (d >> 8) & 0xFF, d & 0xFF, 0x00]
    else:
        raise ValueError("Unknown opcode.")

def assemble(input_file, output_file, log_file):
    """Ассемблирует текстовый файл в бинарный."""
    with open(input_file, 'r') as inp, open(output_file, 'wb') as out, open(log_file, 'w', newline='') as log:
        writer = csv.writer(log)
        writer.writerow(["A", "B", "C", "D"])
        for line in inp:
            binary_command = parse_command(line)
            out.write(bytes(binary_command))
            writer.writerow([binary_command[0], 
                             (binary_command[1] << 16) + (binary_command[2] << 8) + binary_command[3], 
                             (binary_command[4] << 16) + (binary_command[5] << 8) + binary_command[6], 
                             (binary_command[7] << 16) + (binary_command[8] << 8)])

def main():
    parser = argparse.ArgumentParser(description="Ассемблер для учебной виртуальной машины.")
    parser.add_argument("input_file", help="Путь к текстовому файлу исходного кода.")
    parser.add_argument("output_file", help="Путь к бинарному файлу для записи.")
    parser.add_argument("log_file", help="Путь к файлу лога в формате CSV.")
    
    args = parser.parse_args()
    
    assemble(args.input_file, args.output_file, args.log_file)

if __name__ == "__main__":
    main()
    
    