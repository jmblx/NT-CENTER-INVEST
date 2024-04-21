import os
import uuid
from typing import Optional
import io

from fastapi import APIRouter, HTTPException, UploadFile, File
import fastapi
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
async def upload_files(request: fastapi.Request, audio: UploadFile = File(...), text: Optional[str] = None):
    if audio is not None:
        unique_filename = str(uuid.uuid4()) + ".wav"
        file_path = os.path.join(AUDIO_DIR, unique_filename)

        with open(file_path, "wb") as file:
            file.write(await audio.read())

        # Загружаем аудио
        data, rate = librosa.load(file_path, sr=None)

        # Увеличиваем громкость
        volume_factor = 2.0  # Увеличение громкости в 2 раза
        data = data * volume_factor

        # Уменьшаем шум
        reduced_noise = nr.reduce_noise(y=data, sr=rate)

        # Сохраняем обработанное аудио
        clean_file_path = os.path.join(AUDIO_DIR, "clean_" + unique_filename)
        sf.write(clean_file_path, reduced_noise, rate)

        asr_model = request.app.state.asr_model
        transcription = asr_model.transcribe([clean_file_path])
        print(transcription)
        data = RequestAdd(audio_path=file_path, text=transcription[0][0])
        await db.add_one(Request, data)

        return {"message": "File uploaded successfully", "filename": unique_filename, "text": transcription[0][0]}
    elif text is not None:
        data = RequestAdd(text=text)
        await db.add_one(Request, data)
        return {"message": "Text received successfully", "text": text}
    else:
        raise HTTPException(status_code=400, detail="No audio or text provided")
# @router.post("")
# async def upload_files(request: fastapi.Request, audio: UploadFile = File(...), text: Optional[str] = None):
#     if audio is not None:
#         unique_filename = str(uuid.uuid4()) + ".wav"
#         file_path = os.path.join(AUDIO_DIR, unique_filename)
#
#         # Read the audio file directly into memory
#         contents = await audio.read()
#
#         # Use librosa to load the file (it now reads from bytes, not from a saved file)
#         data, rate = librosa.load(io.BytesIO(contents), sr=None, mono=True)  # Ensure the audio is mono
#
#         # Save the mono audio
#         clean_file_path = os.path.join(AUDIO_DIR, "clean_" + unique_filename)
#         sf.write(clean_file_path, data, rate)
#
#         asr_model = request.app.state.asr_model
#         transcription = asr_model.transcribe([clean_file_path])
#         print(transcription)
#
#         data = RequestAdd(audio_path=clean_file_path, text=transcription[0][0])
#         await db.add_one(Request, data)
#
#         return {"message": "File uploaded successfully", "filename": unique_filename, "text": transcription[0][0]}
#     elif text is not None:
#         data = RequestAdd(text=text)
#         await db.add_one(Request, data)
#         return {"message": "Text received successfully", "text": text}
#     else:
#         raise HTTPException(status_code=400, detail="No audio or text provided")
