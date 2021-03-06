package com.playground.githubusers.utils.state

sealed class LoaderState {
    object ShowLoading : LoaderState()
    object HideLoading : LoaderState()
}