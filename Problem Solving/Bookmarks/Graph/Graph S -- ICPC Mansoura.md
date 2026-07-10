[#Sheet1 : Intro To Graph & DFS - Virtual Judge](https://vjudge.net/contest/690295#problem/S)
```C++
#include <vector>
#include <iostream>
#include <unordered_map>
#include <unordered_set>
using namespace std;

int main()
{
    int n,m;
    while(cin>>n>>m)
    {
        unordered_map<char,vector<char>> adj;
        unordered_map<char,int> counter; // Stores count
        unordered_set<char> awake,sleep; // Sets for awake and asleep areas
        int years = 0; // Counter for years taken to wake up the brain

        for(int i = 0; i < 3; i++) //awake brains
        {
            char a;
            cin>>a;
            awake.insert(a);
        }

        for(int i = 0; i < m; i++)
        {
            char from,to;
            cin>>from>>to;

            adj[from].push_back(to);
            adj[to].push_back(from);
        }

        for(auto& node : adj)
        {
            char area = node.first;

            if(awake.find(area) == awake.end())
            {
                sleep.insert(area);

                for(char v : node.second)
                {
                    if(awake.find(v) != awake.end())
                    {
                        counter[area]++;
                    }
                }
            }
        }

        while(!sleep.empty())
        {
            unordered_set<char> newawake;

            //check if the area in slept has at least 3 awake neighbors
            for(char area: sleep)
            {
                if(counter[area] >= 3)
                {
                    newawake.insert(area);
                }
            }

            if(newawake.empty()) break; //no areas wake up

            //waking up new areas
            for(char area : newawake)
            {
                awake.insert(area);
                sleep.erase(area);

                for(char v : adj[area])
                {
                    counter[v]++;
                }
            }
            years++;
        }

        if(awake.size() == n) 
        {
            cout << "WAKE UP IN, " << years << ", YEARS\n";
        }
        else cout << "THIS BRAIN NEVER WAKES UP\n"; 

        string emptyLine;
        if (cin.peek() == '\n') 
        {
            getline(cin, emptyLine);
        }
    }
}
```