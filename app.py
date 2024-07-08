from flask import Flask, request, send_file, render_template, jsonify
import cv2
import numpy as np
import io
from PIL import Image
import logging

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to a real secret key in production

logging.basicConfig(level=logging.DEBUG)

def apply_gaussian_blur(image, ksize):
    logging.debug(f'Applying Gaussian blur with kernel size: {ksize}')
    return cv2.GaussianBlur(image, (ksize, ksize), 0)

def add_noise(image, noise_type='gaussian'):
    logging.debug(f'Adding {noise_type} noise to the image')
    row, col = image.shape
    if noise_type == 'gaussian':
        mean = 0
        var = 0.01
        sigma = var**0.5
        gauss = np.random.normal(mean, sigma, (row, col))
        noisy = image + gauss
        return noisy

def perform_sift(image):
    logging.debug('Performing SIFT')
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(image, None)
    img_with_keypoints = cv2.drawKeypoints(image, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return img_with_keypoints

def edge_detection(image):
    logging.debug('Performing edge detection')
    edges = cv2.Canny(image, 100, 200)
    return edges

def convert_to_grayscale(image):
    logging.debug('Converting to grayscale')
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def apply_threshold(image, threshold_value):
    logging.debug(f'Applying threshold with value: {threshold_value}')
    _, thresh_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    return thresh_image

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    logging.debug('Received request to process image')
    if 'image' not in request.files:
        logging.error('No image provided')
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    operation = request.form.get('operation')
    image = Image.open(io.BytesIO(file.read()))
    image = np.array(image.convert('RGB'))

    logging.debug(f'Operation: {operation}')
    
    if operation == 'gaussian_blur':
        ksize_str = request.form.get('ksize', '5')  # Get ksize as string
        try:
            ksize = int(ksize_str)
        except ValueError:
            ksize = 5  # Default value if conversion fails
        processed_image = apply_gaussian_blur(image, ksize)
    elif operation == 'add_noise':
        processed_image = add_noise(image)
    elif operation == 'sift':
        processed_image = perform_sift(image)
    elif operation == 'edge_detection':
        processed_image = edge_detection(image)
    elif operation == 'convert_to_grayscale':
        processed_image = convert_to_grayscale(image)
    elif operation == 'apply_threshold':
        threshold_value_str = request.form.get('threshold_value', '128')
        try:
            threshold_value = int(threshold_value_str)
        except ValueError:
            threshold_value = 128  # Default value if conversion fails
        processed_image = apply_threshold(image, threshold_value)
    else:
        logging.error('Invalid operation')
        return jsonify({'error': 'Invalid operation'}), 400

    _, img_encoded = cv2.imencode('.png', processed_image)
    logging.debug('Image processing complete, sending response')
    return send_file(io.BytesIO(img_encoded.tobytes()), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
