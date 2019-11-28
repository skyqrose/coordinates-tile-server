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
        if self.path == "/tile":
            self._write_data(200, tile())
        else:
            self._write_data(404, "404")

    def _write_data(self, status, data):
        if type(data) == str:
            data = bytes(data, "utf-8")
        self.send_response(status)
        self.end_headers()
        self.wfile.write(data)

def tile():
    img = Image.new("RGBA", (256, 256), color = (0, 0, 0, 0))
    drawBorders(img)
    imgBytes = io.BytesIO()
    img.save(imgBytes, format="PNG")
    return imgBytes.getvalue()

def drawBorders(img):
    draw = ImageDraw.Draw(img)
    draw.line([(0, 0), (0, 255)], fill = COLOR, width = 1)
    draw.line([(0, 255), (255, 255)], fill = COLOR, width = 1)
    draw.line([(255, 255), (255, 0)], fill = COLOR, width = 1)
    draw.line([(255, 0), (0, 0)], fill = COLOR, width = 1)

if __name__ == "__main__":
    httpd = HTTPServer(('localhost', 6371), request_handler)
    httpd.serve_forever()
