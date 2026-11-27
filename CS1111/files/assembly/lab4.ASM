; god help us

; ==========================================================================
; MAIN CODE
; ==========================================================================

        ; Read in first 2 digit number, then move result from AL to BL
        CALL    30
        PUSH    AL
        POP     BL

        ; Read in second 2 digit number, then move result from AL to CL
        CALL    30
        PUSH    AL
        POP     CL

        ; Read a valid operator, then let subroutine 80 call the calculation
        CALL    80

        ; Display answer in VDU
        CALL    50
        HALT

; ==========================================================================
; Subroutine for reading a two-digit number from the keyboard into AL
; ==========================================================================
        ORG     30

        IN      00              ; Keyboard input (tens digit)
        SUB     AL,30           ; Change ASCII to real number value
        MUL     AL,0A           ; Times 10
        PUSH    AL
        POP     DL              ; DL = tens value
        IN      00              ; Keyboard input (units digit)
        SUB     AL,30           ; Change ASCII to real number value
        ADD     AL,DL           ; AL = total number
        RET

; ==========================================================================
; Subroutine to write the two-digit number in BL to the VDU at C0 and C1
; ==========================================================================
        ORG     50

        ; First digit
        PUSH    BL
        POP     AL
        DIV     AL,0A
        ADD     AL,30
        MOV     [C0],AL

        ; Second digit
        PUSH    BL
        POP     AL
        MOD     AL,0A
        ADD     AL,30
        MOV     [C1],AL
        RET

; ==========================================================================
; Subroutines to add, subtract, multiply and divide BL and CL,
; leaving the result in BL
; ==========================================================================

        ; Addition
        ORG     70
        ADD     BL,CL
        RET

        ; Subtraction
        ORG     74
        SUB     BL,CL
        RET

        ; Multiplication
        ORG     78
        MUL     BL,CL
        RET

        ; Division
        ORG     7C
        DIV     BL,CL
        RET

; ==========================================================================
; Read an operator and call the matching calculation subroutine
; ==========================================================================
        ORG     80

GetOp:
        IN      00
        CMP     AL,2A           ; *
        JZ      DoMul
        CMP     AL,2B           ; +
        JZ      DoAdd
        CMP     AL,2D           ; -
        JZ      DoSub
        CMP     AL,2F           ; /
        JZ      DoDiv
        JMP     GetOp           ; Invalid key, try again

DoAdd:
        CALL    70
        RET
DoSub:
        CALL    74
        RET
DoMul:
        CALL    78
        RET
DoDiv:
        CALL    7C
        RET

        END