# GraphRAG Configuration Examples

This directory contains comprehensive configuration examples for using GraphRAG with various model providers, especially local models via Ollama.

## Quick Start Guides

### 🚀 Basic Ollama Setup
**File**: `ollama_settings.yml`
**Use case**: Get started with local models quickly
**Models**: llama3.2 (chat), nomic-embed-text (embedding)
**Requirements**: 16GB RAM minimum

```bash
# Setup
ollama pull llama3.2
ollama pull nomic-embed-text
cp examples/ollama_settings.yml ./my_project/settings.yml

# Run
python -m graphrag.index --root ./my_project
python -m graphrag.query --root ./my_project --method local "your question"
```

**See also**: `OLLAMA_SETUP.md` for complete installation and usage guide

---

## Advanced Configurations

### 💡 Different Models for Indexing vs Querying
**File**: `ollama_mixed_models.yml`
**Use case**: Optimize performance and cost
**Strategy**: Fast models for one-time indexing, powerful models for ongoing queries

**Example**:
- **Indexing**: llama3.2 (fast, 7B)
- **Querying**: llama3.1:70b (powerful, 70B)
- **Result**: Faster indexing + higher quality answers

**Guide**: See `CONFIGURE_DIFFERENT_MODELS.md` for detailed explanation

---

### 💰 Hybrid Cloud-Local Setup
**File**: `hybrid_cloud_local.yml`
**Use case**: Minimize API costs while maintaining quality
**Strategy**: Free local models for indexing, paid cloud models for queries

**Example**:
- **Indexing**: Ollama qwen2.5:14b (local, FREE)
- **Querying**: OpenAI gpt-4o (cloud, PAID)
- **Savings**: 50-70% cost reduction vs all-cloud

**Best for**: Production deployments with budget constraints

---

### 🌐 Multilingual & Embedding Models
**File**: `ollama_embedding_models.yml`
**Use case**: Choose the right embedding model for your needs
**Covers**: All major embedding models with comparison

**Embedding Models Included**:
- `nomic-embed-text` - Recommended default (768 dims)
- `mxbai-embed-large` - Highest quality (1024 dims)
- `all-minilm` - Fastest, smallest (384 dims)
- `bge-m3` - Best for Chinese+English (1024 dims)
- `paraphrase-multilingual` - 50+ languages (768 dims)
- `snowflake-arctic-embed` - Retrieval-optimized (1024 dims)

**Best for**: Understanding embedding model trade-offs and selecting the right one

---

### 🇨🇳 Chinese-Optimized Configuration (中文优化)
**File**: `ollama_qwen_setup.yml`
**Use case**: Chinese and multilingual content processing
**Models**: Qwen2.5 series + BGE embeddings

**Qwen Models**:
- `qwen2.5:7b` - Fast, good quality (4.7 GB)
- `qwen2.5:14b` - Recommended (9.0 GB)
- `qwen2.5:32b` - High quality (20 GB)
- `qwen2.5:72b` - Best quality (43 GB)

**Embeddings**:
- `bge-m3` - Optimized for Chinese+English

**Best for**: Chinese documents, multilingual content, mixed language processing

---

## Configuration Comparison

| Configuration | Indexing | Querying | Cost | Quality | Best For |
|--------------|----------|----------|------|---------|----------|
| Basic Ollama | Local (llama3.2) | Local (llama3.2) | $0 | ★★★☆☆ | Development, learning |
| Mixed Models | Local (llama3.2) | Local (llama3.1:70b) | $0 | ★★★★☆ | Production local |
| Hybrid | Local (qwen2.5:14b) | Cloud (gpt-4o) | Low | ★★★★★ | Production budget |
| Qwen Setup | Local (qwen2.5:14b) | Local (qwen2.5:32b) | $0 | ★★★★★ | Chinese content |

---

## Documentation

### Complete Guides

1. **`OLLAMA_SETUP.md`** - Comprehensive Ollama setup guide
   - Installation instructions
   - Model selection guide
   - Performance tuning
   - Troubleshooting
   - Advanced configurations

2. **`CONFIGURE_DIFFERENT_MODELS.md`** - Using different models for index vs query
   - Why and when to use different models
   - Configuration patterns
   - Cost optimization strategies
   - Step-by-step examples
   - Best practices

---

## Configuration Files Reference

### Basic Configurations
- `ollama_settings.yml` - Single local setup (recommended starting point)

