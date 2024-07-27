<template>
    <header class="header-main">
        <Logo />
        <nav class="nav-main">
            <button @click="logout" class="btn btn-logout">Logout</button>
            <button @click="settings" class="btn btn-config">Settings</button>
        </nav>
    </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import Logo from './Logo.vue'

const router = useRouter()

const logout = async () => {
    try {
        const response = await fetch('/logout', {
            method: 'GET',
        })
        if (response.ok) {
            router.push('/login')
        } else {
            console.error('Error logging out:', await response.text())
        }
    } catch (error) {
        console.error('Error logging out:', error)
    }
}

const settings = () => {
    router.push('/settings')
}
</script>
