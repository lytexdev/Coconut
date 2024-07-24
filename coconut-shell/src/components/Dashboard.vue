<template>
    <Header />
    
    <main class="main-content">
        <component v-for="module in orderedModules" :is="moduleComponents[module.enum]" :key="module.enum" />
    </main>
</template>

<script setup lang="ts">
import { ref, onMounted, AsyncComponentLoader, defineAsyncComponent } from 'vue'
import Header from './Header.vue'
import modules from '@/modules'

const moduleComponents: { [key: string]: any } = {}
const orderedModules = ref<{ enum: string, component: string }[]>([])

const fetchModules = async () => {
    try {
        const response = await fetch('/setup/modules')
        const data: { modules: { name: string, order: number }[] } = await response.json()
        const sortedModules = data.modules.sort((a, b) => a.order - b.order)

        orderedModules.value = sortedModules.map(module => {
            const foundModule = modules.find(m => m.enum === module.name)
            if (foundModule) {
                return foundModule
            }
            return null
        }).filter(module => module !== null)

        for (const module of orderedModules.value) {
            moduleComponents[module.enum] = defineAsyncComponent(() => import(`./modules/${module.component}.vue`))
        }
    } catch (error) {
        console.error('Error fetching modules:', error)
    }
}

onMounted(fetchModules)
</script>
