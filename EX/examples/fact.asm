section data:
result: 0
a: 15
b: 3
section text:
    _start:
        lw r1, a
        lw r2, b
        div r3, r1, 3
        out r3, 1
        halt