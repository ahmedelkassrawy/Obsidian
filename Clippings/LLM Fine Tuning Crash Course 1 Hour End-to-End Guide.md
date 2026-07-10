---
title: "LLM Fine Tuning Crash Course: 1 Hour End-to-End Guide"
source: "https://www.youtube.com/watch?v=mrKuDK9dGlg&list=PLrLEqwuz-mRIEtuUEN8sse2XyksKNN4Om"
author:
  - "[[AI Anytime]]"
published: 2023-12-30
created: 2026-05-03
description: "Welcome to my comprehensive tutorial on fine-tuning Large Language Models (LLMs)! In this 1-hour crash course, I dive deep into the essentials and advanced t..."
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=mrKuDK9dGlg)

## Transcript

**0:03** · hello everyone welcome to AI anytime channel so I'm starting a new playlist called finetuning of large language models in this playlist I will cover you know the different aspect of fine-tuning a large language model how to you know finetune on your data set you will have your custom data sets you want to fine tune llms in this entire playlist we'll

**0:26** · have multiple videos we'll start with the fundamentals and we starting in this video as well the fundamentals you know the different steps of pre-training fine-tuning and the Noel techniques like Laura and Kora how to select the right hyper parameters for fine tuning task what other tools that you can use to fine tune like Excel toll for example that we'll cover in this video which is a low code fine-tuning tool and you know

**0:50** · how to use Laura and Kora to fine tune uh with reduced memory uh consumption now in this playlist we'll have videos to F tune Lama 2 F tune Mistral fine tune open Lama and fine tune other open source llms and also the Clos Source One like for example you want to find tune the GPT models for example 3.5 you know on your data or the Vex AI models like

**1:15** · you know that that basically fuels the Palm uh Google B the Palm 2 models we also fine tune with those so this is completely focused on fine tuning this entire playlist will have at least 10 to 12 videos but the first video today we have going to talk about how to you know F tune an llm and how to select the tool

**1:37** · the techniques and the data set and how to configure and set it up uh in your infrastructure for example how to choose a compute what kind of cloud providers you can use so all those nuances will cover in this video this is a beginner friendly video where we when I'm uh assuming that you don't have fine-tuning uh experience prior to this video okay so let's start our experimentation with uh this first video where we look at the fundamentals of pre-training fine-tuning and the techniques like Laura and

**2:11** · Kora all right uh guys so when we talk about you know training llms there are essentially three approaches that we see and that's what we're going to look at here so what I'm going to write first is

**2:28** · training uh llms and we'll understand uh in very brief about these three approaches so the three approach that I'm talking so let me first write the three approaches so the three approaches that we're going to have is

**2:52** · pre-training and after pre-training we have fine tuning and then then we have on a very high level there are more but I'm just writing here which are the commonly used that we have used to fine tune in the community so these are three approaches pre-training fine-tuning Laura and Q Laura now fine tuning and luras and the

**3:18** · you know even if you go more Downstream uh I'm keeping this separate because I will explain why I'm keeping fine tuning separate uh than Lowa of course you can use use Laura qora to F tune we'll see that let's start a bit with definition

**3:36** · we'll go into code we'll also find tune uh shortly but let's first try to understand because when I talk to you know people who are trying to fine tune basically they lack the fundamentals or basic basics of these you know natural language or the terminologies that we see so I was talking to many of my you know um colleagues or Community friends

**4:02** · and I was ask them like what are Q projections what are projections that you see in the lowas that you target modules or whatever they had no idea about it and that's what I want to cover here that your fundamentals and Basics should be covered because rest of the thing I will show that how easily you can f tune with tools like Exel all and

**4:21** · we'll see that uh in a bit now what do you mean by pre-training now it's pre-training involves several steps now imagine if you have a massive data set of Text data so let me just write it over here you have

**4:40** · uh massive Text data now the source can be you know Wikipedia already Twitter now X and you have you have your own you know kind of an um your own proprietary data kind of a thing and these are mainly in terabytes okay we talking

**5:00** · about if you go to Lama 2 they say two or three trillion I think it's two trilon tokens we'll come to the tokens later but just imagine extracting or creating two trillion tokens would need at least even more than terabytes of data for you so in the pre-training step is first is that you need a massive text Data okay in in terabytes once you have that you then identify uh model architecture so let me just write here

**5:30** · identify the model architecture and here I'm covering because these topics are really vast uh but I'm just covering on the very high level but even once you have text Data the lot of pre-processing steps like you know removing pii you know looking at the D duplications kind of a thing a lot of other things that we look at but we'll explain that once we are fine-tuning okay but here just on very high level to give you a definition of pre-training fine-tuning and lowas and

**5:58** · qas now uh once you have a model architecture chosen or created specifically for the task at hand then you need a tokenizer okay so you need a tokenizer Let me just write it over here you need a tokenizer okay that is trained to appropriately handle your data handle the data ensuring that it can efficiently encode and decode text so

**6:28** · here I'm going to write the tokenizer will play two role one is of encoding and decoding not necessarily always encoding and decoding depends what kind of task you are executing we'll see that now your tokenizer is done then

**6:48** · once you have the tokenizer ready the data set that you have the massive data set that you created is then pre-processed using the tokenizer vocabulary okay so let me just write it over here data set is

**7:10** · pre-processed data set is pre-processed using the tokenizers vocab okay so you create the vocab vocab or vocabulary of your tokenizers using libraries like sentence piece that goes you know that that becomes one of the additions in the Transformers I will see that uh shortly now you have data set is pre-processed using you know tokenizers vocabulary so let me just write it over here tokenizers vocab okay now this is important because

**7:42** · this will convert the raw text that you have you have a raw text into a uh into a format that is suitable for training the model now here you will have once you have this after this St you will have a suitable you know uh uh data in a format for

**8:14** · training right now and this steps involve you know mapping uh tokens to the corresponding IDs incorporating necessarily special token so let me just write it because once I'm explaining the config file the yaml file once we find tune where you have lot of you know special tokens like EOS BOS blah blah blah this is how we'll cover that so suitable data in a format for training now here what we do now this steps involves so I will keep it uh like this

