# CodeX-Zynga-Hackathon


A proof-of-concept system to verify **age** and **identity** by comparing a **simulated Aadhaar card** image with a **live selfie**, ensuring that both belong to the same person and meet age-based eligibility (e.g., 18+).

---

##  Problem Statement

Develop a mobile or web-based system to:

- Extract **DOB and photo** from a simulated Aadhaar card image (JPEG/PDF).
- Capture a **live selfie** using webcam or phone camera.
- Match the extracted Aadhaar photo with the selfie using face recognition.
- Determine whether the **age is 18+** and whether both photos belong to the **same individual**.

---

##  Solution Overview

Our solution is divided into four major components:

1. **Aadhaar OCR**  
   Extracts **DOB** and **face image** from Aadhaar using **EasyOCR** and **OpenCV**.

2. **Selfie Capture**  
   Captures live image using device webcam via **React** interface.

3. **Face Comparison**  
   Uses **FaceNet** to compare Aadhaar photo and selfie via **facial embeddings**.

4. **Verification Output**  
   Displays:
   - Age verification result (e.g., ✅ Above 18)
   - Face match result (e.g., 88.3% Match)
   - Feedback on lighting, blurriness, or mismatch

---

##  Architecture

```
Frontend (React)  <-->  Backend API (Flask/FastAPI)
                                |
               ------------------------------------
              |                  |                |
        OCR & DOB          Face Matching     Data Security
```

---

## Tools & Technologies Used

| Tool | Purpose |
|------|---------|
| **EasyOCR** | OCR for extracting DOB and text |
| **OpenCV** | Image pre-processing |
| **FaceNet** | Face embedding & comparison |
| **React** | Frontend for file upload & selfie |
| **Flask** | Backend APIs |
| **PIL, NumPy** | Image manipulation |
| **Regex** | DOB & Aadhaar parsing |
| **Google Colab** | Model prototyping and testing |

---

##  How It Works (Pipeline)

### 🧾 Aadhaar OCR
1. Pre-process image (blur, sharpen, rotate)
2. Extract text + bounding boxes using **EasyOCR**
3. Use Regex to extract **DOB** in formats like `DD/MM/YYYY`
4. Extract Aadhaar photo region using **face detection**

###  Selfie Capture
- Live photo taken using webcam.
- Converted to numpy image array for embedding.

### Face Comparison
1. Extract 128D or 512D embeddings using **FaceNet**
2. Compute cosine similarity
3. Threshold-based verification (e.g., > 0.50 match)

### Final Decision
- If DOB age ≥ 18 → ✅  
- If face similarity ≥ threshold → ✅  
- Show combined result and confidence score.

---

##  Sample Output

```
Extracted DOB: 12/03/2005
Age: 19 ✅
Face Match: 87.3% ✅
Final Result: ✅ Verified
```

---

##  Data Security Measures

- No images or PII are stored.
- All processing is in-memory.
- HTTPS (for hosted version).
- Future scope: Encryption of input images.

---

##  Bonus Features (Implemented/In Progress)

- [x] Show confidence level of match (e.g., 88.3%)
- [x] Blur or brightness feedback for selfie
- [ ] Multilingual OCR support (Hindi, Tamil, etc.)
- [ ] Liveness detection (future)
- [ ] Encryption + Secure cloud storage (future)

---

##  Team & Responsibilities

| Member                                                                                   | Role                                                  |
|------------------------------------------------------------------------------------------|-------------------------------------------------------|
| Anishka Singh<br>anishkabt002btdmam22@igdtuw.ac.in<br>https://github.com/Anishka24       | Frontend Developer (React + Webcam + Upload UI)       |
| Azmeen Khatoon<br>azmeen017btaiml22@igdtuw.ac.in<br>https://github.com/Hustler-01        | Backend Dev 1 (OCR & DOB extractor using EasyOCR with PyTorch & OpenCV)   |
| Anchal Malik<br>anchal007btaiml22@igdtuw.ac.in<br>https://github.com/anchal405           | Backend Dev 2 (Face comparison using FaceNet)         |
| Mamta Nishad<br>mamta103btcse22@igdtuw.ac.in<br>https://github.com/Mamtagithubrit        | Multilingual OCR, Blur Feedback, Deployment           |
| Kahkasha Bano<br>kahkasha056bteceai22@igdtuw.ac.in<br>https://github.com/Kahkasha-Bano   | GitHub Repo, README, Video Demo, PPT                  |


---

##  Getting Started

Once all code is merged into the repo:

```bash
# Clone the repo
git clone https://github.com/Hustler-01/CodeX-Zynga-Hackathon.git
cd CodeX-Zynga-Hackathon

# Run backend
cd backend/
pip install -r requirements.txt
python app.py

# Run frontend
cd frontend/
npm install
npm run dev
```

---

##  Sample Data

Use fake Aadhaar images like:

- `samples/fake_aadhar_1.jpg`
- `samples/selfie_kahkasha.jpg`

All assets provided inside `samples/` folder.

---

##  Try it 

(https://hackonzeta.netlify.app/)

---

##  Final Notes

This system is for **educational/demo purposes only**. No real Aadhaar data or government APIs are used.
