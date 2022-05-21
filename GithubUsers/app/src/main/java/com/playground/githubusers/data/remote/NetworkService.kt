package com.playground.githubusers.data.remote

import com.playground.githubusers.domain.model.UserDetail
import com.playground.githubusers.domain.model.UsersList
import retrofit2.http.GET
import retrofit2.http.Path
import retrofit2.http.Query

/**
 * CCreated by Shruti on 21/05/22.
 */
interface NetworkService {

    /**
     * Endpoints search User
     */
    @GET("users")
    suspend fun getUser(
        @Query("since") since: Int?,
        @Query("per_page") perPage: Int?
    ): UsersList

    /**
     * Endpoints Detail User
     */
    @GET("users/{username}")
    suspend fun getDetailUser(
        @Path("username") username: String
    ): UserDetail

}