.section .data

.equ GPIO_BASE, 0x3F200000    @ Base address of GPIO registers
.equ PWM_OFFSET, 0x0020C000   @ Offset for PWM peripheral

.equ PWM_CTL, 0               @ PWM Control register offset
.equ PWM_RNG1, 4              @ PWM Range register offset
.equ PWM_DAT1, 8              @ PWM Data register offset

.equ GPIO_FSEL1, 0x04         @ GPIO Function Select 1
.equ GPIO_SET0, 0x1C          @ GPIO Pin Output Set 0
.equ GPIO_CLR0, 0x28          @ GPIO Pin Output Clear 0

.equ PWM_CLK_DIV, 0x5A         @ PWM Clock Divider register offset
.equ PWM_MS_MODE, 0x80        @ PWM Clock Manager Mode register offset

.equ CLK_CTL_PASSWD, 0x5A000000   @ Clock Control Password
.equ CLK_CTL_DIVI, 0x00000100     @ Clock Divisor integer part
.equ CLK_CTL_DIVF, 0x0000000F     @ Clock Divisor fractional part

.section .bss

.comm pwm_regs, 20            @ Space for PWM registers

.section .text
.globl _start

_start:
    @ Map PWM peripheral
    ldr r0, =GPIO_BASE
    ldr r1, =pwm_regs
    add r0, r0, #PWM_OFFSET
    str r0, [r1]

    @ Set GPIO pin 18 as PWM output
    ldr r2, =GPIO_FSEL1
    ldr r3, =pwm_regs
    ldr r4, [r3]
    mov r5, #0x02    @ GPIO pin 18 is in the second nibble
    lsl r5, r5, #6   @ Shift 6 bits for pin 18
    str r5, [r4, r2]

    @ Setup PWM clock
    ldr r0, =pwm_regs
    ldr r1, [r0]
    mov r2, #0x5A000000  @ Password to allow writing to clock register
    orr r1, r1, r2
    str r1, [r0]

    @ Wait for PWM clock to stabilize
    mov r3, #0x5A000000
    mov r4, #0x11
    wait_clk_stable:
        ldr r0, =pwm_regs
        ldr r1, [r0]
        and r1, r1, r3
        cmp r1, r4
        bne wait_clk_stable

    @ Set PWM range
    ldr r0, =PWM_RNG1
    ldr r1, =pwm_regs
    ldr r2, [r1]
    mov r3, #1000  @ Set PWM range to 1000 cycles
    str r3, [r2, r0]

    @ Start PWM
    ldr r0, =PWM_CTL
    ldr r1, =pwm_regs
    ldr r2, [r1]
    mov r3, #1       @ Enable PWM channel 1
    lsl r3, r3, #8
    str r3, [r2, r0]

loop:
    @ Generate square wave by alternating between high and low
    ldr r0, =PWM_DAT1
    ldr r1, =pwm_regs
    ldr r2, [r1]
    mov r3, #500    @ Set duty cycle to 50%
    str r3, [r2, r0]
    mov r3, #10000  @ Delay for a short time (adjust as needed for frequency)
delay_loop:
    subs r3, r3, #1
    bne delay_loop

    @ Invert PWM output
    mov r3, #0      @ Set duty cycle to 0%
    str r3, [r2, r0]
    mov r3, #10000  @ Delay for a short time (adjust as needed for frequency)
delay_loop2:
    subs r3, r3, #1
    bne delay_loop2

    b loop

    @ End program
    mov r7, #1
    swi #0
