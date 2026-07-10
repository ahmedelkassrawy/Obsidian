[#Sheet1 : Intro To Graph & DFS - Virtual Judge](https://vjudge.net/contest/690295#problem/J)
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
using namespace std;


int main()
{
    int t;
    cin>>t;

    while(t--)
    {
        int n;
        cin>>n;

        vector<int> p(n + 1); //given 
        vector<int> child(n + 1,0); //number of children of each node

        vector<vector<int>> adj(n + 1); //graph
        vector<bool>vis(n + 1,false); 

        int root = -1;

        for(int i = 1; i <= n; i++)
        {
            cin>>p[i];

            if(p[i] == i)
            {
                root = i;
            }
            else
            {
                adj[p[i]].push_back(i); //p[i] is parent of i
                child[p[i]]++; //adding in the childs of the parent
            }
        }

        vector<vector<int>> paths;

        for(int i = 1; i <= n; i++) //looping on nodes
        {
            if(child[i] == 0 && !vis[i]) //if the childeren of the nodes and the node itself are not visited
            //we're looping on the leaves ta7t
            {
                vector<int> path;

                int node = i;

                while(!vis[node]) 
                {
                    path.push_back(node); //pushing the node in the path
                    vis[node] = true; //marking the node as visited
                    if(node == root) break; //if the node is the root then break
                    node = p[node]; //moving up to the parent
                }

                reverse(path.begin(),path.end()); //bdl mehya mn ta7t lfoo2 tb2a mn fo2 lta7t
                paths.push_back(path);

            }
        }

        cout<<paths.size()<<endl;
        for(auto path : paths)
        {
            cout<<path.size()<<" ";
            for(auto node : path)
            {
                cout<<node<<" ";
            }
            cout<<endl;
        }
    }
}
```