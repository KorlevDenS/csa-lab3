import tempfile

import machine
import translator


def main():
    with tempfile.TemporaryDirectory() as tmpdirname:
        # получаем код на нашем языке из файла
        source = "examples/cat.asm"
        # получаем ссылку на файл с машинным кодом
        target = "examples/machine_code.txt"
        input_stream = "examples/input.txt"
        # транслируем код в машинный и записываем в файл
        args = [source, target]
        translator.main(args)

        with open(source, 'r') as file:
            for line in file:
                print(line, end='')
        print()

        with open(target, 'r') as file:
            for line in file:
                print(line, end='')
        print()
        args = [target, input_stream]
        machine.main(args)
        return 0


if __name__ == "__main__":
    main()
