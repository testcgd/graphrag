# Configuring Different Models for Indexing vs Querying

This guide explains how to use different models for indexing (building the knowledge graph) versus querying (answering questions) in GraphRAG.

## Table of Contents

- [Why Use Different Models?](#why-use-different-models)
- [How It Works](#how-it-works)
- [Configuration Overview](#configuration-overview)
- [Common Use Cases](#common-use-cases)
- [Step-by-Step Examples](#step-by-step-examples)
- [Model Selection Guide](#model-selection-guide)
- [Cost Optimization](#cost-optimization)
- [Troubleshooting](#troubleshooting)

## Why Use Different Models?

GraphRAG has two distinct phases, each with different requirements:

### Indexing Phase (One-Time, Bulk Processing)
- **Operations**: Entity extraction, summarization, community reports, embeddings
- **Characteristics**: Large volume, one-time cost, batch processing
- **Ideal Models**: Fast, efficient, cost-effective
- **Priority**: Speed and cost over maximum quality

### Query Phase (Ongoing, Interactive)
- **Operations**: Question answering, context retrieval, reasoning
- **Characteristics**: Low volume, ongoing cost, real-time
- **Ideal Models**: High-quality, accurate, capable reasoning
- **Priority**: Quality and accuracy over speed/cost

## How It Works

GraphRAG's configuration system already supports model separation:

```yaml
models:
  # Define multiple models
  fast_model: { ... }
  powerful_model: { ... }

# Indexing operations reference their models
extract_graph:
  model_id: fast_model  # Use fast model for extraction

# Query operations reference their models
local_search:
  chat_model_id: powerful_model  # Use powerful model for queries
```

**No code changes needed** - it's pure configuration!

## Configuration Overview

### Model Definition Section

```yaml
models:
  # You can define as many models as you need
  model_name_1:
    type: ollama_chat | openai_chat | azure_openai_chat
    model: model-identifier
    api_base: endpoint-url
    # ... other parameters

  model_name_2:
    type: ollama_embedding | openai_embedding | azure_openai_embedding
    # ... parameters
```

### Indexing Operations (Model References)

Each indexing operation has a `model_id` field:

```yaml
extract_graph:
  model_id: your_chosen_model  # Entity & relationship extraction

summarize_descriptions:
  model_id: your_chosen_model  # Entity description summarization

community_reports:
  model_id: your_chosen_model  # Community report generation

extract_claims:
  model_id: your_chosen_model  # Claim extraction (if enabled)

embed_text:
  model_id: your_chosen_embedding  # Text embeddings
```

### Query Operations (Model References)

Each query type has `chat_model_id` and/or `embedding_model_id`:

```yaml
local_search:
  chat_model_id: your_chat_model
  embedding_model_id: your_embedding_model

global_search:
  chat_model_id: your_chat_model

drift_search:
  chat_model_id: your_chat_model
  embedding_model_id: your_embedding_model
```

## Common Use Cases

### Use Case 1: All-Local with Different Sizes

**Scenario**: Use local Ollama models, but different sizes for index vs query

```yaml
models:
  # Small, fast for indexing
  index_model:
    type: ollama_chat
    model: llama3.2  # ~7B parameters

  # Large, powerful for querying
  query_model:
    type: ollama_chat
    model: llama3.1:70b  # 70B parameters

# Apply to operations
extract_graph:
  model_id: index_model

local_search:
  chat_model_id: query_model
```

**Benefits**: Save time during indexing, get better answers during queries

### Use Case 2: Hybrid Cloud-Local

**Scenario**: Free local models for indexing, paid cloud for querying

```yaml
models:
  local_index:
    type: ollama_chat
    model: qwen2.5:14b
    api_base: http://localhost:11434/v1

  cloud_query:
    type: openai_chat
    api_key: ${OPENAI_API_KEY}
    model: gpt-4o

extract_graph:
  model_id: local_index  # FREE

local_search:
  chat_model_id: cloud_query  # PAID but high quality
```

**Benefits**: Minimize API costs, maintain query quality

### Use Case 3: Different Cloud Models

**Scenario**: Use cheaper cloud models for indexing, premium for queries

```yaml
models:
  cheap_index:
    type: openai_chat
    model: gpt-4o-mini  # Cheaper

  premium_query:
    type: openai_chat
    model: gpt-4o  # More expensive but better

extract_graph:
  model_id: cheap_index

local_search:
  chat_model_id: premium_query
```

**Benefits**: Reduce indexing costs while maintaining quality queries

### Use Case 4: Specialized Models

**Scenario**: Use models specialized for different tasks

```yaml
models:
  extraction_specialist:
    type: ollama_chat
    model: mistral  # Good at structured extraction
    temperature: 0.0  # Deterministic

  reasoning_specialist:
    type: openai_chat
    model: gpt-4o  # Excellent reasoning
    temperature: 0.1  # Slightly creative

extract_graph:
  model_id: extraction_specialist

local_search:
  chat_model_id: reasoning_specialist
```

**Benefits**: Optimize each phase with best-suited models

## Step-by-Step Examples

### Example 1: Basic Local Separation

**Goal**: Fast indexing, quality queries, all local

**Step 1**: Pull required Ollama models
```bash
ollama pull llama3.2      # Fast indexing model
ollama pull llama3.1:70b  # Quality query model
ollama pull nomic-embed-text  # Embedding model
```

**Step 2**: Create `settings.yml`
```yaml
models:
  index_chat:
    type: ollama_chat
    model: llama3.2
    api_base: http://localhost:11434/v1
    concurrent_requests: 8  # Parallel processing

  query_chat:
    type: ollama_chat
    model: llama3.1:70b
    api_base: http://localhost:11434/v1
    concurrent_requests: 2  # Large model, less parallel

  shared_embedding:
    type: ollama_embedding
    model: nomic-embed-text
    api_base: http://localhost:11434/v1

  default_chat_model:
    type: ollama_chat
    model: llama3.1:70b
    api_base: http://localhost:11434/v1

  default_embedding_model:
    type: ollama_embedding
    model: nomic-embed-text
    api_base: http://localhost:11434/v1

# Indexing uses fast model
extract_graph:
  model_id: index_chat

summarize_descriptions:
  model_id: index_chat

community_reports:
  model_id: index_chat

embed_text:
  model_id: shared_embedding

# Querying uses powerful model
local_search:
  chat_model_id: query_chat
  embedding_model_id: shared_embedding

global_search:
  chat_model_id: query_chat
```

**Step 3**: Run indexing
```bash
python -m graphrag.index --root ./project
```

**Step 4**: Run queries
```bash
python -m graphrag.query --root ./project --method local "Your question"
```

### Example 2: Hybrid Setup

**Goal**: Zero-cost indexing, production-quality queries

**Step 1**: Setup Ollama and pull models
```bash
ollama pull qwen2.5:14b
ollama pull nomic-embed-text
```

**Step 2**: Get OpenAI API key
```bash
export OPENAI_API_KEY="sk-..."
```

**Step 3**: Create `settings.yml`
```yaml
models:
  local_index_chat:
    type: ollama_chat
    model: qwen2.5:14b
    api_base: http://localhost:11434/v1

  local_index_embed:
    type: ollama_embedding
    model: nomic-embed-text
    api_base: http://localhost:11434/v1

  cloud_query_chat:
    type: openai_chat
    api_key: ${OPENAI_API_KEY}
    model: gpt-4o

  cloud_query_embed:
    type: openai_embedding
    api_key: ${OPENAI_API_KEY}
    model: text-embedding-3-large

  default_chat_model:
    type: openai_chat
    api_key: ${OPENAI_API_KEY}
    model: gpt-4o

  default_embedding_model:
    type: openai_embedding
    api_key: ${OPENAI_API_KEY}
    model: text-embedding-3-large

# All indexing uses local (free)
extract_graph:
  model_id: local_index_chat

summarize_descriptions:
  model_id: local_index_chat

community_reports:
  model_id: local_index_chat

embed_text:
  model_id: local_index_embed

# All querying uses cloud (paid, quality)
local_search:
  chat_model_id: cloud_query_chat
  embedding_model_id: cloud_query_embed

global_search:
  chat_model_id: cloud_query_chat
```

**Step 4**: Index locally (no cost)
```bash
python -m graphrag.index --root ./project
```

**Step 5**: Query with GPT-4 (high quality)
```bash
python -m graphrag.query --root ./project --method local "Your question"
```

## Model Selection Guide

### For Indexing (Speed & Efficiency Priority)

#### Chat Models
| Resource Level | Recommended Model | Notes |
|---------------|-------------------|-------|
| Low (8GB) | `llama3.2:1b` | Fastest, basic quality |
| Medium (16GB) | `llama3.2` or `mistral` | Good balance |
| High (32GB+) | `qwen2.5:14b` | High quality, good speed |
| Cloud Budget | `gpt-4o-mini` | Cheap cloud option |

#### Embedding Models
| Resource Level | Recommended Model | Dimensions | Notes |
|---------------|-------------------|------------|-------|
| Low | `all-minilm` | 384 | Fastest, basic quality |
| Medium | `nomic-embed-text` | 768 | Recommended default |
| High | `mxbai-embed-large` | 1024 | Best quality |
| Cloud | `text-embedding-3-small` | 1536 | Good cloud option |

### For Querying (Quality Priority)

#### Chat Models
| Budget | Recommended Model | Notes |
|--------|-------------------|-------|
| Free/Local | `llama3.1:70b` | Best free option |
| Low Cloud | `gpt-4o-mini` | Good quality/cost ratio |
| Production | `gpt-4o` | Best overall quality |
| Specialized | `claude-3.5-sonnet` | Excellent reasoning |

#### Embedding Models
| Type | Recommended Model | Notes |
|------|-------------------|-------|
| Local | `mxbai-embed-large` | Best local quality |
| Cloud | `text-embedding-3-large` | Best cloud quality |

## Cost Optimization

### Strategy 1: All-Local
**Cost**: $0 (electricity only)
**Setup**:
```yaml
# All models point to Ollama
models:
  index_chat: {type: ollama_chat, model: llama3.2}
  query_chat: {type: ollama_chat, model: llama3.1:70b}
```
**Best for**: Privacy-sensitive, high-volume, or development use

### Strategy 2: Hybrid (Recommended)
**Cost**: ~50-70% savings vs all-cloud
**Setup**:
```yaml
# Indexing = local (free), Querying = cloud (paid)
models:
  index_chat: {type: ollama_chat, model: qwen2.5:14b}
  query_chat: {type: openai_chat, model: gpt-4o}
```
**Best for**: Production use with cost constraints

### Strategy 3: Tiered Cloud
**Cost**: ~30-50% savings vs all premium cloud
**Setup**:
```yaml
# Indexing = cheap cloud, Querying = premium cloud
models:
  index_chat: {type: openai_chat, model: gpt-4o-mini}
  query_chat: {type: openai_chat, model: gpt-4o}
```
**Best for**: Cloud-only environments

## Troubleshooting

### Issue: "Model ID not found"

**Cause**: Referenced a model_id that wasn't defined

**Solution**: Ensure all referenced models are defined
```yaml
models:
  my_model:  # Define here
    type: ollama_chat

extract_graph:
  model_id: my_model  # Reference here (must match)
```

### Issue: Different embedding dimensions

**Cause**: Using different embedding models for index vs query

**Solution**: Use the same embedding model, or rebuild index
```yaml
# Option 1: Use same embedding model
embed_text:
  model_id: shared_embeddings
local_search:
  embedding_model_id: shared_embeddings

# Option 2: If you must change, reindex
python -m graphrag.index --root ./project  # Rebuild with new embeddings
```

### Issue: Out of memory during querying

**Cause**: Query model is too large

**Solution**: Use smaller query model or reduce concurrency
```yaml
query_chat:
  model: llama3.2  # Instead of llama3.1:70b
  concurrent_requests: 1  # Reduce parallelism
```

### Issue: Slow indexing

**Cause**: Using large model for indexing

**Solution**: Switch to faster indexing model
```yaml
extract_graph:
  model_id: fast_model  # Use llama3.2 instead of llama3.1:70b
```

## Best Practices

1. **Always use fast models for indexing**: Indexing is one-time, speed matters more than maximum quality

2. **Use quality models for querying**: Queries are ongoing and user-facing, quality is critical

3. **Keep embedding models consistent**: Avoid changing embedding models after indexing

4. **Test before production**: Validate quality with sample queries before committing

5. **Monitor costs**: Track API usage if using cloud models

6. **Document your choices**: Note why you chose specific models in your config file

## Quick Reference

See these example configurations:

- `examples/ollama_settings.yml` - Basic local setup
- `examples/ollama_mixed_models.yml` - Different local models for index vs query
- `examples/hybrid_cloud_local.yml` - Local indexing, cloud querying

## Summary

GraphRAG natively supports using different models for indexing vs querying through simple configuration. This enables:

✓ Cost optimization (use cheaper/free models for indexing)
✓ Performance tuning (use faster models for indexing)
✓ Quality optimization (use better models for querying)
✓ Flexibility (mix local and cloud models)

No code changes required - just configure your `settings.yml` appropriately!
