package com.playground.githubusers

import android.app.Application
import com.playground.githubusers.utils.const
import dagger.hilt.android.HiltAndroidApp

/**
 * Created by Shruti on 20/05/22.
 */
@HiltAndroidApp
class BaseApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        const.init(this)
    }
}