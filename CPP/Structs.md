```C++
struct{
    int fuel;
    string name;
}car;
```

```C++
//could access them using
car.fuel = 9;
car.name = bmw;
```

or you could name the struct
```C++
struct car {  
  string brand;  
  string model;  
  int year;  
};

int main()
{
// Create a car structure and store it in myCar1;  
  car myCar1;  
  myCar1.brand = "BMW";  
  myCar1.model = "X5";  
  myCar1.year = 1999;
}
```