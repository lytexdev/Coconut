<template>
    <div class="container">
        <h1>Login < Coconut</h1>

        <form @submit.prevent="login">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" v-model="username" required>
            </div>
            <br>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" v-model="password" required>
            </div>
            <button type="submit" class="btn">Login</button>
        </form>

        <ul v-if="messages.length">
            <li v-for="message in messages" :key="message">{{ message }}</li>
        </ul>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { getCsrfToken } from '@/csrf'

const router = useRouter()
const username = ref('')
const password = ref('')
const messages = ref([])

const login = async () => {
    try {
        const token = await getCsrfToken()

        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token
            },
            body: JSON.stringify({
                username: username.value,
                password: password.value,
            }),
        })
        const data = await response.json()
        if (data.success) {
            router.push('/')
        } else {
            messages.value = [data.message]
        }
    } catch (error) {
        console.error('Error:', error)
    }
}
</script>
