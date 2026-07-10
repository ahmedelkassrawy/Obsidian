```C++
#include <iostream>
#include <vector>

using namespace std;

void insertionSort(vector<int>& arr) 
{
    for(int i = 1; i < arr.size(); i++)
    {
        int curr = arr[i];
        int j = i - 1;

        while(j >= 0 && arr[j] > curr)
        {
            arr[j + 1] = arr[j];
            j--;
        }

        arr[j + 1] = curr;
        
    }
}

int main() 
{
    vector<int> arr = {5, 2, 4, 6, 1, 3};

    insertionSort(arr);

    cout << "Sorted array: ";
    for (int i = 0; i < arr.size(); i++) 
    {
        cout << arr[i] << " ";
    }
    cout << endl;

    return 0;
}
```