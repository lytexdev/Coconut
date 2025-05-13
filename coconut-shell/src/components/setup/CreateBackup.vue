<template>
    <div class="create-backup">
        <form @submit.prevent="createBackup" class="create-backup-form">
            <div>
                <label for="name">Backup Name:</label>
                <input type="text" v-model="name" id="name" required />
            </div>
            <div>
                <label for="description">Description:</label>
                <input type="text" v-model="description" id="description" />
            </div>
            <div>
                <label for="backupPath">Source Path:</label>
                <input type="text" v-model="backupPath" id="backupPath" required />
            </div>
            <div>
                <label for="destinationPath">Destination Path:</label>
                <input type="text" v-model="destinationPath" id="destinationPath" required />
            </div>
            <div>
                <label for="excludedPaths">Excluded Paths (comma-separated):</label>
                <input type="text" v-model="excludedPaths" id="excludedPaths" />
            </div>
            <div>
                <label for="schedule">Backup Schedule (cron format):</label>
                <input type="text" v-model="schedule" id="schedule" />
            </div>
            <div>
                <label for="maxBackups">Max Backups:</label>
                <input type="number" v-model.number="maxBackups" id="maxBackups" min="1" />
            </div>
            <div style="display: flex;">
                <label for="enabled">Active:</label>
                <input type="checkbox" v-model="enabled" id="enabled" />
            </div>
            <button type="submit" class="btn">Create Backup</button>
        </form>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getCsrfToken } from '@/csrf'

const name = ref('')
const description = ref('')
const backupPath = ref('')
const destinationPath = ref('')
const excludedPaths = ref('')
const schedule = ref('')
const maxBackups = ref(5)
const enabled = ref(true)

const createBackup = async () => {
    try {
        const token = await getCsrfToken()

        const response = await fetch('/setup/create-backup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token,
            },
            body: JSON.stringify({
                name: name.value,
                description: description.value,
                backupPath: backupPath.value,
                destinationPath: destinationPath.value,
                excludedPaths: excludedPaths.value,
                schedule: schedule.value,
                maxBackups: maxBackups.value,
                enabled: enabled.value
            }),
        })

        const data = await response.json()
        if (data.success) {
            alert(`Backup ${name.value} created successfully!`)
            fetchBackups()
        } else {
            alert('Error: ' + data.message)
        }
    } catch (error) {
        console.error('Error creating backup:', error)
    }
}
</script>
