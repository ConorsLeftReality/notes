; ================================================
; TOP LEFT
; ================================================

; Initialise registers
mov al, c0
mov bl, 48

; Print first H
mov [al], bl

; Inc and assign new value to BL
inc al
mov bl, 65

; Print e
mov [al], bl

; Inc and assign new value to BL
inc al
mov bl, 6c

; Print 2* l
mov [al], bl
inc al
mov [al], bl

; Inc and assign new value to BL
inc al
mov bl, 6f

; Print o
mov [al],bl

; ================================================
; BOTTOM RIGHT
; ================================================

; Initialise registers
mov al, fb
mov bl, 48

; Print first H
mov [al], bl

; Inc and assign new value to BL
inc al
mov bl, 65

; Print e
mov [al], bl

; Inc and assign new value to BL
inc al
mov bl, 6c

; Print 2* l
mov [al], bl
inc al
mov [al], bl

; Inc and assign new value to BL
inc al
mov bl, 6f

; Print o
mov [al],bl

END
