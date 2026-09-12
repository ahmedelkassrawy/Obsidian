In this chapter, you will learn the mechanisms of various GenAI models and how to serve them in a FastAPI application

how to preload models for efficiency, and how to use FastAPI features for service monitoring.

we will progressively build a FastAPI service using open source GenAI models that generate text, images, audio, and 3D geometries, all from scratch.

will show you how to serve models across a variety of modalities including:
- Language models based on the transformer neural network architecture
- Audio models in text-to-speech and text-to-audio services based on the aggressive transformer architecture
- Vision models for text-to-image and text-to-video services based on the Stable Diffusion and vision transformer architectures
- 3D models for text-to-3D services based on the conditional implicit function encoder and diffusion decoder architecture
---
### Language Models
we talk about langauge models including transformers and RNNs

Transformers VS RNNs
![[Pasted image 20260911184358.png]]

RNN models historically was used to learn patterns in sequential data such as "free text"
To process text, models chunk text into small pieces as a word or char called token that can be sequentially processed

RNNs maintain a memory store called a "state vector", which carries info from one token to the next throughout the full text sequence until the end.This means that by the time you go to the end of the text sequence , the impact fo early tokens on the state verctor is lot smaller compared to the most recent tokens

Ideally, every token should be as important as the other tokens in any text. However, as RNNs can only predict the next item in a sequence by looking at the items that came before, they struggle with this ideal in capturing long-range dependencies and modeling patterns in large chunks of texts. As a result, they effectively fail to remember or comprehend essential information or context in large documents. With the invention of transformers, recurrent or convolutional modeling could now be replaced with a more efficient approach. Since transformers don’t maintain a hidden state memory and leverage a new capability termed self-attention, they’re capable of modeling relationships between words, no matter how far apart they appeared in a sentence. This self-attention component allows the model to “place attention” on contextually relevant words within a sentence. While RNNs model relationships between neighboring words in a sentence, transformers map pairwise relationships between every word in the text.

![[Pasted image 20260911184841.png]]

What powers the self-attention system are specialized blocks called attention heads that capture pairwise patterns between words as attention maps

- A transformer model contains several attention heads distributed across its neural network layers.
- Each head computes its own attention map independently to capture relationships between words focusing on certain patterns in the inputs.
- Using multiple attention heads, the model can simultaneously analyze the inputs from various angles and contexts to understand complex patterns and dependencies within the data.

![[Pasted image 20260911185532.png]]

- RNNs also required extensive compute power to train, as the training process couldn’t be parallelized on multiple GPU due to the sequential nature of their training algorithms.

- Transformers, on the other hand, process words non-sequentially, so they can run attention mechanisms in parallel on GPUs.

The efficiency of the transformer architecture means that these models are more scalable as long as there is more data, compute power, and memory.

Serving LLMs still remains a challenge due to high memory requirements with requirements doubling if you need to train and fine-tune them on your own dataset. This is because the training process will require caching and reusing model parameters across training batches.

Processing Data:
Tokenization and embedding
Neural networks can’t process words directly as they’re big statistical models that function on numbers. To bridge that gap between language and numbers, you need to use tokenization. With tokenization, you break down text into smaller pieces that a model can process

Any piece of text must be first sliced into a list of tokens that represent words, syllables, symbols, and punctuations. These tokens are then mapped to unique numbers so that patterns can be numerically modeled. 

By providing a vector of input tokens to a trained transformer, the network can then predict the next best token to generate text, one word at a time

So what can you do after you tokenize some text? These tokens need to be processed further before a language model can process them

After tokenization, you need to use an embedder to convert these tokens into dense vectors of real numbers called embeddings, capturing semantic information (i.e., meaning of each token) in a continuous vector space.

![[Pasted image 20260911190145.png]]

![[Pasted image 20260911190215.png]]

After the embedding process, each token is assigned an embedding vector filled with n numbers. Each number in the embedding vector focuses on a dimension that represents a specific aspect of the token’s meaning

Training transformers Once you have a set of embedding vectors, you can train a model on your documents to update the values inside each embedding. During model training, the training algorithm updates the parameters of the embedding layers so that the embedding vectors describe the meaning of each token as close as possible within the input text.

Understanding how embedding vectors work can be challenging, so let’s try a visualization approach. Imagine you used a two-dimensional embedding vectors, meaning the vectors contained only two numbers. Then, if you plot these vectors, before and after model training, you will observe plots similar to Figure 3-7. The embedding vectors of tokens, or words, with similar meanings will be closer to each other

![[Pasted image 20260911190439.png]]

To determine the similarity between two words, you can compute the angle between vectors using a calculation known as cosine similarity.

Smaller angles imply higher similarity, representing similar context and meaning.

