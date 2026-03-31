import re
import json
import time
from typing import Any
import streamlit as st
import google.generativeai as genai


_gemini_model = None


def init_gemini(api_key: str):
    global _gemini_model
    genai.configure(api_key=api_key)
    _gemini_model = genai.GenerativeModel("gemini-2.5-flash")


def get_model():
    return _gemini_model


def _extract_json(text: str) -> Any:
    text = text.strip()
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    try:
        return json.loads(text)
    except Exception:
        pass
    for pat in (r"\{[\s\S]*\}", r"\[[\s\S]*\]"):
        m = re.search(pat, text)
        if m:
            try:
                return json.loads(m.group())
            except Exception:
                pass
    raise ValueError(f"No JSON found:\n{text[:300]}")


def gemini_text(parts, temperature=0.1, json_mode=False):
    model = get_model()
    cfg = {"temperature": temperature, "top_p": 0.95, "max_output_tokens": 4096}
    if json_mode:
        cfg["response_mime_type"] = "application/json"
    for attempt in range(3):
        try:
            return model.generate_content(parts, generation_config=cfg).text
        except Exception as e:
            if "429" in str(e) and attempt < 2:
                wait = 35 * (attempt + 1)
                st.toast(f"Rate limit — retrying in {wait}s", icon="⚠️")
                time.sleep(wait)
            else:
                raise
