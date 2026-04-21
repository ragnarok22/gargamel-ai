import time

try:
    import socket as default_socket
except ImportError:
    try:
        import usocket as default_socket
    except ImportError:
        default_socket = None

try:
    import urequests as requests
except ImportError:
    try:
        import requests
    except ImportError:
        requests = None

REFRESH_MS = 10 * 60 * 1000
RETRY_MS = 30 * 1000
WTTR_FORMAT = "%C|%t|%f|%h"
MAX_WEATHER_RESPONSE_BYTES = 4096


def _ticks_diff(now, then):
    if hasattr(time, "ticks_diff"):
        return time.ticks_diff(now, then)
    return now - then


def wttr_url(location=""):
    location = location.strip().replace(" ", "+")
    if location:
        return "http://wttr.in/{}?m&format={}".format(location, WTTR_FORMAT)
    return "http://wttr.in/?m&format={}".format(WTTR_FORMAT)


def _strip_unit(value, unit):
    value = value.strip()
    value = value.replace("\xc2\xb0", "")
    value = value.replace("\xb0", "")
    value = value.replace(unit, "")
    value = value.strip()
    if value.startswith("+"):
        value = value[1:]
    return value


def _parse_current(text):
    if isinstance(text, bytes):
        text = text.decode()

    lines = text.strip().splitlines()
    if not lines:
        raise OSError("empty weather response")

    parts = [part.strip() for part in lines[0].split("|")]
    if len(parts) != 4:
        raise OSError("invalid weather response")

    description, temp_c, feels_c, humidity = parts
    return {
        "description": description,
        "temp_c": _strip_unit(temp_c, "C"),
        "feels_c": _strip_unit(feels_c, "C"),
        "humidity": _strip_unit(humidity, "%"),
    }


def _response_text(response):
    if hasattr(response, "text"):
        return response.text

    if hasattr(response, "content"):
        content = response.content
        if isinstance(content, bytes):
            return content.decode()
        return content

    raise OSError("weather response has no text")


def _fetch_with_requests(location, http, socket_module=default_socket, timeout_s=8):
    response = None
    timeout_was_set = False
    try:
        if timeout_s is not None and hasattr(socket_module, "setdefaulttimeout"):
            socket_module.setdefaulttimeout(timeout_s)
            timeout_was_set = True
        response = http.get(wttr_url(location))
        return _parse_current(_response_text(response))
    finally:
        if response:
            response.close()
        if timeout_was_set:
            socket_module.setdefaulttimeout(None)


def _parse_http_url(url):
    if not url.startswith("http://"):
        raise ValueError("only http:// URLs are supported")

    host_and_path = url[len("http://") :]
    if "/" in host_and_path:
        host, path = host_and_path.split("/", 1)
        return host, "/" + path
    return host_and_path, "/"


def _socket_write(sock, data):
    if hasattr(sock, "write"):
        sock.write(data)
    else:
        sock.sendall(data)


def _socket_read(sock, size):
    if hasattr(sock, "read"):
        return sock.read(size)
    return sock.recv(size)


def _fetch_text_with_socket(url, socket_module=default_socket, timeout_s=8):
    if socket_module is None:
        raise RuntimeError("socket module missing")

    host, path = _parse_http_url(url)
    socket_type = getattr(socket_module, "SOCK_STREAM", 0)
    address = socket_module.getaddrinfo(host, 80, 0, socket_type)[0][-1]
    sock = socket_module.socket()

    try:
        if timeout_s is not None and hasattr(sock, "settimeout"):
            sock.settimeout(timeout_s)

        sock.connect(address)
        request = (
            "GET {} HTTP/1.0\r\n"
            "Host: {}\r\n"
            "User-Agent: gargamel-ai\r\n"
            "Accept: text/plain\r\n"
            "Accept-Encoding: identity\r\n"
            "Connection: close\r\n\r\n"
        ).format(path, host)
        _socket_write(sock, request.encode())

        chunks = []
        total_size = 0
        while True:
            chunk = _socket_read(sock, 512)
            if not chunk:
                break
            if isinstance(chunk, str):
                chunk = chunk.encode()
            total_size += len(chunk)
            if total_size > MAX_WEATHER_RESPONSE_BYTES:
                raise OSError("weather response too large")
            chunks.append(chunk)

        raw_response = b"".join(chunks)
    finally:
        sock.close()

    header_end = raw_response.find(b"\r\n\r\n")
    if header_end == -1:
        raise OSError("invalid weather response")

    headers = raw_response[:header_end]
    body = raw_response[header_end + 4 :]
    status_line = headers.split(b"\r\n", 1)[0]
    if b" 200 " not in status_line:
        raise OSError("weather HTTP error")

    return body.decode()


def fetch_current(
    location="",
    requests_module=None,
    socket_module=default_socket,
    timeout_s=8,
):
    if requests_module is not None:
        return _fetch_with_requests(location, requests_module, socket_module, timeout_s)

    return _parse_current(
        _fetch_text_with_socket(wttr_url(location), socket_module, timeout_s)
    )


class WeatherService:
    def __init__(
        self,
        location="",
        requests_module=None,
        socket_module=default_socket,
        timeout_s=8,
        refresh_ms=REFRESH_MS,
        retry_ms=RETRY_MS,
    ):
        self.location = location
        self.requests = requests_module
        self.socket = socket_module
        self.timeout_s = timeout_s
        self.refresh_ms = refresh_ms
        self.retry_ms = retry_ms
        self.last_attempt = None
        self.data = None
        self.error = None

    def should_refresh(self, now):
        if self.last_attempt is None:
            return True

        delay = self.retry_ms if self.error or self.data is None else self.refresh_ms
        return _ticks_diff(now, self.last_attempt) > delay

    def refresh(self, now):
        self.last_attempt = now
        self.data = fetch_current(
            self.location,
            self.requests,
            socket_module=self.socket,
            timeout_s=self.timeout_s,
        )
        self.error = None
        return self.data

    def set_error(self, error, now):
        self.last_attempt = now
        self.error = error
