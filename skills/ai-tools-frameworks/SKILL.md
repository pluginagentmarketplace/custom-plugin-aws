---
name: ai-tools-frameworks
description: Master LLM applications, prompt engineering, AI frameworks, and modern AI tools for building intelligent applications.
---

# AI Tools & LLM Frameworks

## Quick Start

Build applications powered by Large Language Models and AI frameworks.

## Large Language Models

### Popular LLMs

**OpenAI**
- GPT-4 / GPT-4 Turbo
- High quality, expensive
- API access

**Anthropic Claude**
- Claude 3 series
- Safety-focused
- Long context windows

**Meta Llama**
- Open source
- Self-hosted capable
- Growing ecosystem

**Google Gemini**
- Multimodal (text, image, video)
- Integrated in Google Cloud

## Prompt Engineering

### Prompt Structure

**System Prompt** - Set context and behavior
```
You are an expert Python developer.
Provide clear, well-documented code.
```

**User Prompt** - User request
```
Write a function to validate email addresses.
```

**Few-shot Examples** - Show examples
```
Example 1: "hello" → hello world
Example 2: "goodbye" → goodbye world
```

### Techniques

**Chain-of-Thought**
- Break down complex problems
- Step-by-step reasoning
- Improves accuracy

**Few-shot Learning**
- Provide examples
- Better than zero-shot
- Cost: more tokens

**Retrieval-Augmented Generation (RAG)**
- Combine retrieval + generation
- Add context from documents
- More accurate, grounded responses

## LLM Frameworks

### LangChain

```python
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

model = ChatOpenAI(model="gpt-4")

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple terms"
)

chain = LLMChain(llm=model, prompt=prompt)
result = chain.run(topic="quantum computing")
```

**Key Concepts**
- Chains (sequences of operations)
- Agents (decision-making entities)
- Tools (external integrations)
- Memory (conversation history)

### LlamaIndex (formerly GPT Index)

```python
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader('data').load_data()
index = GPTVectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("What is the main topic?")
```

**RAG Pipeline**
1. Load documents
2. Create vector embeddings
3. Build index
4. Query with retrieval
5. Generate response

### LiteLLM

```python
import litellm

response = litellm.completion(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hi"}],
)
```

## Embeddings & Vector Databases

### Embedding Models

- OpenAI text-embedding-3
- Sentence Transformers
- Anthropic embeddings

### Vector Databases

**Pinecone** - Managed vector search
**Weaviate** - Open source vector DB
**Milvus** - Scalable vector search
**Qdrant** - Vector DB with filtering
**Chroma** - Simple embeddings store

```python
from pinecone import Pinecone

pc = Pinecone(api_key="...")
index = pc.Index("documents")
index.upsert(vectors=[("1", embedding, {"text": "..."})])
results = index.query(query_embedding, top_k=5)
```

## AI Agent Development

### ReAct Pattern

**R**easoning - Think about the problem
**A**ction - Use available tools
**O**bservation - Get results
**T**hink - Iterate

```python
from langchain.agents import initialize_agent, Tool

tools = [
    Tool(name="Calculator", func=calculate, description="..."),
    Tool(name="WebSearch", func=search, description="...")
]

agent = initialize_agent(
    tools,
    model,
    agent="zero-shot-react-description",
    verbose=True
)

agent.run("What is the population of France and the square root of 2?")
```

## Fine-tuning

### Advantages
- Domain-specific knowledge
- Better performance
- Reduced token usage

### Process
1. Prepare training data
2. Fine-tune model
3. Evaluate performance
4. Deploy fine-tuned version

## Token Management

**Token Counting**
```python
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4")
tokens = enc.encode("Hello world")
print(len(tokens))
```

**Cost Optimization**
- Use cheaper models when possible
- Cache repeated queries
- Batch process requests
- Monitor token usage

## Roadmaps Covered

- AI Engineer (https://roadmap.sh/ai-engineer)
- Prompt Engineering (https://roadmap.sh/prompt-engineering)
