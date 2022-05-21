package com.playground.githubusers.domain.usecase

import androidx.paging.PagingData
import com.playground.githubusers.domain.model.User
import com.playground.githubusers.domain.model.UserDetail
import kotlinx.coroutines.flow.Flow

/**
 * Created by Shruti on 21/05/22.
 */
interface UserUseCase {

    suspend fun getUser(): Flow<PagingData<User>>
    suspend fun getUserDetail(username: String): Flow<UserDetail>

}