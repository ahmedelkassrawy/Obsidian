[Sheet #4 | Number Theory 2 - Virtual Judge](https://vjudge.net/contest/667337#problem/B)

```C++
#include <iostream>
using namespace std;

int main()
{
    string s;
    cin >> s;
    long long n;
    cin >> n;

    long long ans = 0, tenpowx = 1;
    for (int i = s.size() - 1; i >= 0; --i) 
    {
        long long digit = (s[i] - '0') % n;
        ans += (digit * tenpowx) % n;
        ans %= n;
        tenpowx *= 10 % n;
        tenpowx %= n;
    }
    cout << ans << '\n';
}

```

ha5od lrakm fy string wb3deen a5o4 for loop abd2 a5r ll2wl w tenpowx = 1
y5o4 yt3mlo modulus m3 n wb3dha y5o4 ydrb fy 34ra pow rkm w yt3mlo modulus
wb3den modulus lanswer kolha wb3deen tenpow dy htzeed whndrb 10 fyha
wb3deen modulus ltenpowx