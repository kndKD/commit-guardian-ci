"""Optional LLM layer for the Commit Guardian. Disabled by default.

Providers, in order of preference when configured:
1. Ollama (local, free) — set GUARDIAN_LLM=ollama, optional OLLAMA_HOST.
2. OpenAI — set GUARDIAN_LLM=openai and OPENAI_API_KEY (GitHub Secret in CI).
3. Gemini — set GUARDIAN_LLM=gemini and GEMINI_API_KEY.

Never hard-code a key. If no provider is configured, or the call fails,
return None and the caller falls back to the rule-based suggestion.
Uses only the Python standard library so no extra dependency is needed.
"""
import json
import os
import urllib.request

PROMPT = (
    "You are a commit-message reviewer. Analyse this commit message "
    "against the Conventional Commits spec and return JSON only: "
    '{"suggestion": "<type>: <subject>", "reason": "<one sentence>"}. '
    "Message: {message}"
)


def _post(url: str, payload: dict, headers: dict | None = None,
          timeout: int = 20) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def suggest_via_llm(message: str) -> str | None:
    provider = os.environ.get("GUARDIAN_LLM", "").lower()
    if not provider:
        return None
    try:
        if provider == "ollama":
            host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
            data = _post(f"{host}/api/generate", {
                "model": os.environ.get("OLLAMA_MODEL", "llama3.2"),
                "prompt": PROMPT.format(message=message), "stream": False})
            text = data.get("response", "")
        elif provider == "openai":
            key = os.environ.get("OPENAI_API_KEY")
            if not key:
                return None
            data = _post("https://api.openai.com/v1/chat/completions", {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user",
                              "content": PROMPT.format(message=message)}]},
                {"Authorization": f"Bearer {key}"})
            text = data["choices"][0]["message"]["content"]
        elif provider == "gemini":
            key = os.environ.get("GEMINI_API_KEY")
            if not key:
                return None
            data = _post(
                "https://generativelanguage.googleapis.com/v1beta/models/"
                f"gemini-2.0-flash:generateContent?key={key}",
                {"contents": [{"parts": [{"text": PROMPT.format(message=message)}]}]})
            text = data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return None
        parsed = json.loads(text[text.find("{"):text.rfind("}") + 1])
        suggestion = parsed.get("suggestion", "")
        return suggestion.strip() or None
    except Exception:
        return None
