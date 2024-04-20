package com.example.mobile_app.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.background
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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

@Composable
fun ChatUI() {
    var text by remember { mutableStateOf("") }
    var messages by remember { mutableStateOf(listOf<String>()) }
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Чат с банком") },
                backgroundColor = Color(0xFF696F83),
                contentColor = Color.White
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .padding(innerPadding)
                .padding(horizontal = 8.dp)
                .fillMaxSize()
        ) {
            // Messages column
            Column(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .verticalScroll(rememberScrollState())
            ) {
                messages.forEach { message ->
                    Text(
                        text = message,
                        modifier = Modifier
                            .fillMaxWidth()
                            .wrapContentWidth(Alignment.End)
                            .padding(4.dp)
                            .background(color = Color(0xFFC0F5EB), shape = RoundedCornerShape(8.dp))
                            .padding(horizontal = 8.dp, vertical = 4.dp),
                        color = Color.Black
                    )
                }
            }

            // Input field and send button
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ){
                BasicTextField(
                    value = text,
                    onValueChange = { text = it },
                    modifier = Modifier
                        .weight(1f)
                        .padding(8.dp)
                        .background(Color.White, RoundedCornerShape(20))
                        .padding(horizontal = 16.dp),
                    decorationBox = { innerTextField ->
                        if (text.isEmpty()) {
                            Text("Введите сообщение...", color = Color.Gray)
                        }
                        innerTextField()
                    }
                )
                IconButton(onClick = {
                    if (text.isNotBlank()) {
                        messages = messages + text
                        text = ""
                    }
                }) {
                    Icon(Icons.Filled.Send, contentDescription = "Send message")
                }
            }

            // Specialized buttons row
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                Button(onClick = { /* Handle support click */ }) {
                    Text("Поддержка")
                }
                Button(onClick = { /* Handle credit click */ }) {
                    Text("Кредитование")
                }
                Button(onClick = { /* Handle transfers click */ }) {
                    Text("Переводы")
                }
            }
        }
    }
}
