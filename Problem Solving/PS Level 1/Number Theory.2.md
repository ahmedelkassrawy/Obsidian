a % n : finds the remainder after division by n

if time is 6 now 
after 7h -> (6 + 7) % 12 = 1
after 19h -> (6 + 19) % 12 = 1

if before X hours?
if its 6 now 
before 13 hrs ->  ((6 -13) % 12 ) + 12) % 12

because R is always +ve
A % 3 -> [-2,-1,0,1,2]
A % N = 0   -> A divisable by N

A % N == B % N -> (A - B) % N = 0
A % N % N = A % N
(N  ^ X ) % N = 0 
-A % N    !=    A % N
((-A % N) + (A % N)) % N = 0

(A + B) % N = (A % N + B % N) % N
(A * B) % N = (A % N * B % N) % N

divisor preprocessing 
you are given q queries each of those query coinsist of a number X for each query print all the divisor of X

```c++
const int MAX = 1e5;
vector<int> divs[MAXS + 1];
int cnt_of_divs[MAX + 1];

void generate_divs()
{
	for(int i = 1; i <= MAX; i++)
	{
		for(int j = i; j <= MAX; j += i)
		{
			divs[j].push_back(i);
			cnt_of_divs[j]++;
		}
	}
}
```

```c++
int count_divs(int num)
{
	int i,cnt = 0;
	for(int i = 1; i * i < num; i++)
	{
		if(!(num % i))
		{
			cnt += 2;
		}
	}
	
	if((i * i) == num) cnt++;
	return cnt;

}
```