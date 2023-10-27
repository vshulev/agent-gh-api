# GitHub API Agent

An agent based on ChatGPT which can answer questions about the GitHub API.

I have tested this with GPT-3.5 but I suspect GPT-4 will be able to answer more questions.

## How to run?

Code has been tested with Python 3.10. To run, set up a new virtual environment and activate it:

```
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

To run the agent:

```
$ python agent.py --api_key="YOUR_OPEN_AI_API_KEY"
```

An example interaction with the agent is available in the file `example.md`

## Implementation details

The implementaiton uses `llama-index` -- a framework for Retrieval-augmented generation (RAG). The `llama-index` library comes with a variety of tools which are capable of reading different datasources and adds indexing and querying capabilities to an existing LLM. I chose the library because of it's simplicity and the availability of a tool which can ingest OpenAPI specifications.

RAG provides a workaround for the limited context windows of LLMs when working with large amounts of data (e.g. very long documents). It does so by chunking a document or set of document into smaller pieces which are stored in a vector databse. At inference time a similarity search is performed between a user's prompt and the chunks stored in the vector databases. Relevant parts of the documents are injected as part of the prompt given to an LLM before it generates text. Thus the LLM is made "aware" of any information from external sources which is relevant to a user's query.

## Future work

### Automatic evaluation

First and foremost, in order to make this agent production-ready, we need to pick a set of automatic evaluation metrics that will ensure the agent generates helpful and truthful outputs. One possible solution would be to, given a set of questions, ask humans to generate reference answers to those questions. These references can then be compared against agent outputs using machine translation metrics such as BLEU or COMET.

### Choice of LLM

For this example I used GPT-3.5 because I don't have access to GPT-4. However, for production use it is worthwhile considering the requirements and evaluating various LLMs.

The choice of LLM can be dictated by certain requirements. For example, for best generation quality GPT-4 is preferable over GPT-3.5. However, this comes at a higher cost.

Currently the agent is unable to answer questions "What are the core resources exposed by the API?" which may require retriving many relevant document chunks and can thus be unsuitable for RAG. If questions which require referencing many pieces of the document are important then it is probably worthwhile testing a model such as Claude, which is able to fit very large documents (up to 100k tokens) in its context. Additionally a model which supports very large contexts may eliminate the need for a vector database and thus really simplify the agent's architecture.

In case cost or data privacy are important issue, then it would be worthwhile evaluating an open-source model such as llama.cpp, which is potentially capable of running even on CPU. Furthemore, smaller open-source LLMs may be sufficient for the task given that an agent probably doesn't need much world knowledge to answer questions about a document that it has access to.

### Agent memory storage

This example uses a simple in-memory vector store. However, for production use this is going to be most likely insufficient. Thus a production-ready vector store such as FAISS, pinecone, or any other commercial vector database is probably desirable.
