package com.playground.githubusers.domain.usecase

import androidx.paging.PagingData
import com.playground.githubusers.domain.model.User
import com.playground.githubusers.domain.model.UserDetail
import com.playground.githubusers.domain.repository.UserRepository
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject

/**
 * Created by Shruti on 21/05/22.
 */
class UserUseCaseImpl @Inject constructor(
    private val userRepository: UserRepository
) : UserUseCase {
    override suspend fun getUser(): Flow<PagingData<User>> {
        return userRepository.getUser()
    }

    override suspend fun getUserDetail(username: String): Flow<UserDetail> {
        return userRepository.getUserDetail(username = username)
    }
}