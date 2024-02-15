@ Deliverable: Describe what .req is used for.  How is this different than .equ?
@ Deliverable: Add the classinclude.s include file with changes to last two lines.

.include "classinclude.s"

val1	.req r1
val2	.req r2
sum	.req r0
	.text
	.global _start
_start:	MOV	val1, #0x25
	MOV	val2, #0x34
	ADD	sum, val1, val2
	MOV 	R7, #sys_exit
        SWI	#sys_restart_syscall