**8:46** · so This steps involve mapping tokens we we you would have seen something called map using when we are using tokenizer to map it now mapping tokens let me just write mapping tokens to the IDS to the respective or I think it's let's corresponding might be the right

**9:08** · word corresponding IDs and then you know uh incorporation of or rather let's right incorporating any special tokens special tokens okay or attention

**9:27** · mask can be other thing as well I just recall no attention mask okay now once the data is pre-processed now it is ready for uh training by the way these are the these are the part of the same so I will now uh these are the part that depends what kind of architecture you have chosen but now your data is ready you can pre-train

**9:50** · your your you ready to go into the pre-training phase now what happens in the pre-training phase okay let me let me write it over here what happens in the pre-training

**10:12** · phase now in pre-training Phase let me just write it the model learns to predict the next word in a sentence learns to predict the next word in a

**10:38** · sentence that's what happens or not only this because it can also fill in so we'll talk about what is filling and what is Generation fill in missing words as well so you can do fill in missing words as well so let me just write it over here correct this is what it does now

**10:59** · this process of course involves optimizing the models parameters you know like it's trial and error kind of an experimentation right this model you have to optimize through different parameters and that's an iterative training procedure basically that maximizes the likelihood of generating the correct word or sequence of word given the context now to accomplish this

**11:22** · pre-training phase we typically employs a variant of the self-supervised the learning technique the model is presented with partially masked input sequences where certain tokens are of course we intent intentionally hide that and it must predict those missing tokens based on the surrounding context and because we have a massive amounts of data right so we can train it on that now model gradually develops a reach understanding of language patterns

**11:53** · grammar and the semantic relationship now once we talk about filling so you have this fill in missing words that we are talking that's something that has been called as masked language model masked language model which is called MLM and when you talk about

**12:20** · Generation generation now that has been called as as are not limited to by the way but this has been called calar learning model that's called Cal language modeling excuse me not learning Cal language model or

**12:44** · modeling and that's why we use Auto Cal from know pre-trained or whatever when you use a Transformers pipeline now these are the most these are the used one we will be focusing on this this is what we're going to focus C language modeling now unlike masked language modeling where you know certain tokens are masked and the model predicts those missing tokens Cal language modeling

**13:09** · focus on predicting the next word in a sentence given the preceding context now this step whatever you just uh you just uh you just have seen here on the screen this step is a pre-training step here your model is now able to understand the language patterns Now understand uh the IC relationship and all of those things basically it gets the general language knowledge making the model A proficient language encoder right but it lacks a specific

**13:42** · knowledge so after after pre-training right you have a model now it capture General language so let can just write capture General language but you know it lacks and this is what we're going to look at the next fine-tuning step it lacks specific

**14:17** · knowledge lack specific knowledge about a particular task or domain or domain and that's why we fine tune because we want to fine tune it for a specific purpose now to bridge this Gap

**14:38** · a subsequent fine-tuning phase follows pre-training right that's where fine tuning comes in guys in the play now we'll look we'll talk about fine tuning right now we only covering theoretical aspect here we'll go into code a bit uh so uh in a bit now let's talk about fine

**14:56** · tuning if you want to skip this part you can also skip this you know but I will recommend that you should have the knowledge otherwise you will not be able to build or find you know whatever you'll be only having very high level knowledge if you want to achieve that you don't have to even learn those things those are so many low code no code fine tuning tool just upload your data and get a finetune model but if you

**15:17** · want to make your carer in this field you should understand everything from scratch which is required of course when I say everything don't go and read now Marco Chain by the way that will not help uh now once we talk about finetuning now after the pre-training phase where where the model learns General language knowledge fine tuning allows let me write with this now fine tuning

**15:49** · allows us to specialize specialize the models capability specialize the llms I'll write rather llms capabilities and optimize its performance and optimize its

**16:17** · performance okay or let me make it more descriptive on a narrower or a downstream task or a task is specific data set or something like that right let me just write task is

**16:35** · specific data set okay uh this is what we do now fine tuning of course if you look at the pre-training we have covered all of this high level steps text Data identifying the model architecture tokenizer blah blah blah now fing also uh similarly

**16:53** · also it also has many steps so you have you have a task specific data set that has been gathered that that will probably have labeled examples relevant to the desired task now for example let's talk about some a very famous word nowadays in Industry that has been used called instruct tuning or instruction tuned model we call about instruction tuned model now for instruction tuned model a data set of instru instruction

**17:27** · and response pair is gathered so first thing that you need a data set here again a task specific data set so for this if you are talking about instruction uh tuned model you need a data set of your instruction and response instruction and

**17:49** · response data set is gathered now these are basically pairs it can be a question answer pair now the finetuning data set size is significantly smaller than than the you know your pre-training so you don't need that huge data set now but of course even even for this case you need a sufficient uh uh like data set having

**18:11** · you know at least 10,000 question answer pairs or something like that now uh when the pre-training model is initialized with its previously learned parameters the model is then trained on task specific data set optimizing its parameter to minimize a task is specific loss function loss function means how of

**18:32** · the model was from the desired result that basically very lemon terms now I'm writing here uh task specific loss

**18:50** · function task specific loss function now during the fine tuning process the parameters that we will have from the pre-train models are then adjusted okay we we will'll focus on this word a lot that's called adjusted but let me write it over here only now uh the params let me just write like this the params of the pre-trained

**19:23** · model of the pre-trained model are adjusted are adjusted using you know and focus on this word adjusted we always talk about adjusting weights let's adjust the weight and all of those adjustment that we do with the weights it all Bo down to weights guys when you talk about fine tuning Now using something called gradient based

**19:51** · optimization algorithms not limited to but this is what has been used in the recent fine-tuned model that's called gradient based optimization algorithms and if you have worked with deep learning you will probably know about this gradient based optimization alos now one of these alos can be uh

**20:18** · SGD okay let me just write SGD or Adam uh whatever there are there are a lot more okay now SGD for example Le I hope I spelled it right uh sastic and I hope this is right sastic gradient

**20:41** · descent now the gradients are computed by back propagating the law so again the back propagation comes in okay so it the gradients are then first computed by back propagation the LW through the model's layers you will have n numbers of layers allowing the model to learn from its mistakes and update its

