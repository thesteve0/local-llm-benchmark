# Manual Eval: Ornith-1.5-35B-A3B-UD-Q8_K_XL

## Prompt


 Write a comprehensive, detailed technical essay of at least 500 words and less than 1000 words, explaining the architectural differences between Transformer-based Large Language Models and State Space Models (like Mamba). Discuss their respective approaches to the attention mechanism, computational complexity regarding sequence length, and their practical implications for long-context window processing. Use an academic, introductory course style of writing and tone.


## Reasoning

The user wants a comprehensive technical essay comparing Transformer-based LLMs and State Space Models (like Mamba). Let me plan this out.

Requirements:
- At least 500 words, less than 1000 words
- Explain architectural differences
- Discuss attention mechanism approaches
- Computational complexity regarding sequence length
- Practical implications for long-context window processing
- Academic, introductory course style writing and tone

Let me write a well-structured essay covering these points. I'll aim for around 700-850 words to be safely in range.

Let me structure it:
1. Introduction - set up the two paradigms
2. Transformer attention mechanism - self-attention, how it works
3. Computational complexity of Transformers - O(n²) or O(n) per layer discussion
4. State Space Models / Mamba - selective mechanisms
5. Computational complexity of SSMs
6. Practical implications for long context
7. Conclusion

Let me write this in an academic, introductory course style - so it should be accessible but technical, with clear explanations.

Let me be careful about the technical accuracy:

**Transformers:**
- Self-attention mechanism: computes attention scores between all pairs of positions
- Q, K, V projections
- Attention = softmax(QK^T / sqrt(d)) V
- Self-attention is O(n²d) in time and O(n²) in memory for the attention matrix, where n is sequence length and d is dimension
- This quadratic scaling is the key limitation
- Positional encoding needed since attention is permutation invariant
- Parallelizable during training

**State Space Models (SSMs):**
- Originated from control theory (linear state space models)
- Represent sequences through a latent state that evolves
- Continuous: h'(t) = A h(t) + B x(t), y(t) = C h(t)
- Discretized: h_t = A h_{t-1} + B x_t, y_t = C h_t
- Can be computed efficiently via convolution (parallel scan)
- Mamba: selective SSM - the parameters B, C, and Δ (delta/step size) depend on the input, allowing the model to filter information (forget irrelevant, retain relevant)
- Linear complexity O(n) in sequence length
- Sequential nature allows constant memory during inference (just maintain state)
- No need for positional encoding in the same way

**Complexity:**
- Transformer: O(n²) attention computation
- Mamba: O(n) linear

**Long context:**
- Transformers struggle with very long sequences due to quadratic memory/time
- KV caching helps inference but memory grows linearly with context
- SSMs maintain constant memory at inference, scale better
- Hybrid approaches emerging (e.g., combining transformers and Mamba)

Let me write this essay now. I'll aim for good academic tone, clear structure with maybe some headers or just flowing paragraphs. Given it's an "introductory course style," I might use section headers to help organize.

Let me write it.


## Response

# Architectural Paradigms in Modern Language Models: Transformers vs. State Space Models

## Introduction

The rapid advancement of large language models (LLMs) has been driven largely by architectural innovation. For several years, the Transformer architecture has dominated the field, powering models such as GPT and BERT. However, recent research has revived an older class of architectures—State Space Models (SSMs)—with Mamba emerging as a leading example. Understanding the architectural differences between these two paradigms is essential for grasping current trends in sequence modeling, particularly with respect to how each handles long sequences.

## The Attention Mechanism in Transformers

The Transformer, introduced in the seminal 2017 paper "Attention Is All You Need," relies fundamentally on a mechanism called self-attention. In this approach, every token in a sequence can directly attend to every other token, allowing the model to capture long-range dependencies regardless of the distance between them.

Concretely, self-attention computes three learned projections for each token: a query (Q), a key (K), and a value (V). The model then computes attention scores by taking the dot product between queries and keys, scales them, applies a softmax function to produce a probability distribution, and finally aggregates the values accordingly:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^\top}{\sqrt{d}}\right)V$$

This design enables rich, content-based contextualization. A token's representation is shaped by the entire sequence, which is a major source of the Transformer's expressive power. Because attention is permutation-invariant, Transformers also require explicit positional encodings to convey the order of tokens.

## Computational Complexity of Transformers

The primary drawback of self-attention lies in its computational cost. Because each token attends to every other token, the number of pairwise interactions grows quadratically with sequence length *n*. Specifically, self-attention requires O(n²d) time and O(n²) memory, where *d* is the embedding dimension. The quadratic memory cost arises from the need to store the attention matrix, whose dimensions are *n × n*.

This quadratic scaling imposes a hard constraint on context length. For very long documents, the memory required to store attention matrices and the compute required to process them become prohibitive. During inference, techniques such as KV caching mitigate some costs by reusing previously computed keys and values, but the memory footprint still grows linearly with the context window.

## State Space Models and the Mamba Approach

State Space Models trace their origins to classical control theory, where a system is described by a latent state that evolves over time according to linear differential equations. In the continuous formulation:

$$h'(t) = A\,h(t) + B\,x(t), \quad y(t) = C\,h(t)$$

These equations are discretized for use in deep learning, yielding a recurrence in which a hidden state *h* is updated at each timestep based on the current input. Crucially, the state can be computed via a convolution, which permits efficient parallel computation during training.

Mamba improves upon standard SSMs through a "selective" mechanism. In a conventional SSM, the parameters are fixed across all inputs. Mamba makes the parameters—specifically B, C, and the step size Δ—depend on the input itself. This selectivity allows the model to dynamically decide which information to retain in the state and which to discard, effectively functioning as an information filter. This innovation addresses a key weakness of earlier SSMs, which struggled to capture long-range dependencies because information could degrade as it propagated through many timesteps.

## Computational Complexity of State Space Models

The defining advantage of Mamba is its linear complexity. Because the model processes sequences through a recurrent state update rather than computing pairwise interactions, its computational cost scales as O(n) with sequence length. During inference, the model maintains only a fixed-size hidden state, meaning memory usage remains constant regardless of how long the sequence becomes. This stands in stark contrast to the quadratic demands of Transformer attention.

## Practical Implications for Long-Context Processing

These architectural differences have significant practical consequences. Transformers excel at capturing nuanced, global dependencies and are highly parallelizable during training, but they face memory and compute bottlenecks when processing very long sequences. State Space Models, by contrast, scale gracefully to extended contexts and are memory-efficient at inference, making them attractive for tasks involving lengthy documents, long videos, or extended audio.

It is worth noting that neither architecture is universally superior. Transformers remain the default choice for most applications due to their proven performance and mature ecosystem. Consequently, recent research has explored hybrid designs that combine the strong representational capacity of attention with the efficiency of selective state space models, seeking to capture the benefits of both paradigms.

## Conclusion

In summary, Transformers and State Space Models represent two fundamentally different philosophies of sequence modeling. Transformers achieve contextual richness through dense self-attention at the cost of quadratic complexity, whereas models like Mamba achieve efficiency through selective, recurrent state propagation with linear complexity. As the demand for long-context understanding grows, the trade-offs between these approaches will continue to shape the future of language model architecture.

## Timings

- Time to first token: 0.66s
- Temperature: 0.0
- Total generation: 38.46s
- Reasoning tokens: 568
- Answer tokens: 1163
- Total tokens: 1731

## Server Timings (llama.cpp)

- Prompt tokens: 91
- Prompt eval speed: 139.25 t/s
- Prompt eval time: 653.50 ms
- Generation tokens: 1731
- Generation speed: 45.77 t/s
- Generation time: 37800.69 ms
