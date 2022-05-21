package com.playground.githubusers.di

import android.app.Application
import androidx.room.Room
import com.playground.githubusers.BuildConfig
import com.playground.githubusers.data.local.AppDatabase
import com.playground.githubusers.data.local.dao.UserDao
import com.playground.githubusers.data.local.dao.UserDetailsDao
import com.playground.githubusers.data.remote.Network
import com.playground.githubusers.data.remote.NetworkService
import com.playground.githubusers.utils.const.databaseName
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.components.ApplicationComponent
import net.sqlcipher.database.SQLiteDatabase
import net.sqlcipher.database.SupportFactory
import javax.inject.Singleton

/**
 * Created by Shruti on 21/05/22.
 */
@Module
@InstallIn(ApplicationComponent::class)
object CoreModule {

    @Provides
    @Singleton
    fun provideNetworkService(): NetworkService {
        return Network.retrofitClient().create(NetworkService::class.java)
    }

    @Singleton
    @Provides
    fun provideAppDatabase(app: Application): AppDatabase {
        val passPhare: ByteArray = SQLiteDatabase.getBytes(BuildConfig.PASSPHRASE.toCharArray())
        val factory = SupportFactory(passPhare)

        return Room.databaseBuilder(
            app,
            AppDatabase::class.java,
            databaseName
        ).fallbackToDestructiveMigration()
            .openHelperFactory(factory)
            .build()
    }

    @Singleton
    @Provides
    fun provideUserDao(appDatabase: AppDatabase): UserDao {
        return appDatabase.userDao
    }

    @Singleton
    @Provides
    fun provideUserDetailsDao(appDatabase: AppDatabase): UserDetailsDao {
        return appDatabase.userDetailDao
    }
}