**21:01** · parameters accordingly now you will have a back propagation working there for you in this models layers that helps you the model will learn from the mistakes every time and then update the parameter so it improves itself now to enhance the fine tuning you will have you know different additional techniques here so let me just write it in the one point here more

**21:22** · about fine tuning then we move to Lura and Q luras and then we go up in a bit of fine tuning kind of a thing now uh okay so you can also improve as I was saying you can improve through you know uh learning rate scheduling okay there are there lot of other techniques that we can follow uh learning rate scheduling and regular regularization

**21:54** · method like dropouts or weight decays or early stopping to prevent overfitting and whatnot right now these techniques help optimize the models generalization always remember that your fin tuned model should not memorize but should generalize okay uh on your unseen data

**22:11** · or the validation of new data now model generalization and prevent it from memorizing as I said the train data set too closely now this is on the fine tuning step now we are moving towards some of the newly developed techniques uh in the ecosystem that's called a Lowa low rank adaptation they have a very good research paper on Laura everybody should read that paper low rank

**22:45** · adaptation now Laura is interesting without Laura we would not have seen this you know uh I'll say the rise of the open source llms like mral or Jer whatever you know the way we find unit because we do not have the resources to do that right so for people like you know the US the researchers the developers the people working in startups they need these kind of you know Frameworks to work with now because

**23:13** · see fine tuning is expensive as you know don't be live in a Dreamland if you are a a researcher or that you will be able to create something like llama to with a limited budget it's not possible when you see how Mistral has been trained they had invested Millions into that so you can of course fine tune a few models on your small data set but the performance then again will not be similar so it's fine tuning age so let

**23:43** · me write ft is expensive it's simple it's really expensive that requires you know 100 of GBS of virtual Rams the vram that's where GPU comes in guys you know to train you know multi-billion parameters models to solve this specific problem Laura was introduced okay it was proposed uh you know it's compared to compared to if you compare to fine tuning opt opt 175 B with Adam that that

**24:16** · has been the benchmarked in the paper also Lura can reduce the number of trainable parameters by 10,000 times and the GPU memory requirement by over three times just as in right now a 3X memory requirement reduction is still in the realm of unfeasible for us people like us because 3x is still not that right then that's we need Kora we'll talk about that okay so let's talk about so if Laura is giving you for example

**24:45** · and we will cover Laura in detail that's why I'm not writing a lot of things over here we will because we have to work with Laura and Kora when we are fine tuning so we'll focus on that now Lura uh 3x okay I was saying 3x X now 3x memory requirement now imagine but this is also not something that we can work with it even we need more and that's where Kora came in picture Okay so with

**25:11** · Kora and if you don't understand right now about Lura and K don't worry I will cover that each and everything in detail each and every line that we write in luras and Q the code the confix whatever the argument that we work with I will explain each and every line now Kora just word just add the word quantized so I'm not writing everything but quantization quantized okay a quantized

**25:37** · low rank adaptation it uses a library that's called bits and bytes okay so it uses a library called bits and bytes B andb this is a library that you know it uses on the Fly By the way and it

**25:56** · achieves a near lossless quantization so when I talk about lossless your performance degradation is not much of course there can be a bit of performance degradation or there will be reduction in the performance but that might be myth nobody has you know has done a really a research on big sample

**26:16** · that that really happens once you quantize the llm but of course there can be a bit of performance degradation but that's why we calling it bits and bites and that provides you a lossless quantization of language models and applies it to the Lowa procedure because QA is based on luras by the way now this

**26:37** · results in a massive reductions in memory requirement enabling the training of models as large as like Llama 270b Or you can do that on you know for example 2x 2x RTX 3090 you can do that you can also uh and

**26:59** · and by the way if you compare let me just uh write it okay let me just do it if you compare without Kora this will take around a00 which is one of the most used GPU to train llms or create llms you need which is by the way 800 is 80GB 80GB GPU now you you need 16 x you need 16

**27:25** · different a00 gpus not one GPU node that you need you need 16 okay so just imagine how much it reduce if you use Kora you know it boils down to 2 RTX 390 and of course if you have 1 a00 much better okay to do that uh but just imagine uh and the cost goes down once you use loraa and Q okay now let's see the question comes

**27:52** · in that okay we have been talking about all of this thing how can we achieve our task how can we you know F tune what kind of machine we have to use and all of the question that you will have in your mind so for that I will tell you that let's go into fine tuning so let me

**28:08** · just write over here fine tuning we are now going into uh fine tuning step uh in this tutorial that I'm creating you know we'll be focusing of you know 6B or 7B llms not more than

**28:26** · that because I want to keep it as a tutorial you can explore yourself if you have compute and all I do have compute but you should learn and you should of course do it yourself right now the first thing that you think will come in your mind is training compute that tell me about training compute and that's what I also you know get worried okay training comput now for

**28:53** · training of course you need a GPU to do that we'll talk about model and data set separately that's something that we'll have something uh now if you want to F tune uh model like Lama 27b or Mistral 7B let

**29:09** · me just write it over here now these are the model I'm writing because this models are commercially available to use with an Enterprise you can make money you know using these models guys because you'll be building a product so don't see that just you'll be making money by using this model but once you build a product on top of this now Lama to 7B and mral 7B if you want to F tune on a very uh on a very high level I'll say these are the requirement that you need the alha talk about memory and this is based on Uther Uther

**29:42** · AI Transformers math 101 blog post I will give the link in description if you want to understand how calcul calculations work you know to decide a compute you should look at Transformer math 101 blog post find the link in description now now the memory

**29:59** · requirement is around let's keep it like 150 to 195 GB this would be the memory requirement you know to F tune okay now so renting gpus now the next thing is how to rent gpus or how to use a GPU there are many options that you can consider uh one is uh the most I will

**30:28** · it's not in any order but I will write in my Preferred Choice okay uh in an order I rely on runpod runp pod. I rely on runp pod then there is V AI then there is Lambda

**30:48** · labs and then then you have hyperscalers like big players you know I will just only write AWS say maker because I have worked with it a lot so these are the top and you have your Google collab also how can I forget collab our life saer right now run pod is my Preferred Choice

**31:08** · hands down run pod is my preferred choice I will recommend you to choose runp or between Lambda Labs but Lambda Labs service support and all that are very bad okay so runp pod is something that I recommend it's extremely easy to work with and also affordable if you're looking for cheapest option that you can afford which is V so let me call it

