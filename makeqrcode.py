import qrcode
from PIL import Image



input_data = 'http://127.0.0.1:5000/'

def makeQRCode():
    qr = qrcode.QRCode(
        version = 1,
        box_size = 10,
        border = 5
        )

    qr.add_data(input_data)
    qr.make(fit=True)

    img=qr.make_image(fill='black', back_color='white')
    img.save('app/static/qrcode001.png')
    


