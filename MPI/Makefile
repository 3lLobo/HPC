EXECUTABLES= vector-matrix vm-omp test test2

EXPENSIVE_JUNK += $(EXECUTABLES)

SRC = vector-matrix.c vm-omp.c test.c test2.c

JUNK +=

CFLAGS += -O3 -Wall -W --std=c11 -lm
CXXFLAGS += -O3 -Wall -W --std=c++11 -lm -Wno-cast-function-type
OMP_CFLAGS = $(CFLAGS) -fopenmp
MPI_CFLAGS = $(CXXFLAGS) -lmpi

help:
	@echo "help\tShow this help text"
	@echo "all\tMake all executables"
	@echo "clean\tThrow away all files that are easy to produce again"
	@echo "empty\tThrow away all files that can be produced again"

all: $(EXECUTABLES)

clean:
	rm -rf $(JUNK)

empty:
	rm -rf $(JUNK) $(EXPENSIVE_JUNK)

test2: test2.c
	mpiCC $(MPI_CFLAGS) -o test2 test2.c

test: test.c
	mpiCC $(MPI_CFLAGS) -o test test.c

vm-omp: vm-omp.c
	$(CC) $(OMP_CFLAGS) -o vm-omp vm-omp.c

vector-matrix: vector-matrix.c
	mpiCC $(MPI_CFLAGS) -o vector-matrix vector-matrix.c


