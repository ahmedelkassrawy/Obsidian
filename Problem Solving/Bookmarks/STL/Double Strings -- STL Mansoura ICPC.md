[Problem - U - Codeforces](https://codeforces.com/group/5pUldkahAU/contest/521118/problem/U)

```C++
#include <iostream>
#include <unordered_set>
#include <vector>
#include <string>

using namespace std;

int main() {
    int t;  // Number of test cases
    cin >> t;

    while (t--) 
    {
        int n;  // Number of strings in the current test case
        cin >> n;
        
        vector <string> strings(n);
        unordered_set <string> stringSet;

        for(int i =0; i< n; i++)
        {
            cin>>strings[i];
            stringSet.insert(strings[i]);
        }

        string result(n,'0'); //strings full of zeros

        for(int i = 0; i < n; i++)
        {
            string curr = strings[i];

            for(int j = 1; j < curr.length();j++)
            {
                string s1 = curr.substr(0,j);
                string s2 = curr.substr(j);

                if(stringSet.count(s1) && stringSet.count(s2))
                {
                    result[i] = '1';
                    break;
                }
            }
        }
        cout<<result<<endl;
    }

}
```