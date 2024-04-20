import noisereduce as nr
import librosa
import soundfile as sf

# Загрузка аудиофайла
data, rate = librosa.load('poexali.wav', sr=None)

# Применение функции уменьшения шума
# noisereduce автоматически определяет участки шума как участки тишины
reduced_noise = nr.reduce_noise(y=data, sr=rate)

# Сохранение очищенного аудиофайла
sf.write('clean_audio_file.wav', reduced_noise, rate)
