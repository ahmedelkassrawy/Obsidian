---
title: "Ch.3 — Serving GenAI Models with FastAPI"
book: Building GenAI Services
tags: [genai, fastapi, transformers, diffusion, notes]
---

# Chapter 3 — Serving GenAI Models with FastAPI

> [!abstract] What this chapter covers
> How different GenAI models actually work under the hood, and how to serve them from a FastAPI app. You'll build a service — from scratch — that generates **text, images, audio, and 3D geometry** using open-source models. Along the way you'll learn how to preload models so they're fast, and how to monitor the service while it runs.

We build the service step by step, one modality at a time. The four families of models we serve:

- **Language models** — text generation, built on the transformer architecture.
- **Audio models** — text-to-speech and text-to-audio, also transformer-based.
- **Vision models** — text-to-image and text-to-video, built on Stable Diffusion and vision transformers.
- **3D models** — text-to-3D, built on a conditional implicit-function encoder with a diffusion decoder.

---

## Language Models

This section is about language models — mainly **transformers**, and the older **RNNs** they replaced.

### Transformers vs. RNNs

![[Pasted image 20260911184358.png]]

RNNs (recurrent neural networks) were the go-to for learning patterns in sequential data like free-flowing text.

> [!definition] Token
> A small piece of text — a word, part of a word, or a single character — that a model reads one at a time. Before a model can process text, the text is chopped into tokens.

Here's the core idea behind an RNN. As it reads text token by token, it keeps a running memory called a **state vector**. That memory is passed forward from one token to the next, all the way to the end of the sequence.

> [!definition] State vector
> The RNN's running memory. It carries information from earlier tokens forward as the model reads. Because it's updated at every step, older information gets "diluted" the further along you go.

The problem: by the time the RNN reaches the end of a long text, the earliest tokens barely influence the state vector anymore. Recent tokens dominate. In an ideal model, every token would matter equally — but an RNN can only look backward, one step at a time, so it struggles to capture **long-range dependencies**.

In practice that means RNNs forget important context in long documents. They lose the thread.

### What transformers changed

Transformers threw out the recurrent (and convolutional) approach and replaced it with something more efficient. They don't keep a hidden memory at all. Instead they use a mechanism called **self-attention**.

> [!definition] Self-attention
> A mechanism that lets a model weigh the relationship between every word and every other word in a sentence — no matter how far apart they are. It "places attention" on the words that actually matter for understanding a given word.

The difference in one line:

- **RNNs** model relationships between *neighboring* words.
- **Transformers** map relationships between *every pair* of words in the text.

![[Pasted image 20260911184841.png]]

### Attention heads

Self-attention is powered by specialized blocks called **attention heads**.

> [!definition] Attention head
> A component that looks for one specific kind of pairwise relationship between words and records it as an **attention map**. A transformer has many of them spread across its layers.

- A transformer contains several attention heads distributed across its neural-network layers.
- Each head builds its own attention map independently, focusing on a different pattern in the input.
- Using many heads at once lets the model read the input from multiple angles simultaneously — so it can catch complex patterns and dependencies a single head would miss.

![[Pasted image 20260911185532.png]]

### Why transformers scale better

- **RNNs are slow to train.** Their training can't be split across multiple GPUs, because each step depends on the one before it — the process is inherently sequential.
- **Transformers process words in parallel.** They don't wait for the previous word, so attention runs across many GPUs at once.

That parallelism is why transformers scale: give them more data, more compute, and more memory, and they keep improving.

> [!warning] Serving LLMs is still hard
> The memory cost is high — and it roughly **doubles** if you want to train or fine-tune on your own data, because training has to cache and reuse model parameters across batches.

---

## Processing Data: Tokenization and Embedding

Neural networks can't read words. They're big statistical machines that only understand numbers. So we need to translate language into numbers in two steps: **tokenization**, then **embedding**.

### Tokenization

> [!definition] Tokenization
> Breaking text into small pieces (tokens) — words, syllables, symbols, punctuation — and mapping each piece to a unique number so the model can work with it mathematically.

