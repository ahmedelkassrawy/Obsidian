3ndk gdwl feh mw3eed kolha intersect b3dha ht3ml eh 34an tmly lyoum 3la 2ad ma te2dr .
Sounds like a hard problem, right? Actually, the algorithm is so easy, it might surprise you. Here’s how it works: 
1. Pick the class that ends the soonest. This is the first class you’ll hold in this classroom. 
2. 2. Now, you have to pick a class that starts after the first class. Again, pick the class that ends the soonest. This is the second class you’ll hold.

Fakr [[Knapsack]] you could use greedy algo there:
1. pick the most expensive thing
2. pick the next most expensive thing
mtf3nna4 brdo leeh 34an enta hta5od expensive bs mhowa mokn sum two items > expensive one.

3ndk radio show 3ayz twslo l7ad 50 state fy stations kteer wa8lbhom by8ty aktr mn region aw state t3ml eh? tgrb greedy 
1. Pick the station that covers the most states that haven’t been covered yet. **It’s OK if the station covers some states that have been covered already. 
2. Repeat until all the states are covered.

Solution In code for this example:
Turn the array of stations into a set (each item appears once)
```python
stations = {} 
stations["kone"] = set(["id", "nv", "ut"]) 
stations["ktwo"] = set(["wa", "id", "mt"]) stations["kthree"] = set(["or", "nv", "ca"]) stations["kfour"] = set(["nv", "ut"]) 
stations["kfive"] = set(["ca", "az"])
```

keys are station names , values are the states they cover
you need a final set of stations you'll use
```python
final_stations = set()
```

```python
best_station = None 
states_covered = set() 
for station, states_for_station in stations.items():
	covered = states_needed & states_for_station
	if len(covered) > len(states_covered):
		best_station = station
		states_covered = covered


final_stations.add(best_station)
#You also need to update states_needed. Because this station covers some states, those states aren’t needed anymore:
states_needed -= states_covered

```

The for loop allows you to loop over every station to see which one is the best station. 

covered is a set of states that were in both states_needed and states_for_station. So covered is the set of uncovered states that this station covers! Next you check whether this station covers more states than the current best_station.

FULL CODE
```python
while states_needed: 
	best_station = None 
	states_covered = set() 
	for station, states in stations.items(): 
		covered = states_needed & states 
		if len(covered) > len(states_covered): 
			best_station = station 
			states_covered = covered 
	
	states_needed -= states_covered
	final_stations.add(best_station)
```