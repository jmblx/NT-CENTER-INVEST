package com.example.mobile_app.screens

import androidx.compose.runtime.Composable
import java.util.Calendar
import java.util.Locale
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.AlertDialogDefaults.containerColor
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Alignment.Companion.Start
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Color.Companion.White
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.PopupProperties
import com.example.mobile_app.R

@OptIn(ExperimentalMaterialApi::class)
@Composable
fun ExposedDropdownSample() {
    var expanded by remember { mutableStateOf(false) }
    val options = listOf("Творческий", "Официальный", "Разговорный")
    var selectedIndex by remember { mutableStateOf(0) }

    Row (
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.End
    ) {
        ExposedDropdownMenuBox(
            expanded = expanded,
            onExpandedChange = {
                expanded = !expanded
            }
        ) {
            TextField(
                readOnly = true,
                value = options[selectedIndex],
                onValueChange = { },
                label = { Text("Выберите стиль речи")},
                trailingIcon = {
                    ExposedDropdownMenuDefaults.TrailingIcon(
                        expanded = expanded
                    )
                },
                colors = ExposedDropdownMenuDefaults.textFieldColors(
                    backgroundColor =  Color.White,
                    focusedIndicatorColor = Color(0xFF696F83),
                    unfocusedIndicatorColor = Color(0xFF696F83)
                ),
                modifier = Modifier
                    .padding(5.dp)
                    .border(1.dp, Color(0xFF696F83), RoundedCornerShape(4.dp))
            )
            ExposedDropdownMenu(
                expanded = expanded,
                onDismissRequest = {
                    expanded = false
                }
            ) {
                options.forEachIndexed { index, selectionOption ->
                    DropdownMenuItem(
                        onClick = {
                            selectedIndex = index
                            expanded = false
                        }
                    ) {
                        Text(text = selectionOption, color = Color.Black)
                    }
                }
            }
        }
    }
}

@Composable
fun currentDate(): String {
    val calendar = Calendar.getInstance()
    val monthName = calendar.getDisplayName(Calendar.MONTH, Calendar.LONG, Locale("ru"))
    val dayOfMonth = calendar.get(Calendar.DAY_OF_MONTH)
    val dayOfWeek = calendar.getDisplayName(Calendar.DAY_OF_WEEK, Calendar.SHORT, Locale("ru"))

    return "$dayOfMonth $monthName $dayOfWeek"
}

@Composable
fun ChatUI2() {
    var text by remember { mutableStateOf("") }
    var messages by remember { mutableStateOf(listOf<String>()) }

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
                    Text(
                        text = message,
                        color = Color.Black,
                        modifier = Modifier
                            .background(
                                color = Color(0xFFC0F5EB),
                                shape = RoundedCornerShape(8.dp)
                            )
                            .padding(horizontal = 8.dp, vertical = 4.dp)
                    )
                }
            }
        }
        Row (
            modifier = Modifier
                .padding(10.dp)
                .align(Alignment.CenterHorizontally)
                .fillMaxWidth(),
            horizontalArrangement = Arrangement.End
        ) {
            Button(
                modifier = Modifier.padding(5.dp),
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
                modifier = Modifier.padding(5.dp),
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
                modifier = Modifier.padding(5.dp),
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
        ExposedDropdownSample()
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
                IconButton(onClick = {}) {
                    Icon(painter = painterResource(id = R.drawable.photo),
                        contentDescription = "Import Image",
                        Modifier.size(26.dp))
                }
                BasicTextField(
                    value = text,
                    onValueChange = { text = it },
                    modifier = Modifier
                        .weight(1f)
                        .padding(horizontal = 8.dp),
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
                        messages = messages + text
                        text = ""
                    }
                }) {
                    Icon(Icons.Filled.Send, contentDescription = "Send message")
                }
                IconButton(onClick = {}) {
                    Icon(painter = painterResource(id = R.drawable.micro),
                        contentDescription = "Record voice message",
                        Modifier.size(26.dp))
                }
            }
        }
    }
}

