package com.playground.githubusers.utils

import android.content.Context

/**
 * Created by Shruti on 20/05/22.
 */
object const {
    const val databaseName = "git_user_database"
    lateinit var mContext: Context

    fun init(context: Context) {
        this.mContext = context
    }
}