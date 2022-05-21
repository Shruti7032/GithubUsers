package com.playground.githubusers.presentation.home

import android.os.Bundle
import android.util.Log
import android.view.View
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import androidx.paging.PagingData
import androidx.recyclerview.widget.LinearLayoutManager
import com.playground.githubusers.databinding.ActivityHomeBinding
import com.playground.githubusers.domain.model.User
import com.playground.githubusers.utils.state.LoaderState
import com.playground.githubusers.utils.viewUtils.setGone
import com.playground.githubusers.utils.viewUtils.setVisible
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch

/**
 * Created by Shruti on 20/05/22.
 */
@AndroidEntryPoint
class HomeActivity : AppCompatActivity() {

    private val HomeViewModel: HomeViewModel by viewModels()

    private val HomeAdapter: HomeAdapter by lazy {
        HomeAdapter(this)
    }

    private val binding: ActivityHomeBinding by lazy {
        ActivityHomeBinding.inflate(layoutInflater)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)
        initToolbar()
        getUsers()
        initRecyclerView()
        initObserver()
        initSwipeToRefresh()
    }

    private fun initToolbar() {
        supportActionBar?.elevation = 0f
    }

    private fun getUsers() {
        setIllustration(false)
        HomeViewModel.getUserFromApi()

    }

    private fun initObserver() {
        with(HomeViewModel) {
            state.observe(this@HomeActivity) {
                it?.let {
                    Log.d("DEBUG", "Loader state --> $it")
                    handleStateLoading(it)
                }
            }
            resultUserApi.observe(this@HomeActivity) {
                it?.let {
                    Log.d("DEBUG", "resultUserApi --> $it")
                    handleUserFromApi(it)
                }
            }
            networkError.observe(this@HomeActivity) {
                it?.let {
                    Log.d("DEBUG", "networkError --> $it")
                    setIllustration(true)
                }
            }
        }
    }

    private fun initSwipeToRefresh() {
        binding.swpRefreshUser.apply {
            setOnRefreshListener {
                getUsers()
                binding.swpRefreshUser.isRefreshing = false
                binding.rvUser.scrollToPosition(0)
            }
        }
    }

    private fun initRecyclerView() {
        val mlayoutManager = LinearLayoutManager(
            this@HomeActivity, LinearLayoutManager.VERTICAL, false
        )
        binding.rvUser.apply {
            layoutManager =
                mlayoutManager
            adapter = HomeAdapter
        }
        HomeAdapter.setActivity(this)
    }

    private fun handleUserFromApi(result: PagingData<User>) {
        lifecycleScope.launch {
            HomeAdapter.submitData(lifecycle, result)
        }
    }

    private fun handleStateInternet(error: Boolean) {
        with(binding) {
            if (error) {
                setIllustration(true)
                baseLoading.root.setGone()
                rvUser.setVisible()
            } else {
                setIllustration(false)
                baseLoading.root.setVisible()
                rvUser.setGone()
            }
        }

    }

    private fun handleStateLoading(loading: LoaderState) {
        with(binding) {
            if (loading is LoaderState.ShowLoading) {
                baseLoading.root.setVisible()
                setIllustration(false)
                rvUser.setGone()
            } else {
                baseLoading.root.setGone()
                setIllustration(false)
                rvUser.setVisible()
            }
        }

    }

    private fun setIllustration(status: Boolean) {
        binding.baseEmpty.root.visibility = if (status) View.VISIBLE else View.INVISIBLE
    }
}