**31:29** · here cheapest I'm writing cheapest I'm not writing affordable affordable is like runp now here security can be a concern so look at if you looking at secure cloud or Community Cloud kind of a thing I recommend runp that's I said okay now if you have a super computer you can also do with that but I do not have now the next thing is uh once you have training compute decided once you have a training compute then you have to gather data set I show you that how you can get a data set if you do not have one the main

**32:01** · source for learning purpose is hugging face data sets once you have the data set and I'll cover a few things in data set because you know once if you have you are creating your own data set you have to look at something called Uh there's few things you have to look at one is diversity in data you do not want your models to only do one very specific task you know you should have a bit of diversity now

**32:26** · assumed a use case like you know you're training a chat model that does not mean that data would only be about one specific type of chat right you you will want to diversify the chat examples you know the samples uh

**32:42** · like different scenarios so model can learn how to generate outputs of various type of input now imagine one of your Ender comes in and start putting about some question that your model have not even seen you know so at Le those kind of things so it it understands the semantics better now the size of data set on a very uh like a thumb Ru your

**33:04** · file size should be 10 MB that's how I decide if you are using a CSV with question answer payers your file size should be 10 MB that's how I go with okay 10 MB of your data okay now or at least I'll recommend 10,000 question answer pair and the quality of data the this is important because if you look at the latest model and this is the most important by the way this is the most important thing F example F llm by

**33:36** · Microsoft or Orca for example these are the examples where organizations have shown that how a better quality data can help you you know train an llm on a very smaller size like 3B or 1.5b kind of a parameter of parms this is important to understand now we'll not talk about data at this moment let's let's see that so to use runp pod what we have to do is to go to runp pod uh dashboard here and you can see I

**34:10** · already have a template has been deployed but it's very easy to do that you have to come to secure Cloud you can also look for Community Cloud but I prefer this it's Community cloud is bit cheaper because your GPU can be also availability is an issue on community Cloud because the same GPU can be rented by somebody else's as well if you are not using that now that's on the community Cloud uh on secure Cloud they

**34:35** · have two things latest generation and previous generation on latest generation you will see the latest of gpus like h00 which gives you 80GB vram with 250 GB Ram you know which which is the most expensive one over here then you also have previous generation with a00 then that's what we're going to use okay so a00 you can see almost $2 per hour so

**34:59** · one hour training you cost $2 so on for example if you have decent enough data set like 2,000 3,000 rows $5 you'll be able to uh do it now uh for that let me first show you a couple of things we have eight eight maximum that you can uh you know spin up over here the eight different node of that particular 800 GPU but this is not what we want to do okay uh so let's see how we can deploy

**35:25** · it uh uh how we can find unit so I already have deployed what you have to do you have to click on deploy and it will deploy it will take a few minutes to deploy it and then there will be option to connect once you click on connect it will show open Jupiter lab and that's what I did over here I have a Jupiter lab now the first thing that we have to do is we have to get clone the Excel toll so let's get clone so get

**35:49** · clone uh and then we'll take that from here so come over here let me just click on this this this and then you clone you'll see a folder here now let's let's go inside the folder in the examples you will see different models which are supported you can also see the mial are also supported very soon in this okay if you click on mial you will see mial yaml so mial is also there 8X 7B model by

**36:15** · Mistral the mixture of experts now if you go back to examples you will see Cod llama Lama 2 Mamba Mistral MPT pythia red Pama and some other LMS are also there let's open for example open Lama so if you open open Lama you will see config yaml now in config yaml you will see all

**36:35** · these details I will explain each and everything you know in a bit what what do we mean by loading 8bit loading 4bit what is Lura R which is not there because that will be in your QA or Lura if you click on Lura yal this is a configuration file which helps you you know Excel toll basically takes this single file as an input and F tune your model here you have to Define your data set if you look at the data set it says gp4 llm clean there is nothing but this

**37:01** · is available on your hugging face repository so basically T the data from there but you can also do it from locally as well so if you have local uh uh machine where you are running this and you have your data locally you can also uh uh assign the path from that local machine as well it has your validation adapter blah blah blah and we'll explain that everything uh in a bit what do we mean by qware bits and

**37:25** · bite things will come in picture you can see load in 4bit will be true for Q because we want to load this model in 4bit and something like that right let's do that so what I'm going to do is uh first thing let me go back to my folder here and you will have a requirements txt let's expand that now you have your

**37:45** · requirements txt now in requirement txt we'll find out everything okay what are the requirements thing that you know you have extra and Cuda you are getting from here and lot of other things that you are getting now uh we'll make some hashes we don't need this or rather what we can do we can just remove this from here we do not need this anymore because we already have Cuda with us over here

**38:10** · now Cuda is not required any other cudas that you see I do not see any other cudas over here I'm just looking for torch Auto packaging pip Transformers tokenizers bits and bytes accelerate deep speed you know uh add fire pyl data sets flash attention you can see 2.3.3 sentence piece wend B ws and biases eops

**38:39** · X forers Optimum HF Transformers Kama Numba Bird score for evaluation evaluate R rou score for Val evaluation as well you know we have psychic learn art FS chat graduate and fine let's save this here here okay now once you save it I'll just close this now let's go CD inside it have to CD so let's do CD so CD XEL

**39:07** · to and you can see ax AO I am always you know typing it wrong but I'll just CD inside it and let's do a PWD to find out what is my present working directory you can see it Exel tall uh now the next thing that we have to do is okay we have to look at the inst installing the packages let's do what they suggest I'm going to do pip install packaging the PIP install packaging will is a requirement already satisfied the next thing is PIP install and then hyphen e which

**39:38** · basically says okay within this directory or we can you can also take it from you know their uh I'm saying okay flash attention and deep speed so let me just do not need that okay deep speed okay flash attention and deep speed uh to let's run

**39:59** · this what what are the thing that I am making a mistake uh deep speed flash attention H it should not be dot here my bad it should be dot should be the outside of

**40:14** · here okay you have your flash attention and deep speed thing going on okay over there it will install everything which is in your requirements txt you can see Bird score Numba sentence piece which the dependency of Transformer helps with you know vocabulary addition tokenizer blah blah blah know pep has been installed bits and bytes accelerate that's looking good uh let's see it out over there come down flash attention make sure you have

