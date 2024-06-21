<template>
    <Header />
    <main class="main-content">
        <component v-for="module in orderedModules" :is="moduleComponents[module]" :key="module" />
    </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Header from './Header.vue'
import modulesConfig from '@/modules'
import System from './modules/System.vue'
import DockerContainers from './modules/Docker.vue'
import Backup from './modules/Backup.vue'

const moduleComponents: { [key: string]: any } = {
    SYSTEM: System,
    BACKUP: Backup,
    DOCKER: DockerContainers
}

interface Module {
    name: string
    order: number
}

const orderedModules = ref<string[]>([])

const fetchModules = async () => {
    try {
        const response = await fetch('/setup/modules')
        const data: { modules: Module[] } = await response.json()
        orderedModules.value = data.modules.map(m => m.name)
    } catch (error) {
        console.error('Error fetching modules:', error)
    }
}

onMounted(fetchModules)
</script>