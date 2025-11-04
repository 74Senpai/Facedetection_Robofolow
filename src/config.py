import dotenv
import os

dotenv.load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
MODEL_ID = os.getenv("MODEL_ID")
FACE_DETEC_THRESHOLD = os.getenv("FACE_DETEC_THRESHOLD")
FACE_RECO_THRESHOLD = float(os.getenv("FACE_RECO_THRESHOLD", 0.5))
DATABASE_PATH = os.getenv("DATABASE_PATH")