<template>
    <div class="panel-module system-info">
        <h2>System Information</h2>
        <p>CPU Usage: {{ cpuUsage }}%</p>
        <p>RAM Usage: {{ ramUsage }}%</p>
        <p>Disk Usage: {{ diskUsage }}</p>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const cpuUsage = ref('Loading...')
const ramUsage = ref('Loading...')
const diskUsage = ref('Loading...')

const updateSystemInfo = () => {
    fetch('/api/system_info')
        .then((response) => response.json())
        .then((data) => {
            cpuUsage.value = data.cpu_usage
            ramUsage.value = data.ram_usage
            diskUsage.value = data.disk_used
        })
        .catch((error) => console.error('Error fetching system info:', error))
}

onMounted(() => {
    updateSystemInfo()
    setInterval(updateSystemInfo, 2000)
})
</script>