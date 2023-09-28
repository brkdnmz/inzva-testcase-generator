#include <bits/stdc++.h>
using namespace std;
using ll = long long;

/**
 * This is your solution code.
 * It takes input files that the Python script generates as the input,
 * and outputs to the output file specified as the second command line argument.
 */

/**
 * Be careful when printing the output!
 * It should NOT contain trailing whitespaces, "\n"s etc.
 * Please take this serious. This is especially crucial for Pythoners.
 */

int main(int argc, char **argv) {
    freopen(argv[1], "r", stdin);
    freopen(argv[2], "w", stdout);
    ios::sync_with_stdio(0);
    cin.tie(0);
    int n;
    cin >> n;
    int a[n];
    for (int &x : a)
        cin >> x;
    set<int> s;
    for (int i = 0; i < n; i++) {
        s.insert(a[i]);
        cout << s.size();
        if (i + 1 != n)
            cout << " ";
    }
}