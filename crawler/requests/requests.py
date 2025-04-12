import http.client
import ssl
import threading
from urllib.parse import urlparse
from collections import defaultdict

class HTTPClient:
    def __init__(self, max_connections=10):
        self.max_connections = max_connections
        self.lock = threading.Lock()
        self.headers = {}
        self.cookies = defaultdict(dict)
        self.connection_pool = defaultdict(list)

    def set_headers(self, headers):
        with self.lock:
            self.headers.update(headers)

    def set_cookies(self, domain, cookies):
        with self.lock:
            self.cookies[domain].update(cookies)

    def _get_connection(self, host, is_https):
        with self.lock:
            pool = self.connection_pool[host]
            if pool:
                return pool.pop()
            if is_https:
                context = ssl.create_default_context()
                # 自定义 TLS 指纹（示例）
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                return http.client.HTTPSConnection(host, context=context)
            else:
                return http.client.HTTPConnection(host)

    def _release_connection(self, host, conn):
        with self.lock:
            pool = self.connection_pool[host]
            if len(pool) < self.max_connections:
                pool.append(conn)
            else:
                conn.close()

    def request(self, method, url, headers=None, body=None):
        parsed_url = urlparse(url)
        host = parsed_url.netloc
        is_https = parsed_url.scheme == 'https'
        path = parsed_url.path
        if parsed_url.query:
            path += '?' + parsed_url.query

        conn = self._get_connection(host, is_https)
        try:
            with self.lock:
                request_headers = self.headers.copy()
                if headers:
                    request_headers.update(headers)
                if host in self.cookies:
                    cookie_str = '; '.join([f'{k}={v}' for k, v in self.cookies[host].items()])
                    request_headers['Cookie'] = cookie_str

            conn.request(method, path, body=body, headers=request_headers)
            response = conn.getresponse()
            response_headers = response.getheaders()

            with self.lock:
                # 解析响应中的 Cookie
                if 'Set-Cookie' in response_headers:
                    cookie_list = response_headers['Set-Cookie'].split(', ')
                    for cookie in cookie_list:
                        key, value = cookie.split('=', 1)
                        self.cookies[host][key] = value

            return response
        finally:
            self._release_connection(host, conn)

    def close(self):
        with self.lock:
            for host, pool in self.connection_pool.items():
                for conn in pool:
                    conn.close()
                self.connection_pool[host].clear()

# 示例使用
if __name__ == "__main__":
    client = HTTPClient(max_connections=5)
    client.set_headers({'User-Agent': 'MyClient/1.0'})
    client.set_cookies('example.com', {'session_id': '12345'})

    response = client.request('GET', 'https://example.com')
    print(response.status, response.read().decode())

    client.close()