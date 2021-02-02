#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <time.h>

/*
 * 	Matrix-Matrix Multiplication MPI Parallel
 *	Algorithm 2
 *
 *	Because algorithm 2 will only work when n divisible by p,
 *	given p should be 4, 9, 16, 25, 36, 64,
 *	and n is 100, 200, 300, ..., 1000,
 *	when p is the following, do for the following n:
 *	p=4: 100~1000
 *	p=9: 900
 *	p=16: 400, 800
 *	p=25: 100~1000
 *	p=36: 900
 *	p=64: none
 */

// Global Default Matrix Size and Debug Variable
#define MATRIXSIZE 4
#define DEBUG 0

int main(int argc, char **argv) {

  // Communicator Size and Process Rank
	int comm_sz, my_rank;

  // If size of matrix is an argument, change matrix size
	int n = MATRIXSIZE;
	if (argc > 1) n = strtol(argv[1], NULL, 10);

  // Declare both matrices and partitions and result matrix
	int matrix[n][n];
	int vector[n];
	int partitionA[n];
	int partitionB[n];
	int partitionC[n];
	int matrix_out[n];

  // Declare start, finish, and final times
	double start_time, finish_time, final_time;

	// Create random integers in matrices (0-9)
	srand(time(NULL));
	int num;
	for (int i = 0; i < n; i++) {
		num = (rand() % 10)
		vector[i] = num;
		for (int j = 0; j < n; j++) {
			num = (rand() % 10);
			matrix[i][j] = num;
		}
	}

  // Initialize MPI Parallel and get commicator size and process rank
	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &comm_sz);
	MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);

  // Declare request and status values to control processes in parallel
	MPI_Request request;
	MPI_Status status;

	// Exit if n is not divisble by # processes
	if (n%comm_sz != 0) {
		if (my_rank == 0) printf("Matrix size %d not divisible by process count %d\n\n", n, comm_sz);
		MPI_Finalize();
		return 0;
	}

  // Start Parallel calculations
	start_time = MPI_Wtime();

  // Partition Matrices A and B
	if (my_rank == 0) {
		// change matrix into one-dimension array by row
		for (int row = 0; row < n; row++) {
			for (int col = 0; col < n; col++) {
				partitionA[(row*n)+col] = matrixA[row][col];
			}
		}

	}

	if (DEBUG && my_rank==0) printf("Begin scattering\n");

	// Broadcast vector to every process
	//broadcast vector to all processes
   	 MPI_Bcast(&vector, n, MPI_INT, 0, MPI_COMM_WORLD);
	
	// MPI_Scatter to send n/p blocks of elements of matrices to all processes
	// Scatter will work because we're working under the assumption n divisible by p
	// e.g., p=4, n=100; each process will have a block of 25 elements
	int localCalcA[n*n/comm_sz];
	MPI_Scatter(&partitionA, n*n/comm_sz, MPI_INT, &localCalcA, n*n/comm_sz, MPI_INT, 0, MPI_COMM_WORLD);

  // Each process will contain an element of C
	int localCalcC[n/comm_sz];
	int j = my_rank;
	int sum = 0;

	// all processes do their respective calculations
	for (int iter = 0; iter < comm_sz; iter++) {
		int ret = 0;
		for (int i = 0; i < n/comm_sz; i++) {	// how many rows per process
			ret += localCalcA[i]*b[i];
		}
	}

    // If last process, send to master, else, send to next process in array
	if (j == comm_sz-1) j = 0;
	else j++;

	if (DEBUG && my_rank==0) printf("Finished iter %d\n", iter+1);

	// process my_rank sends their set of rows to process my_rank+1
	MPI_Isend(&localCalcA, n*n/comm_sz, MPI_INT, (my_rank==0 ? comm_sz-1 : my_rank-1), 0, MPI_COMM_WORLD, &request);
	MPI_Irecv(&localCalcA, n*n/comm_sz, MPI_INT, (my_rank==comm_sz-1 ? 0 : my_rank+1), 0, MPI_COMM_WORLD, &request);
	MPI_Wait(&request, &status);
	if (DEBUG && my_rank==0) printf("Finished ring pass\n");
}

	if (DEBUG && my_rank==0) printf("Completed scatter and calculations\n");

	// Process 0 MPI_Gather into result matrix
	MPI_Gather(&localCalcC, n*n/comm_sz, MPI_INT, &partitionC, n*n/comm_sz, MPI_INT, 0, MPI_COMM_WORLD);

  // Gather Partitions
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			matrixC[j][i] = partitionC[(i*n)+j];
		}
	}

  // Set finish time
	finish_time = MPI_Wtime();

	if (DEBUG && my_rank==0) printf("Finished matrix.\n");

	if (my_rank == 0) {
		// validation
		if (n < 8) { // only print out for validation if matrix size is reasonable (n<8)
			for (int i = 0; i < n; i++) {
				for (int j = 0; j < n; j++) {
					printf("%2d", matrixA[i][j]);
				}
				printf("   ");
				for (int j = 0; j < n; j++) {
					printf("%2d", matrixB[i][j]);
				}
				printf("   ");
				for (int j = 0; j < n; j++) {
					printf("%4d", matrixC[i][j]);
				}
				printf("\n");
			}
			printf("\n");
		}
		
		// Print Time
		final_time = finish_time - start_time;
		printf("Processes: %2d \t Matrix Size: %4d \t Final Time: %f\n\n", comm_sz, n*n, final_time);
	}

  // End All Processes
	MPI_Finalize();

	return 0;
 }
