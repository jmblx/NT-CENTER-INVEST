import os
import uuid
from typing import Optional
import io
import json

import base64
from fastapi import APIRouter, HTTPException, UploadFile, File
import fastapi
import librosa
import soundfile as sf
import noisereduce as nr
import wave
import numpy as np
from starlette.responses import Response, StreamingResponse, JSONResponse

from constants import AUDIO_DIR
from crud import Db
from reqs.models import Request
from reqs.neero import match_question
from reqs.schemas import RequestAdd, SpeechRequest

router = APIRouter(prefix="/response")
db = Db()


@router.post("/recognize_audio")
async def recognize_audio(request: fastapi.Request, audio: UploadFile = File(...), text: Optional[str] = None):
    if audio is not None:
        unique_filename = str(uuid.uuid4()) + ".wav"
        file_path = os.path.join(AUDIO_DIR, unique_filename)

        with open(file_path, "wb") as file:
            file.write(await audio.read())

        # Загрузка и обработка аудио
        data, rate = librosa.load(file_path, sr=None)
        data = data * 2.0  # Увеличение громкости
        reduced_noise = nr.reduce_noise(y=data, sr=rate)

        clean_file_path = os.path.join(AUDIO_DIR, "clean_" + unique_filename)
        sf.write(clean_file_path, reduced_noise, rate)

        # ASR для преобразования аудио в текст
        asr_model = request.app.state.asr_model
        transcription = asr_model.transcribe([clean_file_path])
        if transcription[0][0]:
            text = transcription[0][0]
        elif text is not None:
            pass
        else:
            raise HTTPException(status_code=400, detail="Не удалось распознать аудио")

        # Сохранение результатов в базу данных
        data = RequestAdd(audio_path=file_path, text=text)
        await db.add_one(Request, data)
        answer = match_question(user_query=text)

        return {"message": "File uploaded successfully", "filename": unique_filename, "text": text, "answer": answer}
    elif text is not None:
        data = RequestAdd(text=text)
        await db.add_one(Request, data)
        answer = match_question(text, data)
        return {"message": "File uploaded successfully", "answer": answer}
    else:
        raise HTTPException(status_code=400, detail="No audio provided")


@router.post("/synthesize_speech")
# async def synthesize_speech(request: fastapi.Request, text: str, model_name: str = "kseniya"):
async def synthesize_speech(request: fastapi.Request, data: SpeechRequest):
    data = data.model_dump()
    if data.get("model_name") not in ['aidar', 'baya', 'kseniya', 'xenia', 'eugene', 'random']:
        raise HTTPException(status_code=400, detail="Invalid model name")

    sample_rate = 48000
    audio = request.app.state.tts_model.apply_tts(
        text=data.get("text"),
        speaker=data.get("model_name"),
        sample_rate=sample_rate,
        put_accent=True,
        put_yo=True
    )

    if len(audio) == 0:
        raise HTTPException(status_code=500, detail="Generated audio is empty")
    print(len(audio))

    virtual_file = io.BytesIO()
    with wave.open(virtual_file, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        audio_bytes = np.int16(audio.numpy() * 32767).tobytes()
        f.writeframes(audio_bytes)

    virtual_file.seek(0)
    audio_base64 = base64.b64encode(virtual_file.read()).decode('utf-8')

    return JSONResponse(content={"audio": audio_base64})


# @router.post("")
# async def upload_files(request: fastapi.Request, audio: UploadFile = File(...), text: Optional[str] = None):
#     if audio is not None:
#         unique_filename = str(uuid.uuid4()) + ".wav"
#         file_path = os.path.join(AUDIO_DIR, unique_filename)
#
#         with open(file_path, "wb") as file:
#             file.write(await audio.read())
#
#         # Загружаем аудио
#         data, rate = librosa.load(file_path, sr=None)
#
#         # Увеличиваем громкость
#         volume_factor = 2.0  # Увеличение громкости в 2 раза
#         data = data * volume_factor
#
#         # Уменьшаем шум
#         reduced_noise = nr.reduce_noise(y=data, sr=rate)
#
#         # Сохраняем обработанное аудио
#         clean_file_path = os.path.join(AUDIO_DIR, "clean_" + unique_filename)
#         sf.write(clean_file_path, reduced_noise, rate)
#
#         asr_model = request.app.state.asr_model
#         transcription = asr_model.transcribe([clean_file_path])
#         print(transcription)
#         data = RequestAdd(audio_path=file_path, text=transcription[0][0])
#         await db.add_one(Request, data)
#         sample_rate = 48000
#         audio = request.app.state.tts_model.apply_tts(
#             text=text,
#             speaker='kseniya',
#             sample_rate=sample_rate,
#             put_accent=True,
#             put_yo=True
#         )
#         # Преобразование аудио в WAV
#         audio_buffer = io.BytesIO()
#         sf.write(audio_buffer, audio, sample_rate, format='WAV')
#         audio_buffer.seek(0)
#
#         # Создание многочастного ответа
#         boundaries = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
#         response = Response(
#             content=(
#                 f"--{boundaries}\r\nContent-Disposition: form-data; name=\"data\"\r\n\r\n"
#                 f"{json.dumps({'message': 'File created successfully', 'filename': 'filename.wav', 'text': text})}\r\n"
#                 f"--{boundaries}\r\nContent-Disposition: form-data; name=\"audio\"; filename=\"audio.wav\"\r\nContent-Type: audio/wav\r\n\r\n"
#                 f"{audio_buffer.read()}\r\n--{boundaries}--"
#             ),
#             media_type=f"multipart/form-data; boundary={boundaries}"
#         )
#         return response
#
#         # return {"message": "File uploaded successfully", "filename": unique_filename, "text": transcription[0][0]}
#     elif text is not None:
#         data = RequestAdd(text=text)
#         await db.add_one(Request, data)
#         return {"message": "Text received successfully", "text": text}
#     else:
#         raise HTTPException(status_code=400, detail="No audio or text provided")
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
