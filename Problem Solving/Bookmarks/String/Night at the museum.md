https://codeforces.com/group/MWSDmqGsZm/contest/223206/problem/Q

3ayz tlf 3la dyra aw ors ltelephone bta3 zman wtwsl llrkam fy akl 3dd 5twat 
lfkra enk ht2smo blnos fl alphabets b 26 rkm
```C++
#include <iostream>
#include <algorithm>
#include <string>
using namespace std;

int main()
{
    int counts = 0; //3ddad el5tawat
    string str;
    cin >> str;
    char current = 'a'; //kda kda howa m7ddlk tbd2 mn "a"
    for (int i = 0; i < str.size(); i++)
    {
        int result = abs(str[i] - current); //ta5od absolute diff beftween letter lhowa md5lo wa5r rkm m3ana

        if (result <= 13) // right
        {
            counts += result;
        }
        else // left
        {
            counts += (26 - result);
        }
        
        current = str[i]; //lazm t8yr a5r 7rf enta kont wa2f 3ndo 34an ybd2 mn 3ndo tany
    }
    cout << counts << endl;
}
```