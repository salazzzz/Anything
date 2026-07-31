import http.server, os, socketserver
class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = path.split('?')[0].split('#')[0].lstrip('/')
        for cand in (p, p + '.html', os.path.join(p, 'index.html')):
            full = os.path.join(os.getcwd(), cand)
            if cand and os.path.isfile(full):
                return full
        return super().translate_path(path)
    def log_message(self, *a): pass
socketserver.TCPServer.allow_reuse_address = True
socketserver.TCPServer(("", 8902), H).serve_forever()
