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
        <h1>Select Modules < Setup</h1>
        <ModuleSelection />

        <div class="separator"></div>
        <button @click="nextStep" class="btn">Next</button>
    </div>

    <div class="container" v-else>
        <h1>Setup Complete</h1>
        <p>Setup is complete! You can now login.</p>

        <div class="separator"></div>
        <button class="btn btn-success">Finish Setup</button>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import CreateUser from './CreateUser.vue';
import ModuleSelection from './ModuleSelection.vue';
import Logo from '../Logo.vue';

const setup = ref(1)

const nextStep = () => {
    setup.value += 1
}
</script>
