# Copyright (c) 2025 Microsoft Corporation.
# Licensed under the MIT License

"""Ollama model provider implementations."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fnllm.openai import (
    create_openai_chat_llm,
    create_openai_client,
    create_openai_embeddings_llm,
)

from graphrag.language_model.providers.fnllm.events import FNLLMEvents
from graphrag.language_model.providers.fnllm.utils import (
    _create_cache,
    _create_error_handler,
    run_coroutine_sync,
)
from graphrag.language_model.response.base import (
    BaseModelOutput,
    BaseModelResponse,
    ModelResponse,
)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Generator

    from fnllm.openai.types.client import OpenAIChatLLM as FNLLMChatLLM
    from fnllm.openai.types.client import OpenAIEmbeddingsLLM as FNLLMEmbeddingLLM

    from graphrag.cache.pipeline_cache import PipelineCache
    from graphrag.callbacks.workflow_callbacks import WorkflowCallbacks
    from graphrag.config.models.language_model_config import (
        LanguageModelConfig,
    )


def _create_ollama_config(config: LanguageModelConfig):
    """Create an Ollama config from a LanguageModelConfig.

    Ollama is OpenAI API compatible, so we use the PublicOpenAIConfig.
    The main differences are:
    - Default base_url is http://localhost:11434/v1
    - API key can be any value (Ollama doesn't use authentication)
    """
    from fnllm.base.config import JsonStrategy, RetryStrategy
    from fnllm.openai import PublicOpenAIConfig
    from fnllm.openai.types.chat.parameters import OpenAIChatParameters

    # Default Ollama endpoint if not specified
    base_url = config.api_base or "http://localhost:11434/v1"

    # Ollama doesn't use API keys, but fnllm requires one, so use a placeholder
    api_key = config.api_key or "ollama"

    # Ollama models generally don't support JSON mode, so use LOOSE strategy
    json_strategy = (
        JsonStrategy.VALID if config.model_supports_json else JsonStrategy.LOOSE
    )

    chat_parameters = OpenAIChatParameters(
        frequency_penalty=config.frequency_penalty,
        presence_penalty=config.presence_penalty,
        top_p=config.top_p,
        max_tokens=config.max_tokens,
        n=config.n,
        temperature=config.temperature,
    )

    return PublicOpenAIConfig(
        api_key=api_key,
        base_url=base_url,
        json_strategy=json_strategy,
        organization=config.organization,
        retry_strategy=RetryStrategy(config.retry_strategy),
        max_retries=config.max_retries,
        max_retry_wait=config.max_retry_wait,
        requests_per_minute=config.requests_per_minute,
        tokens_per_minute=config.tokens_per_minute,
        timeout=config.request_timeout,
        max_concurrency=config.concurrent_requests,
        model=config.model,
        encoding=config.encoding_model,
        chat_parameters=chat_parameters,
        sleep_on_rate_limit_recommendation=False,  # Ollama doesn't have rate limits
    )


class OllamaChatModel:
    """An Ollama Chat Model provider using the fnllm library.

    Ollama is OpenAI API compatible, so this implementation leverages
    the OpenAI client with custom configuration.
    """

    model: FNLLMChatLLM

    def __init__(
        self,
        *,
        name: str,
        config: LanguageModelConfig,
        callbacks: WorkflowCallbacks | None = None,
        cache: PipelineCache | None = None,
    ) -> None:
        model_config = _create_ollama_config(config)
        error_handler = _create_error_handler(callbacks) if callbacks else None
        model_cache = _create_cache(cache, name)
        client = create_openai_client(model_config)
        self.model = create_openai_chat_llm(
            model_config,
            client=client,
            cache=model_cache,
            events=FNLLMEvents(error_handler) if error_handler else None,
        )

    async def achat(
        self, prompt: str, history: list | None = None, **kwargs
    ) -> ModelResponse:
        """
        Chat with the Model using the given prompt.

        Args:
            prompt: The prompt to chat with.
            history: The conversation history.
            kwargs: Additional arguments to pass to the Model.

        Returns
        -------
            The response from the Model.
        """
        if history is None:
            response = await self.model(prompt, **kwargs)
        else:
            response = await self.model(prompt, history=history, **kwargs)
        return BaseModelResponse(
            output=BaseModelOutput(content=response.output.content),
            parsed_response=response.parsed_json,
            history=response.history,
            cache_hit=response.cache_hit,
            tool_calls=response.tool_calls,
            metrics=response.metrics,
        )

    async def achat_stream(
        self, prompt: str, history: list | None = None, **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        Stream Chat with the Model using the given prompt.

        Args:
            prompt: The prompt to chat with.
            history: The conversation history.
            kwargs: Additional arguments to pass to the Model.

        Returns
        -------
            A generator that yields strings representing the response.
        """
        if history is None:
            response = await self.model(prompt, stream=True, **kwargs)
        else:
            response = await self.model(prompt, history=history, stream=True, **kwargs)
        async for chunk in response.output.content:
            if chunk is not None:
                yield chunk

    def chat(self, prompt: str, history: list | None = None, **kwargs) -> ModelResponse:
        """
        Chat with the Model using the given prompt.

        Args:
            prompt: The prompt to chat with.
            history: The conversation history.
            kwargs: Additional arguments to pass to the Model.

        Returns
        -------
            The response from the Model.
        """
        return run_coroutine_sync(self.achat(prompt, history=history, **kwargs))

    def chat_stream(
        self, prompt: str, history: list | None = None, **kwargs
    ) -> Generator[str, None]:
        """
        Stream Chat with the Model using the given prompt.

        Args:
            prompt: The prompt to chat with.
            history: The conversation history.
            kwargs: Additional arguments to pass to the Model.

        Returns
        -------
            A generator that yields strings representing the response.
        """
        msg = "chat_stream is not supported for synchronous execution"
        raise NotImplementedError(msg)


class OllamaEmbeddingModel:
    """An Ollama Embedding Model provider using the fnllm library.

    Ollama is OpenAI API compatible, so this implementation leverages
    the OpenAI client with custom configuration.
    """

    model: FNLLMEmbeddingLLM

    def __init__(
        self,
        *,
        name: str,
        config: LanguageModelConfig,
        callbacks: WorkflowCallbacks | None = None,
        cache: PipelineCache | None = None,
    ) -> None:
        model_config = _create_ollama_config(config)
        error_handler = _create_error_handler(callbacks) if callbacks else None
        model_cache = _create_cache(cache, name)
        client = create_openai_client(model_config)
        self.model = create_openai_embeddings_llm(
            model_config,
            client=client,
            cache=model_cache,
            events=FNLLMEvents(error_handler) if error_handler else None,
        )

    async def aembed_batch(self, text_list: list[str], **kwargs) -> list[list[float]]:
        """
        Embed the given text using the Model.

        Args:
            text_list: The list of texts to embed.
            kwargs: Additional arguments to pass to the Model.

        Returns
        -------
            The embeddings of the text.
        """
        response = await self.model(text_list, **kwargs)
        if response.output.embeddings is None:
            msg = "No embeddings found in response"
            raise ValueError(msg)
        embeddings: list[list[float]] = response.output.embeddings
        return embeddings

    async def aembed(self, text: str, **kwargs) -> list[float]:
        """
        Embed the given text using the Model.

        Args:
            text: The text to embed.
            kwargs: Additional arguments to pass to the Model.

        Returns
        -------
            The embeddings of the text.
        """
        response = await self.model([text], **kwargs)
        if response.output.embeddings is None:
            msg = "No embeddings found in response"
            raise ValueError(msg)
        embeddings: list[float] = response.output.embeddings[0]
        return embeddings

    def embed_batch(self, text_list: list[str], **kwargs) -> list[list[float]]:
        """
        Embed the given text using the Model.

        Args:
            text_list: The list of texts to embed.
            kwargs: Additional arguments to pass to the Model.

        Returns
        -------
            The embeddings of the text.
        """
        return run_coroutine_sync(self.aembed_batch(text_list, **kwargs))

    def embed(self, text: str, **kwargs) -> list[float]:
        """
        Embed the given text using the Model.

        Args:
            text: The text to embed.
            kwargs: Additional arguments to pass to the Model.

        Returns
        -------
            The embeddings of the text.
        """
        return run_coroutine_sync(self.aembed(text, **kwargs))
