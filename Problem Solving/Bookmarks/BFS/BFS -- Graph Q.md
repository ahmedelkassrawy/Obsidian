[#Sheet2 : BFS & Graph Applications - Virtual Judge](https://vjudge.net/contest/692604#problem/Q)
```C++
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <array>
#include <map>
using namespace std;

vector<vector<int>> adj(26);
vector<int> indegree(26);


int main()
{
    int n;
    cin>>n;

    string last; //will use it for comparison
    cin>>last;

    for(int i = 0; i < n - 1; i++)
    {
        string s;
        cin>>s;

        if(s == last) continue;
        if(last.size() > s.size() && s == last.substr(0, s.size()))
        {
            cout<<"Impossible";
            return 0;
        }

        for(int j = 0; j < min(s.size(),last.size()); j++)
        {   
            if(s[j] != last[j]) //We iterate over the characters of s and last until the first difference.
            {
                adj[last[j] - 'a'].push_back(s[j] - 'a');//char of last is parent of s
                indegree[s[j] - 'a']++;
                break;
            }

        }

        last = s;
    }

    queue<int> q;
    for(int i = 0; i < 26; i++)
    {
        if(indegree[i] == 0)
        {
            q.push(i);
        }
    }

    string ans;

    while(!q.empty())
    {
        int curr = q.front();
        q.pop();

        ans.push_back(curr + 'a');

        for(auto u : adj[curr])
        {
            indegree[u]--;

            if(indegree[u] == 0) 
            {
                q.push(u);
            }
        }
    }

    cout<<(ans.size() == 26 ? ans : "Impossible"); //if not then there was a cycle
}
```