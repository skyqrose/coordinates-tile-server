from http.server import HTTPServer, BaseHTTPRequestHandler
from PIL import Image, ImageDraw
import io

COLOR = (214, 65, 216, 255)

class request_handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            try:
                file = open("index.html").read()
                self._write_data(200, file)
            except:
                self._write_data(500, "500")
        elif self.path.startswith("/tiles/") and self.path.endswith(".png"):
            path_segments = self.path.split("/")
            if len(path_segments) == 5:
                z = path_segments[2]
                x = path_segments[3]
                y = path_segments[4][:-4]
                self._write_data(200, tile(z, x, y))
            else:
                self._write_data(404, "404")
        else:
            self._write_data(404, "404")

    def _write_data(self, status, data):
        if type(data) == str:
            data = bytes(data, "utf-8")
        self.send_response(status)
        self.end_headers()
        self.wfile.write(data)

def tile(z, x, y):
    img = Image.new("RGBA", (256, 256), color = (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # borders
    draw.line([(0, 0), (0, 255)], fill = COLOR, width = 1)
    draw.line([(0, 255), (255, 255)], fill = COLOR, width = 1)
    draw.line([(255, 255), (255, 0)], fill = COLOR, width = 1)
    draw.line([(255, 0), (0, 0)], fill = COLOR, width = 1)

    # text
    text = f"z: {z}\nx: {x}\ny: {y}"
    draw.multiline_text((12, 8), text, fill=COLOR, align="left")

    # convert to bytes
    imgBytes = io.BytesIO()
    img.save(imgBytes, format="PNG")
    return imgBytes.getvalue()

if __name__ == "__main__":
    httpd = HTTPServer(('localhost', 6371), request_handler)
    httpd.serve_forever()
