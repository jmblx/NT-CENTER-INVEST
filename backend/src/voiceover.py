import fastapi


async def text_to_speech(request: fastapi.Request, text: str):
    sample_rate = 48000
    audio = request.app.state.tts_model.apply_tts(
        text=text,
        speaker='baya',
        sample_rate=sample_rate,
        put_accent=True,
        put_yo=True
    )
    # Преобразование аудио в WAV
    buffer = io.BytesIO()
    sf.write(buffer, audio, sample_rate, format='WAV')
    buffer.seek(0)
    return Response(content=buffer.read(), media_type="audio/wav")