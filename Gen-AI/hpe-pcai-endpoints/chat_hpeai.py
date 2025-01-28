import requests
from requests.adapters import HTTPAdapter, Retry
from typing import List, Dict, Generator, Optional


class ChatHPEAI:
    """
    ChatHPEAI is a utility for interacting with AI model APIs.
    It handles retry logic, supports streaming, and offers methods
    for structured and history-aware interactions.
    """
    def __init__(
        self,
        endpoint_url: str,
        headers: Optional[Dict[str, str]] = None,
        verify_ssl: bool = False,
        retries: int = 3,
        backoff_factor: float = 0.3,
    ):
        self.endpoint_url = endpoint_url  # Placeholder for the endpoint
        self.headers = headers or {"Content-Type": "application/json"}
        self.verify_ssl = verify_ssl
        self.session = self._configure_session(retries, backoff_factor)

    def _configure_session(self, retries: int, backoff_factor: float) -> requests.Session:
        """Configure HTTP session with retry logic."""
        session = requests.Session()
        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _send_request(self, payload: Dict, stream: bool = False) -> requests.Response:
        """Send HTTP POST requests with retries."""
        try:
            response = self.session.post(
                self.endpoint_url,
                json=payload,
                headers=self.headers,
                stream=stream,
                verify=self.verify_ssl
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request failed: {str(e)}")

    def chat(self, model: str, prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> str:
        """Basic chat interaction."""
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        response = self._send_request(payload=payload)
        return response.json()["choices"][0]["message"]["content"]

    def stream(self, model: str, prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> Generator[str, None, None]:
        """Stream responses chunk-by-chunk."""
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True,
        }
        response = self._send_request(payload=payload, stream=True)
        for chunk in response.iter_lines(decode_unicode=True):
            if chunk:
                yield chunk

    def chat_with_history(self, model: str, history: List[Dict[str, str]], new_prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> str:
        """Chat interaction with conversation history."""
        payload = {
            "model": model,
            "messages": history + [{"role": "user", "content": new_prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        response = self._send_request(payload=payload)
        return response.json()["choices"][0]["message"]["content"]

    def structured_response(self, model: str, prompt: str) -> Dict:
        """Structured response based on custom schemas."""
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100,
            "temperature": 0.7,
        }
        response = self._send_request(payload=payload)
        return response.json()