Any text is first sliced into a list of tokens, and each token is assigned a unique number. Once patterns are represented as numbers, the model can learn them.

Feed a trained transformer a vector of input tokens, and it predicts the next best token — generating text one word at a time.

But tokens alone aren't enough. They need one more transformation before the model can find meaning in them.

### Embedding

> [!definition] Embedding
> A dense vector of real numbers that represents a token's *meaning*. Instead of an arbitrary ID number, each token becomes a point in a continuous "meaning space."

![[Pasted image 20260911190145.png]]

![[Pasted image 20260911190215.png]]

After embedding, every token has a vector of `n` numbers. Each number captures one dimension of the token's meaning — one aspect of what the word "is about."

### Training the embeddings

Once you have embedding vectors, training refines them. The training algorithm nudges the numbers inside each embedding so that the vectors describe each token's meaning as accurately as possible for your text.

Here's an intuition. Imagine your embeddings had only **two** numbers each, so you could plot them on a 2D chart. Before and after training you'd see something like the figure below — and after training, **words with similar meanings sit close together**.

![[Pasted image 20260911190439.png]]

### Measuring similarity: cosine similarity

To measure how similar two words are, you measure the **angle** between their vectors, using **cosine similarity**.

> [!definition] Cosine similarity
> A number that measures the angle between two vectors. A **small angle → high similarity** (similar meaning and context). A large angle → the words are unrelated.

After training, computing cosine similarity on two similar words confirms their vectors point in nearly the same direction.

![[Pasted image 20260911190538.png]]

Once the embedding layer is trained, you can use it to embed any new text you feed the transformer.

### Positional encoding

There's one more step before the embeddings reach the attention layers: **positional encoding**.

> [!definition] Positional encoding
> Extra information added to each token's embedding to record *where* it sits in the sequence. Without it, the model wouldn't know word order.

The positional encoding produces a positional vector, which is added to the token's embedding vector.

Why is this needed? Transformers read all words at once, not in order — so they'd have no sense of sequence otherwise. Positional encoding restores word order and context (which matters a lot in a sentence). The combined vector now carries **both meaning and position**, so the attention heads have everything they need to learn patterns correctly.

![[Pasted image 20260911191105.png]]

### Autoregressive prediction

> [!definition] Autoregressive model
> A model that predicts the next value based on the values that came before it. A transformer generates text this way — one token at a time, each new token conditioned on all the previous ones.

![[Pasted image 20260911191249.png]]

The loop looks like this:

1. The model receives input tokens.
2. It embeds them and passes them through the network.
3. It predicts the next best token.
4. It repeats — until a stop signal like `<stop>` or end-of-sentence `<eos>` is generated.

### The context window

There's a hard limit on how many tokens the model can hold in memory while predicting the next one. That limit is the **context window** — and it's a key factor when choosing a model.

> [!definition] Context window
> The maximum number of tokens a model can "see" at once. Anything beyond it can't influence the next prediction.

When the window fills up, the model **discards the least recently used tokens**. In practice, it forgets the oldest sentences in a document or the earliest messages in a conversation.

The trade-off:

- **Short windows** → lost information, harder to hold a conversation, answers drift off from the user's question.
- **Long windows** → much larger memory needs; can cause slowdowns or performance issues when thousands of users hit your service at once.

> [!tip] Cost matters too
> Larger context windows are more expensive to run (more compute, more memory). The right choice depends on your budget and what your users actually need.

![[Pasted image 20260912141839.png]]

![[Pasted image 20260912141857.png]]

### The three transformer variants

Each transformer type is specialized for different tasks.

**Encoder–decoder transformers**
- Transform one sequence into another.
- Best at: translation, summarization, question answering.

**Encoder-only transformers**
- Focus on understanding and representing the meaning of an input.
- Best at: sentiment analysis, entity extraction, text classification.

**Decoder-only transformers**
- Focus on predicting the next token.
- Best at: text generation, conversation, language modeling.

---

## Audio Models

We use the **Bark** model. Bark is actually four models chained together into a pipeline that turns a text prompt into an audio waveform.

![[Pasted image 20260912142142.png]]