After training, the cosine similarity calculation of two embedding vectors with similar meanings will validate that those vectors are close to each other

![[Pasted image 20260911190538.png]]

Once you have a trained embedding layer, you can now use it to embed any new input text to the transformer model

Positional encoding A final step before forwarding the embedding vectors to the attention layers in the transformer network is to implement positional encoding. The positional encoding process produces the positional embedding vectors that then are summed with the token embedding vectors.

Since transformers process words simultaneously rather than sequentially, positional embeddings are needed to record the word order and context within the sequential data, like sentences. The resultant embedding vectors capture both meaning and positional information of words in the sentences before they’re passed to the attention mechanisms of the transformer. This process ensures attention heads have all the information they need to learn patterns effectively.

![[Pasted image 20260911191105.png]]

Autoregressive prediction
The transformer is an autoregressive (i.e., sequential) model as future predictions are based on the past values

![[Pasted image 20260911191249.png]]

The model receives input tokens that are then embedded and passed through the network to make the next best token prediction. This process repeats until a "<stop>" or end of sentence <eos> is generated

However there is a limit tot the number fo tokens that the mdoel can storre in the memory to generate the next token , this token limit is referred to as the model context window which is important factor during the model selection

If the context window limit is reached, the model simply discards the least recently used tokens. This means it can forget the least recently used sentences in documents or messages in a conversation

Short windows will lead to loss of information, difficulty maintaining conversations, and reduced coherence with the user query. 
On the other hand, long context windows have larger memory requirements and can lead to performance issues or slow services when scaling to thousands of concurrent users who are using your service.

In addition, you will need to consider the costs of relying on models with larger context windows as they tend to be more expensive due to increased compute and memory requirements. The correct choice will depend on your budget and user needs in your use case

![[Pasted image 20260912141839.png]]

![[Pasted image 20260912141857.png]]

Each transformer variant has its own unique capabilities and specializes in certain tasks.

Encoder-decoder transformers 
- Used for transforming one sequence of information into another
- Excel at translation, text summarization, question and answering tasks

Encoder-only transformers 
- Used for understanding and representing the meanings of input sequences 
- Specialize in sentiment analysis, entity extraction, and text classification tasks

Decoder-only transformers 
- Used for predicting the next token in a sequence 
- Outshine other transformers in text generation, conversational and language modeling tasks

---
Audio Models
The Bark model consists of four models chained together as a pipeline to synthesize audio waveforms from textual prompts

![[Pasted image 20260912142142.png]]

1. Semantic text model 
- A causal (sequential) autoregressive transformer model accepts tokenized input text and captures the meaning via semantic tokens.
- Autoregressive models predict future values in a sequence by reusing their own previous outputs.

2. Coarse acoustics model
- A causal autoregressive transformer receives the semantic model’s outputs and generates the initial audio features, which lack finer details.
- Each prediction is based on past and present information in the semantic token sequence.

3.Fine acoustics model
- A noncausal auto-encoder transformer refines the audio representation by generating the remaining audio features.
- As the coarse acoustics model has generated the entire audio sequence, the fine model doesn’t need to be casual.

4. Encodec audio codec model
- The model decodes the output audio array from all previously generated audio codes.

Bark synthesizes the audio waveform by decoding the refined audio features into the final audio output in the form of spoken words, music, or simple audio effects.

