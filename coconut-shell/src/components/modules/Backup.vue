<template>
    <div class="panel-module">
        <h2>Backups</h2>

        <p>Current backups: {{ backupCount }}</p>
        <button :class="buttonClass" :disabled="isDisabled" @click="createBackup" class="btn">{{ buttonText }}</button>

        <Modal v-if="showModal" :title="'Delete Backup'" :visible="showModal" :confirmText="'Delete'"
            :cancelText="'Cancel'" @close="showModal = false" @confirm="deleteBackup">
            <p>Do you want to delete the oldest backup: {{ oldestBackup }}?</p>
        </Modal>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Modal from './Modal.vue'

const buttonText = ref('Create Backup')
const buttonClass = ref('btn')
const isDisabled = ref(false)
const backupCount = ref(0)
const oldestBackup = ref(null)
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
                oldestBackup.value = data.oldest_backup
                showModal.value = true
            }
            getBackupCount() // Update backup count after creation
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

const deleteBackup = () => {
    fetch('/api/delete_backup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ backup_to_delete: oldestBackup.value })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message)
            oldestBackup.value = null
            getBackupCount()
            showModal.value = false
        })
        .catch(error => {
            console.error('Error deleting backup:', error)
        })
}

onMounted(() => {
    getBackupCount()
})
</script>
