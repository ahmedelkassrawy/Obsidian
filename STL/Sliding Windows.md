```C++
for (int i = k; i < n; i++) 
{ 
// Slide the window right: subtract the element going out and add the element coming in 
	windowSum += arr[i] - arr[i - k]; 
	maxSum = max(maxSum, windowSum); `
// Update maxSum if needed 
}
```
```C++
for(int i = k; i < n; i++)
{
	if (s[i - k] == 'W') 
	{
	   current_changes--;
	}
	// Add the effect of the character coming into the window

	if (s[i] == 'W') 
	{
		current_changes++;
	}
	
	// Update the minimum changes required
	min_changes = min(min_changes, current_changes);
}
```

arr[i] --> +++
arr[i-k] --> ---