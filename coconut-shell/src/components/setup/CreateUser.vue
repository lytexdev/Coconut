<template>
    <form @submit.prevent="createUser">
        <div class="form-group">
            <label for="username">Nickname</label>
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

    <ul v-if="messages.length">
        <li v-for="message in messages" :key="message">{{ message }}</li>
    </ul>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const username = ref('')
const password = ref('')
const role = ref('OWNER')
const messages = ref([])

const roles = [
    { value: 'OWNER', text: 'Owner' },
    { value: 'ADMIN', text: 'Admin' },
]

const createUser = () => {
    fetch('/setup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username.value,
            password: password.value,
            role: role.value,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                messages.value = ['User created successfully!']
            } else {
                messages.value = [data.message]
            }
        })
        .catch((error) => {
            console.error('Error:', error)
        })
}
</script>