**1. Semantic text model**
- A causal (sequential) autoregressive transformer. It takes tokenized text and captures its *meaning* as semantic tokens.
- Reminder: autoregressive models predict the next value by reusing their own previous outputs.

**2. Coarse acoustics model**
- A causal autoregressive transformer. It takes the semantic model's output and generates the first, rough audio features (no fine detail yet).
- Each prediction is based on the past and present tokens in the semantic sequence.

**3. Fine acoustics model**
- A non-causal auto-encoder transformer. It refines the audio by filling in the remaining detail.
- Because the coarse model already produced the whole sequence, this model can look at the full context — so it doesn't need to be causal.

**4. Encodec audio codec model**
- Decodes the final audio array from all the generated audio codes.

Put together, Bark decodes the refined features into the final output — spoken words, music, or sound effects.

### Loading and running the small Bark model

```python
# schemas.py
from typing import Literal

VoicePresets = Literal["v2/en_speaker_1", "v2/en_speaker_9"]
```

```python
# models.py
import torch
import numpy as np
from transformers import AutoProcessor, AutoModel, BarkProcessor, BarkModel
from schemas import VoicePresets

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_audio_model() -> tuple[BarkProcessor, BarkModel]:
    processor = AutoProcessor.from_pretrained("suno/bark-small", device=device)
    model = AutoModel.from_pretrained("suno/bark-small", device=device)
    return processor, model


def generate_audio(
    processor: BarkProcessor,
    model: BarkModel,
    prompt: str,
    preset: VoicePresets,
) -> tuple[np.array, int]:
    inputs = processor(text=[prompt], return_tensors="pt", voice_preset=preset)
    output = model.generate(**inputs, do_sample=True).cpu().numpy().squeeze()
    sample_rate = model.generation_config.sample_rate
    return output, sample_rate
```

What's happening here:

- `VoicePresets` uses a `Literal` type to lock down the supported voices.
- The **processor** prepares the text prompt for the model; the **model** does the audio generation. You need both.
- `return_tensors="pt"` returns a PyTorch tensor of the tokenized input, embedding the chosen speaker voice.
- The output is an audio array of amplitude values over time, plus the **sampling rate** you'll need to play it back.

> [!definition] Sampling rate
> How many times per second the audio signal's amplitude is measured. Higher rate → better quality but bigger files.

When a model generates audio, the output is a sequence of floating-point numbers — the strength (amplitude) of the signal at each moment. To play it, you convert it to a digital format by **sampling** at a fixed rate and **quantizing** the amplitudes to a fixed number of bits.

The `soundfile` library handles writing the audio file:

```bash
pip install soundfile
```

### Streaming the audio to the client

```python
# utils.py
from io import BytesIO
import soundfile
import numpy as np


def audio_array_to_buffer(audio_array: np.array, sample_rate: int) -> BytesIO:
    buffer = BytesIO()
    soundfile.write(buffer, audio_array, sample_rate, format="wav")
    buffer.seek(0)
    return buffer
```

```python
# main.py
from fastapi import FastAPI, status
from fastapi.responses import StreamingResponse
from models import load_audio_model, generate_audio
from schemas import VoicePresets
from utils import audio_array_to_buffer


@app.get(
    "/generate/audio",
    responses={status.HTTP_200_OK: {"content": {"audio/wav": {}}}},
    response_class=StreamingResponse,
)
def serve_text_to_audio_model_controller(
    prompt: str,
    preset: VoicePresets = "v2/en_speaker_1",
):
    processor, model = load_audio_model()
    output, sample_rate = generate_audio(processor, model, prompt, preset)
    return StreamingResponse(
        audio_array_to_buffer(output, sample_rate), media_type="audio/wav"
    )
```

Key points:

- Write the audio array to an in-memory buffer, reset the cursor to the start, and return it.
- The endpoint returns `audio/wav` content as a `StreamingResponse`.

> [!definition] StreamingResponse
> A FastAPI response that streams data in chunks instead of sending it all at once. It uses a generator that yields pieces of the response — ideal for large files or generated content the client can start consuming immediately.