**40:42** · flash attention greater than 2.0 flat flash attention one point will give you error okay uh let's come down it's installing it once you install that you have you can also go to the data set path if you don't want to use this data you can also do that with other data as well but I will keep the same data but we can make few changes if you

**41:05** · want let's know because we are relying on Laura here we'll use Lura so if you come to Lura okay let me come to Laura low rank adaptation now once you come to Laura you can do a bit of changes like you know let me see what is the EPO okay uh where is that uh number of

**41:26** · epoch this is too much I don't want four Epoch okay let's do it for one Epoch okay so for we'll do it for one Epoch okay the number of epo become your number epox become one micro batch size I will also make it one and gradient accumulation steps I'll make this eight

**41:45** · okay I will explain that don't worry if you don't understand these terms we'll explain each and every this terminologist which has been written over here now I made some changes uh and then I'll go back back and then I will execute my learnings okay that's what I'm going to do okay now let me just do a

**42:04** · save okay uh and if you come you can also see it over here this how you can train it out you can see it says uses this how you can train this is how you can inference all right so execution of learning will happen like that so let's come to fine tuning here okay now we are done we'll add few sales and once you have done all of these changes let's go back and maybe you can copy this thing uh quickly let's copy this let me come over

**42:37** · here and I have to add that you can see excelerate launch hyphen M Exel to CLI train examples it has open Llama now for example if currently you see it says open Lama now you have to go to open Lama 3B I don't know which one I changed up okay uh if you go to

**43:00** · Laura yeah uh yeah this is what I also changed okay fine now let me just uh close this one low yl and let's run

**43:15** · it now once you run it you will see a few warnings you can ignore those warnings don't not have to worry about those warnings you can see it's currently downloading the data from hugging face it will you know uh create a train and validation splits you can see it's currently doing it will also map the to with the tokenizers will also do that you can see it's happening happening over

**43:46** · here you have to wait for all these process basically what they do guys right it's imagine this as a low code fine tuning tool if you don't want to write a lot of code you just want to make some changes because they already have created the yaml for you okay this is what they have done you can see total number of steps total number of tokens over here find out the total number of tokens currently getting the model file which is PCH model. bin the file that it's

**44:17** · getting you can see it's around 6.85 GB you know runport is basically will have some cash of course definitely they will have some cash and contain cast in the container because you know you are just fetching it from hugging fish directly that's why it's bit faster if you do it of course locally it will probably be not that FAS okay uh it will

**44:38** · take a bit of time let's see how much time it takes I don't want to pause the video because I want to show you each and everything that goes if you want to you can skip the video of course you can see you know extra special tokens EOS BOS paddings total number of tokens supervised tokens all those details over here which have been listed okay that you can find it out

**45:04** · once the model has been downloaded which is your pytorch model. bin the next thing that we have to do it will also load the model okay so basically once it load the model in the in that uh once it loads the model you Cuda kernel should be there because once it's loading it needs GPU to load that okay on on a device that's when we do dot two device or something to you know pipe that with CA

**45:39** · okay you can see it says starting trainer so it has a trainer argument I will explain that don't worry if you do not know about trainers and all we'll explain each and everything in detail now guys what will happen you see can it has started training okay you can see efficiency estimate total number of tokens per device it's training your on your data now what I'm going to do is I'm going to pause the video till it train or F Tunes it and then we'll look after that all right uh so you can see

**46:07** · uh it has been fine tuned the model that we wanted to fine tune we have fine tuned the llm and you can find out uh train samples per second train runtime train steps per second train loss EPO it has been completed 100% it took more than 1 hour it took around 2 hours you know it took 1 hour 55 minutes you can see it over here uh let's go back here in the workspace Exel all and you can find out here you have a

**46:40** · folder called Laura out now in Lura out you have your last checkpoint and you can keep on saving checkpoints we'll cover that maybe in the upcoming videos where we will have a lot of videos on fine tuning now but what I'm trying to say is that you can also save it on multiple checkpoints for example if you want to use a th checkpoints with you can also do that but you can see here we have our adapter model. bin and adapter config right now you can also merge that

**47:06** · with Pip but I'm not covering that part right now here because you would have no idea about pip if you a beginner so now you just you just saw that how we find tuna model and we got our checkpoint weights over here you can find out this is the last checkpoint if you want to use this which has a config Json which

**47:25** · has if you click on the config Json it will open a Json file for you then you have your you know safe tensors okay the model weights then you have Optimizer dopy PT then you have your scheder you have your Trend State you can file out all the related information over here you can also close this target module seven items you can find out all the different projections I will cover each and everything in detail what do we mean by this now it shows that uh sometimes

**47:52** · it gives you error uh if you look at this gradi if you run this gradio sometimes in runp it it gives you an error also because let's try it out try it out our luck here I just want to show you that you can also do that yeah gradio installation has issues with in within runp pod sometimes when you are using it but anyway uh we'll move if it works

**48:19** · it will open a gradio uh for you a gradio app gradio is a python library that helps you build you know uh web apps okay you can see it says running on local over here okay now it runs on a local URL okay you have to probably do a true uh s equals to True something to you know get it on a URL okay now you can also click on let's click on this now once you click on this it says this share link expires in

**48:50** · 72 hours for free permanent hosting and GPU upgrades run gradate deploy okay now you can see that we have an axel toall gradio interface okay now here you can try it out now if you let's copy this and see what kind of response or even if it's generating any response or not so if you click on this it will either give you an error or

**49:14** · it says okay you can see give three tips for staying healthy and you can see it out over here eat a healthy diet consume plenty of fruits vegetables whole grains lean proteins blah blah blah and you can see the speed as well because we are on 800 right now that you know and it's generating your responses pretty fast right look at the tokens per second over here now you have an interface that that is working on your data your data that

**49:37** · you have from hugging face for example we have used Alpa here Alpa 2K test you can see it's how it says how can we reduce air pollution let me ask a similar question but not exactly the same so what I'm going to ask here is tell me the ways I can reduce pollution let me ask this

