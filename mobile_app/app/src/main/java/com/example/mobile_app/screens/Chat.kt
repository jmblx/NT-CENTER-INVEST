package com.example.myapplication

import androidx.compose.foundation.BorderStroke
import com.example.mobile_app.R
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.material.*
import com.example.mobile_app.CurrentDate

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ChatUIWithScaffold() {
    var text by remember { mutableStateOf("") }
    var messages by remember { mutableStateOf(listOf("Чем я могу вам помочь?")) }
    val rowCards = listOf("Поддержка", "Кредитование", "Переводы")

    Scaffold(
        topBar = { CardTopBar() },
        bottomBar = { UserInput(
            text = text,
            onTextChanged = { newText -> text = newText },
            onSendMessage = {
                if (text.isNotBlank()) {
                    messages = listOf(text) + messages
                    text = ""
                }
            }
        ) },
        snackbarHost = { SnackbarHost(hostState = remember { SnackbarHostState() }) }
    ) { innerPadding ->
        ChatUI(modifier = Modifier.padding(innerPadding))
    }
}

@Composable
fun ChatUI(modifier: Modifier = Modifier) {
    var text by remember { mutableStateOf("") }
    var messages by remember { mutableStateOf(listOf("Чем я могу вам помочь?")) }
    val rowCards = listOf("Поддержка", "Кредитование", "Переводы")

    Column(modifier = Modifier.fillMaxSize().background(Color(0xFFF7F7F7))) {
        CurrentDate()
        Spacer(modifier = Modifier.height(8.dp))
        MessageSpace(messages)
        BottomButtonsRow(rowCards)
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CardTopBar() {
    TopAppBar(
        title = { Text(text = "Чат с банком", color = Color.White) },
        colors = TopAppBarDefaults.mediumTopAppBarColors(containerColor = Color(0xFF696F83))
    )
}

@Composable
fun MessageSpace(messages: List<String>) {
    LazyColumn(
        modifier = Modifier
            .fillMaxHeight(0.8f)
            .padding(horizontal = 8.dp),
        reverseLayout = true
    ) {
        items(messages) { message ->
            MessageCard(message)
        }
    }
}

@Composable
fun MessageCard(message: String) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp)
    ) {
        Text(
            text = message,
            modifier = Modifier
                .align(Alignment.TopEnd)
                .background(Color(0xFFC0F5EB), RoundedCornerShape(8.dp))
                .padding(horizontal = 16.dp, vertical = 8.dp),
            color = Color.Black
        )
    }
}

@Composable
fun BottomButtonsRow(buttons: List<String>) {
    LazyRow(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp, horizontal = 4.dp),
        horizontalArrangement = Arrangement.Center
    ) {
        items(buttons) { buttonLabel ->
            BottomButton(text = buttonLabel)
        }
    }
}

@Composable
fun BottomButton(text: String) {
    OutlinedButton(
        onClick = { /* TODO: Реализуйте действие кнопки */ },
        modifier = Modifier.padding(horizontal = 4.dp),
        border = BorderStroke(1.dp, Color(0xFF46578B)),
        shape = RoundedCornerShape(8.dp),
        colors = ButtonDefaults.buttonColors(
            containerColor = Color(0xFFB2DFDB)
        )
    ) {
        Text(text = text, color = Color.Black, fontSize = 16.sp)
    }
}

@Composable
fun UserInput(text: String, onTextChanged: (String) -> Unit, onSendMessage: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 8.dp, vertical = 8.dp)
            .background(Color.White),
        verticalAlignment = Alignment.Bottom

    ) {
        BasicTextField(
            value = text,
            onValueChange = onTextChanged,
            singleLine = true,
            keyboardOptions = KeyboardOptions.Default.copy(
                keyboardType = KeyboardType.Text,
                imeAction = ImeAction.Send
            ),
            keyboardActions = KeyboardActions(
                onSend = { onSendMessage() }
            ),
            modifier = Modifier
                .weight(1f)
                .padding(8.dp),
            decorationBox = { innerTextField ->
                Row(
                    Modifier
                        .background(Color(0xFFE0E0E0), RoundedCornerShape(24.dp))
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    if (text.isEmpty()) {
                        Text("Введите сообщение...", color = Color.Gray)
                    }
                    innerTextField()
                }
            }
        )
        IconButton(onClick = onSendMessage) {
            Icon(
                painter = if (text.isNotEmpty()) painterResource(id = R.drawable.send_button) else painterResource(id = R.drawable.micro),
                contentDescription = if (text.isNotEmpty()) "Отправить сообщение" else "Голосовой ввод",
                tint = Color(0xFF00796B)
            )
        }
    }
}

@Preview(showBackground = true)
@Composable
fun ChatUIPreview() {
    ChatUI()
}
