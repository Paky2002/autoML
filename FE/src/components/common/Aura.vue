<template>
  <div class="aura-container" :class="`palette-${currentPalette}`">
    <div class="blobs">
      <svg viewBox="0 0 1200 1200">
        <g class="blob blob-1">
          <path />
        </g>
        <g class="blob blob-2">
          <path />
        </g>
        <g class="blob blob-3">
          <path />
        </g>
        <g class="blob blob-4">
          <path />
        </g>
        <g class="blob blob-1 alt">
          <path />
        </g>
        <g class="blob blob-2 alt">
          <path />
        </g>
        <g class="blob blob-3 alt">
          <path />
        </g>
        <g class="blob blob-4 alt">
          <path />
        </g>
      </svg>
    </div>
    
    <!-- Switcher opzionale -->
    <div v-if="showSwitcher" class="switcher">
      <div 
        v-for="palette in availablePalettes" 
        :key="palette"
        class="switch-button" 
        :class="`palette-${palette}`"
        @click="changePalette(palette)"
      >
        <div class="blobs mini">
          <svg viewBox="0 0 1200 1200">
            <g class="blob blob-1"><path /></g>
            <g class="blob blob-2"><path /></g>
            <g class="blob blob-3"><path /></g>
            <g class="blob blob-4"><path /></g>
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Aura',
  props: {
    palette: {
      type: Number,
      default: 3,
      validator: (value) => value >= 1 && value <= 6
    },
  watch: {
    palette(newPalette) {
      this.currentPalette = newPalette;
    }
  },
    showSwitcher: {
      type: Boolean,
      default: false
    },
    size: {
      type: String,
      default: '60vmin', // vmin = min(vw, vh)
      validator: (value) => typeof value === 'string'
    },
    width: {
      type: String,
      default: null,
      validator: (value) => value === null || typeof value === 'string'
    },
    height: {
      type: String,
      default: null,
      validator: (value) => value === null || typeof value === 'string'
    }
  },
  data() {
    return {
      currentPalette: this.palette,
      availablePalettes: [1, 2, 3, 4, 5, 6]
    }
  },
  computed: {
    containerWidth() {
      return this.width || '100%';
    },
    containerHeight() {
      return this.height || '100%';
    },
    blobsSize() {
      // Se width e height sono specificati, usa quelli, altrimenti usa size
      if (this.width && this.height) {
        return `min(${this.width}, ${this.height})`;
      }
      return this.size;
    }
  },
  methods: {
    changePalette(paletteNumber) {
      this.currentPalette = paletteNumber;
      this.$emit('palette-changed', paletteNumber);
    }
  }
}
</script>

<style scoped>
/* Le forme blob sono definite direttamente nelle keyframes */

/* Palette colori */
.aura-container,
.palette-1 {
  --bg-0: #101030;
  --bg-1: #050515;
  --blob-1: #984ddf;
  --blob-2: #4344ad;
  --blob-3: #74d9e1;
  --blob-4: #050515;
}

.palette-2 {
  --bg-0: #545454;
  --bg-1: #150513;
  --blob-1: #ff3838;
  --blob-2: #ff9d7c;
  --blob-3: #ffdda0;
  --blob-4: #fff6ea;
}

.palette-3 {
  --bg-0: #300030;
  --bg-1: #000000;
  --blob-1: #291528;
  --blob-2: #3a3e3b;
  --blob-3: #9e829c;
  --blob-4: #f0eff4;
}

.palette-4 {
  --bg-0: #ffffff;
  --bg-1: #d3f7ff;
  --blob-1: #bb74ff;
  --blob-2: #7c7dff;
  --blob-3: #a0f8ff;
  --blob-4: #ffffff;
}

.palette-5 {
  --bg-0: #968e85;
  --bg-1: #8cc084;
  --blob-1: #c1d7ae;
  --blob-2: #9eff72;
  --blob-3: #ffcab1;
  --blob-4: #ecdcb0;
}

.palette-6 {
  --bg-0: #ffffff;
  --bg-1: #4e598c;
  --blob-1: #ff8c42;
  --blob-2: #fcaf58;
  --blob-3: #f9c784;
  --blob-4: #ffffff;
}

.aura-container {
  background: var(--bg-1);
  width: v-bind(containerWidth);
  height: v-bind(containerHeight);
  min-height: 300px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: background 1000ms ease;
}

.aura-container::after {
  position: absolute;
  content: "";
  width: min(50%, 50%);
  height: min(50%, 50%);
  background: var(--bg-0);
  border-radius: 50%;
  filter: blur(10rem);
  transition: background 500ms ease;
}

.blobs {
  width: v-bind(blobsSize);
  height: v-bind(blobsSize);
  max-height: 100%;
  max-width: 100%;
}

.blobs svg {
  position: relative;
  height: 100%;
  z-index: 2;
}

