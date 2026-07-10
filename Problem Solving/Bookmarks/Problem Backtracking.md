```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <set>
using namespace std;

vector<int> arr(10);
vector<int> ans;
int k;

bool f(int pos,int sum , set<int> st)
{

    if(st.empty()) //if the set is empty then return true
    {
        return true;
    }

    set<int> temp = st; //to have another dupliacte to remove from
    
    for(auto i : temp)
    {
        if(sum + arr[pos] * i > k) break; //for time complexity reasons

        ans.push_back(i);  //first push back
        st.erase(i); //remove what u used

        if(f(pos+1,sum + arr[pos]*i,st)) return true;

        st.insert(i); //for backtracking reasons
        ans.pop_back(); //for backtracking reasons
    }

    return false;

}

int main() 
{
    int t;
    cin>>t;

    while(t--)
    {
        arr.clear();
        arr.resize(10);
        ans.clear();


        for(int i = 0; i < 10; i++)
        {
            cin>>arr[i];
        }

        cin>>k;

        set<int> st = {0,1,2,3,4,5,6,7,8,9};

        f(0,0,st);

        if(ans.empty()) //if ans is empty then no answers
        {
            cout<<-1<<"\n";
            continue;
        }

        for(auto i : ans)
        {
            cout<<i<<" ";
        }

        cout<<"\n";
    }
}
```