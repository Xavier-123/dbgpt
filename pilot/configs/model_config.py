#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os

# import nltk

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(ROOT_PATH, "models")
PILOT_PATH = os.path.join(ROOT_PATH, "pilot")
VECTORE_PATH = os.path.join(PILOT_PATH, "vector_store")
LOGDIR = os.path.join(ROOT_PATH, "logs")
DATASETS_DIR = os.path.join(PILOT_PATH, "datasets")
DATA_DIR = os.path.join(PILOT_PATH, "data")
# nltk.data.path = [os.path.join(PILOT_PATH, "nltk_data")] + nltk.data.path
PLUGINS_DIR = os.path.join(ROOT_PATH, "plugins")
FONT_DIR = os.path.join(PILOT_PATH, "fonts")

current_directory = os.getcwd()

new_directory = PILOT_PATH
os.chdir(new_directory)


def get_device() -> str:
    try:
        import torch

        return (
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )
    except ModuleNotFoundError:
        return "cpu"


LLM_MODEL_CONFIG = {
    "flan-t5-base": os.path.join(MODEL_PATH, "flan-t5-base"),
    "vicuna-13b": os.path.join(MODEL_PATH, "vicuna-13b"),
    "vicuna-7b": os.path.join(MODEL_PATH, "vicuna-7b"),
    # (Llama2 based) see https://huggingface.co/lmsys/vicuna-13b-v1.5
    "vicuna-13b-v1.5": os.path.join(MODEL_PATH, "vicuna-13b-v1.5"),
    "vicuna-7b-v1.5": os.path.join(MODEL_PATH, "vicuna-7b-v1.5"),
    "codegen2-1b": os.path.join(MODEL_PATH, "codegen2-1B"),
    "codet5p-2b": os.path.join(MODEL_PATH, "codet5p-2b"),
    "chatglm-6b-int4": os.path.join(MODEL_PATH, "chatglm-6b-int4"),
    "chatglm-6b": os.path.join(MODEL_PATH, "chatglm-6b"),
    # "chatglm2-6b": os.path.join(MODEL_PATH, "chatglm2-6b"),
    "chatglm2-6b": os.path.join("/project/LLM_MODEL/", "chatglm2-6b"),
    "chatglm2-6b-int4": os.path.join(MODEL_PATH, "chatglm2-6b-int4"),
    "guanaco-33b-merged": os.path.join(MODEL_PATH, "guanaco-33b-merged"),
    "falcon-40b": os.path.join(MODEL_PATH, "falcon-40b"),
    "gorilla-7b": os.path.join(MODEL_PATH, "gorilla-7b"),
    "gptj-6b": os.path.join(MODEL_PATH, "ggml-gpt4all-j-v1.3-groovy.bin"),
    "proxyllm": "chatgpt_proxyllm",
    "chatgpt_proxyllm": "chatgpt_proxyllm",
    "bard_proxyllm": "bard_proxyllm",
    "claude_proxyllm": "claude_proxyllm",
    "wenxin_proxyllm": "wenxin_proxyllm",
    "tongyi_proxyllm": "tongyi_proxyllm",
    "zhipu_proxyllm": "zhipu_proxyllm",
    "llama-2-7b": os.path.join(MODEL_PATH, "Llama-2-7b-chat-hf"),
    "llama-2-13b": os.path.join(MODEL_PATH, "Llama-2-13b-chat-hf"),
    "llama-2-70b": os.path.join(MODEL_PATH, "Llama-2-70b-chat-hf"),
    "baichuan-13b": os.path.join(MODEL_PATH, "Baichuan-13B-Chat"),
    # please rename "fireballoon/baichuan-vicuna-chinese-7b" to "baichuan-7b"
    "baichuan-7b": os.path.join(MODEL_PATH, "baichuan-7b"),
    "baichuan2-7b": os.path.join(MODEL_PATH, "Baichuan2-7B-Chat"),
    "baichuan2-13b": os.path.join(MODEL_PATH, "Baichuan2-13B-Chat"),
    # (Llama2 based) We only support WizardLM-13B-V1.2 for now, which is trained from Llama-2 13b, see https://huggingface.co/WizardLM/WizardLM-13B-V1.2
    "wizardlm-13b": os.path.join(MODEL_PATH, "WizardLM-13B-V1.2"),
    "llama-cpp": os.path.join(MODEL_PATH, "ggml-model-q4_0.bin"),
    # https://huggingface.co/internlm/internlm-chat-7b-v1_1, 7b vs 7b-v1.1: https://github.com/InternLM/InternLM/issues/288
    "internlm-7b": os.path.join(MODEL_PATH, "internlm-chat-7b"),
    "internlm-7b-8k": os.path.join(MODEL_PATH, "internlm-chat-7b-8k"),
    "internlm-20b": os.path.join(MODEL_PATH, "internlm-20b-chat"),
}

EMBEDDING_MODEL_CONFIG = {
    # "text2vec": os.path.join(MODEL_PATH, "text2vec-large-chinese"),
    "text2vec": os.path.join("/project/EMBEDDING_MODEL", "text2vec-large-chinese"),   # xaw
    "text2vec-base": os.path.join(MODEL_PATH, "text2vec-base-chinese"),
    # https://huggingface.co/moka-ai/m3e-large
    "m3e-base": os.path.join(MODEL_PATH, "m3e-base"),
    # https://huggingface.co/moka-ai/m3e-base
    "m3e-large": os.path.join(MODEL_PATH, "m3e-large"),
    # https://huggingface.co/BAAI/bge-large-en
    "bge-large-en": os.path.join(MODEL_PATH, "bge-large-en"),
    "bge-base-en": os.path.join(MODEL_PATH, "bge-base-en"),
    # https://huggingface.co/BAAI/bge-large-zh
    "bge-large-zh": os.path.join(MODEL_PATH, "bge-large-zh"),
    "bge-base-zh": os.path.join(MODEL_PATH, "bge-base-zh"),
    "sentence-transforms": os.path.join(MODEL_PATH, "all-MiniLM-L6-v2"),
    "proxy_openai": "proxy_openai",
    "proxy_azure": "proxy_azure",
}

# Load model config
ISDEBUG = False

VECTOR_SEARCH_TOP_K = 10
VS_ROOT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vs_store")
KNOWLEDGE_UPLOAD_ROOT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data"
)
KNOWLEDGE_CHUNK_SPLIT_SIZE = 100
