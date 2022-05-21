package com.playground.githubusers.data.paging

import androidx.paging.ExperimentalPagingApi
import androidx.paging.LoadType
import androidx.paging.PagingState
import androidx.paging.RemoteMediator
import androidx.room.withTransaction
import com.playground.githubusers.data.local.AppDatabase
import com.playground.githubusers.data.local.entity.RemoteKeysEntity
import com.playground.githubusers.data.local.entity.UserEntity
import com.playground.githubusers.data.remote.NetworkService
import com.playground.githubusers.utils.DataMapper
import com.playground.githubusers.utils.const
import com.playground.githubusers.utils.isConnectedNetwork
import okio.IOException
import retrofit2.HttpException

/**
 * Created by Shruti on 21/05/22.
 */

const val STARTING_PAGE_INDEX = 0
const val ELEMENT_PER_PAGE = 30

@OptIn(ExperimentalPagingApi::class)
class UsersRemoteMediator(
    private val networkService: NetworkService,
    private val mAppDB: AppDatabase,
) : RemoteMediator<Int, UserEntity>() {

    override suspend fun initialize(): InitializeAction {
        return InitializeAction.LAUNCH_INITIAL_REFRESH
    }

    override suspend fun load(
        loadType: LoadType, state: PagingState<Int, UserEntity>
    ): MediatorResult {
        val pageKeyData = getKeyPageData(loadType, state)
        val page = when (pageKeyData) {
            is MediatorResult.Success -> {
                return pageKeyData
            }
            else -> {
                pageKeyData as Int
            }
        }

        try {
            if (!const.mContext.isConnectedNetwork()) {
                return MediatorResult.Success(endOfPaginationReached = true)
            }
            val response = networkService.getUser(since = page, perPage = state.config.pageSize)

            val isEndOfList = response.isEmpty()
            mAppDB.withTransaction {
                if (loadType == LoadType.REFRESH) {
                    mAppDB.userDao.clearAllUser()
                    mAppDB.remoteKeysDao.clearAll()
                }
                val prevKey = if (page == STARTING_PAGE_INDEX) null else page - ELEMENT_PER_PAGE
                val nextKey = if (isEndOfList) null else page + ELEMENT_PER_PAGE
                val keys = response.map {
                    RemoteKeysEntity(it.id, prevKey = prevKey, nextKey = nextKey)
                }
                mAppDB.userDao.insertUser(DataMapper.mapUserResponseToEntities(response))
                mAppDB.remoteKeysDao.insertAll(keys)
            }
            return MediatorResult.Success(endOfPaginationReached = isEndOfList)
        } catch (exception: IOException) {
            return MediatorResult.Error(exception)
        } catch (exception: HttpException) {
            return MediatorResult.Error(exception)
        }
    }

    private suspend fun getKeyPageData(
        loadType: LoadType,
        state: PagingState<Int, UserEntity>
    ): Any {
        return when (loadType) {
            LoadType.REFRESH -> {
                val remoteKeys = getRemoteKeyClosestToCurrentPosition(state)
                remoteKeys?.nextKey?.minus(1) ?: STARTING_PAGE_INDEX
            }
            LoadType.APPEND -> {
                val remoteKeys = getLastRemoteKey(state)
                val nextKey = remoteKeys?.nextKey
                return nextKey ?: MediatorResult.Success(endOfPaginationReached = false)
            }
            LoadType.PREPEND -> {
                val remoteKeys = getFirstRemoteKey(state)
                val prevKey = remoteKeys?.prevKey ?: return MediatorResult.Success(
                    endOfPaginationReached = false
                )
                prevKey
            }
        }
    }

    private suspend fun getRemoteKeyClosestToCurrentPosition(state: PagingState<Int, UserEntity>): RemoteKeysEntity? {
        return state.anchorPosition?.let { position ->
            state.closestItemToPosition(position)?.id?.let { repoId ->
                mAppDB.remoteKeysDao.getRemoteKeys(repoId)
            }
        }
    }

    private suspend fun getLastRemoteKey(state: PagingState<Int, UserEntity>): RemoteKeysEntity? {
        return state.pages
            .lastOrNull { it.data.isNotEmpty() }
            ?.data?.lastOrNull()
            ?.let { cat -> mAppDB.remoteKeysDao.getRemoteKeys(cat.id) }
    }

    private suspend fun getFirstRemoteKey(state: PagingState<Int, UserEntity>): RemoteKeysEntity? {
        return state.pages
            .firstOrNull { it.data.isNotEmpty() }
            ?.data?.firstOrNull()
            ?.let { cat -> mAppDB.remoteKeysDao.getRemoteKeys(cat.id) }
    }


}