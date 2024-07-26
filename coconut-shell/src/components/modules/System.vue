<template>
    <div class="panel-module">
        <h2>System Information</h2>

        <div class="panel-module-grid">
            <div>
                <p>Uptime: {{ uptime }}</p>
                <p>CPU Usage: {{ cpuUsage }}%</p>
            </div>
            <div>
                <h3>Random-Access Memory</h3>
                <p>Usage: {{ ramUsage }}</p>
                <p>Total: {{ ramTotal }}</p>
                <p>Available: {{ ramAvailable }}</p>
                <p>Used: {{ ramUsed }}</p>
            </div>
            <div>
                <h3>Swap</h3>
                <p>Total: {{ swapTotal }}</p>
                <p>Used: {{ swapUsed }}</p>
                <p>Free: {{ swapFree }}</p>
            </div>
            <div>
                <h3>Disk</h3>
                <p>Usage: {{ diskPercent }}%</p>
                <p>Storage: {{ diskUsed }} / {{ diskTotal }}</p>
                <p>Total Read: {{ diskRead }}</p>
                <p>Total Written: {{ diskWrite }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
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

const updateSystemInfo = () => {
    fetch('/api/system_info')
        .then((response) => response.json())
        .then((data) => {
            cpuUsage.value = data.cpu_usage
            ramUsage.value = data.ram_percent + '%'
            ramTotal.value = data.ram_total
            ramAvailable.value = data.ram_available
            ramUsed.value = data.ram_used
            swapTotal.value = data.swap_total
            swapUsed.value = data.swap_used
            swapFree.value = data.swap_free
            diskPercent.value = data.disk_percent + '%'
            diskTotal.value = data.disk_total
            diskUsed.value = data.disk_used
            diskRead.value = data.disk_read
            diskWrite.value = data.disk_write
            uptime.value = data.uptime
        })
        .catch((error) => console.error('Error fetching system info:', error))
}

onMounted(() => {
    updateSystemInfo()
    setInterval(updateSystemInfo, 3000)
})
</script>