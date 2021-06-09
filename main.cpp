#include<iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <queue>
#include <math.h>
#include "bigint.h"
using namespace std;


void print_v (const vector<bigint> &v ){
    for (int i = 0; i < v.size(); ++i) {
        cout << v[i] << " ";
    }
    cout << endl;
}

void print_vv(const vector<vector<bigint>>(&m)){
    for (int i = 0; i < m.size(); ++i) {
        print_v(m[i]);
    }
    cout << endl;
}

bigint factorial(bigint n){
    if ( n < bigint(2)) return 1;
    return n * factorial(n-1);
}

// vector<vector<vector<int>>> (n+1,vector<vector<int>> (k+1,vector<int> (target+1,-1)));

int subset_sum(int n, int k, long target, vector<vector<vector<int>>>& memo,int offset){ // const vector<int>& U
    if (k==0){
        return int(target == 0);
    }
    if (target <= offset or n==0){
        return 0;
    }
    if (memo[n][k][target] == -1){
        memo[n][k][target] = subset_sum(n - 1, k, target, memo, offset)
        + subset_sum(n - 1, k - 1, target - (n+offset), memo, offset); // si l'objet est encore dispo
    }
    return memo[n][k][target];
}

bigint bob_expected_utility(int n, int k, int offset,vector<vector<vector<int>>>& memo){
    long total_utility = (n*(n+1))/2 + n * offset;      // = ((n+offset) * (n+offset+1) - offset * (offset + 1))/2;
    long min_picked = (k*(k+1))/2 + k * offset;
    long max_picked = total_utility - ((n-k)*(n-k+1))/2 - k*offset;
    long sum(0);
    for (long picked = min_picked; picked <= max_picked ; ++picked) {
        sum += (total_utility - picked) * subset_sum(n,k,picked,memo, offset);
    }

    return ((bigint(sum) * factorial(k) * factorial(n-k))/ factorial(n));
}


vector<bigint> optimal_egalitarian_2cut(int n, int offset){
    long total_utility = (n*(n+1))/2 + n * offset;
    bigint last_min = 0;
    vector<vector<vector<int>>> memo (n+1,vector<vector<int>> (total_utility+1,vector<int> (total_utility+1,-1)));
    bigint alice,bob;
    for (int k = 1; k <= n ; ++k) {
        alice = total_utility - ((n-k)*(n-k+1))/2 - (n-k) * offset;
        bob = bob_expected_utility(n,k,offset,memo);
        cout << " " << k << " " << alice << " " << bob << endl;
       /* if (alice > bob){
            if (last_min > min(alice,bob)){
                k --;
                alice = alice = total_utility - ((n-k)*(n-k+1))/2 - (n-k) * offset;
                bob = bob_expected_utility(n,k,offset,memo);
            } return vector<bigint> {k,alice,bob};
        } last_min = min(alice,bob); */
    }
    cout << "wtf";
    return vector<bigint> {alice,bob};
}

int main() {
    print_v(optimal_egalitarian_2cut(50,0));
    return 0;
}