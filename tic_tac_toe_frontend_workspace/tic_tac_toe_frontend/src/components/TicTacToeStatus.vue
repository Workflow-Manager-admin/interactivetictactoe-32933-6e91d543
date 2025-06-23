<template>
  <div class="ttt-status">
    <div v-if="!gameStarted" class="waiting-message">Waiting to start a game...</div>
    <div v-else>
      <div v-if="result" class="result-message" :class="resultClass">{{ result }}</div>
      <div v-else class="turn-message">
        Turn: <span :class="currentClass">{{ turnMsg }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue"

const props = defineProps<{
  gameStarted: boolean,
  currentPlayer?: string,
  yourSymbol?: string,
  nextTurnSymbol?: string,
  result?: string,
}>()

const turnMsg = computed(() => {
  if (!props.currentPlayer || !props.yourSymbol || !props.nextTurnSymbol) return "";
  return props.nextTurnSymbol === props.yourSymbol ? "Your Move" : `Opponent's Move`
})

const resultClass = computed(() =>
  props.result?.includes('won') ? 'accent' :
  props.result?.includes('draw') ? 'secondary' : ''
)
const currentClass = computed(() =>
  props.nextTurnSymbol === 'X' ? 'accent' : props.nextTurnSymbol === 'O' ? 'secondary' : ''
)
</script>

<style scoped>
.ttt-status {
  margin-top: 1.2rem;
  font-size: 1.25rem;
  text-align: center;
  min-height: 2.1em;
}
.result-message {
  font-weight: bold;
  font-size: 1.35rem;
}
.result-message.accent {
  color: #e74c3c;
}
.result-message.secondary {
  color: #2ecc71;
}
.turn-message .accent {
  color: #e74c3c;
  font-weight: bold;
}
.turn-message .secondary {
  color: #2ecc71;
  font-weight: bold;
}
.waiting-message {
  color: #aaa;
}
</style>
