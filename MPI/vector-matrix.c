#define N 4
#include <stdio.h>
#include <math.h>
#include <sys/time.h>
#include <stdlib.h>
#include <stddef.h>
#include "mpi.h"


void print_results(char *prompt, int a[N]);

int multiplicate(double vec[], double M[],  int len) {

	// Create resulting row
	int res[len];

	// Multiply every element of vector with corresponding matrixrow
	for (int i = 0; i < len; i++){
		res[i] = vec[i] * M[i];
	}

	return 1;
}

int main(int argc, char *argv[])
{
    int i, rank, size, cc =0;
    int b[N]={1,2,3,4};
    int a[N][N]={{1,1,1,2},{1,1,1,3},{1,1,1,4},{1,1,1,5}};
    int c[N];
    int aa[N];

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    //scatter rows matrix to different processes     
    MPI_Scatter(&a, N*N/size, MPI_INT, aa, N, MPI_INT, 0, MPI_COMM_WORLD);

    //broadcast vector to all processes
    MPI_Bcast(&b, N, MPI_INT, 0, MPI_COMM_WORLD);

    MPI_Barrier(MPI_COMM_WORLD);

    //perform vector multiplication by all processes

	 for (i = 0; i < N; i++){
          	cc = cc + aa[i] * b[i];               
	   }

    MPI_Gather(&cc, N*N/size, MPI_INT, c, 1, MPI_INT, 0, MPI_COMM_WORLD);

    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Finalize();
    if (rank == 0)
        print_results("Resulting vector = ", c);
}

void print_results(char *prompt, int a[N])
{
    int i;

    printf ("\n\n%s\n", prompt);
    for (i = 0; i < N; i++) {
        printf(" %d", a[i]);
    }
    printf ("\n\n");
}