.blob {
  animation: rotate 25s infinite alternate ease-in-out;
  transform-origin: 50% 50%;
  opacity: 0.7;
}

.blob path {
  animation: blob-anim-1 5s infinite alternate cubic-bezier(0.45, 0.2, 0.55, 0.8);
  transform-origin: 50% 50%;
  transform: scale(0.8);
  transition: fill 800ms ease;
}

.blob.alt {
  animation-direction: alternate-reverse;
  opacity: 0.3;
}

.blob-1 path {
  fill: var(--blob-1);
  filter: blur(1rem);
}

.blob-2 {
  animation-duration: 18s;
  animation-direction: alternate-reverse;
}

.blob-2 path {
  fill: var(--blob-2);
  animation-name: blob-anim-2;
  animation-duration: 7s;
  filter: blur(0.75rem);
  transform: scale(0.78);
}

.blob-2.alt {
  animation-direction: alternate;
}

.blob-3 {
  animation-duration: 23s;
}

.blob-3 path {
  fill: var(--blob-3);
  animation-name: blob-anim-3;
  animation-duration: 6s;
  filter: blur(0.5rem);
  transform: scale(0.76);
}

.blob-4 {
  animation-duration: 31s;
  animation-direction: alternate-reverse;
  opacity: 0.9;
}

.blob-4 path {
  fill: var(--blob-4);
  animation-name: blob-anim-4;
  animation-duration: 10s;
  filter: blur(10rem);
  transform: scale(0.5);
}

.blob-4.alt {
  animation-direction: alternate;
  opacity: 0.8;
}

/* Animazioni keyframes con forme definite direttamente */
@keyframes blob-anim-1 {
  0% { 
    d: path("M 100 600 q 0 -500, 500 -500 t 500 500 t -500 500 T 100 600 z");
  }
  30% { 
    d: path("M 100 600 q -50 -400, 500 -500 t 450 550 t -500 500 T 100 600 z");
  }
  70% { 
    d: path("M 100 600 q 0 -400, 500 -500 t 400 500 t -500 500 T 100 600 z");
  }
  100% { 
    d: path("M 150 600 q 0 -600, 500 -500 t 500 550 t -500 500 T 150 600 z");
  }
}

@keyframes blob-anim-2 {
  0% { 
    d: path("M 100 600 q 0 -400, 500 -500 t 400 500 t -500 500 T 100 600 z");
  }
  40% { 
    d: path("M 150 600 q 0 -600, 500 -500 t 500 550 t -500 500 T 150 600 z");
  }
  80% { 
    d: path("M 100 600 q -50 -400, 500 -500 t 450 550 t -500 500 T 100 600 z");
  }
  100% { 
    d: path("M 100 600 q 100 -600, 500 -500 t 400 500 t -500 500 T 100 600 z");
  }
}

@keyframes blob-anim-3 {
  0% { 
    d: path("M 100 600 q -50 -400, 500 -500 t 450 550 t -500 500 T 100 600 z");
  }
  35% { 
    d: path("M 150 600 q 0 -600, 500 -500 t 500 550 t -500 500 T 150 600 z");
  }
  75% { 
    d: path("M 100 600 q 100 -600, 500 -500 t 400 500 t -500 500 T 100 600 z");
  }
  100% { 
    d: path("M 100 600 q 0 -400, 500 -500 t 400 500 t -500 500 T 100 600 z");
  }
}

@keyframes blob-anim-4 {
  0% { 
    d: path("M 150 600 q 0 -600, 500 -500 t 500 550 t -500 500 T 150 600 z");
  }
  30% { 
    d: path("M 100 600 q 100 -600, 500 -500 t 400 500 t -500 500 T 100 600 z");
  }
  70% { 
    d: path("M 100 600 q -50 -400, 500 -500 t 450 550 t -500 500 T 100 600 z");
  }
  100% { 
    d: path("M 150 600 q 0 -600, 500 -500 t 500 550 t -500 500 T 150 600 z");
  }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Switcher stili */
.switcher {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 1rem;
  z-index: 10;
}

.switch-button {
  cursor: pointer;
  width: min(8vh, 4rem);
  height: min(8vh, 4rem);
  background: radial-gradient(var(--bg-0), var(--bg-1));
  border-radius: 0.5rem;
  backdrop-filter: blur(1rem);
  border: 1px solid rgba(120, 120, 120, 0.5);
  overflow: hidden;
  transition: all 0.3s ease;
}

.switch-button:hover {
  transform: scale(1.1);
}

.blobs.mini {
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.blobs.mini svg {
  width: 100%;
  height: 100%;
}

.blobs.mini .blob {
  animation-duration: 8s;
}

.blobs.mini .blob path {
  animation-duration: 3s;
  filter: blur(0.2rem);
}
</style>