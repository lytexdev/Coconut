<template>
    <header class="header-main">
        <Logo />

        <nav class="nav-main">
            <button @click="logout" class="btn btn-logout">Logout</button>
            <button @click="configure" class="btn btn-config">Configuration</button>
        </nav>
    </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import Logo from './Logo.vue';

const router = useRouter()

const logout = () => {
    fetch('/logout', {
        method: 'GET',
    })
        .then(() => {
            router.push('/login')
        })
        .catch((error) => {
            console.error('Error logging out:', error)
        })
}

const configure = () => {
    // TODO: Implement configuration page
    alert('Configuration button clicked')
}
</script>