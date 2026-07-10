[Sheet #5 | Recursion and Backtracking - Virtual Judge](https://vjudge.net/contest/669349#problem/F)

```C++
#include <iostream>
#include <vector>
#include <set>
using namespace std;

string s;
vector<int> vis;
set<string> ans;

void f(string curr,string &s)
{
    if(curr.size() == s.size())
    {
        ans.insert(curr);
    }

    for(int i = 0; i< s.size(); i++)
    {
        if(vis[i]) continue;

        vis[i] = 1; //34an a3rf eny kda 5dt lrakm
        f(curr + s[i],s);
        vis[i] = 0; //34an a2dr-backtrack l7arf da tany 
    }

}

int main() 
{
    cin>>s;

    vis.resize(s.size(),0);

    f("",s);

    cout<<ans.size()<<"\n";

    for(auto c: ans)
    {
        cout<<c<<"\n";
    }

}
```