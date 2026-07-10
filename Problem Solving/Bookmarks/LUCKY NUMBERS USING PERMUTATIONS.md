```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
using namespace std;

int main()
{
    string s;
    cin>>s;

    long long a = stoll(s);

    vector<long long> v;
    string x = "47";
    while(x.size() <= 10)
    {
        do
        {
            v.push_back(stoll(x));
        }
        while(next_permutation(x.begin(), x.end()));

        x += "47";
        sort(x.begin(), x.end());

    }

    auto it = lower_bound(v.begin(), v.end(), a);
    cout<<*it<<endl;
}


```

```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
using namespace std;

// Function to generate super lucky numbers
void generateSuperLuckyNumbers(string current, int count4, int count7, int maxLength, vector<long long>& superLucky) {
    if (current.length() == maxLength) {
        if (count4 == count7) {
            superLucky.push_back(stoll(current));
        }
        return;
    }

    generateSuperLuckyNumbers(current + "4", count4 + 1, count7, maxLength, superLucky);
    generateSuperLuckyNumbers(current + "7", count4, count7 + 1, maxLength, superLucky);
}

int main() {
    long long n;
    cin >> n;

    vector<long long> superLucky;
    int maxLength = 2; // Start with smallest even lengths

    while (true) {
        generateSuperLuckyNumbers("", 0, 0, maxLength, superLucky);
        sort(superLucky.begin(), superLucky.end());

        // Find the smallest number >= n
        for (auto number : superLucky) {
            if (number >= n) {
                cout << number << endl;
                return 0;
            }
        }

        // Increase the length to generate larger numbers
        superLucky.clear();
        maxLength += 2;
    }

    return 0;
}


```