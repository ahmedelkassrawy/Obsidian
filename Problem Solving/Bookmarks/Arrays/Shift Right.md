

```C++
#include <iostream>
using namespace std;
void shift_right()
{
    int size, times;
    cin >> size >> times;
    int arr[size] = {};
    for (int i = 0; i < size; i++) {
        cin >> arr[i];
    }
    int ntimes = times % size;
    for (int i = 0; i < ntimes; i++) {
        int temp[size] = {};
        temp[0] = arr[size - 1];
        for (int j = 1; j < size; j++)
        {
            temp[j] = arr[j - 1];
        }
        for (int j = 0; j < size; j++)
        {
            arr[j] = temp[j];
        }
    }
    for (int i = 0; i < size; i++) {
        cout << arr[i] << " ";
    }
}
 
int main() {
    shift_right();
    return 0;
}
```