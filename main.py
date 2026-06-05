from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import numpy as np
import joblib
import os

app = FastAPI(title="Sonelgaz DGA Diagnostic System")
templates = Jinja2Templates(directory="templates")

# Load AI Engine
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'models_saved', 'sonelgaz_dga_model.pkl')
scaler_path = os.path.join(base_dir, 'models_saved', 'sonelgaz_scaler.pkl')

try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
except Exception as e:
    model = None
    scaler = None
    print(f"Error loading models: {e}")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main diagnostic form."""
    # التعديل هنا: استخدام request=request و name=... لتفادي الخطأ
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "result": None}
    )


@app.post("/", response_class=HTMLResponse)
async def predict(
        request: Request,
        h2: float = Form(...),
        ch4: float = Form(...),
        c2h6: float = Form(...),
        c2h4: float = Form(...),
        c2h2: float = Form(...),
):
    """Handle form submission and return AI diagnosis."""
    if model is None or scaler is None:
        # التعديل هنا أيضاً
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "error": "System Error: ML Models are not loaded. Contact Administrator."
            }
        )

    try:
        # Prepare data
        input_data = np.array([[h2, ch4, c2h6, c2h4, c2h2]])
        input_scaled = scaler.transform(input_data)

        # Predict
        prediction = model.predict(input_scaled)[0]

        # Determine Severity Level for the UI
        severity = "info"
        if "Arc" in prediction or "High" in prediction:
            severity = "danger"
        elif "Spark" in prediction or "Middle" in prediction:
            severity = "warning"

        result_data = {
            "diagnosis": prediction,
            "severity": severity,
            "inputs": {"H2": h2, "CH4": ch4, "C2H6": c2h6, "C2H4": c2h4, "C2H2": c2h2}
        }

        # التعديل هنا أيضاً
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"request": request, "result": result_data}
        )

    except Exception as e:
        # التعديل هنا أيضاً
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"request": request, "error": str(e)}
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)