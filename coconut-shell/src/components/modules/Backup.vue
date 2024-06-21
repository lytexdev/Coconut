<template>
    <div class="panel-module">
        <h2>Backups</h2>

        <div class="backup-management">
            <p>Current backups: {{ backupCount }}</p>
            <button :class="buttonClass" :disabled="isDisabled" @click="createBackup" class="btn">{{ buttonText }}</button>
        </div>

        <ul class="backup-list">
            <li v-for="backup in backups" :key="backup">
                {{ backup }}
                <button @click="confirmDeleteBackup(backup)" class="btn btn-danger">Remove</button>
            </li>
        </ul>

        <Modal v-if="showModal" :title="'Delete Backup'" :visible="showModal" :confirmText="'Delete'"
            :cancelText="'Cancel'" @close="showModal = false" @confirm="deleteBackup">
            <p>Do you want to delete the backup: {{ backupToDelete }}?</p>
        </Modal>

        <Modal v-if="showDeleteOldestModal" :title="'Delete Oldest Backup'" :visible="showDeleteOldestModal"
            :confirmText="'Delete'" :cancelText="'Cancel'" @close="showDeleteOldestModal = false"
            @confirm="deleteOldestBackup">
            <p>Do you want to delete the oldest backup: {{ oldestBackup
                }}?</p>
        </Modal>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Modal from '../Modal.vue'

const buttonText = ref('Create Backup')
const buttonClass = ref('btn')
const isDisabled = ref(false)
const backupCount = ref(0)
const backups = ref<string[]>([])
const backupToDelete = ref<string | null>(null)
const oldestBackup = ref<string | null>(null)
const showModal = ref(false)
const showDeleteOldestModal = ref(false)

const createBackup = async () => {
    buttonText.value = 'Creating...'
    buttonClass.value = 'btn btn-danger'
    isDisabled.value = true

    try {
        const response = await fetch('/api/create_backup', { method: 'POST' })
        const data = await response.json()
        buttonText.value = 'Create Backup'
        buttonClass.value = 'btn'
        isDisabled.value = false
        if (data.oldest_backup) {
            oldestBackup.value = data.oldest_backup
            showDeleteOldestModal.value = true
        }
        await getBackupList()
        await getBackupCount()
    } catch (error) {
        console.error('Error creating backup:', error)
        buttonText.value = 'Error'
        buttonClass.value = 'btn btn-danger'
        isDisabled.value = false
    }
}

const getBackupCount = async () => {
    try {
        const response = await fetch('/api/backup_count')
        const data = await response.json()
        backupCount.value = data.count
    } catch (error) {
        console.error('Error fetching backup count:', error)
    }
}

const getBackupList = async () => {
    try {
        const response = await fetch('/api/list_backups')
        const data = await response.json()
        backups.value = data.backups
    } catch (error) {
        console.error('Error fetching backup list:', error)
    }
}

const confirmDeleteBackup = (backup: string) => {
    backupToDelete.value = backup
    showModal.value = true
}

const deleteBackup = async () => {
    try {
        const response = await fetch('/api/delete_backup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ backup_to_delete: backupToDelete.value })
        })
        const data = await response.json()
        console.log(data.message)
        backupToDelete.value = null
        await getBackupList()
        await getBackupCount()
        showModal.value = false
    } catch (error) {
        console.error('Error deleting backup:', error)
    }
}

const deleteOldestBackup = async () => {
    try {
        const response = await fetch('/api/delete_backup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ backup_to_delete: oldestBackup.value })
        })
        const data = await response.json()
        console.log(data.message)
        oldestBackup.value = null
        await getBackupList()
        await getBackupCount()
        showDeleteOldestModal.value = false
    } catch (error) {
        console.error('Error deleting oldest backup:', error)
    }
}

onMounted(() => {
    getBackupList()
    getBackupCount()
})
</script>
