<template>
    <div class="module-selection">
        <div v-for="module in modules" :key="module.enum" class="module-option">
            <label>
                <input type="checkbox" v-model="selectedModules" :value="module.enum" />
                {{ module.text }}
            </label>
            <input type="number" v-model="moduleOrder[module.enum]" min="1" v-if="selectedModules.includes(module.enum)"
                placeholder="Order" />
        </div>
        <button @click="saveModules" class="btn">Save Modules</button>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import modulesConfig from '@/modules'

interface ModuleOrder {
    [key: string]: number;
}

interface FetchModule {
    name: string;
    order: number;
}

const modules = modulesConfig

const selectedModules = ref<string[]>([])
const moduleOrder = ref<ModuleOrder>({})

const saveModules = () => {
    const payload = selectedModules.value.map(module => ({
        name: module,
        order: moduleOrder.value[module] || 0
    }))

    fetch('/setup/modules', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ modules: payload }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert('Modules saved successfully!')
            } else {
                alert('Error saving modules')
            }
        })
        .catch((error) => {
            console.error('Error:', error)
        })
}

onMounted(() => {
    fetch('/setup/modules')
        .then(response => response.json())
        .then(data => {
            selectedModules.value = data.modules.map((m: FetchModule) => m.name)
            moduleOrder.value = data.modules.reduce((acc: ModuleOrder, m: FetchModule) => {
                acc[m.name] = m.order
                return acc
            }, {})
        })
})
</script>
