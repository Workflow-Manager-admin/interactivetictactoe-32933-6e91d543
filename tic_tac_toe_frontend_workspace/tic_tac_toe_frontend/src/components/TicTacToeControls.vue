<template>
  <div class="ttt-controls">
    <form @submit.prevent="newGame" class="ttt-form">
      <button type="submit" class="primary-btn">New Game</button>
    </form>
    <form @submit.prevent="joinGame" class="ttt-form">
      <input
        v-model="joinCode"
        placeholder="Enter Game Code"
        maxlength="8"
        class="gamecode-input"
      />
      <button type="submit" class="secondary-btn">Join Game</button>
    </form>
    <div v-if="playerName" class="user-info">
      <span><strong>Player:</strong> {{ playerName }}</span>
      <span v-if="gameId"><strong>Game:</strong> {{ gameId }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { defineProps, defineEmits } from 'vue'

defineProps<{
  playerName?: string,
  gameId?: string,
}>()

const emits = defineEmits<{
  (e: 'new-game'): void
  (e: 'join-game', joinCode: string): void
}>()

const joinCode = ref('')

// PUBLIC_INTERFACE
function newGame() {
  emits('new-game')
}

// PUBLIC_INTERFACE
function joinGame() {
  if (joinCode.value.trim()) {
    emits('join-game', joinCode.value.trim())
    joinCode.value = ''
  }
}
</script>

<style scoped>
.ttt-controls {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 0.7rem;
}
.ttt-form {
  display: flex;
  gap: 0.5rem;
  margin: 0.2rem 0;
}
.primary-btn {
  background: #3498db;
  color: #fff;
  border: 0;
  border-radius: 6px;
  padding: 0.45rem 1.1rem;
  font-size: 1rem;
  cursor: pointer;
}
.secondary-btn {
  background: #2ecc71;
  color: #fff;
  border: 0;
  border-radius: 6px;
  padding: 0.45rem 1.1rem;
  font-size: 1rem;
  cursor: pointer;
}
.gamecode-input {
  border: 1px solid #bbb;
  border-radius: 5px;
  padding: 0.35rem 0.7rem;
  font-size: 1rem;
  min-width: 116px;
}
.user-info {
  font-size: 1.08rem;
  margin-top: 0.5rem;
  color: var(--color-heading);
  display: flex;
  gap: 1.3rem;
}
</style>
