package com.example.myapplication

import retrofit2.Call
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.POST

// Data classes corresponding directly to Flask payload formats
data class AskRequest(
    val question: String,
    val phone: String
)

data class AskResponse(
    val success: Boolean,
    val model: String,
    val answer: String
)

data class FeedbackRequest(
    val question: String,
    val answer: String,
    val rating: String,
    val comments: String = ""
)

data class FeedbackResponse(
    val success: Boolean,
    val message: String
)

interface ApiService {
    @POST("ask")
    fun askGemini(@Body request: AskRequest): Call<AskResponse>

    @POST("feedback")
    fun sendFeedback(@Body request: FeedbackRequest): Call<FeedbackResponse>
}

object RetrofitClient {
    // IMPORTANT: Change "192.168.1.50" to your laptop's actual IPv4 Wi-Fi address!
    private const val BASE_URL = "http://192.168.1.50:5000/" 

    val instance: ApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
}