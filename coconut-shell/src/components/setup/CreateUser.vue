<template>
    <form @submit.prevent="createUser">
        <div class="form-group">
            <label for="username">Username</label>
            <input type="text" id="username" v-model="username" required>
        </div>
        <br>
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" v-model="password" required>
        </div>
        <br>
        <div class="form-group">
            <label for="role">Role</label>
            <select id="role" v-model="role" required>
                <option v-for="role in roles" :key="role.value" :value="role.value">{{ role.text }}</option>
            </select>
        </div>
        <button type="submit" class="btn">Create User</button>
    </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { getCsrfToken } from '@/csrf'

const router = useRouter()

const username = ref('')
const password = ref('')
const role = ref('OWNER')
const messages = ref([])

const roles = [
    { value: 'OWNER', text: 'Owner' },
    { value: 'ADMIN', text: 'Admin' },
]

const createUser = async () => {
    try {
        const token = await getCsrfToken()

        const response = await fetch('/setup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token
            },
            body: JSON.stringify({
                username: username.value,
                password: password.value,
                role: role.value,
            }),
        })
        const data = await response.json()
        if (data.success) {
            alert('User created successfully!')
        } else {
            alert('Error creating user: ' + data.message)
        }
    } catch (error) {
        console.error('Error:', error)
    }
}
</script>
