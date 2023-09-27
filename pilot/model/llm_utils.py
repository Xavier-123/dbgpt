#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import traceback
from pathlib import Path
from queue import Queue
from threading import Thread
import transformers

from typing import List, Optional, Dict
import cachetools

from pilot.configs.config import Config
from pilot.configs.model_config import LLM_MODEL_CONFIG, EMBEDDING_MODEL_CONFIG
from pilot.model.base import Message, SupportedModel
from pilot.utils.parameter_utils import _get_parameter_descriptions


def create_chat_completion(
    messages: List[Message],  # type: ignore
    model: Optional[str] = None,
    temperature: float = None,
    max_tokens: Optional[int] = None,
) -> str:
    """Create a chat completion using the vicuna local model

    Args:
       messages(List[Message]): The messages to send to the chat completion
       model (str, optional): The model to use. Defaults to None.
       temperature (float, optional): The temperature to use. Defaults to 0.7.
       max_tokens (int, optional): The max tokens to use. Defaults to None

     Returns:
        str: The response from chat completion
    """
    cfg = Config()
    if temperature is None:
        temperature = cfg.temperature

    for plugin in cfg.plugins:
        if plugin.can_handle_chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        ):
            message = plugin.handle_chat_completion(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            if message is not None:
                return message

        response = None
        # TODO impl this use vicuna server api_v1


class Stream(transformers.StoppingCriteria):
    def __init__(self, callback_func=None):
        self.callback_func = callback_func

    def __call__(self, input_ids, scores) -> bool:
        if self.callback_func is not None:
            self.callback_func(input_ids[0])
        return False


class Iteratorize:

    """
    Transforms a function that takes a callback
    into a lazy iterator (generator).
    """

    def __init__(self, func, kwargs={}, callback=None):
        self.mfunc = func
        self.c_callback = callback
        self.q = Queue()
        self.sentinel = object()
        self.kwargs = kwargs
        self.stop_now = False

        def _callback(val):
            if self.stop_now:
                raise ValueError
            self.q.put(val)

        def gentask():
            try:
                ret = self.mfunc(callback=_callback, **self.kwargs)
            except ValueError:
                pass
            except:
                traceback.print_exc()
                pass

            self.q.put(self.sentinel)
            if self.c_callback:
                self.c_callback(ret)

        self.thread = Thread(target=gentask)
        self.thread.start()

    def __iter__(self):
        return self

    def __next__(self):
        obj = self.q.get(True, None)
        if obj is self.sentinel:
            raise StopIteration
        else:
            return obj

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_now = True


def is_sentence_complete(output: str):
    """Check whether the output is a complete sentence."""
    end_symbols = (".", "?", "!", "...", "。", "？", "！", "…", '"', "'", "”")
    return output.endswith(end_symbols)


def is_partial_stop(output: str, stop_str: str):
    """Check whether the output contains a partial stop str."""
    for i in range(0, min(len(output), len(stop_str))):
        if stop_str.startswith(output[-i:]):
            return True
    return False


@cachetools.cached(cachetools.TTLCache(maxsize=100, ttl=60 * 5))
def list_supported_models():
    from pilot.model.parameter import WorkerType

    models = _list_supported_models(WorkerType.LLM.value, LLM_MODEL_CONFIG)
    models += _list_supported_models(WorkerType.TEXT2VEC.value, EMBEDDING_MODEL_CONFIG)
    return models


def _list_supported_models(
    worker_type: str, model_config: Dict[str, str]
) -> List[SupportedModel]:
    from pilot.model.adapter import get_llm_model_adapter
    from pilot.model.parameter import ModelParameters
    from pilot.model.loader import _get_model_real_path

    ret = []
    for model_name, model_path in model_config.items():
        model_path = _get_model_real_path(model_name, model_path)
        model = SupportedModel(
            model=model_name,
            path=model_path,
            worker_type=worker_type,
            path_exist=False,
            proxy=False,
            enabled=False,
            params=None,
        )
        if "proxyllm" in model_name:
            model.proxy = True
        else:
            path = Path(model_path)
            model.path_exist = path.exists()
        param_cls = None
        try:
            llm_adapter = get_llm_model_adapter(model_name, model_path)
            param_cls = llm_adapter.model_param_class()
            model.enabled = True
            params = _get_parameter_descriptions(
                param_cls, model_name=model_name, model_path=model_path
            )
            model.params = params
        except Exception:
            pass
        ret.append(model)
    return ret
