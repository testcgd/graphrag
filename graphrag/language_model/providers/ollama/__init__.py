# Copyright (c) 2025 Microsoft Corporation.
# Licensed under the MIT License

"""Ollama model provider."""

from graphrag.language_model.providers.ollama.models import (
    OllamaChatModel,
    OllamaEmbeddingModel,
)

__all__ = ["OllamaChatModel", "OllamaEmbeddingModel"]