**50:01** · question and I'm asking tell me the ways I can reduce pollution it says make a conso and when you are working with python you have to use a prom to look at the uh basically to par the output a bit but this is fantastic right now you can see it says make a conscious effort to walk

**50:17** · bike or car Pole to work is school or irand rather than relying on a single occupancy vehicle huge public transportation car pooling blah blah blah Reduce Reuse and recycle talking about a bit of sustainability over here now this is fantastic you saw in two hours at least for one EPO of course that is fully customizable as we saw in the uh over there in the yaml files but

**50:41** · this is how easy it is nowadays to F tune guys we'll now talk about we'll go back to our uh cast here and we'll talk about each and everything in detail okay now how did we find tune what are the sh config that we have considered and all of those things so let's start our journey with all these parameters now let's understand how Laura works and what is Laura and how these parameters are being decided that we have seen in

**51:09** · the yaml file as well so let me just write about Laura here so we're going to talk about Laura now now it's a Training Method let's see this as a Training Method let's keep it lemon so you can understand better it's a Training Method so I'm writing it's a Training Method to designed to ex designed to expedite the training process of

**51:47** · llms training process of llms this helps you with of course memory consumption it reduces the memory conj by introducing something called pairs of rank decomposition weight matrices this is important so what I'm going to write here is look at this word here okay something called rank

**52:15** · decomposition and basically that's a pairs so I'm going to write pairs of rank decomposition matrices and this basically also known as right we have a as we also talked about this earlier called update matrices okay and you will have some existing weights already of the pre-trained llms that we're going to use so basically you know it it helps you you know add these

**52:47** · weights okay training this basically the new added weights okay now there are three things that you should consider when we talking about loraa the first is the or I'll say three or fours let's let's understand that okay preservation of pre-trained Weights so let me just write it over here so preservation of pre-trained

**53:20** · Weights that's the first thing now what we understand by this like Laura basically maintains the Frozen state of previously trained weights that basically minimize the risk of catastrophic forgetting now this particular step ensures that the model retains it existing knowledge so let me just write it over here okay

**53:46** · model retains the its existing knowledge while adopting to existing knowledge while adapting to the new data that's why we call it right that LM still has the base knowledge and that's why sometimes it hallucinates gives it from the base knowledge right while adapting to new

**54:14** · data now the second thing which is important for you to understand the portability of trained weights can you port that okay so let me just write it over here portability of trained

**54:32** · weights the rank decomposition matrices that that gets used in loraa have significantly fewer parameters of course right that's why it helps you with the memory reduction right when you compare this with original model now this particular characteristic allows the trained loraa weights to be easily transferred and utilized in other context making them highly portable so it's highly portable now the third thing is the

**55:01** · third advantage that we're going to talk about is integration with attention layers integration with attention layer now Lowa matrices are you know Incorporated basically into the attention layers of the original model the adaptation scale parameters we we'll see that parameter once we are looking at the code allows control over the

**55:30** · extent to which model adjust to the new training data and that's where we'll see about you know alpha or the scales that has been used now the next one is memory efficiency that's the advantage that we also talk about is memory efficiency now it's improved memory efficiency as we know opens up you know the possibility of running fine tune task unless then as we discussed earlier 3x the required compute for a native fine tuning process say without Laura

**55:56** · let's look at the Lura hyper parameter let's look at the code now to understand uh the Lura hyper parameter so go to examples of the same exal GitHub repository let's open any we trained basically open Lama right find now you can also open Mistral Also let's open oh let me open Mistral now to show you so you can see I'm opening Mistral and the mistal let's go to Kora now on the cura I will first talk about the Laura config let me make it

**56:27** · bigger so you can see it and let's talk about this these are your Lura hyper parameters that we're going to talk about and I will explain that what we mean by this you find tun any llms you go to any videos any blog you will see this code now you should have you should have the understanding you should know that what are these means okay so let me just show you over s it over here that what are these things mean now on the memory efficiency

**56:56** · the next thing that we're going to talk about is Lowa hyper parameters so I'm just writing Lura hyper parameters now the first thing if you go back you have something called Lura R which is nothing but the Lowa rank okay so let me just write first thing you should know what is Lowa rank okay so let me just write it like that okay that's called basically your Lowa rank low rank adaptation rank what do we mean

**57:26** · by lower rank gu this basically determines the number of rank decomposition matrices rank decomposition is applied to weight matrices in order to reduce memory consumption and computational requirements if you look at the original Lura paper recommends a rank of R equals

**57:48** · to weight eight okay so by standard let me just write here you know by the paper they recommend standard r equal to 8 but here you can see for mistal you know in Axel to GitHub repository for mral is it's has been written 32 and eight is the minimum amount keep in mind that higher rank if you have higher rank leads to better

**58:16** · results better results and there's one tradeoff now but for that you need High compute so now you should know that if you are getting any errors like okay you have you know taking a lot of computational power you can play around this hyper parameter which lower rank make it eight from 32 make it 16 or or something like that you know even know it's a trial and error experimentation now the more complex your data set your rank should be higher

**58:44** · if you have a very complex data set where you have lot of relationship a lot of derived relations and so on and so forth you need your rank to be on the higher side okay okay now to match a you know a a full fine tune you can set the rank to equal to the models hidden size

**59:04** · this is however of course not recommended because it's a massive waste of resources now how can you find out the models hidden size but of course you have to go through the config Json by the way okay or so there are two ways of reading or basically finding out so let's say is reading hidden size now there are two way one is config

**59:29** · Json and the other is that you can do it through Transformers Auto model Transformers Auto model I I think I can quickly you know write the code here so let me just write the code for you now this is how you have your auto model so from Transformer let's quickly get it so for example from Transformers

**59:59** · import you have Auto model as we as we do it we do auto model for Cal so you have your Cal LM that's how you import you define a model name then you'll have an identifier so let's define that model name whatever then you have your that you basically get your model now through Auto model something like that now how do you find the hidden size this is the code to get the hidden size you do it something called Model do

**1:00:30** · config do hidden State that's how you do it hidden size and then just print the hidden size This Is How We Do It print the hidden size right let me open uh here Lama 2 let's go to you know any of this okay it's fine

