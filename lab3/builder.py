import json
from typing import Any, Optional


# Сложный продукт
class HttpRequest:
    def __init__(self) -> None:
        self.method: str = "GET"
        self.url: str = ""
        self.headers: dict[str, str] = {}
        self.params: dict[str, str] = {}
        self.body: Optional[str] = None
        self.timeout: int = 30

    def __repr__(self) -> str:
        return (
            f"HTTP Запрос:\n"
            f"  {self.method} {self.url}\n"
            f"  Params: {self.params}\n"
            f"  Headers: {self.headers}\n"
            f"  Body: {self.body}\n"
            f"  Timeout: {self.timeout}s"
        )


class HttpRequestBuilder:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> 'HttpRequestBuilder':
        self._request = HttpRequest()
        return self

    def set_method(self, method: str) -> 'HttpRequestBuilder':
        self._request.method = method.upper()
        return self

    def set_url(self, url: str) -> 'HttpRequestBuilder':
        self._request.url = url
        return self

    def add_header(self, key: str, value: str) -> 'HttpRequestBuilder':
        self._request.headers[key] = value
        return self

    def add_bearer_auth(self, token: str) -> 'HttpRequestBuilder':
        return self.add_header("Authorization", f"Bearer {token}")

    def add_param(self, key: str, value: str) -> 'HttpRequestBuilder':
        self._request.params[key] = value
        return self

    def set_json_body(self, payload: dict[str, Any]) -> 'HttpRequestBuilder':
        self._request.body = json.dumps(payload)
        self.add_header("Content-Type", "application/json")
        return self

    def set_timeout(self, seconds: int) -> 'HttpRequestBuilder':
        self._request.timeout = seconds
        return self

    def build(self) -> HttpRequest:
        if not self._request.url:
            raise ValueError("URL запроса обязателен для заполнения")
        result = self._request
        self.reset()
        return result


def main() -> None:
    builder = HttpRequestBuilder()

    get_request = (
        builder.reset()
        .set_url("https://api.github.com/users")
        .add_param("page", "1")
        .add_param("per_page", "10")
        .set_timeout(5)
        .build()
    )
    print(get_request)
    print()

    post_request = (
        builder.reset()
        .set_method("POST")
        .set_url("https://api.payments.com/v1/charge")
        .add_bearer_auth("sk_test_9491048123910")
        .set_json_body({"amount": 4990, "currency": "RUB", "order_id": 42})
        .build()
    )
    print(post_request)


if __name__ == "__main__":
    main()