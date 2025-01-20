import qrcode
import qrcode.image.svg
from qrcode.image.pure import PyPNGImage

img = qrcode.make('https://conferenceyoungbotanists.com/abstracts/mattia.pallanza02', image_factory=qrcode.image.svg.SvgImage)

with open('qr.svg', 'wb') as qr:
    img.save(qr)

img = qrcode.make('https://conferenceyoungbotanists.com/abstracts/mattia.pallanza02', image_factory=PyPNGImage)

with open('qr.png', 'wb') as qr:
    img.save(qr)