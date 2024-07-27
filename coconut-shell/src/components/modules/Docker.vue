<template>
    <div class="panel-module ">
        <h2>Docker</h2>
        <div class="panel-module-list">
            <ul>
                <li v-for="container in containers" :key="container.id">
                    <span :class="['status-dot', container.status === 'running' ? 'online' : 'offline']"></span>
                    {{ container.name }} - {{ container.image }} - {{ container.status }}
                    <div class="btn-group">
                        <button @click="confirmAction('start', container.id)">Start</button>
                        <button @click="confirmAction('stop', container.id)">Stop</button>
                        <button @click="confirmAction('remove', container.id)">Remove</button>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Container {
    id: string;
    name: string;
    image: string;
    status: string;
}

const containers = ref<Container[]>([])

const updateDockerContainers = async () => {
    try {
        const response = await fetch('/api/docker_containers')
        containers.value = await response.json()
    } catch (error) {
        console.error('Error fetching Docker containers:', error)
    }
}

const confirmAction = (action: string, id: string) => {
    const actionMessages: Record<string, string> = {
        start: 'start this container',
        stop: 'stop this container',
        remove: 'remove this container',
    }
    if (confirm(`Are you sure you want to ${actionMessages[action]}?`)) {
        performAction(action, id)
    }
}

const performAction = async (action: string, id: string) => {
    const urls: Record<string, string> = {
        start: '/api/docker_start',
        stop: '/api/docker_stop',
        remove: '/api/docker_remove',
    }
    try {
        const response = await fetch(urls[action], {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id }),
        })
        if (response.ok) {
            console.log(`Container ${action}ed successfully`)
            updateDockerContainers()
        } else {
            console.error(`Error ${action}ing container:`, await response.text())
        }
    } catch (error) {
        console.error(`Error ${action}ing container:`, error)
    }
}

onMounted(() => {
    updateDockerContainers()
    setInterval(updateDockerContainers, 60000)
})
</script>
