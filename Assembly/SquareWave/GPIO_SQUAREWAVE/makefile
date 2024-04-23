OBJS = Linux_asm_squarewave.o
ifdef DEBUG
DEBUGFLGS = -g
else
DEBUGFLGS =
endif

%.o : %.s
	as $(DEBUGFLGS) $< -o $@
GPIO_OFF: $(OBJS)
	gcc -o SquareWave $(OBJS)

clean:
	rm *.o SquareWave
