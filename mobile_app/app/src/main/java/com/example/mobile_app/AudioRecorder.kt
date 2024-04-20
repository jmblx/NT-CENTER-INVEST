package com.example.mobile_app

import android.content.Context
import android.media.MediaRecorder
import java.io.File

class AudioRecorder(private val context: Context) {
    private var mediaRecorder: MediaRecorder? = null
    private var audioFile: File? = null

    fun startRecording() {
        audioFile = File.createTempFile("record_", ".3gp", context.cacheDir)
        mediaRecorder = MediaRecorder().apply {
            setAudioSource(MediaRecorder.AudioSource.MIC)
            setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP)
            setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB)
            setOutputFile(audioFile?.absolutePath)
            prepare()
            start()
        }
    }

    fun stopRecording() {
        mediaRecorder?.apply {
            stop()
            release()
        }
        mediaRecorder = null

        // Ensure audioFile is not null before passing it to sendAudioToChat
        audioFile?.let {
            AudioUploader.sendAudioToChat(it) // Only call if audioFile is not null
        }
    }
}
