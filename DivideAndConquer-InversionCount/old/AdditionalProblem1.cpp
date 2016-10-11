#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <stdlib.h>
using namespace std;

// Merges two sorted arrays of size n 
// O(n)
int* mergeArray(int* a, int* b, int n) {
    int* ptrA=a;
    int* ptrB=b;
    int* result=new int[2*n];
    int* ptrWrite=result;
    for (int i=0; i<2*n; i++) {
        if (*ptrA < *ptrB) {
            *(ptrWrite++)=*(ptrA++);
        }
        else {
            *(ptrWrite++)=*(ptrB++);
        }
    }
    return result;
}

// Recursively counts the number of inversions
// Also sorts the array in the process (will be used)
// INPUTS:
// - a,n: input array of size n
// OUTPUTS:
// - invCount: total number of inversions
// - sortedA: final sorted array
void countInversion(int* a, int n, long long int* invCount, int* sortedA) {
    long long int countB=0, countC=0;
    int nB=(n>>1);  // number of elements in B
    int nC=(n-(n>>1));
    int* sortedB=new int[nB];
    int* sortedC=new int[nC];
    
//    cout << "running recursive on size: " << n << endl;
    // Base cases
    if (n==1) {
        sortedA[0]=a[0];
        return;
    }
    
    countInversion(a, nB, &countB, sortedB);    // count the inversions inside left half
    countInversion(a+nB, nC, &countC, sortedC);    // count the inversions inside right half
    *invCount += countB;
    *invCount += countC;
    
    int j=0, k=0;
    
    for (int i=0; i<n; i++) {
        if ((j!=nB) && (sortedB[j]<sortedC[k] || k==nC)) {  // Make sure left and right scans have not reached the end
            sortedA[i]=sortedB[j];
            j++;
        } 
        else {
            sortedA[i]=sortedC[k];
            (*invCount) += (nB-j);
            k++;
        }
    }
//    
//    cout << "ending recursive step n=" << n 
//        << ",invCount=" << *invCount 
//        << ",sortedA[0]=" << sortedA[0]
//        << ",sortedB[0]=" << sortedB[0]
//        << ",sortedC[0]=" << sortedC[0]
//        << endl;
}

int main() {
	// your code goes here
	int arrayB[3]={4,9,10};
	int arrayC[3]={3,6,7};
	
 	cout << mergeArray(arrayB, arrayC, 3)[0] << endl;
	
	
	int arrayA[6]={6,5,4,3,2,1};
	long long int invCount=0;
	int sortedA[6];
	countInversion(arrayA, 6, &invCount, sortedA);
	cout << "invCount:" << invCount << endl;
	cout << "sortedA[0]:" << sortedA[0] << endl;
	cout << "sortedA[1]:" << sortedA[0] << endl;
	cout << "sortedA[2]:" << sortedA[0] << endl;
	cout << "sortedA[3]:" << sortedA[0] << endl;
	
    
    //Reading out the file
    int inputArray[100000];
    int cur_val;
    char testCString[100];
    string line;
    int lineNumber=0;
    ifstream  myfile("c:\\IntegerArray.txt");
    if (myfile.is_open()) {
        while(getline(myfile,line))
        {
//            cout << line << endl;
            cur_val = atoi(line.c_str());
//            cout << cur_val << endl;
            inputArray[lineNumber++]=cur_val;
        }
        myfile.close();
    }
    else {
        cout << "Unable to open file" << endl;
    }
    
    
    long long int invCountBig=0;
	int sortedABig[100000];
	countInversion(inputArray, 100000, &invCountBig, sortedABig);
	cout << "invCountBig:" << invCountBig << endl;
	cout << "sortedABig[0]:" << sortedABig[0] << endl;
	cout << "sortedABig[1]:" << sortedABig[0] << endl;
	cout << "sortedABig[2]:" << sortedABig[0] << endl;
	cout << "sortedABig[3]:" << sortedABig[0] << endl;
	
    
	return 0;
}