strings when given are added as a pipe each letter is added to the other , at the end there is /n;
which is a whitespace to indicate the enter button you pressed.
```C++
int main()
{
    int n;
    string s;

    cin>>n; //lw b3tlha enter hya ht3tbr enk mb3t4 7aga wtfdl mstnya klma
    cin.ignore(); //bt5leeny at8ada 3n el backslach n dy wtms7ha b3d mdlha input bta3y lhow hena 3obara 3n rakm
    for(int i =0; i < n; i++)
    {
        getline(cin,s); //bta5od kol da8ta blm3na l7AERFY leha
        cout<<"the 5ara is"<< s<<endl;
    }
}
```