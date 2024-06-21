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

        <Modal v-if="showModal" :title="'Delete Backup'" :visible="showModal" :confirmText="'Delete'" :cancelText="'Cancel'"
            @close="showModal = false" @confirm="deleteBackup">
            <p>Do you want to delete the backup: {{ backupToDelete }}?</p>
        </Modal>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Modal from '../Modal.vue'

const buttonText = ref('Create Backup')
const buttonClass = ref('btn')
const isDisabled = ref(false)
const backupCount = ref(0)
const backups = ref([])
const backupToDelete = ref(null)
const showModal = ref(false)

const createBackup = () => {
    buttonText.value = 'Creating...'
    buttonClass.value = 'btn btn-danger'
    isDisabled.value = true

    fetch('/api/create_backup', {
        method: 'POST'
    })
        .then(response => response.json())
        .then(data => {
            buttonText.value = 'Create Backup'
            buttonClass.value = 'btn'
            isDisabled.value = false
            if (data.oldest_backup) {
                backupToDelete.value = data.oldest_backup
                showModal.value = true
            }
            getBackupList() 
            getBackupCount()
        })
        .catch(error => {
            console.error('Error creating backup:', error)
            buttonText.value = 'Error'
            buttonClass.value = 'btn btn-danger'
            isDisabled.value = false
        })
}

const getBackupCount = () => {
    fetch('/api/backup_count')
        .then(response => response.json())
        .then(data => {
            backupCount.value = data.count
        })
        .catch(error => {
            console.error('Error fetching backup count:', error)
        })
}

const getBackupList = () => {
    fetch('/api/list_backups')
        .then(response => response.json())
        .then(data => {
            backups.value = data.backups
        })
        .catch(error => {
            console.error('Error fetching backup list:', error)
        })
}

const confirmDeleteBackup = (backup) => {
    backupToDelete.value = backup
    showModal.value = true
}

const deleteBackup = () => {
    fetch('/api/delete_backup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ backup_to_delete: backupToDelete.value })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message)
            backupToDelete.value = null
            getBackupList()
            getBackupCount()
            showModal.value = false
        })
        .catch(error => {
            console.error('Error deleting backup:', error)
        })
}

onMounted(() => {
    getBackupList()
    getBackupCount()
})
</script>
