```C++
#include <iostream>
#include <vector>
using namespace std;
 

int main() 
{
    int n;
    cin >> n;

    vector<long long> v(n + 1);
    vector<vector<long long>> prefixBits(64, vector<long long>(n + 1));

  

    for (int i = 1; i <= n; i++) 
    {
        cin >> v[i];
    }


    for (int bit = 0; bit < 64; bit++) 
    {
        for (int i = 1; i <= n; i++) 
        {
            prefixBits[bit][i] = prefixBits[bit][i - 1] + ((v[i] >> bit) & 1);
        }
    }

    int q;
    cin >> q;

    while (q--) 
    {
        int l, r;
        cin >> l >> r; //1 indexed

        long long OR = 0;
        for (int bit = 0; bit < 64; bit++) 
        {
            int cnt = prefixBits[bit][r] - prefixBits[bit][l - 1];
            
            if (cnt)
            {
                OR += (1LL << bit);
            }
        }

        cout << OR << endl;

        long long AND = 0;
        for (int bit = 0; bit < 64; bit++)
        {
            int cnt = prefixBits[bit][r] - prefixBits[bit][l - 1];

            if (cnt == r - l + 1)
            {  // This calculates bitwise AND instead of OR
                AND += (1LL << bit);
            }
        }
        cout << AND << endl;
    }

    return 0;
}
```

```
// arr = [0 , 5 , 7 , 3] // arr 1-indexed

// 5 --> 101

// 7 --> 111

// 3 --> 011
   
    
// (2)power of 0 --> [0 , 1 , 2 , 3]

// why this happened because we had the first digit in all = 1

// so we prefix summed them



// 2 power of 1 --> [0, 0 , 1 , 2]

// why because the 5 doesn’t have 1 in the 2nd pos here
```
    
```C++
void check_parity(int n)
{
    cout << ((n & 1) ? "odd" : "even") << endl;
}


bool check_bit(int n, long long i)
{
    if ((n & (1LL << i)) != 0) // i starts from zero to get the first digit
    {
        return 1;
    }
    else
    {
        return 0;
    }
}


long long toggle_bit(long long n, long long bit)
{
    return (n ^ (1LL << bit)); // starts from zero
    // bits are numbered from right to left
}

  
long long pow2(long long n)
{
    return ((__builtin_popcountll(n)) == 1); // counts if only one bit is 1 then its pow of 2
}
  
long long XOR(long long n)
{
    long long ans = 0;

    for (long long i = n;; i--)
    {
        if (i % 4 == 3) break;
        ans = ans ^ i;
    }

    return ans;
}
```