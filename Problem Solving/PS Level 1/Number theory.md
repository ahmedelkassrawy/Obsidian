```C++
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

vector<int> divisor(int n)
{
    vector<int> ret;
    for(int i = 0; i * i <= n; i++)
    {
        if(n % i == 0) //this means i is a divisor
        {
            ret.push_back(i); //push it back
            if(i*i != n)  ret.push_back(n / i); 
            //check if the i we saved is prime or not
            //if it was prime we wouldnt need this loop if not prime we
            //have to save the other divisor
            // 3 is a divisor for 12 while also 4 a divisor for 12
            //so we save both but 25 there is no any other than 5
        }
    }
    return ret;
}
```

### Prime factorization and its various versions
```C++
vector<int> prime_factorization(int n)
{
    vector<int> ret;
    while(n != 1)
    {
        bool divide = false;
        for(int i = 2; i*i<= n; i++)
        //why only i * i not i
        //to be able to detect the prime numbers and break them out
        //of the big loop of division since i know that there will be only
        //2 divisors
        {
            if(n % i == 0)
            {
                ret.push_back(i);
                n /= i;
                divide = true;
                break;
            }
            
            if(!divide) //e2fesh prime
            {
                ret.push_back(n); //cause its the only divisor
                //so we make n = 1 3la tool 34an nbreak loop
                n = 1;
            }
        }
    }
    return ret;
}
```

```C++
vector<int> prime_factorization2(int n) 
//3ayz ageeb as8r 3dd mn arkam
//lw etdrbt fy b3d tdeeny n
{
    vector<int> ret;
    for(int i = 2; i * i <= n; i++)
    {
        while(n % i == 0) //check if the i is a divisor
        {
            ret.push_back(i); //yes it was
            n /= i; //hena h3ml kda 34an akll l3d nos zy mbn3ml fl 72ee2a
        }
    }

    if(n != 1) //lmfrood lw howa rkm tbee3y m4 prime y3dy w myd5ol4 hena
    {
        ret.push_back(n); //this means its prime so save the n only
        n = 1;
    }
   
    return ret;
}
```

### The sieve used in preprocessing
```C++
vector<bool> sieve(int n)
{
    vector<int> divide(n+1,0); 
    //returns the first number we can divide the number we have by

    vector<bool> is_prime(n+1,true);
     //lets declare an array tells us if the number is prime or not
    //so that any query we want related to prime will be O(1)
    //we set them first all equal to true
    //the 0 and 1 have to be done manually isnce they aren't prime
    //all the next are numbers if the number is prime then all its multiplicate relatives aren't
    //if they aren't prime masl7a yaba

    is_prime[0] = is_prime[1] = false;

    for(int i = 2; i <= n; i++) //we start from 2 (1,0 declared already)
    {
        if(is_prime[i]) //it should be true
        {
            divide[i] = i; //the number can be ofc divided by itself
  
            for(int j = 2*i; j <= n; j += i) 
            // the loop for the multiplicate relatives
            {
                is_prime[j]  = false; //
                if(divide[j] == 0)
                {
                    divide[j] = i;
                }
            }
        }
    }
    return is_prime;
}
```

```C++
vector<int> prime_factorization3(int n, vector<int> &divide)
{
    vector<int> ret;
    while(n != 1)
    {
        int p = divide[n];
        ret.push_back(p);
        n /= p;
    }

    return ret;
}
```

```C++
bool is_prime(long long n)
{
    if (n <= 1) return false;
    for (long long i = 2; i * i <= n; i++)
    {
        if (n % i == 0) return false;
    }
    return true;
}
```

[Math/Level 1 at main · UwUkareem/Math · GitHub](https://github.com/UwUkareem/Math/tree/main/Level%201)