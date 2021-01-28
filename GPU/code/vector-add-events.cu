#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include "timer.h"
#include <iostream>

using namespace std;

/* Utility function, use to do error checking.

   Use this function like this:

   checkCudaCall(cudaMalloc((void **) &deviceRGB, imgS * sizeof(color_t)));

   And to check the result of a kernel invocation:

   checkCudaCall(cudaGetLastError());
*/
static void checkCudaCall(cudaError_t result) {
    if (result != cudaSuccess) {
        cerr << "cuda error: " << cudaGetErrorString(result) << endl;
        exit(1);
    }
}


__global__ void vectorAddKernel(int opr, float* A, float* B, float* Result) {
    int i = (blockIdx.x * blockDim.x) + threadIdx.x;

    if (opr == 0) {
    	Result[i] = A[i] + B[i];
    }
    else if (opr == 1){
	Result[i] = A[i] - B[i];
    }
    else if (opr == 2){
	Result[i] = A[i] * B[i];
    }
    else
    {
	if (A[i] > 0) {Result[i] = (float) A[i] / B[i];}
        else { Result[i] = 0; } 
    }

}

void vectorAddCuda(int opr, int n, float* a, float* b, float* result) {
    int threadBlockSize = 512;

    // allocate the vectors on the GPU
    float* deviceA = NULL;
    checkCudaCall(cudaMalloc((void **) &deviceA, n * sizeof(float)));
    if (deviceA == NULL) {
        cout << "could not allocate memory!" << endl;
        return;
    }
    float* deviceB = NULL;
    checkCudaCall(cudaMalloc((void **) &deviceB, n * sizeof(float)));
    if (deviceB == NULL) {
        checkCudaCall(cudaFree(deviceA));
        cout << "could not allocate memory!" << endl;
        return;
    }
    float* deviceResult = NULL;
    checkCudaCall(cudaMalloc((void **) &deviceResult, n * sizeof(float)));
    if (deviceResult == NULL) {
        checkCudaCall(cudaFree(deviceA));
        checkCudaCall(cudaFree(deviceB));
        cout << "could not allocate memory!" << endl;
        return;
    }

    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);

    // copy the original vectors to the GPU
    checkCudaCall(cudaMemcpy(deviceA, a, n*sizeof(float), cudaMemcpyHostToDevice));
    checkCudaCall(cudaMemcpy(deviceB, b, n*sizeof(float), cudaMemcpyHostToDevice));

    // execute kernel
    cudaEventRecord(start, 0);
    vectorAddKernel<<<ceil((double)n/threadBlockSize), threadBlockSize>>>(opr, deviceA, deviceB, deviceResult);
    cudaEventRecord(stop, 0);

    // check whether the kernel invocation was successful
    checkCudaCall(cudaGetLastError());

    // copy result back
    checkCudaCall(cudaMemcpy(result, deviceResult, n * sizeof(float), cudaMemcpyDeviceToHost));

    checkCudaCall(cudaFree(deviceA));
    checkCudaCall(cudaFree(deviceB));
    checkCudaCall(cudaFree(deviceResult));

    // print the time the kernel invocation took, without the copies!
    float elapsedTime;
    cudaEventElapsedTime(&elapsedTime, start, stop);
    
    cout << "kernel invocation took \t\t" << elapsedTime << " milliseconds" << endl;
}


int main(int argc, char* argv[]) {
    int arr[3] = { 65536, 655360, 1000000 };
    const char *ops[] = {"Adding", "Subtracting", "Multiply", "Divide"};
    int opr;
    
    for (int j = 0; j<4; j++){
	opr = j;   
	for (int i = 0; i < 3; i++){
	    int n = arr[i];
            float* a = new float[n];
            float* b = new float[n];
            float* result = new float[n];
            float* result_s = new float[n];

            if (argc > 1) n = atoi(argv[1]);
            cout << ops[j] << " two vectors of " << n << " integer elements." << endl;
            // initialize the vectors.
            for(int i=0; i<n; i++) {
                a[i] = i;
                b[i] = i;
            }

            vectorAddCuda(opr, n, a, b, result);

            cout << "Done!" << endl;

            delete[] a;
            delete[] b;
            delete[] result;
            delete[] result_s;

        }
    }

    return 0;
}
