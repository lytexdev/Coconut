<template>
    <div class="panel-module system-info">
        <h2>System Information</h2>
        <div class="panel-module-grid">
            <div>
                <p>Uptime: {{ uptime }}</p>
                <p>CPU Usage: {{ cpuUsage }}%</p>
            </div>
            <div>
                <p>RAM Usage: {{ ramUsage }}</p>
                <p>RAM Total: {{ ramTotal }}</p>
                <p>RAM Available: {{ ramAvailable }}</p>
                <p>RAM Used: {{ ramUsed }}</p>
            </div>
            <div>
                <p>Swap Total: {{ swapTotal }}</p>
                <p>Swap Used: {{ swapUsed }}</p>
                <p>Swap Free: {{ swapFree }}</p>
            </div>
            <div>
                <p>Disk Usage: {{ diskPercent }}%</p>
                <p>Disk Storage: {{ diskUsed }} / {{ diskTotal }}</p>
                <p>Disk Read: {{ diskRead }}</p>
                <p>Disk Write: {{ diskWrite }}</p>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const cpuUsage = ref('...')
const ramUsage = ref('...')
const ramTotal = ref('...')
const ramAvailable = ref('...')
const ramUsed = ref('...')
const swapTotal = ref('...')
const swapUsed = ref('...')
const swapFree = ref('...')
const diskPercent = ref('...')
const diskTotal = ref('...')
const diskUsed = ref('...')
const diskRead = ref('...')
const diskWrite = ref('...')
const uptime = ref('...')

const updateSystemInfo = async () => {
    try {
        const response = await fetch('/api/system_info')
        const data = await response.json()
        cpuUsage.value = data.cpu_usage
        ramUsage.value = data.ram_percent + '%'
        ramTotal.value = data.ram_total
        ramAvailable.value = data.ram_available
        ramUsed.value = data.ram_used
        swapTotal.value = data.swap_total
        swapUsed.value = data.swap_used
        swapFree.value = data.swap_free
        diskPercent.value = data.disk_percent
        diskTotal.value = data.disk_total
        diskUsed.value = data.disk_used
        diskRead.value = data.disk_read
        diskWrite.value = data.disk_write
        uptime.value = data.uptime
    } catch (error) {
        console.error('Error fetching system info:', error)
    }
}

onMounted(() => {
    updateSystemInfo()
    setInterval(updateSystemInfo, 10000)
})
</script>
