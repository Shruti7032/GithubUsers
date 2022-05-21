package com.playground.githubusers.domain.model

import com.google.gson.annotations.SerializedName

/**
 * Created by Shruti on 21/05/22.
 */
data class User(
    @SerializedName("id") val id: Int?,

    @SerializedName("avatar_url") val avatarUrl: String?,

    @SerializedName("login") val login: String?,
)
