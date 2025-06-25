import React, { useRef, useState } from "react";
import Webcam from "react-webcam";

const App = () => {
  const webcamRef = useRef(null);
  const canvasRef = useRef(null);
  const [capturedImage, setCapturedImage] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [cameraError, setCameraError] = useState(false);
  const [isBlurry, setIsBlurry] = useState(false);

  const isImageBlurry = (image) => {
    return new Promise((resolve) => {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      const img = new Image();
      img.src = image;
      img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);
        const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        let total = 0;
        for (let i = 0; i < imgData.data.length; i += 4) {
          const gray = 0.299 * imgData.data[i] + 0.587 * imgData.data[i + 1] + 0.114 * imgData.data[i + 2];
          total += gray;
        }
        const mean = total / (imgData.data.length / 4);
        let variance = 0;
        for (let i = 0; i < imgData.data.length; i += 4) {
          const gray = 0.299 * imgData.data[i] + 0.587 * imgData.data[i + 1] + 0.114 * imgData.data[i + 2];
          variance += Math.pow(gray - mean, 2);
        }
        variance = variance / (imgData.data.length / 4);
        resolve(variance < 100);
      };
    });
  };

  const capture = async () => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (!imageSrc) {
      alert("⚠️ Camera capture failed.");
      return;
    }
    const blurry = await isImageBlurry(imageSrc);
    setCapturedImage(imageSrc);
    setIsBlurry(blurry);
    if (blurry) {
      alert("⚠️ Image is blurry. Please retake.");
    } else {
      alert("✅ Clear selfie captured!");
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setUploadedFile(file);
    alert("✅ Aadhaar uploaded!");
  };

  const handleSubmit = async () => {
    if (!uploadedFile || !capturedImage) {
      alert("⚠️ Aadhaar and selfie both required.");
      return;
    }
    if (isBlurry) {
      alert("❌ Blurry selfie. Please recapture.");
      return;
    }

    setLoading(true);
    try {
      const blob = await (await fetch(capturedImage)).blob();
      const formData = new FormData();
      formData.append("aadhar", uploadedFile);
      formData.append("selfie", blob, "selfie.jpg");

      const response = await fetch("http://127.0.0.1:5000/verify", {
  method: "POST",
  body: formData,
});
console.log("Request sent to /verify");

if (!response.ok) {
  const errRes = await response.json();
  throw new Error(errRes.error || "Server error");
}

const data = await response.json();
if (!data.dob || data.age === undefined || data.is18Plus === undefined) {
  throw new Error("Incomplete data from server");
}
setResult(data);


    } catch (err) {
      alert("❌ Verification failed: " + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Age & Face Verification</h1>

      <div>
        <label>Upload Aadhaar (PDF/JPG/PNG): </label>
        <input type="file" accept=".pdf,.jpg,.jpeg,.png" onChange={handleFileChange} />
      </div>

      {uploadedFile && (
        <img
          src={URL.createObjectURL(uploadedFile)}
          alt="Aadhaar Preview"
          style={{ width: "100%", marginTop: "10px", borderRadius: "8px" }}
        />
      )}

      <div style={{ textAlign: "center", marginTop: "20px" }}>
        <Webcam
          audio={false}
          height={240}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          width={240}
          videoConstraints={{ facingMode: "user" }}
          onUserMediaError={() => setCameraError(true)}
          style={{ borderRadius: "50%", border: "3px solid #333" }}
        />
        <button onClick={capture} style={{ marginTop: "10px" }}>Capture Selfie</button>
        {cameraError && <p style={{ color: "red" }}>❌ Camera not available.</p>}
      </div>

      {capturedImage && (
        <img
          src={capturedImage}
          alt="Selfie Preview"
          style={{
            width: "200px",
            height: "200px",
            borderRadius: "50%",
            margin: "10px auto",
            display: "block",
            objectFit: "cover",
            border: "3px solid green"
          }}
        />
      )}

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Verifying..." : "Submit"}
      </button>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h3>Verification Results</h3>
          <p><strong>Age:</strong> {result.age !== undefined ? result.age : "N/A"} years</p>
          <p><strong>18+:</strong> {result.is18Plus !== undefined ? (result.is18Plus ? "✅ Yes" : "❌ No") : "N/A"}</p>
          <p><strong>Face Match:</strong> {result.isMatch !== undefined ? (result.isMatch ? "✅ Match" : "❌ No Match") : "N/A"}</p>
          <p><strong>Match Score:</strong> {result.matchScore !== undefined ? `${result.matchScore.toFixed(2)}%` : "N/A"}</p>
          <p><strong>ID Quality:</strong> {result.quality?.id_quality || "N/A"}</p>
          <p><strong>Selfie Quality:</strong> {result.quality?.selfie_quality || "N/A"}</p>
        </div>
      )}

      <canvas ref={canvasRef} style={{ display: "none" }} />
    </div>
  );
};

export default App;