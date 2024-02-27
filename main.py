import os
import tempfile

import machine
import translator_asm


def main():
    with tempfile.TemporaryDirectory() as tmpdirname:
        # получаем код на нашем языке из файла
        source = "examples/hello.asm"
        # получаем ссылку на файл с машинным кодом
        target = os.path.join(tmpdirname, "machine_code.out")
        input_stream = "examples/input.txt"
        # транслируем код в машинный и записываем в файл
        translator_asm.main(source, target)
        with open(source, 'r') as file:
            for line in file:
                print(line, end='')
        print()

        with open(target, 'r') as file:
            for line in file:
                print(line, end='')
        print()

        # machine.main(target, input_stream)
        return 0


if __name__ == "__main__":
    main()
