package com.example.mobile_app

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.speech.RecognizerIntent
import androidx.activity.result.contract.ActivityResultContract
import java.util.Locale

class SpeechRecognizerContract:ActivityResultContract<Unit,ArrayList<String>?>() {
    override fun createIntent(context: Context, input: Unit): Intent {
        // Запуск записи голоса
        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        intent.putExtra(
            RecognizerIntent.EXTRA_LANGUAGE_MODEL, // Модель языка
            RecognizerIntent.LANGUAGE_MODEL_WEB_SEARCH // Оптимизирует распознавание для коротких фраз, как при веб-поиске
        )
        // Устанавливается язык, который установлен на устройстве по умолчанию
        intent.putExtra(
            RecognizerIntent.EXTRA_LANGUAGE,
            Locale.getDefault()
        )
        // Подсказка
        intent.putExtra(
            RecognizerIntent.EXTRA_PROMPT,
            "Скажите что-нибудь"
        )
        return intent
    }
    override fun parseResult(resultCode: Int, intent: Intent?): ArrayList<String>? {
        // Если все ОК, то извлекает результаты распознавания речи
        if (resultCode != Activity.RESULT_OK){
            return null
        }
        return intent?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
    }
}