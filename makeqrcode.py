import qrcode
from PIL import Image
from datetime import date


today = date.today()
today = today.strftime("%d/%m/%Y")




input_data = 'https://merenda-gestao.herokuapp.com/avaliacao'

def makeQRCode():
    qr = qrcode.QRCode(
        version = 1,
        box_size = 10,
        border = 5
        )

    qr.add_data(input_data)
    qr.make(fit=True)

    img=qr.make_image(fill='black', back_color='white')
    img.save('app/static/qrcode003.png')
    
makeQRCode()