**1:00:59** · you can see it over here hidden size is here 8192 right this is your hidden size you can find it like here also and you can also find it you know through Transformers Library as on but this is not recommended because it's a waste of resource otherwise why would you use Lura then but this is what it is right if you want to really achieve those performances of pre-training uh like how meta has created Lama 2 or M A has cre Mistral the next is let's go back next

**1:01:30** · is Lura Alpha okay so let's write it Alpha here this is a scaling Factor now I'm writing Lowa Alpha now it's a scaling factor for the Lura determines the extent to which the model is adapted towards new TR the alpha value adjust the contribution of the

**1:01:51** · update matrices during the training process or during the train proc process lower value gives more weight to the original data so if you have lower value it gives more weight to the original and it maintains the models existing knowledge to a greater extent so it will it will be more inclined towards the you know your base knowledge the base data that you have so let me just write it so for example you you will able to uh make a note of it I will write lower

**1:02:22** · value Gibs more weight to the original data to the original data and maintain maintain the

**1:02:46** · models existing knowledge knowledge to a greater extent let's try it like this okay this is what now if you can see here it says Lowa Alpha and that Lowa Alpha is 16 you can make eight also you can make 16 also that depends now the next is let's talk about Lowa Target modules which is again

**1:03:15** · very important you know talking about the Lowa Target modules that you see over there now Lowa Target modules is one of the important thing so let me just write Lowa Target

**1:03:30** · module oh you cannot see it I just noticed Lowa Target module now in the Lowa Target module here you can determine which specific weights and matrices are to be trained the most basic ones to train are the query vectors that's basically called Q projection okay you would have seen that word q projection so the most basic ones are the query ve query vectors and value vectors so let me just write it over here you know query

**1:04:05** · vectors and then you have value vectors that's called Q projection Q Pro and this called V Pro these are all project projection matrices the names of these matrices will differ from model to model of of course depends on which llm you are using you can find out the exact names again there's a what you have to do keep the same code AS written above just make one changes which is your layer

**1:04:35** · names so layer names we you know basically it's a dictionary that's how you'll get it let me so it write it over here model. State dict model do state dict and then do keys this is how you will get the and

**1:04:53** · basically you need a for Loop now because there will be n number of layers so you can get the for name in layer names and then you can print that so you'll see Q projection you know you will see K projection you will see V projection you will see o projection you will see gate projection you will see down projection you will see up projection layer Norm weight blah blah blah right so there can be n number of Weights now the naming convention is very easy model name do layer layer number component and then it goes like that so this is what you should note the

**1:05:21** · Q projection the projection matri Matrix apply to the query vectors in your attention mechanism of the Transformer blocks transforms the input hidden states to the desired dimensions for Effective query representation and V projection is bit different it's called a value vectors in the tension mechanism transforms the input hidden states to the desired dimension for Effective value representation so these two are very important Q Pro and V Pro there are others like that like K Pro which is key vectors then you have o Pro different so

**1:05:54** · you can keep on looking at you know different basically oo are nothing but the output to the attention mechanism so you know so however three or four you know there are outliers as well we have to look at outliers they don't follow the naming convention is specified here that I'm writing but they have embedding token weights embed tokens normalization weights normalize then you have LM heads these are also if

**1:06:19** · you go back by the way excuse me sorry then you have your you know which is not of course here here because this might not be using it but you have LM head let me just write it out over here you have LM head so you have LM head then you have embed

**1:06:37** · tokens then you have embed tokens then you have normalization Norm these are also that we consider when we are training it now the LM head is nothing but the output layer of a language model language modeling I will say rather it's responsible for generating predictions or scores for the next token based on the Learned representation from the preceding layers the previous one you know basically they

**1:07:03** · are placed in the bottom so important to Target if your data data set has custom syntax LM head is very important let me just write it over here if your data if your data has custom syntax which is you know really

**1:07:22** · complex embed token they represent the parameters associated with the embedding layers of the model is like very self-explanatory usually placed at the beginning of the model as it just has to map input tokens to their Vector representation you have your input tokens you have to first convert it to a vector then the model will be able to understand right it it needs a numerical representation it cannot understand your text Data it's important to Target again if you have your custom syntax so this goes same now normalization is very like

**1:07:53** · know very I say common it's a normalization layer within your model used to improve the stability and convergence so basically helps you with the convergence of you know deep neural networks this is what we look at the Lura guys then we look at the Q Laura now in QA we talk about few things we'll talk about if you go back here let me just

**1:08:21** · explain QA bits and bytes will be on somewhere here so basically just explain so quantized Lura is an efficient fine tuning approach you know even makes it more uh memory reduction so it include few things the number one is back propagation so let me just write over here back propagation of

**1:08:48** · gradients through a through a 4bit quantized you know through a frozen let's write uh through a frozen 4bit quantized 4bit quantized which is very very important quantized into

**1:09:08** · Laura that's the first thing the second thing is it's basically uses of a new data type called nf4 you would have seen that nf4 that's word now what do we mean by nf4 that's called 4bit normal flat excuse me not flat flat float 4bit normal float now 4bit normal float basically

**1:09:31** · you know optimally handles normally distributed weights you will have your distributed weights it basically helps you optimize those it's a new data type you see nf4 so if you make nf4 true you have to use bits and bytes and all for of course for that as well now you have your nf4 then you also have few other things like paged optimizers double quantization you know to reduce use the average memory footprint even further by quanti quantizing the quantization

**1:09:58** · constant now these are the things that are associated with Laura and qora then you have your hyper parameters like batch size and aox now I'll explain that you don't need the tab or this to explain that because these are very common so now you understand this part this part is very much self-explanatory a base model code of you know you use

**1:10:18** · any fine tuning code take it from medium take it from other YouTube videos anywhere you will find this code on very similar 99% of the code will be same only thing that you have to change is your data and the way you tokenize and map those that's it and few of the times if you are using some other LMS now your data set is this you have your data set where you are you know storing

**1:10:38** · it data set validations output directory qora out then you have your adapter which is qora then the sequence length you can see it says 8192 P to sequence true Laura I I have already explained this part here Wenda B which is weights and biases okay weights and biases for you know machine learning experimentation uh tracking and monitoring now we'll talk about uh a few

**1:11:08** · things which is important let me first come down okay this is special tokens we have covered it now let me just go up and explain that to you okay now what is number of epo guys let's talk about about number of number of epoch the number of epoch excuse me the number of AO is an hyper

