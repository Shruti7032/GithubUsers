package com.playground.githubusers.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import com.playground.githubusers.data.local.dao.RemoteKeysDao
import com.playground.githubusers.data.local.dao.UserDao
import com.playground.githubusers.data.local.dao.UserDetailsDao
import com.playground.githubusers.data.local.entity.RemoteKeysEntity
import com.playground.githubusers.data.local.entity.UserDetailEntity
import com.playground.githubusers.data.local.entity.UserEntity

/**
 * Created by Shruti on 21/05/22.
 */
@Database(
    entities = [UserEntity::class, UserDetailEntity::class, RemoteKeysEntity::class],
    version = 1,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {

    abstract val userDao: UserDao
    abstract val userDetailDao: UserDetailsDao
    abstract val remoteKeysDao: RemoteKeysDao
}