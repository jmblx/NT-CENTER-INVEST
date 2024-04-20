package com.example.myapplication

import androidx.compose.runtime.Composable
import android.os.Bundle
import androidx.compose.foundation.text.KeyboardOptions
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Send
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import java.time.LocalDate
import java.time.LocalTime
import java.time.format.DateTimeFormatter

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            ChatUI()
        }
    }
}

@Composable
fun CurrentDate() {
    val currentDate = LocalDate.now()
    val formatter = DateTimeFormatter.ofPattern("EEEE, d MMMM")
    var formattedDate = currentDate.format(formatter)
    formattedDate = formattedDate.replaceFirstChar { it.uppercase() }

    Box(
        modifier = Modifier.fillMaxWidth(),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = formattedDate,
            color = Color(0xFFB8B8B8)
        )
    }
    Box(
        modifier = Modifier.fillMaxWidth(),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = "Чем я могу вам помочь?" ,
            color = Color(0xFFB8B8B8)
        )
    }
}

data class Message(val text: String, val time: String)

@Composable
fun ChatUI() {
    var text by remember { mutableStateOf("") }
    var messages by remember { mutableStateOf(listOf<Message>()) }

    fun sendMessage() {
        val currentTime = LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm"))
        messages = messages + Message(text, currentTime)
        text = ""
    }

    Column(modifier = Modifier.fillMaxWidth()) {
        Row (
            modifier = Modifier
                .fillMaxWidth()
                .background(Color(0xFF696F83)),
        ) {
            Text(text = "Чат с банком",
                Modifier.padding(10.dp),
                color = Color.White,
                fontSize = 25.sp
            )
        }

        CurrentDate()

        Column(
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth()
                .verticalScroll(rememberScrollState())
                .padding(8.dp)
        ) {
            messages.forEach { message ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .wrapContentWidth(Alignment.End)
                        .padding(4.dp),
                    horizontalArrangement = Arrangement.End
                ) {
                    Column {
                        Text(
                            text = message.text,
                            color = Color.Black,
                            modifier = Modifier
                                .background(
                                    color = Color(0xFFC0F5EB),
                                    shape = RoundedCornerShape(8.dp)
                                )
                                .padding(horizontal = 8.dp, vertical = 4.dp)
                        )
                        Text(
                            text = message.time,
                            color = Color.Gray,
                            fontSize = 12.sp
                        )
                    }
                }
            }
        }
        LazyRow (
            modifier = Modifier
                .padding(10.dp)
                .align(Alignment.CenterHorizontally)
                .fillMaxWidth(),
            horizontalArrangement = Arrangement.End
        ) {
            item { Button(
                modifier = Modifier
                    .height(50.dp)
                    .padding(5.dp),
                onClick = { /* TODO */ },
                colors = ButtonDefaults.buttonColors(backgroundColor = Color.White, contentColor = Color(0xFF46578B)),
                border = BorderStroke(2.dp, Color(0xFF46578B)),
                shape = RoundedCornerShape(20),
            ) {
                Text(
                    text = "Поддержка",
                    fontSize = 15.sp
                )
            }
                Button(
                    modifier = Modifier
                        .height(50.dp)
                        .padding(5.dp),
                    onClick = { /* TODO */ },
                    colors = ButtonDefaults.buttonColors(backgroundColor = Color.White, contentColor = Color(0xFF46578B)),
                    border = BorderStroke(2.dp, Color(0xFF46578B)),
                    shape = RoundedCornerShape(20),
                ) {
                    Text(
                        text = "Кредитование",
                        fontSize = 15.sp
                    )
                }
                Button(
                    modifier = Modifier
                        .height(50.dp)
                        .padding(5.dp),
                    onClick = { /* TODO */ },
                    colors = ButtonDefaults.buttonColors(backgroundColor = Color.White, contentColor = Color(0xFF46578B)),
                    border = BorderStroke(2.dp, Color(0xFF46578B)),
                    shape = RoundedCornerShape(20),
                ) {
                    Text(
                        text = "Переводы",
                        fontSize = 15.sp
                    )
                }
            }
        }
        Row (
            modifier = Modifier
                .fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ){
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .shadow(4.dp, shape = RoundedCornerShape(20))
                    .background(Color.White, RoundedCornerShape(20))
                    .padding(8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                BasicTextField(
                    value = text,
                    onValueChange = { text = it },
                    modifier = Modifier
                        .weight(1f)
                        .padding(horizontal = 8.dp),
                    keyboardOptions = KeyboardOptions(
                        keyboardType = KeyboardType.Text,
                        imeAction = ImeAction.Done
                    ),
                    decorationBox = { innerTextField ->
                        Row(Modifier.background(Color.Transparent)) {
                            if (text.isEmpty()) {
                                Text("Введите сообщение...", color = Color.Gray)
                            }
                            innerTextField()
                        }
                    }
                )
                IconButton(onClick = {
                    if (text.isNotBlank()) {
                        val currentTime = LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm"))
                        val newMessage = Message(text, currentTime)
                        messages = messages + newMessage
                        text = ""
                    }
                }) {
                    Icon(Icons.Filled.Send, contentDescription = "Send message")
                }
                IconButton(onClick = {}) {
                    Icon(painter = painterResource(id = R.drawable.microphone_1082810),
                        contentDescription = "Record voice message",
                        Modifier.size(26.dp))
                }
            }
        }
    }
}