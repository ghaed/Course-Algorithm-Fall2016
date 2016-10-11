#include <iostream>
using namespace std;

// Finds the winners
// Inputs:
// -A,n: Array of size N to find winners in
// Outputs:
// -winner: The largest number in array A
// -losers: Array of numbers that lost to A
// -m:number of losers
void findWinners(int* A, int n, int* winner, int* losers, int* m) {
    int* winnerB=new int;
    int* winnerC=new int;
    int* losersB=new int[n];
    int* losersC=new int[n];
    int* mB=new int;
    int* mC=new int;
    
    cout << "running function on size:" << n << endl;
    
    if (n==1) {
        *m=0;
        *winner=A[0];
        return;
    }
    
    findWinners(A, n>>1, winnerB, losersB, mB);
    findWinners(A+(n>>1), n>>1, winnerC, losersC, mC);
    if (*winnerB>*winnerC) {
        *winner=*winnerB;
        losers[0]=*winnerC;
        for (int i=0; i<*mB; i++) {
            losers[i+1]=losersB[i];
        }
        *m=(*mB)+1;
    }
    else {
        *winner=*winnerC;
        losers[0]=*winnerB;
        for (int i=0; i<*mC; i++) {
            losers[i+1]=losersC[i];
        }
        *m=(*mC)+1;
    }
    
    cout << "winner:" << *winner << ",losersB[0]:" << losers[0] << ",m:" << *m << endl; 
    
}

int findSecond(int* A, int n) {
	int winner;
	int* losers = new int[n];
	int m;
	int result=A[0];
	findWinners(A, n, &winner, losers, &m);
	for (int i=0; i<m; i++) {
        if (losers[i]>result) {
            result=losers[i];
        }
    }
    return result;
}

int main() {
	// your code goes here
	int a[4]={3, 4, 2, 1};
	int winner;
	int losers[4]={0};
	int m;
	cout << "Hello world" << endl;
	findWinners(a, 4, &winner, losers, &m);
	cout << "winner:" << winner << endl;
	cout << "losers:";
	for (int i=0; i<4; i++) {
	    cout << i << ":" << losers[i] << ","; 
	}
	cout << endl << "m:" << m << endl;
	cout << endl << "2nd Biggest:" << findSecond(a, 4) << endl;
	
	return 0;
}