> [!tip] Stream from memory, not disk
> Streaming audio straight from a memory buffer is faster than writing a file to disk and streaming that. If you're short on memory, you *can* write to a file first and stream from it — you're trading latency for memory.

Note: earlier examples (text, images) didn't stream, because that content is small. Audio and video are big enough that streaming pays off.

### Rendering audio in the Streamlit UI

```python
# client.py
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        content = message["content"]
        if isinstance(content, bytes):
            st.audio(content)
        else:
            st.markdown(content)

if prompt := st.chat_input("Write your prompt in this input field"):
    response = requests.get(
        "http://localhost:8000/generate/audio",
        params={"prompt": prompt},
    )
    response.raise_for_status()
    with st.chat_message("assistant"):
        st.text("Here is your generated audio")
        st.audio(response.content)
```

With Streamlit you just swap components to render whatever you need — images, audio, video. Here `st.audio` plays the generated clip.

---

## Vision Models

These models produce very realistic output far faster than any human, and they can understand and edit existing visual content. That makes them useful for image generators and editors, object detection, classification, captioning, and augmented reality.

The most popular architecture for training image models is **Stable Diffusion (SD)**.

### How Stable Diffusion works

- SD models are trained to **encode** an input image into a **latent space**.

> [!definition] Latent space
> A compressed mathematical representation of the patterns a model learned from its training data. It's not a picture you can look at — if you tried, an encoded image would look like TV static (white noise).

![[Pasted image 20260912143053.png]]

- The magic is that SD models can also **decode** a noisy image back into the original.
- They learn to **remove white noise** from an encoded image to reconstruct it.
- This denoising happens over several iterations, not in one shot.

### From reconstruction to creation

You don't just want to recreate images you already have — you want *new* ones. Here's the trick:

1. Encoded noisy images live in the latent space.
2. You **change the noise** in that space.
3. When the model denoises and decodes it, you get a brand-new image it has never seen.

But that alone would produce random images. How do you *control* what comes out? By encoding **text descriptions alongside the images** during training.

The latent patterns get mapped to text descriptions of what each image contains. Now you can use a **text prompt** to steer which part of the noisy latent space you sample — so the denoised result is what you actually asked for. That's how SD generates new, never-before-seen images.

### Serving a generated image

```python
# utils.py
from typing import Literal
from PIL import Image
from io import BytesIO


def img_to_bytes(
    image: Image.Image, img_format: Literal["PNG", "JPEG"] = "PNG"
) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format=img_format)
    return buffer.getvalue()
```

```python
# main.py
from fastapi import FastAPI, Response, status
from models import load_image_model, generate_image
from utils import img_to_bytes


@app.get(
    "/generate/image",
    responses={status.HTTP_200_OK: {"content": {"image/png": {}}}},
    response_class=Response,
)
def serve_text_to_image_model_controller(prompt: str):
    pipe = load_image_model()
    output = generate_image(pipe, prompt)
    return Response(content=img_to_bytes(output), media_type="image/png")
```

Notes:

- Save the image to an in-memory buffer, then return the raw bytes.
- The `responses=` and `status` args feed FastAPI's auto-generated Swagger docs.
- Setting `response_class=Response` stops FastAPI from also advertising `application/json` as an acceptable response type.
- The model returns a Pillow image, so we wrap the PNG bytes in FastAPI's `Response` class.

Testing `/generate/image` in Swagger with the prompt *"A cosy living room with trees in it"* returns a generated image.

### Rendering the image in Streamlit

```python
# client.py
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.image(message["content"])

if prompt := st.chat_input("Write your prompt in this input field"):
    response = requests.get(
        "http://localhost:8000/generate/image",
        params={"prompt": prompt},
    )
    response.raise_for_status()
    with st.chat_message("assistant"):
        st.text("Here is your generated image")
        st.image(response.content)
```

Images travel over HTTP as binary, so the display function renders binary content with `st.image`.

### Current limitations of open-source SD models

> [!warning] What SD still gets wrong
> - **Coherency** — can't render every detail of complex prompts or compositions.
> - **Output size** — fixed sizes only, like 512×512 or 1024×1024.
> - **Composability** — you can't fully control the layout of what's in the image.
> - **Photorealism** — outputs often have tell-tale "AI" details.
> - **Legible text** — many models can't render readable text.

