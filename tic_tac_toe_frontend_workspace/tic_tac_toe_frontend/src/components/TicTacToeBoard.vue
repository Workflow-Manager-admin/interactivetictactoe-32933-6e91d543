<template>
  <div class="tic-tac-toe-board">
    <div
      v-for="(row, rIdx) in 3"
      :key="rIdx"
      class="ttt-row"
    >
      <button
        v-for="(col, cIdx) in 3"
        :key="cIdx"
        class="ttt-cell"
        :class="{ 'accent': board[rIdx][cIdx] === 'X', 'secondary': board[rIdx][cIdx] === 'O' }"
        :disabled="isCellDisabled(rIdx, cIdx)"
        @click="makeMove(rIdx, cIdx)"
      >
        {{ board[rIdx][cIdx] }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

const props = defineProps<{
  board: string[][]
  currentPlayer: string
  gameOver: boolean
}>()

const emits = defineEmits<{
  (e: 'move', row: number, col: number): void
}>()

// PUBLIC_INTERFACE
function makeMove(row: number, col: number) {
  emits('move', row, col)
}

// PUBLIC_INTERFACE
function isCellDisabled(row: number, col: number) {
  return props.board[row][col] !== '' || props.gameOver
}
</script>

<style scoped>
.tic-tac-toe-board {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.ttt-row {
  display: flex;
}

.ttt-cell {
  width: 80px;
  height: 80px;
  font-size: 2rem;
  font-weight: bold;
  margin: 4px;
  border: 2px solid var(--color-border);
  background: var(--color-background-soft);
  color: var(--color-heading);
  border-radius: 12px;
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
  cursor: pointer;
}
.ttt-cell.accent {
  color: #e74c3c;
}
.ttt-cell.secondary {
  color: #2ecc71;
}
.ttt-cell:disabled {
  background: #f2f2f2;
  color: #bbb;
  cursor: not-allowed;
}
@media (max-width: 600px) {
  .ttt-cell {
    width: 48px;
    height: 48px;
    font-size: 1.3rem;
  }
}
</style>