Example 3-4 shows how to use the small Bark model. Example 3-4. Download and load the small Bark model from the Hugging Face repository # schemas.py from typing import Literal VoicePresets = Literal["v2/en_speaker_1", "v2/en_speaker_9"] # models.py import torch import numpy as np from transformers import AutoProcessor, AutoModel, BarkProcessor, BarkModel from schemas import VoicePresets device = torch.device("cuda" if torch.cuda.is_available() else "cpu") def load_audio_model() -> tuple[BarkProcessor, BarkModel]: processor = AutoProcessor.from_pretrained("suno/bark-small", device=device) model = AutoModel.from_pretrained("suno/bark-small", device=device) return processor, model def generate_audio( processor: BarkProcessor, model: BarkModel, prompt: str, preset: VoicePresets, ) -> tuple[np.array, int]: inputs = processor(text=[prompt], return_tensors="pt",voice_preset=preset) output = model.generate(**inputs, do_sample=True).cpu().numpy().squeeze() sample_rate = model.generation_config.sample_rate return output, sample_rate Specify supported voice preset options using a Literal type. Download the small Bark processor, which prepares the input text prompt for the core model. Download the Bark model, which will be used to generate the output audio. Both objects will be needed for audio generation later. Preprocess the text prompt with a speaker voice preset embedding and return a Pytorch tensor array of tokenized inputs using return_tensors="pt" . Generate an audio array that contains amplitude values of the synthesized audio signal over time. Get the sampling rate from model generating configurations, which can be used to produce the audio. When you generate audio using a model, the output is a sequence of floating-point numbers that represent the amplitude (or strength) of the audio signal at each point in time. To play back this audio, it needs to be converted to a digital format that can be sent to the speakers. This involves sampling the audio signal at a fixed rate and quantizing the amplitude values to a fixed number of bits. The soundfile library can help you here by generating the audio file using a sampling rate. The higher the sampling rate, the more samples that are taken, which enhances the audio quality but also increases the file size. You can install the soundfile audio library for writing audio files using pip : $ pip install soundfile Example 3-5 shows how you can stream the audio content to the client. Example 3-5. FastAPI endpoint for returning generated audio # utils.py from io import BytesIO import soundfile import numpy as np def audio_array_to_buffer(audio_array: np.array, sample_rate: int) -> BytesIO: buffer = BytesIO() soundfile.write(buffer, audio_array, sample_rate, format="wav") buffer.seek(0) return buffer # main.py from fastapi from import FastAPI, status fastapi. responses from models import StreamingResponse import load_audio_model, generate_audio from schemas import VoicePresets from utils import audio_array_to_buffer @app.get( "/generate/audio", responses={status.HTTP_200_OK: {"content": {"audio/wav": {}}}}, response_class=StreamingResponse, ) def serve_text_to_audio_model_controller( prompt: str, preset: VoicePresets = "v2/en_speaker_1", ): processor, model = load_audio_model() output, sample_rate = generate_audio(processor, model, prompt, preset) return StreamingResponse( audio_array_to_buffer(output, sample_rate), media_type="audio/wav" ) Install the soundfile library to write the audio array to memory buffer using its sampling rate. Reset the buffer cursor to the start of the buffer and return the iterable buffer. Create a new audio endpoint that returns the audio/wav content type as StreamingResponse . StreamingResponse is typically used when you want to stream the response data, such as when returning large files or when generating the response data. It allows you to return a generator function that yields chunks of data to be sent to the client. Convert the generated audio array to an iterable buffer that can be passed to streaming response. In Example 3-5, you generated an audio array using the small Bark model and streamed the memory buffer of the audio content. Streaming is more efficient for larger files as the client can consume the content as it is being served. In previous examples, we didn’t use streaming responses, as generated images or text can be fairly small compared to audio or video content. TIP Streaming audio content directly from a memory buffer is faster and more efficient than writing the audio array to a file and streaming the content from the hard drive. If you need the memory available for other tasks, you can write the audio array to a file first and then stream from it using a file reader generator. You wil be trading off latency for memory. Now that you have an audio generation endpoint, you can update your Streamlit UI client code to render audio messages. Update your Streamlit client code as shown in Example 3-6. Example 3-6. Streamlit audio UI consuming the FastAPI /audio generation endpoint # client.py for message in st.session_state.messages: with st.chat_message(message["role"]): content = message["content"] if isinstance(content, bytes): st.audio(content) else: st.markdown(content) if prompt := st.chat_input("Write your prompt in this input field"): response = requests.get( f"http://localhost:8000/generate/audio", params={"prompt": prompt} ) response.raise_for_status() with st.chat_message("assistant"): st.text("Here is your generated audio") st.audio(response.content) Update the Streamlit client code to render audio content. With Streamlit, you can swap components to render any type of content including images, audio, and video.

---
### Vision Models

these models can produce very realistic outputs faster than any human and can understand and manipulate existing visual content, they’re extremely useful for applications like image generators and editors, object detection, image classification and captioning, and augmented reality

One of the most popular architectures used to train image models is called Stable Diffusion (SD)

- SD models are trained to encode input images into a latent space
- This latent space is the mathematical representation of patterns in the training data that the model has learned.
- If you try to visualize an encoded image, all you would see is a white noise image, similar to the black and white dots you would see on your TV screen when it loses signal.

the full process for training and inference and visualizes how images are encoded and decoded via the forward and reverse diffusion processes
A text encoder using text, images, and semantic maps assists in controlling the output via the reverse diffusion
![[Pasted image 20260912143053.png]]

- What makes these models magical is their ability to decode noisy images back into original input images.
-  the SD models also learn to remove white noise from an encoded image to reproduce the original image.
- The model performs this denoising process over several iterations.

However, you don’t want to re-create images you already have. You will want the model to create new, never-before-seen images.
But how can an SD model achieve this for you? The answer lies in the latent space where the encoded noisy images live.
You can change the noise in these images so that when the model denoises them and decodes them back, you get a whole new image that the model has never seen before.