### Video Models

Video models are among the most resource-hungry generative models — you usually need a GPU just to make a short, decent clip. They have to generate **dozens of frames per second of video**, even with no audio.

Stability AI has released open-source video models based on the SD architecture. We use a compressed image-to-video model for faster animation.

> [!note] Requirements
> Running the example may need a CUDA-capable NVIDIA GPU. For commercial use of `stable-video-diffusion-img2vid`, check its model card.

```python
# models.py
import torch
from diffusers import StableVideoDiffusionPipeline
from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_video_model() -> StableVideoDiffusionPipeline:
    pipe = StableVideoDiffusionPipeline.from_pretrained(
        "stabilityai/stable-video-diffusion-img2vid",
        torch_dtype=torch.float16,
        variant="fp16",
        device=device,
    )
    return pipe


def generate_video(
    pipe: StableVideoDiffusionPipeline, image: Image.Image, num_frames: int = 25
) -> list[Image.Image]:
    image = image.resize((1024, 576))
    generator = torch.manual_seed(42)
    frames = pipe(
        image, decode_chunk_size=8, generator=generator, num_frames=num_frames
    ).frames[0]
    return frames
```

What each part does:

- **Resize the input** to the size the model expects (also guards against oversized inputs).
- **Fixed random seed (42)** makes frame generation reproducible.
- The pipeline generates all frames at once, then we grab the first batch. This step needs a lot of VRAM.
- `num_frames` = how many frames to produce; `decode_chunk_size` = how many to decode at a time.

### Exporting frames to a streamable video

To turn a list of frames into a playable video, you encode them into a video container using `av` — Python bindings for **ffmpeg**.

```bash
pip install av
```

```python
# utils.py
from io import BytesIO
from PIL import Image
import av


def export_to_video_buffer(images: list[Image.Image]) -> BytesIO:
    buffer = BytesIO()
    output = av.open(buffer, "w", format="mp4")
    stream = output.add_stream("h264", 30)
    stream.width = images[0].width
    stream.height = images[0].height
    stream.pix_fmt = "yuv444p"
    stream.options = {"crf": "17"}

    for image in images:
        frame = av.VideoFrame.from_image(image)
        packet = stream.encode(frame)
        output.mux(packet)

    packet = stream.encode(None)
    output.mux(packet)
    return buffer
```

Walking through it:

- Open an MP4 buffer for writing and configure a video stream.
- Encode with **h264 at 30 fps**; the frame size must match the frames you pass in.
- Pixel format `yuv444p` gives each pixel full resolution for brightness (`y`) and both color channels (`u`, `v`).

> [!definition] CRF (constant rate factor)
> A knob controlling video quality vs. compression. Lower = higher quality, bigger file. `crf=17` is near-lossless with minimal compression.

- Encode each frame into packets and add ("mux") them into the container.
- Finally, flush any leftover frames from the encoder and return the buffer.

### Serving the video endpoint

To accept image uploads, install:

```bash
pip install python-multipart
```

```python
# main.py
from fastapi import status, FastAPI, File
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image
from models import load_video_model, generate_video
from utils import export_to_video_buffer


@app.post(
    "/generate/video",
    responses={status.HTTP_200_OK: {"content": {"video/mp4": {}}}},
    response_class=StreamingResponse,
)
def serve_image_to_video_model_controller(
    image: bytes = File(...), num_frames: int = 25
):
    image = Image.open(BytesIO(image))
    model = load_video_model()
    frames = generate_video(model, image, num_frames)
    return StreamingResponse(
        export_to_video_buffer(frames), media_type="video/mp4"
    )
```

