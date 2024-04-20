import os
import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException, UploadFile, File
import librosa
import soundfile as sf
import noisereduce as nr

from constants import AUDIO_DIR
from crud import Db
from reqs.models import Request
from reqs.schemas import RequestAdd

router = APIRouter(prefix="/response")
db = Db()

@router.post("")
async def upload_files(audio: Optional[UploadFile] = None, text: Optional[str] = None):
    # Проверяем, был ли предоставлен файл аудио
    if audio is not None:
        unique_filename = str(uuid.uuid4()) + ".wav"
        file_path = os.path.join(AUDIO_DIR, unique_filename)

        with open(file_path, "wb") as file:
            file.write(await audio.read())

        data, rate = librosa.load(file_path, sr=None)
        reduced_noise = nr.reduce_noise(y=data, sr=rate)

        clean_file_path = os.path.join(AUDIO_DIR, "clean_" + unique_filename)
        sf.write(clean_file_path, reduced_noise, rate)

        data = RequestAdd(file_name=clean_file_path)
        await db.add_one(Request, data)

        asr_model = router.asr_model
        transcription = asr_model.transcribe([clean_file_path])
        print(transcription)

        return {"message": "File uploaded successfully", "filename": unique_filename, "text": transcription}
    elif text is not None:
        return {"message": "Text received successfully", "text": text}
    else:
        raise HTTPException(status_code=400, detail="No audio or text provided")
