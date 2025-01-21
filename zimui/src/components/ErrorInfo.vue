<script setup lang="ts">
import dead_kiwix from '../assets/dead_kiwix.png'
</script>

<template>
  <div class="page">
    <div class="container">
      <div class="content">
        <p class="text"><slot></slot></p>
      </div>
      <div class="image-container">
        <img :src="dead_kiwix" class="image" alt="error image" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px;
  text-align: center;
}
.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 40px;
  margin: 60px 0;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 40px;
}
.content {
  flex: 1;
  text-align: left;
}
.text {
  color: #222;
  margin: 10px 0;
  max-width: 500px;
  line-height: 1.6;
  font-size: 18px;
}
.image-container {
  flex: 1;
  display: flex;
  justify-content: center;
}

@media (max-width: 768px) {
  .container {
    flex-direction: column;
    text-align: center;
  }

  .text {
    margin: 20px auto;
    font-size: 16px;
  }

  .image {
    width: 300px;
  }
}
</style>