- `File(...)` marks `image` as a form file upload.
- We rebuild a Pillow image from the uploaded bytes (that's what the pipeline expects).
- The frames are exported to MP4 and streamed back to the client.

Now you can upload an image and get an animated video in return.

### Sora — a generalist vision transformer

**Sora** is a large vision diffusion transformer that generates videos and images across many durations, aspect ratios, and resolutions — up to a full minute of HD video. Its architecture combines the transformer (like LLMs) with the diffusion process.

> [!definition] Visual patch
> Sora's equivalent of a text token. Where an LLM works with text tokens, Sora works with small chunks of an image or video frame called patches.

**Why base Sora on transformers?** Transformers scale extremely well across language, vision, and image generation, and they handle diverse inputs (text, images, video frames). Because they capture long-range dependencies, Sora — as a vision transformer — can track fine-grained relationships across time and space between frames, producing smooth, coherent video.

**Why also use diffusion?** Sora borrows SD's iterative noise-reduction to generate high-quality, visually coherent frames with fine detail and precise control. Combining the two — the transformer's sequential reasoning plus SD's iterative refinement — lets Sora generate high-resolution, smooth video from mixed inputs like text and images, even for abstract concepts.

Sora's network uses a **U-shaped architecture** that compresses high-dimensional visual data into a latent noisy space, then generates patches from it via denoising diffusion.

> [!note] 2D vs. 3D U-Net
> Image-based SD uses a 2D U-Net. OpenAI trained Sora on a **3D U-Net**, where the third dimension is a sequence of frames over time — which is what makes it video.

![[Pasted image 20260912145804.png]]

By compressing videos into patches, the model learns high-dimensional representations that scale across videos and images of varying resolution, duration, and aspect ratio.

![[Pasted image 20260912145832.png]]

Through diffusion, Sora turns noisy patches into clean videos and images at any size or aspect ratio — matching a device's native screen size directly.

> [!info] The core analogy
> A text transformer predicts the **next token**. Sora's vision transformer predicts the **next patch** — to build an image or video.

![[Pasted image 20260912145910.png]]

By training on varied datasets, OpenAI overcame long-standing problems in training vision models — like the shortage of quality captions and the sheer dimensionality of video data.

### Emergent abilities Sora demonstrates

- **3D consistency** — objects stay consistent and adjust to perspective as the camera moves and rotates.
- **Object permanence & long-range coherence** — objects that leave the frame or get blocked still look right when they return. The model effectively remembers them (this is *temporal consistency*, which most video models struggle with).
- **World interaction** — actions realistically change the environment. For example, Sora "knows" biting a burger should leave a bite mark.
- **Simulating environments** — Sora can simulate real or fictional worlds (like games) while following their rules — e.g. playing a character in a Minecraft level. In effect, it has learned to act as a data-driven physics engine.

![[Pasted image 20260912150001.png]]

---

## 3D Models

Generating 3D geometry needs a different approach from text, audio, or images. You have to account for **spatial relationships, depth, and geometric consistency** — extra layers of complexity that flat data doesn't have.

### Meshes

3D shapes are defined by **meshes**. Tools like Autodesk 3ds Max, Maya, and SolidWorks create, edit, and render them.

> [!definition] Mesh
> A collection of **vertices, edges, and faces** in 3D space that together define an object's shape.
> - **Vertices** — points in space (given by `x, y, z` coordinates).
> - **Edges** — lines connecting vertices.
> - **Faces** — flat surfaces (polygons, usually triangles or quads) formed when edges enclose an area.

The arrangement and connection of vertices form the surfaces of the mesh, which define the geometry.

![[Pasted image 20260912150128.png]]

### The naive approach (and why it's slow)

You *could* train a transformer to predict the next vertex, treating the vertex coordinates as a sequence — generating a shape by predicting the next set of vertices and faces.

The catch: a smooth surface needs **thousands** of vertices and faces. So each object takes a long time to generate, and the result may still look low-fidelity.

### The better approach: implicit functions

> [!definition] Implicit function
> Instead of listing every vertex explicitly, an implicit function *describes* a surface mathematically across continuous 3D space. This is great for smooth surfaces and intricate detail that discrete meshes handle poorly.

A trained model uses an **encoder** that maps learned patterns to an implicit function. Rather than spitting out sequences of vertices, a conditional 3D model **evaluates** the implicit function across continuous 3D space. The payoff: far more freedom, control, and flexibility — and high-fidelity output suited to detailed geometry.

### Rendering the scene: NeRF

Once the encoder produces implicit functions, the decoder uses **NeRF** to build the actual 3D scene.

> [!definition] NeRF (Neural Radiance Fields)
> A rendering technique that maps two inputs — a 3D point and a 3D viewing direction — to two outputs: the object's **density** and **RGB color** at that point.

To render a new view, NeRF treats the viewport as a grid of rays. Each pixel corresponds to a ray that starts at the camera and extends in the viewing direction. The pixel's color comes from evaluating the implicit function along that ray and integrating the results into a final RGB value.

### Building the mesh: SDFs

Once the scene is computed, **signed distance functions** turn it into an actual mesh.

> [!definition] Signed distance function (SDF)
> A function that, for any point in space, returns how far that point is from the object's nearest surface — with a sign:
> - **Negative** → the point is inside the object.
> - **Zero** → the point is exactly on the surface.
> - **Positive** → the point is outside.
>
> The surface is defined by all the points where the value is zero. Collect those and you have your mesh.

> [!warning] Quality caveat
> Even with implicit functions, generated 3D still lags behind human-made assets and can look cartoonish. But it's great for quickly generating a starting geometry to iterate on and refine.

---

## Model-Serving Strategies

### Strategy 1 — Be model-agnostic: swap models on every request

So far, each endpoint loads a model, runs generation, and returns the result. FastAPI loads the model into RAM (or VRAM on a GPU), generates, returns, and **unloads** the model. Then it repeats for the next request.

**The upside:** memory is freed after each request, so you can dynamically swap different models between requests — handy if you're juggling several large models and don't have enough RAM.

![[Pasted image 20260912151122.png]]

**The downside:** it's slow. Because the model is loaded and unloaded every single time, and FastAPI processes requests **FIFO** (first in, first out), concurrent requests pile up in a queue and wait.

> [!definition] FIFO (first in, first out)
> Requests are handled in arrival order. Request #2 can't be served until request #1 finishes.

> [!warning] Prototyping only
> This strategy is fine for trying things on a low-powered machine with a few users, when you must swap between models you can't all fit in memory. **Never use it in production** — the wait times will frustrate your users.

### Strategy 2 — Be compute-efficient: preload models with the FastAPI lifespan

The most efficient approach loads models **once, at application startup**, and unloads them at shutdown (where you can also do cleanup like logging or clearing temp files).

> [!definition] Application lifespan
> A FastAPI hook that runs setup code when the app starts and teardown code when it stops. It's the right place to preload heavy models.

The benefit: you never reload a heavy model per request. Load it once, reuse it for every request. You trade a chunk of RAM (or VRAM) for much faster responses — and a much better user experience.

```python
# main.py
from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI, Response, status
from models import load_image_model, generate_image
from utils import img_to_bytes

models = {}


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    models["text2image"] = load_image_model()
    yield
    # Run cleanup code here
    models.clear()


app = FastAPI(lifespan=lifespan)


@app.get(
    "/generate/image",
    responses={status.HTTP_200_OK: {"content": {"image/png": {}}}},
    response_class=Response,
)
def serve_text_to_image_model_controller(prompt: str):
    output = generate_image(models["text2image"], prompt)
    return Response(content=img_to_bytes(output), media_type="image/png")
```

How it works:

- A global `models` dict holds one or more preloaded models.
- The `@asynccontextmanager` decorator turns `lifespan` into an async context manager. The `yield` splits it in two:
  - **Before `yield`** → runs at startup, before any request is handled. Here we preload the model.
  - **After `yield`** → runs at shutdown. Here we clear the model.
- `app = FastAPI(lifespan=lifespan)` wires it up.
- The endpoint reuses the preloaded model instead of loading its own.

Start the app now and you'll see the model load immediately — before, it only loaded on the first request.

> [!warning] Don't preload too many big models
> You *can* preload several models with the lifespan, but it's impractical with large GenAI models. The most powerful consumer GPUs ship with only **24 GB of VRAM**, and a single model can need ~18 GB just for inference. Better to deploy big models on separate instances / GPUs.

> [!note] Legacy: startup and shutdown events
> Before lifespan context managers arrived in FastAPI **0.93.0**, people used separate `@app.on_event("startup")` and `@app.on_event("shutdown")` handlers. You'll still see this older style around, so it's worth recognizing:
> ```python
> # main.py
> from models import load_image_model
>
> models = {}
> app = FastAPI()
>
>
> @app.on_event("startup")
> def startup_event():
>     models["text2image"] = load_image_model()
>
>
> @app.on_event("shutdown")
> def shutdown_event():
>     with open("log.txt", mode="a") as logfile:
>         logfile.write("Application shutdown")
> ```

![[Pasted image 20260912151231.png]]

---

## Monitoring with Middleware

You can build a simple monitoring tool that logs prompts, responses, and token usage. You *could* drop logging calls inside each controller — but with many models and endpoints, **middleware** is far cleaner.

> [!definition] Middleware
> A block of code that runs **before and after** every request is processed by your route handlers. It sits between the client and your controllers, acting as an intermediary on both the request and the response.

Great uses for middleware: logging and monitoring, rate limiting, content filtering, and CORS.

```python
# main.py
import csv
import time
from datetime import datetime, timezone
from uuid import uuid4
from typing import Awaitable, Callable
from fastapi import FastAPI, Request, Response

# preload model with a lifespan ...
app = FastAPI(lifespan=lifespan)

csv_header = [
    "Request ID",
    "Datetime",
    "Endpoint Triggered",
    "Client IP Address",
    "Response Time",
    "Status Code",
    "Successful",
]


@app.middleware("http")
async def monitor_service(
    req: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    request_id = uuid4().hex
    request_datetime = datetime.now(timezone.utc).isoformat()
    start_time = time.perf_counter()

    response: Response = await call_next(req)

    response_time = round(time.perf_counter() - start_time, 4)
    response.headers["X-Response-Time"] = str(response_time)
    response.headers["X-API-Request-ID"] = request_id

    with open("usage.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(csv_header)
        writer.writerow(
            [
                request_id,
                request_datetime,
                req.url,
                req.client.host,
                response_time,
                response.status_code,
                response.status_code < 400,
            ]
        )
    return response
```

Example log entry:

```text
Request ID:        3d15d3d9b7124cc9be7eb690fc4c9bd5
Datetime:          2024-03-07T16:41:58.895091
Endpoint triggered: http://localhost:8000/generate/text
Client IP Address: 127.0.0.1
Processing time:   26.7210 seconds
Status Code:       200
Successful:        True
```

What the middleware does:

- `@app.middleware("http")` registers the function. To be valid, it must accept the `Request` and a `call_next` callback.
- `call_next(req)` passes the request on to the actual route handler and returns its response.
- A `request_id` is generated **up front**, so requests are still tracked even if `call_next` raises an error.
- Response time is measured to four decimal places and attached as custom headers.
- The URL, timestamp, request ID, client IP, response time, and status code are appended to a CSV on disk.

> [!warning] Logging request/response bodies
> Middleware is more efficient than adding loggers to every handler. But if you log the actual prompts and generated content, watch out for **privacy and performance** — users can submit sensitive or very large data, which needs careful handling.

---

## Summary

We covered a lot. Quick recap:

- **Downloaded and served** open-source GenAI models from Hugging Face, with a simple Streamlit UI in just a few lines.
- **Served five modalities** via FastAPI endpoints — text, image, audio, video, and 3D — and saw how each processes data.
- **Learned the architectures** and the mechanisms behind them: transformers and attention, Stable Diffusion, Sora, implicit functions / NeRF / SDFs.
- **Compared serving strategies** — swapping models per request, preloading with the lifespan, and serving models outside FastAPI (e.g. BentoML or third-party APIs).
- **Noticed the latency** of larger models.
- **Built a monitoring system** using FastAPI middleware, logging usage to disk for later analysis.

> [!success] Where you are now
> You should feel more confident building your own GenAI services from a variety of open-source models. Next chapter: **type safety** — how it kills bugs and reduces uncertainty when working with external APIs, and how validating request/response schemas makes your services more reliable.
