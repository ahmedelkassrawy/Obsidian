3andi array feha 3dd msln 10  arkam btre2a 34wa2ya 3ayz eny a3rf kol rakm etkarr kam mara w ytb3 bl 3dd frequency da

```C++

#include <iostream>
using namespace std;
const int SIZE = 10;    // Size of the array
const int RANGE = 10;  // Range of values in the array

int main() {
int arr[SIZE] = {1, 3, 5, 7, 9, 1, 3, 5, 7, 9};
int freq[RANGE] = {0}; // Initialize frequency array with zeros
}
```

What's the difference between size , range?
size da size array input lenta medy leh compiler enma range da range elrkam lhowa hyt7rk feha fmsln momkn array tb2a {1,4,99,4,56,..} whtb2a a5r rakm momkn ywslo howa rakm range

```C++
// Count occurrences
for (int i = 0; i < SIZE; i++)
{
freq[arr[i]]++;
}
```

hn3tmd 3la enno array freq lindex bta3tha heya larkam bm3na eno rakm 1 lw 3ayz a3rf howa etkrr kam mra yb2a hroo7 llindex of 1 fhena for loop ht3dy 3la array of name array w tzwd ay rkam heya htl2eh htrg3 l array frequency tbd2 t7ot feh +1 whkza.

![[Screenshot (8).png]]

[[Frequency Array]]

Triple
```C++
#include <iostream>

using namespace std;

int main() {
    int t;
    cin >> t;  // Number of test cases

    while (t--) {
        int n;
        cin >> n;  // Size of the array

        int RANGE = n;  // Range of values in the array
        int arr[n];
        for (int i = 0; i < n; i++) {
            cin >> arr[i];
        }

        int freq[RANGE + 1] = {0};  // Initialize frequency array with zeros

        // Count occurrences
        for (int i = 0; i < n; i++) {
            freq[arr[i]]++;
        }

        // Print the value that appears at least three times
        int ans = -1;
        for (int i = 1; i <= RANGE; i++) {
            if (freq[i] >= 3) {
                ans = i;
                break;
            }
        }

        cout << ans << "\n";
    }
    return 0;
}
```

SPY detected
```C++
#include <iostream>

using namespace std;

int main() {
    int t;
    cin >> t;  // Number of test cases

    while (t--) {
        int n;
        cin >> n;  // Size of the array

        int RANGE = 100 + 1;  // Range of values in the array
        int arr[n],ind[100 + 1],freq[RANGE] = {0};
        for (int i = 0; i < n; i++) {
            cin >> arr[i];
			freq[arr[i]]++;
			ind[arr[i]] = i + 1;
        }

        // Print the value that appears at least three times
		int ans;
        for (int i = 1; i <= RANGE; i++) {
            if (freq[i] == 1) {
                ans = ind[i];
                break;
            }
        }
		cout<<ans<<endl;
    }
    return 0;
}
```

Pangram 
look into the given word if it contains all the words in alphabet or not
```C++
#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;  // Number of test cases

    while (t--) {
        int n;
        cin >> n;  // Size of the array

        int RANGE = 100 + 1;  // Range of values in the array
        int arr[n],ind[RANGE],freq[RANGE] = {0};
        for (int i = 0; i < n; i++) {
            cin >> arr[i];
			freq[arr[i]]++;
			ind[arr[i]] = i + 1;
        }

        // Print the value that appears at least three times
		int ans;
        for (int i = 1; i <= RANGE; i++) {
            if (freq[i] == 1) {
                ans = ind[i];
                break;
            }
        }
		cout<<ans<<endl;
    }
	return 0;
}
```

