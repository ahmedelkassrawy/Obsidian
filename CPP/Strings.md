```C++
#include <iostream>
#include <string>
using namespace std;

int main() {
    string line;
    
    // Read a line of text from standard input (cin)
    cout << "Enter a line of text: ";
    getline(cin, line);
    
    // Display the line of text
    cout << "You entered: " << line << endl;
    
    return 0;
}

```

## Checking if Digit or not (Chars)
```C++
#include <iostream>
#include <string>
using namespace std;
int main() {
    char c = 'A';
    if(c >= '0' && c <= '9') cout<<"ITS DIGIT";
}
```