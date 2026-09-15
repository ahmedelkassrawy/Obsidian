---
description: "Short crib sheet on what padding, kernel size, stride and pooling each do to a CNN's activation maps."
domain: ml
type: reference
status: stub
tags:
  - domain/ml
  - type/reference
  - status/stub
  - topic/cnn
aliases:
  - "conv hyperparameters"
  - "kernel size"
  - "padding stride"
hubs:
  - "[[CNN]]"
---
**Padding**
	conserves data at the borders of activation maps,it can help preserve the input's spatial size,which leads to better performance
**Kernel size**
	often also referred to as filter size,refers to the dimensions of the sliding window over the input. Small kernel sizes are able to extract a much larger amount of information containing highly local features from the input.
larger kernels --> less info extracted --> faster reduction in layer  --> worst performance

**Stride** 
	indicates how many pixels the kernel should be shifted over at a time.
stride decrease --> more feature learned --> more data extracted --> large output layers
