<template>
    <div class="container" v-if="setup === 1">
        <div class="setup-header">
            <Logo />
            <h1>Create Login < Setup</h1>
            <p>Create a Admin user to login to Coconut.
                <br>After setup is complete, you can add more users at the configuration page.
            </p>
        </div>
        <CreateUser />
        <div class="separator"></div>
        <button @click="nextStep" class="btn btn-success">Next</button>
    </div>

    <div class="container" v-else-if="setup === 2">
        <div class="setup-header">
            <Logo />
            <h1>Select Modules < Setup</h1>
            <p>Select the modules you want to use in Coconut and the order they should appear.
                <br>You can always change this later in the configuration page.
            </p>
        </div>
        <ModuleSelection />
        <div class="separator"></div>
        <button @click="previousStep" class="btn">Back</button>
        <button @click="nextStep" class="btn btn-success">Next</button>
    </div>

    <div class="container" v-else>
        <div class="setup-header">
            <Logo />
            <h1> X < Setup</h1>
            <p>Setup is complete! You can now finish the setup and start using Coconut.</p>
        </div>
        <div class="separator"></div>
        <button @click="previousStep" class="btn">Back</button>
        <button @click="finishSetup" class="btn btn-success" title="Click to finish the setup">Finish Setup</button>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import CreateUser from './CreateUser.vue';
import ModuleSelection from './ModuleSelection.vue';
import Logo from '../Logo.vue';

const router = useRouter();
const setup = ref<number>(1);
const modules = ref<string[]>([]);

const nextStep = () => {
    setup.value += 1;
}

const previousStep = () => {
    setup.value -= 1;
}

const finishSetup = async () => {
    try {
        const response = await fetch('/setup/finish', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        if (data.success) {
            router.push('/login');
        } else {
            alert('Error finishing setup');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

const fetchEnabledModules = async () => {
    try {
        const response = await fetch('/setup/modules')
        const data = await response.json()
        modules.value = data.modules.map((m: any) => m.name)
    } catch (error) {
        console.error('Error fetching enabled modules:', error)
    }
}

onMounted(fetchEnabledModules)
</script>
