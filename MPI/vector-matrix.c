#define N 16000
#include <stdio.h>
#include <math.h>
#include <sys/time.h>
#include <stdlib.h>
#include <stddef.h>
#include "mpi.h"


void print_vector(char *prompt, int a[N]);
void print_matrix(char *prompt, int a[N][N]);


int main(int argc, char *argv[])
{
    int i, rank, size, sum=0;
    int vector[N];
    int matrix[N][N];
    int result[N];
    int *chunk;
    double start, end, final;

    //Initialize simple vectors
    for(int k=0; k < N; k++){
	vector[k] = k+1;
	for (int r=0; r < N; r++){
	    if (r == (N-1)) {matrix[k][r] = r+k;}
	    else { matrix[k][r] = 1; } 
	}
    }

    //Initialize MPI parallel, get comm size and process rank
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);


    // Determine size of processes
    int local = (int)ceil((double)(N/size));

    //Allocate memory for distributed vector
    chunk = (int*)malloc(N*local*sizeof(int));

    //scatter rows matrix to different processes     
    MPI_Scatter(&matrix, N*local, MPI_INT, chunk, N*local, MPI_INT, 0, MPI_COMM_WORLD);

    //broadcast vector to all processes
    MPI_Bcast(&vector, N, MPI_INT, 0, MPI_COMM_WORLD);

    // Time calculations
    start = MPI_Wtime();

    MPI_Barrier(MPI_COMM_WORLD);

    //perform vector multiplication by all processes
     int cc[local];
     for (i=0; i<local; i++) { 
     sum = 0;
         for (int j=0; j<N; j++){ 
        	sum += vector[j]*chunk[j+(i*N)];
	} cc[i] = sum;
     }  

    MPI_Gather(&cc, local, MPI_INT, result, local, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Barrier(MPI_COMM_WORLD);

    end = MPI_Wtime();
    MPI_Finalize();
    if (rank == 0){
	final = end - start;
        printf("Processes: %2d \t Matrix size: %4d \t Time Elapsed: %f\n\n", size, N, final);
//        print_vector("Initial vector = ", vector);
//	print_matrix("Initial Matrix = ", matrix);
//	print_vector("Resulting vector = ", result);
    }
}

void print_vector(char *prompt, int a[N])
{
    int i;

    printf ("\n\n%s\n", prompt);
    for (i = 0; i < N; i++) {
        printf(" %d", a[i]);
    }
    printf ("\n");
}

void print_matrix(char *prompt, int a[N][N])
{
    int i, j;

    printf ("\n\n%s\n", prompt);
    for (i = 0; i < N; i++) {
	for (j=0; j<N; j++) {
            printf(" %d", a[i][j]);
    } printf("\n"); }
    printf ("\n");
}
