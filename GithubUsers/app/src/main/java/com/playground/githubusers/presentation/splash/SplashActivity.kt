package com.playground.githubusers.presentation.splash

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.view.animation.AnimationUtils
import androidx.appcompat.app.AppCompatActivity
import com.playground.githubusers.R
import com.playground.githubusers.databinding.ActivitySplashBinding
import com.playground.githubusers.presentation.home.HomeActivity

/**
 * Created by Shruti on 20/05/22.
 */
class SplashActivity : AppCompatActivity() {

    private val binding : ActivitySplashBinding by lazy {
        ActivitySplashBinding.inflate(layoutInflater)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)
        loadAnimation()
        startIntent()
    }

    private fun loadAnimation() {
        val logoAnimation = AnimationUtils.loadAnimation(this, R.anim.logo_animation)
        val textAnimation = AnimationUtils.loadAnimation(this, R.anim.bottom_to_top_animation)

        binding.apply {
            imageView.startAnimation(logoAnimation)
            txtTitle.startAnimation(textAnimation)
        }
    }

    private fun startIntent() {
        Handler(mainLooper).postDelayed({
            startActivity(Intent(this, HomeActivity::class.java)).also { finish() }
        },2000)
    }
}