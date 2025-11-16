# Using Local Models with GraphRAG via Ollama

This guide explains how to configure GraphRAG to use local models through Ollama instead of cloud-based APIs like OpenAI or Azure OpenAI.

## Why Use Local Models?

- **Privacy**: Keep your data local and private
- **Cost**: No API usage fees
- **Offline**: Works without internet connection
- **Customization**: Use fine-tuned or specialized models

## Prerequisites

### 1. Install Ollama

Visit [ollama.ai](https://ollama.ai) and download Ollama for your platform:

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### 2. Pull Required Models

You need two types of models for GraphRAG:

#### Chat Model (for LLM operations)
```bash
# Recommended options:
ollama pull llama3.2          # Meta's latest model (best balance)
ollama pull llama3.1:70b      # Larger, more capable (requires more RAM)
ollama pull mistral           # Fast and efficient
ollama pull qwen2.5:14b       # Good multilingual support
```

#### Embedding Model (for vector embeddings)
```bash
# Recommended options:
ollama pull nomic-embed-text  # Recommended (768 dimensions)
ollama pull mxbai-embed-large # High quality (1024 dimensions)
ollama pull all-minilm        # Fast, smaller (384 dimensions)
```

### 3. Start Ollama

Ollama usually starts automatically, but you can start it manually:

```bash
ollama serve
```

Verify it's running:
```bash
ollama list
```

## Configuration

### Method 1: Using Dedicated Ollama Model Types (Recommended)

Use the provided example configuration:

```bash
cp examples/ollama_settings.yml settings.yml
```

Or create your own `settings.yml`:

```yaml
models:
  default_chat_model:
    type: ollama_chat
    model: llama3.2
    api_base: http://localhost:11434/v1
    max_tokens: 4000
    temperature: 0.0
    tokens_per_minute: 0  # 0 = unlimited
    requests_per_minute: 0
    model_supports_json: false
    concurrent_requests: 4
    async_mode: threaded

  default_embedding_model:
    type: ollama_embedding
    model: nomic-embed-text
    api_base: http://localhost:11434/v1
    tokens_per_minute: 0
    requests_per_minute: 0
    concurrent_requests: 4
    async_mode: threaded
```

### Method 2: Using OpenAI-Compatible Mode

Alternatively, since Ollama is OpenAI API compatible, you can use:

```yaml
models:
  default_chat_model:
    type: openai_chat
    model: llama3.2
    api_key: "not-required"  # Ollama doesn't need authentication
    api_base: http://localhost:11434/v1
    max_tokens: 4000
    temperature: 0.0

  default_embedding_model:
    type: openai_embedding
    model: nomic-embed-text
    api_key: "not-required"
    api_base: http://localhost:11434/v1
```

## Running GraphRAG with Ollama

Once configured, use GraphRAG normally:

```bash
# Initialize (if first time)
python -m graphrag.index --init --root ./ragtest

# Copy your Ollama settings
cp examples/ollama_settings.yml ./ragtest/settings.yml

# Add your data
cp your_data.txt ./ragtest/input/

# Run indexing
python -m graphrag.index --root ./ragtest

# Query
python -m graphrag.query --root ./ragtest --method local "Your question here"
```

## Performance Tuning

### For Limited RAM

If you have limited RAM (8-16GB):

```yaml
models:
  default_chat_model:
    model: llama3.2:1b  # Smaller variant
    concurrent_requests: 2  # Reduce parallelism

  default_embedding_model:
    model: all-minilm  # Smaller embedding model
    concurrent_requests: 2
```

### For Better Performance

If you have more RAM (32GB+):

```yaml
models:
  default_chat_model:
    model: llama3.1:70b  # Larger model
    concurrent_requests: 8  # More parallelism

  default_embedding_model:
    model: mxbai-embed-large  # Better embeddings
    concurrent_requests: 8
```

### Remote Ollama Server

If running Ollama on a different machine:

```yaml
models:
  default_chat_model:
    api_base: http://192.168.1.100:11434/v1  # Your Ollama server IP
```

## Model Recommendations

### Best Overall Balance
- **Chat**: `llama3.2` or `qwen2.5:14b`
- **Embedding**: `nomic-embed-text`

### Best Quality (Requires 32GB+ RAM)
- **Chat**: `llama3.1:70b`
- **Embedding**: `mxbai-embed-large`

### Fastest (8GB RAM minimum)
- **Chat**: `llama3.2:1b` or `phi3`
- **Embedding**: `all-minilm`

### Multilingual
- **Chat**: `qwen2.5:14b` (excellent for Chinese, Japanese, Korean, etc.)
- **Embedding**: `nomic-embed-text` (supports multiple languages)

## Troubleshooting

### Connection Refused
```bash
# Ensure Ollama is running
ollama serve

# Check if accessible
curl http://localhost:11434/api/tags
```

### Out of Memory
- Use smaller models (llama3.2:1b instead of llama3.1:70b)
- Reduce `concurrent_requests` to 1 or 2
- Close other applications

### Slow Performance
- Use GPU acceleration if available (Ollama auto-detects)
- Reduce `max_tokens` if generating long outputs
- Use faster models (phi3, mistral)

### Model Not Found
```bash
# List available models
ollama list

# Pull the model if missing
ollama pull llama3.2
```

## Alternative Local Model Solutions

Besides Ollama, GraphRAG can be extended to support:

1. **LM Studio**: Similar to Ollama, OpenAI-compatible
   - Use `openai_chat` type with custom `api_base`

2. **vLLM**: High-performance inference server
   - Use `openai_chat` type with custom `api_base`

3. **LocalAI**: OpenAI-compatible API
   - Use `openai_chat` type with custom `api_base`

## Example: Complete Workflow

```bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Pull models
ollama pull llama3.2
ollama pull nomic-embed-text

# 3. Verify models are available
ollama list

# 4. Initialize GraphRAG project
python -m graphrag.index --init --root ./my_project

# 5. Configure for Ollama
cp examples/ollama_settings.yml ./my_project/settings.yml

# 6. Add your documents
cp my_documents/*.txt ./my_project/input/

# 7. Build the knowledge graph
python -m graphrag.index --root ./my_project

# 8. Query the graph
python -m graphrag.query --root ./my_project --method local "What are the main themes?"
```

## Additional Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Ollama Model Library](https://ollama.ai/library)
- [GraphRAG Documentation](https://microsoft.github.io/graphrag/)