**1:11:34** · parameter in gradient descent you would have seen the maxima and Minima you would have seen this that that hyper parabolic or parabolic graph once we see the way you know back propagation works and the model learns and the when we talk about neural networks hyper parameters in gradient descent which controls the number of complete passes through the training data set each Epoch involves processing the entire data set once and the models parameters are updated after every Epoch

**1:12:06** · now batch size is a hyper parameter in again gradient descent that determines the number of training samples processed before it's in batches it stands in the batches how many sample are used in each iteration to calculate the error and then adjust the model in your back propagation steps we'll talk about stochastic gradient descent it's an

**1:12:23** · optimiz algorithm as we discussed earlier to find the best internal parameters for a model aiming to minimize performance measures like logarithmic loss or a mean square error msse and you can find it out more on the on internet as well about that yeah so now batch gradient descent sastic gradient descent and mini batch gradient descent there are three different ways commonly used you know for training the models

**1:12:52** · effectively now you would have sometime this question the difference between the batch versus Epoch so the batch size is the number of samples processed before the model is updated the number of epo is the number of complete passes through the training data set so these are two different NS understand with a quick example I'll just show it this is the last maybe that I will show but let me uh show that okay over here now assume you have a data set so you have a data set of 200

**1:13:27** · samples a rows or it can be question answer pair of rows in a csb and you choose a batch size of five so for example batch size of five and AO is th000 this will not we will not do it in a fine tuning llm because the computer to Too Much five now this means the data set will divided into how many the data set will be divided into 4 40 batches so dat will be divided into 40

**1:13:59** · batches because you have 200 samples it has to be in 40 batches 40 batches each with five samples how many each with five samples right now the model weights will be updated after each batch of five samples after each batch of five samples model weights will update model weights will get

**1:14:31** · updated now this will also mean that one Epoch will involve 40 batches or 40 updates to the model how many one aoch will involve 40

**1:14:48** · batches or 40 update this is very important guys you should know the fundamentals to fine tune the best way right now with 1,000 aox the model will will be exposed to the entire data set 1,000 times so that is total of how many 40,000 batches just imagine how much compute power do you need to do that so the larger B size results in higher GPU memory right higher GPU

**1:15:21** · memory and that's where will be using gradient accumulation steps you see this here gradient accumulation steps that's why it is important right gradient uh that that has been used to overcome this problem okay over there now you have learning rates you can see 0.02 learning rate is not that like you know so SGD stochastic gradient descent

**1:15:47** · know estimates the errors and the the way it learns right so think of learning rate as a no that control the size of steps taken to improve the model if the learning rate is too small the model may take a long time to learn or get stuck in a suboptimal solution it might might get a local Minima right so on the other hand if the learning rate is too large the model May learn too quickly and end up with unstable so you need to find the optimal or the right learning rate right you know it is important as well now the learning rate what else do we have so

**1:16:18** · gradient accumulation is very important so higher batch sizes results in higher memory consumption now that's where we bring gradient accumulation Ms to fix this it's a mechanism to split the batch of samples so you will have your for example you have a global badge let me just draw it if I can let me show it you cannot see if here Global badge then you will have your uh mini badge so let me call it MB

**1:16:48** · so you have mb0 then you have mb1 mini batch one and you can you can see it over here that's called micro batch size two right it's all associated with it mb1 then you have mb2 and then you have mb3 now imagine if you have this then you have grad zero again this will be the inside only so you have grad zero you have grad one you

**1:17:11** · have grad two gradient two basically and then you have grad three and then you have Global batch gradient very very interesting right Global batch gradients now into basically it splits into

**1:17:29** · several mini batches of samples that will be run sequentially right now I'm not covering back propagation because I hope that you know what is back propagation if you don't I will recommend to watch you know some of the videos which are already available on uh YouTube there will be n number of videos for that but yeah I think that concludes

**1:17:48** · for I think this part guys so what we did in this video you know now you'll be able to to understand each and everything over here now you know what is gradient checkpointing and these are like warm- up state after how many steps you want it to warm up how after how many EPO you want to evaluate the model on your validation data whatever you know your saves after how many EPO you want to save the weights and all of those things right so these are bit uh

**1:18:12** · again you can go and there can be others uh parameters as well but I wanted to cover as much as possible now what we did in this video guys so far it's a big video it's a lengthy video I know but I will recommend you to watch this video completely as I said in the beginning as well we started with the understanding

**1:18:32** · of pre-training training llms we looked at the three different approach let me summarize it we looked at the three different approaches pre-training fine tuning and Laura and Kora we covered all of this theoretically till high level on here and then we moved after training compute to run pod and on the runp we set up something called Excel toll you know Excel toll is a low code uh fine-tuning tool for you so when

**1:19:01** · I say low code you should understand how it works but you know it's very very very powerful it's really important to use this kind of tool to help on you on your uh productivity and it helps you become more efficient once you are fine tuning it so we looked at Excel toll to fine tune a large language model on this particular data which is Alpa data I

**1:19:22** · also shown that how where you can change your data you can look at a jonl file and then you can f tune right we F tune it for 2 hours almost and we got a gradio application that we saw you could see that how easy it is to spin up a gradio that's already there for you and we tested out with couple of prompts and then we are ending with all of the hyper parameters that are important as are required you should know it we explain that I hope you understood you got some clarity now and you will have enough understanding to now fine tune an llm

**1:19:52** · this ends our experiment guys in this video that's all for this video guys I hope you now have the enough understanding of how to fine-tune a large language model and how to select the optimal hyperparameters for the fine-tuning task and how can you use tool like Excel toall that's the low code uh tool for fine-tuning llms this

**1:20:19** · was the agenda of the video as well to give you enough understanding and where I wanted to cover the fundamentals of pre-training fine-tuning and the novel techniques like Laura and Cur if you have any thoughts or feedbacks please let me know in the comment box you can also reach out to me through my social media channels please find those details on the channel about us on the channel Banner that's all uh for this video

**1:20:44** · please like the video hit the like icon and if you haven't subscribed the Channel please do subscribe the channel share the video and Channel with your friends and appear thank you so much for watching see you in the next