### Advanced Configurations
- `ollama_mixed_models.yml` - Different models for index/query
- `hybrid_cloud_local.yml` - Cloud-local hybrid
- `ollama_embedding_models.yml` - Embedding model guide
- `ollama_qwen_setup.yml` - Chinese-optimized setup

### Azure/Cloud Configurations
- `azure/settings.yml` - Azure OpenAI configuration
- `text/settings.yml` - General cloud configuration

---

## Common Use Cases

### Use Case 1: Local-Only (Privacy-Focused)
**Configuration**: `ollama_settings.yml` or `ollama_qwen_setup.yml`
**Cost**: $0 (electricity only)
**Privacy**: Complete - no data leaves your machine
**Best for**: Sensitive data, offline work, development

### Use Case 2: Cost Optimization
**Configuration**: `hybrid_cloud_local.yml`
**Cost**: 50-70% savings vs all-cloud
**Strategy**: Local indexing (one-time), cloud queries (ongoing)
**Best for**: Budget-conscious production deployments

### Use Case 3: Maximum Quality
**Configuration**: `ollama_mixed_models.yml` with large models
**Models**: llama3.1:70b or qwen2.5:72b
**Cost**: $0 but requires powerful hardware
**Best for**: Quality-critical applications with local hardware

### Use Case 4: Multilingual Content
**Configuration**: `ollama_qwen_setup.yml` or `ollama_embedding_models.yml`
**Models**: qwen2.5 + bge-m3 or paraphrase-multilingual
**Best for**: Mixed language documents, Chinese content

### Use Case 5: Development & Testing
**Configuration**: `ollama_settings.yml` with small models
**Models**: llama3.2:1b or qwen2.5:7b
**Resources**: Minimal (8GB RAM)
**Best for**: Quick iteration, testing, learning GraphRAG

---

## Quick Selection Guide

### Choose Your Configuration:

**I want to...**

- ✅ Get started quickly → `ollama_settings.yml`
- 💰 Save money on APIs → `hybrid_cloud_local.yml`
- 🚀 Optimize performance → `ollama_mixed_models.yml`
- 🌏 Process Chinese content → `ollama_qwen_setup.yml`
- 🔍 Choose best embeddings → `ollama_embedding_models.yml`
- 📖 Understand concepts → `CONFIGURE_DIFFERENT_MODELS.md`
- 🛠️ Troubleshoot issues → `OLLAMA_SETUP.md`

---

## Model Requirements

### Memory Requirements by Model Size

| Model Size | RAM Needed | Examples | Use Case |
|------------|-----------|----------|----------|
| 1-3B | 8GB | llama3.2:1b, qwen2.5:3b | Testing, low-resource |
| 7-14B | 16GB | llama3.2, qwen2.5:14b | Recommended default |
| 30-40B | 32GB | qwen2.5:32b | High quality |
| 70B+ | 48GB+ | llama3.1:70b, qwen2.5:72b | Maximum quality |

### Disk Space

- **Chat models**: 500MB - 43GB (depending on size)
- **Embedding models**: 23MB - 2.3GB
- **GraphRAG index**: Varies by corpus size (typically 1-10GB)

---

## Getting Help

### Troubleshooting Resources

1. **Installation issues**: See `OLLAMA_SETUP.md` → Troubleshooting section
2. **Configuration errors**: See `CONFIGURE_DIFFERENT_MODELS.md` → Troubleshooting
3. **Model selection**: See `ollama_embedding_models.yml` → Model comparison
4. **Performance tuning**: See `OLLAMA_SETUP.md` → Performance Tuning

### Common Issues

- **Out of memory**: Use smaller models or reduce `concurrent_requests`
- **Slow performance**: Check GPU usage, reduce model size, or increase concurrency
- **Model not found**: Run `ollama pull <model-name>`
- **Poor quality**: Use larger models or better embedding models

---

## Contributing

Found an issue or want to add a configuration example? Please submit a PR or issue to the GraphRAG repository.

---

## Additional Resources

- [GraphRAG Documentation](https://microsoft.github.io/graphrag/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Ollama Model Library](https://ollama.ai/library)
- [Qwen Models](https://github.com/QwenLM/Qwen2.5)
- [BGE Embeddings](https://github.com/FlagOpen/FlagEmbedding)

---

## License

These configuration examples are part of the Microsoft GraphRAG project and are licensed under the MIT License.
