# CLAUDE.md

We are running local AI models on our machines and want to have a way to benchmark them. We are specifically benchmarking for agentic use of the models so there will only be 1 concurrent user. 

We will only use Ramalama for model serving. It's documentation is here: https://ramalama.ai/docs/introduction. When you are going to give a Ramala command you should ALWAYS read the documentation from the website first.

We are going to use GuideLLM as our benchmark tool and we will only run it inside a container. Here is the web site for GuideLLM: https://vllm-project.github.io/guidellm/stable/
Since we are testing only 1 concurrent user we will always use the flag `--rate-type synchronous"

## Project Status

We are just getting started