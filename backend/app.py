from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import cv2
from utils.ocr_utils import ocr_extract_info, convert_pdf_to_image
from face_detector import FaceDetector
from face_embedder import FaceEmbedder
from face_comparator import FaceComparator
from face_verification import FaceVerificationSystem
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize face verification
face_detector = FaceDetector(
    prototxt_path="models/deploy.prototxt.txt",
    model_path="models/res10_300x300_ssd_iter_140000.caffemodel"
)
face_embedder = FaceEmbedder()
face_comparator = FaceComparator(threshold=0.65)
face_verifier = FaceVerificationSystem(face_detector, face_embedder, face_comparator)

@app.route('/verify', methods=['POST'])
def verify_faces():
    try:
        if 'aadhar' not in request.files or 'selfie' not in request.files:
            return jsonify({"error": "Both Aadhaar and Selfie images are required"}), 400

        aadhar = request.files['aadhar']
        selfie = request.files['selfie']

        if not allowed_file(aadhar.filename) or not allowed_file(selfie.filename):
            return jsonify({"error": "Invalid file format"}), 400

        aadhaar_path = os.path.join(UPLOAD_FOLDER, secure_filename(aadhar.filename))
        selfie_path = os.path.join(UPLOAD_FOLDER, secure_filename(selfie.filename))

        aadhar.save(aadhaar_path)
        selfie.save(selfie_path)

        # Convert PDF if Aadhaar is a PDF
        if aadhaar_path.lower().endswith(".pdf"):
            aadhaar_path = convert_pdf_to_image(aadhaar_path)

        # OCR extraction
        ocr_result = ocr_extract_info(aadhaar_path)

        # Load images
        id_image = cv2.imread(aadhaar_path)
        selfie_image = cv2.imread(selfie_path)

        # Face verification
        verification = face_verifier.verify_faces(id_image, selfie_image)

        if verification['status'] != 'success':
            return jsonify({"error": verification.get('error', 'Verification failed')}), 500

        return jsonify({
            "dob": ocr_result.get('dob', 'N/A'),
            "age": ocr_result.get('age', 'N/A'),
            "is18Plus": ocr_result.get('is_18_or_more', 'N/A'),
            "isMatch": verification['verification'].get('match', False),
            "matchScore": verification['verification'].get('confidence', 0),
            "quality": verification['verification'].get('quality', {})
        })

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Server processing error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
