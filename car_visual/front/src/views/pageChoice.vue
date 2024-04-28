<template>
  <div class="login-box">
    <button class="button-effect" @click="goToAPage">远程数据库车辆轨迹可视化</button>
    <button class="button-effect" @click="goToBPage">自上传文件车辆轨迹可视化</button>
  </div>
</template>

<script>
export default {
  name: "pageChoice",
  methods: {
    goToAPage() {
      this.$router.push('/carPage');
    },
    goToBPage() {
      this.$router.push('/uploadVisual');
    }
  }
};
</script>

<style>
.login-box {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.button-effect {
  display: block; /* 使按钮单独占据一行 */
  width: 80%; /* 或者任何你想要的宽度 */
  margin: 30px auto 30px auto; /* 这将在按钮的上方和下方各添加30px的间距，总共60px */
  padding: 10px 20px;
  color: #03e9f4;
  font-size: 16px;
  text-decoration: none;
  text-transform: uppercase;
  overflow: hidden;
  transition: .5s;
  letter-spacing: 4px;
  cursor: pointer;
  background: rgba(0, 0, 128, 0.8);
  border: none;
  border-radius: 10px;
  box-shadow: 0 15px 25px rgba(0, 0, 0, .6);
}

.button-effect:hover {
  background: #03e9f4;
  color: #fff;
  border-radius: 5px;
  box-shadow: 0 0 5px #03e9f4,
  0 0 25px #03e9f4,
  0 0 50px #03e9f4,
  0 0 100px #03e9f4;
}

.button-effect span {
  position: absolute;
  display: block;
}

.button-effect span:nth-child(1) {
  top: 0;
  left: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #03e9f4);
  animation: btn-anim1 1s linear infinite;
}

/* Repeat other span styles and keyframes here... */

@keyframes btn-anim1 {
  0% {
    left: -100%;
  }
  50%, 100% {
    left: 100%;
  }
}

/* Repeat other keyframes here... */
</style>
