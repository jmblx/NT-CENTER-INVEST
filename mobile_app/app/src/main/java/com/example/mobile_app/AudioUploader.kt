package com.example.mobile_app

import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.File
import java.io.IOException

object AudioUploader {
    fun sendAudioToChat(file: File) {
        // Corrected usage of MediaType with toMediaType() extension
        val mediaType = "audio/wav".toMediaType()

        val requestBody = MultipartBody.Builder()
            .setType(MultipartBody.FORM)
            .addFormDataPart("audio", file.name, file.asRequestBody(mediaType))
            .build()

        val request = Request.Builder()
            .url("https://yourapi.com/upload")
            .post(requestBody)
            .build()

        OkHttpClient().newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                e.printStackTrace()  // Handle the error
            }

            override fun onResponse(call: Call, response: Response) {
                if (response.isSuccessful) {
                    // Handle the successful response
                }
                response.close()  // Ensure the response is closed
            }
        })
    }
}
