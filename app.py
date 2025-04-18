from flask import Flask, render_template, request, send_file
import qrcode
import io
import base64
from PIL import Image

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_image = None
    if request.method == 'POST':
        text = request.form.get('text')
        size = request.form.get('size', 300, type=int)  # Default to 300px if not provided
        
        if text:
            # Calculate box_size based on desired pixel size (approx. size/25 for reasonable scaling)
            box_size = max(4, size // 25)  # Ensure box_size is at least 4 for clarity
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=box_size,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64 for display
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            qr_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            # Save image for download
            img.save('static/qr_code.png')
            
    return render_template('index.html', qr_image=qr_image)

@app.route('/download')
def download():
    return send_file('static/qr_code.png', as_attachment=True, download_name='qr_code.png')

if __name__ == '__main__':
    app.run(debug=True)