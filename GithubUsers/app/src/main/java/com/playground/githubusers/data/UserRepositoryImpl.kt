package com.playground.githubusers.data

import androidx.paging.ExperimentalPagingApi
import androidx.paging.Pager
import androidx.paging.PagingConfig
import androidx.paging.PagingData
import com.playground.githubusers.data.local.AppDatabase
import com.playground.githubusers.data.paging.UsersRemoteMediator
import com.playground.githubusers.data.remote.NetworkService
import com.playground.githubusers.domain.model.User
import com.playground.githubusers.domain.model.UserDetail
import com.playground.githubusers.domain.repository.UserRepository
import com.playground.githubusers.utils.DataMapper
import kotlinx.coroutines.Dispatchers.IO
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.flowOn
import kotlinx.coroutines.flow.map
import javax.inject.Inject

/**
 * Created by Shruti on 21/05/22.
 */
@OptIn(ExperimentalPagingApi::class)
class UserRepositoryImpl @Inject constructor(
    private val networkService: NetworkService,
    private val mAppDB: AppDatabase,
) : UserRepository {

    override suspend fun getUser(): Flow<PagingData<User>> {
        val pagingSourceFactory = { mAppDB.userDao.fetchUser() }
        return Pager(
            config = PagingConfig(
                pageSize = 30,
                prefetchDistance = 0,
                maxSize = PagingConfig.MAX_SIZE_UNBOUNDED,
                jumpThreshold = Int.MIN_VALUE,
                enablePlaceholders = true,
            ),
            remoteMediator = UsersRemoteMediator(
                networkService,
                mAppDB,
            ),
            pagingSourceFactory = pagingSourceFactory
        ).flow.map { UserEntityPagingData ->
            DataMapper.mapUserResponseToDomain(UserEntityPagingData)
        }
    }

    override suspend fun getUserDetail(username: String): Flow<UserDetail> {
        return flow {
            try {
                val userDetailsDao = mAppDB.userDetailDao
//                Query whether the database exists, if not, request the network
                var userDetails_db = userDetailsDao.getUserDetailsByUserName(username)

                if (userDetails_db == null) {
                    //network request
                    val response = networkService.getDetailUser(username = username)
                    //Convert the data requested by the network into the model of the database, and then insert it into the database
                    userDetails_db = DataMapper.mapUserDetailResponseToEntities(
                        response
                    )
                    userDetailsDao.addUserDetailsToDB(userDetails_db);
                }

                // Convert the model of the data source to the model used by the upper layer,
                // ui cannot directly hold the data source to prevent the change of the data source from affecting the upper layer ui
                val dataMaped = DataMapper.mapUserDetailResponseToDomain(userDetails_db)
                emit(dataMaped)

            } catch (e: Exception) {
                e.printStackTrace()
//                emit(e.toString(), 500)
            }
        }.flowOn(IO)
    }
}