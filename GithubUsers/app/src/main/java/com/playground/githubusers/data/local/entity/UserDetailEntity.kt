package com.playground.githubusers.data.local.entity

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Created by Shruti on 21/05/22.
 */
@Entity(tableName = "user_details_table")
data class UserDetailEntity(
    @PrimaryKey
    val id: Int?,

    @ColumnInfo(name = "name")
    val name: String?,

    @ColumnInfo(name = "avatar_url")
    val avatarUrl: String?,

    @ColumnInfo(name = "email_Id")
    val emailId: String?,

    @ColumnInfo(name = "company")
    val company: String?,

    @ColumnInfo(name = "followers")
    val followers: Int?,

    @ColumnInfo(name = "following")
    val following: Int?,

    @ColumnInfo(name = "created_at")
    val createdAt: String?,

    @ColumnInfo(name = "login")
    val login: String?,
)
