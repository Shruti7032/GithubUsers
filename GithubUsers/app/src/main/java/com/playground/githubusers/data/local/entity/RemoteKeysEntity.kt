package com.playground.githubusers.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Created by Shruti on 21/05/22.
 */
@Entity(tableName = "remote_keys")
data class RemoteKeysEntity(
    @PrimaryKey
    val rpoId: Int?,
    val prevKey: Int?,
    val nextKey: Int?
)