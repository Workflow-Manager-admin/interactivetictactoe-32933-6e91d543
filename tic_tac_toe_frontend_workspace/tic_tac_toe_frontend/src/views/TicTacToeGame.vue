<script setup lang="ts">
import { ref } from 'vue'
import TicTacToeBoard from '../components/TicTacToeBoard.vue'
import TicTacToeControls from '../components/TicTacToeControls.vue'
import TicTacToeStatus from '../components/TicTacToeStatus.vue'

// BACKEND API CONFIG (placeholder URL for now)
// const API_BASE = import.meta.env.VITE_TTT_BACKEND_URL || 'http://localhost:3001/api'

const playerName = ref<string>('')
const gameId = ref<string>('')
const yourSymbol = ref<string>('X')
const board = ref<string[][]>([['', '', ''], ['', '', ''], ['', '', '']])
const nextTurnSymbol = ref<string>('X')
const gameStarted = ref(false)
const gameOver = ref(false)
const result = ref<string>('')

// PUBLIC_INTERFACE
async function createGame() {
  // TODO: Replace with actual backend call
  // const res = await fetch(`${API_BASE}/games`, { method: 'POST' })
  // ...
  playerName.value = 'Player 1'
  yourSymbol.value = 'X'
  gameId.value = Math.random().toString(36).slice(2, 7).toUpperCase()
  resetBoard()
  gameStarted.value = true
  nextTurnSymbol.value = 'X'
  gameOver.value = false
  result.value = ''
}

// PUBLIC_INTERFACE
async function joinGame(joinCode: string) {
  // TODO: Replace with backend join
  playerName.value = 'Player 2'
  yourSymbol.value = 'O'
  gameId.value = joinCode
  resetBoard()
  gameStarted.value = true
  nextTurnSymbol.value = 'X'
  gameOver.value = false
  result.value = ''
}

function resetBoard() {
  board.value = [['', '', ''], ['', '', ''], ['', '', '']]
}

function getWinner() {
  const b = board.value
  const winPatterns = [
    [[0,0],[0,1],[0,2]],
    [[1,0],[1,1],[1,2]],
    [[2,0],[2,1],[2,2]],
    [[0,0],[1,0],[2,0]],
    [[0,1],[1,1],[2,1]],
    [[0,2],[1,2],[2,2]],
    [[0,0],[1,1],[2,2]],
    [[0,2],[1,1],[2,0]],
  ]
  for (const pattern of winPatterns) {
    const [a, b1, c] = pattern
    const v1 = b[a[0]][a[1]]
    if (v1 && v1 === b[b1[0]][b1[1]] && v1 === b[c[0]][c[1]]) {
      return v1
    }
  }
  return null
}

// PUBLIC_INTERFACE
function handleMove(row: number, col: number) {
  if (!gameStarted.value || gameOver.value) return
  if (board.value[row][col]) return
  if (yourSymbol.value !== nextTurnSymbol.value) return
  board.value[row][col] = nextTurnSymbol.value
  const winner = getWinner()
  if (winner) {
    gameOver.value = true
    result.value = winner === yourSymbol.value ? 'You won!' : 'Opponent won!'
  } else if (board.value.flat().every(cell => cell)) {
    gameOver.value = true
    result.value = 'It\'s a draw!'
  } else {
    nextTurnSymbol.value = nextTurnSymbol.value === 'X' ? 'O' : 'X'
  }
}
</script>

<template>
  <div class="ttt-game-root">
    <TicTacToeControls
      :playerName="playerName"
      :gameId="gameId"
      @new-game="createGame"
      @join-game="joinGame"
    />
    <div class="game-board-container">
      <TicTacToeBoard
        :board="board"
        :currentPlayer="yourSymbol"
        :gameOver="gameOver"
        @move="handleMove"
      />
    </div>
    <TicTacToeStatus
      :gameStarted="gameStarted"
      :currentPlayer="playerName"
      :yourSymbol="yourSymbol"
      :nextTurnSymbol="nextTurnSymbol"
      :result="result"
    />
  </div>
</template>

<style scoped>
.ttt-game-root {
  max-width: 420px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: flex-start;
  padding: 2rem 1rem 3rem 1rem;
  background: var(--color-background-soft);
  border-radius: 18px;
  box-shadow: 0 4px 28px 2px rgba(52,152,219,0.13);
  min-height: 78vh;
  margin-top: 2rem;
}
.game-board-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1rem;
}
@media (max-width: 600px) {
  .ttt-game-root {
    padding: 0.7rem 0.2rem 2rem 0.2rem;
    margin-top: 0.6rem;
    min-height: 0;
  }
}
</style>
