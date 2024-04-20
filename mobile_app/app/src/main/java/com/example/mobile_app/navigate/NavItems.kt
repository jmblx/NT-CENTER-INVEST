package com.example.mobile_app.navigate

import com.example.mobile_app.R

data class NavItem(
    val icon: Int,
    val title: String,
    val route: String
)

val listOfNavItems = listOf(
    NavItem(R.drawable.chat, title = "Чат с банком", route = Screens.Chat.name),
)