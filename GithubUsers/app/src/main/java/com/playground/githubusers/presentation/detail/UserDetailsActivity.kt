package com.playground.githubusers.presentation.detail

import android.os.Bundle
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import com.playground.githubusers.R
import com.playground.githubusers.databinding.ActivityUserDetailBinding
import com.playground.githubusers.domain.model.UserDetail
import com.playground.githubusers.utils.DataMapper
import com.playground.githubusers.utils.viewUtils.load
import dagger.hilt.android.AndroidEntryPoint

/**
 * Created by Shruti on 20/05/22.
 */
@AndroidEntryPoint
class UserDetailsActivity : AppCompatActivity() {

    private val binding: ActivityUserDetailBinding by lazy {
        ActivityUserDetailBinding.inflate(layoutInflater)
    }

    private val userDetailViewModel: UserDetailViewModel by viewModels()

    private var userDetail: UserDetail? = null

    private var username: String? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)
        handleIntent()
        initObserver()
        fetchData()
        initToolbar()

    }

    fun getUsername(): String? {
        return username
    }

    private fun initToolbar() {
        supportActionBar?.apply {
            setDisplayHomeAsUpEnabled(true)
            setDisplayShowHomeEnabled(true)
            elevation = 0f
            title = "$username\'s Detail"
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        onBackPressed()
        return super.onSupportNavigateUp()
    }

    private fun fetchData() {
        username?.let {
            userDetailViewModel.getUserDetailFromApi(it)
        }
    }

    private fun handleIntent() {
        username = intent.getStringExtra(USERNAME_KEY) as String
    }

    private fun initObserver() {
        with(userDetailViewModel) {
            state.observe(this@UserDetailsActivity) {
//                handleStateLoading(it)
            }
            resultUserDetail.observe(this@UserDetailsActivity) {
                handleResultUserDetail(it)
            }
        }

    }

    private fun handleResultUserDetail(data: UserDetail) {
        userDetail = data
        binding.apply {
            txtUsername.text = data.name
            txtEmail.text = data.emailId ?: getString(R.string.no_email)
            txtFollower.text = data.followers.toString()
            txtFollowing.text = data.following.toString()
            txtCompany.text = data.company ?: getString(R.string.no_company)
            txtCreatedOn.text = DataMapper.getFormatDateAndTime(data.createdAt.toString())
            ivUser.load(data.avatarUrl)
        }

    }

    override fun onBackPressed() {
        super.onBackPressed()
        supportFinishAfterTransition()
    }

    companion object {
        const val USERNAME_KEY = "username_key"
    }
}