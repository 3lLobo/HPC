/**
 * Simple demo program for MPI: a master/worker program that searches for prime numbers in a range of numbers.
 */

#include <stdio.h>
#include <mpi.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>


/**
 * Given a value 'n', return {\code true} iff the value is prime.
 *
 * @param n The value to examine.
 * @return {\code true} iff the value is prime.
 */

bool multiplicate(double vec[], double M[],  int len) {

	\\ Create resulting row
	double res[len];

	\\ Multiply every element of vector with corresponding matrixrow
	for (int i = 0; i < len; i++){
		result[i] = vec[i] * M[i];
	}

	return res;
}


/**
 * Given a value to send and a worker to send the value to, send
 * a message ordering the worker to compute whether the given value
 * is prime. The special value '0' means that the worker should quit.
 * The worker will send a message to the master with the verdict.
 *
 * @param worker  The worker to send the message to.
 * @param val The value to examine.
 */

void send_work_command(int worker, double vector[], double matrix[], int len) {
    // printf("send_work_command: worker=%d val=%lu\n", worker, val);
    MPI_Send(&vector, &matrix, 2*len, MPI_DOUBLE, worker, 0, MPI_COMM_WORLD);
}


/**
 * Given a result to send, send a message telling the master that
 * the value it sent is prime or not. Note that the value for which the
 * result has been computed is not sent, since nobody cares about it.
 *
 * @param result The result.
 */
void send_result(int result) {
    MPI_Send(&result, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
}


/**
 * Wait for the next value to compute. The value zero means that the worker should quit.
 *
 * @param val A pointer to the value to fill with the received value.
 */
void await_command(long int *val) {
    MPI_Recv(val, 1, MPI_LONG, 0, MPI_ANY_TAG, MPI_COMM_WORLD,
             MPI_STATUS_IGNORE);
}


/**
 * Wait for the next result from a worker.
 *
 * @param worker A pointer to the variable that will hold the worker that sent the result.
 * @param result A pointer to the variable that will hold the result.
 */
void await_result(int *worker, int *result) {
    MPI_Status status;
    MPI_Recv(result, 1, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD,
             &status);
    *worker = status.MPI_SOURCE;
}


/**
 * The code to run as master: send jobs to the workers, and await their replies.
 * There are `worker_count` workers, numbered from 1 up to and including `worker_count`.
 *
 * @param worker_count The number of workers
 * @param startval  The first value to examine.
 * @param nval The number of values to examine.
 * @return The number of values in the specified range.
 */

int run_as_master(int worker_count, double vector[], double matrix[], int len) {
    int active_workers = 0, row = 0;
    double resulting[len][len];

    for (int worker = 1; worker <= worker_count && worker < len; worker++) {
        send_work_command(worker, matrix[row]);
        row += 1;
        active_workers++;
    }
    while (active_workers > 0) {
        int worker, result;
        await_result(&worker, &result);
        primes += result;
        if (val <= endval) {
            send_work_command(worker, val);
            val += 2;
        } else {
            send_work_command(worker, 0);
            active_workers--;
        }
    }
    return primes;
}

/**
 * The code to run as worker: receive jobs, execute them, and terminate when told to.
 */

void run_as_worker(void) {
    while(true) {
        double row[len];

        await_command(&row);
        if (val == 0) {
            break;  // The master told us to stop.
        }
        int result = is_prime(val);
        if (result == true){ printf("PRIME ADDED: %ld\n", val); }
        send_result(result);
    }
}

int main(int argc, char *argv[]) {
    int rank, size;

    \\ Specify dimension of matrix and vector
    int len = 3;
    double matrix[len][len];
    double vector[len];
    int i, j;

    \\ Create vector and matrix
    for(i=0; i<len; i++){
	vector[i] = i+1;
	for(j=0; j<len; j++){
	    matrix[i][j] = 1;
	}
    }

    /* Start up MPI */
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const bool am_master = 0 == rank;

    if (am_master) {
        int workers = size -1;
        printf("Running as master with %d workers\n", workers);
        const double start = MPI_Wtime();
        double[len] = run_as_master(workers, vector, matrix);
        const double finish = MPI_Wtime();
        printf("Stopped as master\n Output Matrix:\n");
	for (i = 0; i < m; i++)  {
		for (j = 0; j < n; j++) {
            	printf("%d\t", matrix[i][j]);
        	}
        	printf("\n");
    	}
        } else {
            printf("Running as worker %d\n", rank);
            run_as_worker();
            printf("Stopped as worker %d\n", rank);
    	}

    MPI_Finalize();

    return 0;
}
