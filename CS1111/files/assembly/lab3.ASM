; Read two 2-digit numbers from the keyboard, add them,
; and show the sum on the VDU at C0-C1. Then repeat.

Start:
; First Number to BL
; ============================
IN   00         ; take input from keyboard (00), ASCII code goes into AL
SUB  AL,30      ; change ASCII number value to real number value
MUL  AL,0A      ; times 10 (tens digit)
PUSH AL         ; copy AL to BL via the stack
POP  BL         ; BL = tens digit * 10
IN   00         ; units digit
SUB  AL,30
ADD  BL,AL      ; BL = first number

; Second Number to CL
; ============================
IN   00         ; tens digit
SUB  AL,30
MUL  AL,0A
PUSH AL         ; copy AL to CL via the stack
POP  CL
IN   00         ; units digit
SUB  AL,30
ADD  CL,AL      ; CL = second number

; Add together
; ============================
ADD  BL,CL      ; BL = total

; First digit to VDU
; ============================
PUSH BL         ; copy BL to AL via the stack (BL keeps the total)
POP  AL
DIV  AL,0A      ; AL = total / 10 = tens digit
ADD  AL,30      ; convert to ASCII for the VDU
MOV  [C0],AL    ; write tens digit to C0

; Second digit to VDU
; ============================
PUSH BL         ; copy BL to AL again
POP  AL
MOD  AL,0A      ; AL = total mod 10 = units digit
ADD  AL,30      ; convert to ASCII for the VDU
MOV  [C1],AL    ; write units digit to C1

JMP  Start      ; loop back for the next two numbers
END