A _constructor_ is automatically called when an _object_ of the _class_ is declared.

- A _constructor_ is a _member_ function that is usually `public`.
- A _constructor_ can be used to initialize _member_ variables when an _object_ is declared.

> **Note:** A _constructor’s_ **name** must be the **same** as the _name_ of the _class_ it is declared in

**A constructor cannot _return_ a value**.
> **Note:** No _return_ type, not even `void` can be used while declaring a _constructor_

```C++
#include <iostream>
using namespace std;

class DayOfYear
{
	public:
	    DayOfYear(int new_month, int new_day); //declaring constructor
	    DayOfYear(); //default constructor without any parameters

	    int myVar;
	    void output( );
	    int get_month( );
	    int get_day( );

	private:  
	    void check_date( );  
	    int month;    
	    int day;
};


int main(){
  DayOfYear birthday(11,23); //creating object and calling constructor
  DayOfYear today; //creating object and calling default constructor
  cout << "Birthday day is: " << birthday.get_day()<<endl;
  cout << "Birthday month is: "<< birthday.get_month()<<endl;
  cout << "Today the day is: " << today.get_day()<<endl;
  cout << "Today month is: " << today.get_month()<<endl;
  return 0;

}
```


_Constructors_ can be _overloaded_ by defining _constructors_ with **different** _parameters_ list.