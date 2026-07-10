![[Pasted image 20240519205223.png]]
![[Pasted image 20240519205347.png]]

Feature Extraction
- You can extract the features from the person or object itself.

These are the two basic things you’ll do with KNN— classification and regression: 
Classification = categorization into a group 
Regression = predicting a response (like a number)

So far, you’ve been using the distance formula to compare the distance between two users. Is this the best formula to use?
They both loved Manmohan Desai’s Amar Akbar Anthony. Paul rated it 5 stars, but Rowan rated it 4 stars. If you keep using the distance formula, these two users might not be each other’s neighbors, even though they have similar taste

Cosine similarity doesn’t measure the distance between two vectors. Instead, it compares the angles of the two vectors.

## picking up good features
- Features that directly correlate to the movies you’re trying to recommend 
- Features that don’t have a bias (for example, if you ask the users to only rate comedy movies, that doesn’t tell you whether they like action movies)

There’s no one right answer when it comes to picking good features. You have to think about all the different things you need to consider



## Machine Learning
Machine learning is all about making your computer more intelligent. You already saw one example of machine learning: building a recommendations system. Let’s look at some other examples.

OCR stands for optical character recognition.
. It means you can take a photo of a page of text, and your computer will automatically read the text for you. Google uses OCR to digitize books.

How would you automatically figure out what number this is? You can use KNN for this: 1. Go through a lot of images of numbers, and extract features of those numbers. 2. When you get a new image, extract the features of that image, and see what its nearest neighbors are!

![[Pasted image 20240519214142.png]]
*Feature extraction is a lot more complicated in OCR than the fruit example.*
*But it’s important to understand that even complex technologies build on simple ideas, like KNN.*

When you upload a photo to Facebook, sometimes it’s smart enough to tag people in the photo automatically. That’s machine learning in action

The first step of OCR, where you go through images of numbers and extract features, is called training

## Building A Spam Filter
Spam filters use another simple algorithm called the Naive Bayes classifier. First, you train your Naive Bayes classifier on some data.