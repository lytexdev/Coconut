<template>
    <div class="container" v-if="setup === 1">
        <div class="setup-header">
            <Logo />
            <h1>Create Login < Setup</h1>
        </div>
        <CreateUser />
        <div class="separator"></div>
        <button @click="nextStep" class="btn">Next</button>
    </div>

    <div class="container" v-else-if="setup === 2">
        <div class="setup-header">
            <Logo />
            <h1>Select Modules < Setup</h1>
        </div>
        <ModuleSelection />
        <div class="separator"></div>
        <button @click="nextStep" class="btn">Next</button>
    </div>

    <div class="container" v-else>
        <div class="setup-header">
            <Logo />
            <h1>Setup Complete</h1>
            <p>Setup is complete! You can now login.</p>
        </div>
        <div class="separator"></div>
        <button @click="finishSetup" class="btn btn-success">Finish Setup</button>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'
import CreateUser from './CreateUser.vue';
import ModuleSelection from './ModuleSelection.vue';
import Logo from '../Logo.vue';

const router = useRouter()
const setup = ref(1)

const nextStep = () => {
    setup.value += 1
}

const finishSetup = async () => {
    try {
        const response = await fetch('/setup/finish', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        const data = await response.json()
        if (data.success) {
            router.push('/')
        } else {
            alert('Error finishing setup')
        }
    } catch (error) {
        console.error('Error:', error)
    }
}
</script>
