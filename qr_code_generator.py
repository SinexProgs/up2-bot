from io import BytesIO
import qrcode


def generate_qr_code(text):
    img = qrcode.make(text)

    bytes_io = BytesIO()
    bytes_io.name = "qr_code.jpeg"

    img.save(bytes_io, 'JPEG')

    bytes_io.seek(0)
    return bytes_io