<template>
    <div class="modal-overlay" v-if="visible">
        <div class="modal-content">
            <div class="modal-header">
                <h3>{{ title }}</h3>
                <button @click="closeModal" class="modal-close">&times;</button>
            </div>
            <div class="modal-body">
                <slot></slot>
            </div>
            <div class="modal-footer">
                <button @click="confirmAction" class="btn">{{ confirmText }}</button>
                <button @click="closeModal" class="btn">{{ cancelText }}</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
    title: String,
    visible: Boolean,
    confirmText: {
        type: String,
        default: 'Yes'
    },
    cancelText: {
        type: String,
        default: 'Cancel'
    }
})

const emit = defineEmits(['close', 'confirm'])

const closeModal = () => {
    emit('close')
}

const confirmAction = () => {
    emit('confirm')
}
</script>