#define N 4
#define Z 2
#include <stdio.h>
#include <math.h>
#include <sys/time.h>
#include <stdlib.h>
#include <stddef.h>
#include "mpi.h"

void print_vector(char *prompt, double a[N]);
void print_matrix(char *prompt, double a[N][N]);


int main(int argc, char *argv[])
{
    int i, rank, size;
    double sum=0;
    double vector[N];
    double matrix[N][N];
    double result[N];
    double *chunk;
    double start, end, final;

    //Initialize simple vectors
    for(int k=0; k < N; k++){
	vector[k] =(double) k+1;
	for (int r=0; r < N; r++){
	    if (r == (N-1)) {matrix[k][r] =(double) r+k;}
	    else { matrix[k][r] = (double)1; } 
	}
    }

    //Initialize MPI parallel, get comm size and process rank
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);


    // Determine size of processes
    int local = (int)ceil((double)(N/size));

    //Allocate memory for distributed vector
    chunk = (double*)malloc(N*local*sizeof(double));

    //scatter rows matrix to different processes     
    MPI_Scatter(&matrix, N*local, MPI_DOUBLE, chunk, N*local, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    // Time calculations
    start = MPI_Wtime();

    // Declare local variable
    double cc[local];

    for(int R=0; R<Z; R++){
	if(R==0){ 
	    //Broadcast Vector to all processes
	    MPI_Bcast(&vector, N, MPI_DOUBLE, 0, MPI_COMM_WORLD);
        	for (i=0; i<local; i++) { 
        		sum = 0;
                	for (int j=0; j<N; j++){ 
                        	sum += vector[j]*chunk[j+(i*N)];
                	} cc[i] = sum;
        } }
	else
	{
   	//broadcast vector to all processes
  	MPI_Bcast(&result, N, MPI_DOUBLE, 0, MPI_COMM_WORLD);


    	//perform vector multiplication by all processes
     	for (i=0; i<local; i++) { 
     	sum = 0;
         	for (int j=0; j<N; j++){ 
        		sum += result[j]*chunk[j+(i*N)];
		} cc[i] = sum;
     	} }
	MPI_Barrier(MPI_COMM_WORLD);

    	MPI_Gather(&cc, local, MPI_DOUBLE, result, local, MPI_DOUBLE, 0, MPI_COMM_WORLD);

//	printf("Loop number: %d\n", R);
//	print_vector("Vector used = ", vector);
//	for(int h=0; h<N; h++){ vector[h] = result[h]; } 
//	print_vector("Resulting vector = ", result);
//	printf("\n");
    } 

    end = MPI_Wtime();
    MPI_Finalize();

    if (rank == 0){
	final = end - start;
        printf("Processes: %2d \t Loops: %d \t Matrix size: %4d \t Time Elapsed: %f\n\n", size, Z, N, final);
        print_vector("Initial vector = ", vector);
	print_matrix("Initial Matrix = ", matrix);
	print_vector("Final vector = ", result);
    }
}

void print_vector(char *prompt, double a[N])
{
    int i;

    printf ("\n\n%s\n", prompt);
    for (i = 0; i < N; i++) {
        printf(" %lf", a[i]);
    }
    printf ("\n");
}

void print_matrix(char *prompt, double a[N][N])
{
    int i, j;

    printf ("\n\n%s\n", prompt);
    for (i = 0; i < N; i++) {
	for (j=0; j<N; j++) {
            printf(" %lf", a[i][j]);
    } printf("\n"); }
    printf ("\n");
}
