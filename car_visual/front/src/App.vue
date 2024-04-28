<template>
  <div id="app">
    <div class="header">
      <div class="bg-blue-500 text-white text-center py-4">
        <div class="flex justify-between container mx-auto">
          <a href="/login" class="text-white uppercase">首页</a>
          <a href="#" class="text-white uppercase">关于</a>
          <a href="#" class="text-white uppercase">联系方式</a>
        </div>
      </div>
    </div>
    <div class="main">
      <router-view></router-view>
    </div>
    <div class="footer">
      <div class="bg-gray-800 text-white text-center py-4">
        © 2024 Car Data Visualization. All rights reserved.<br>
        Powered by Vue & Element UI | Data provided by XYZ Corporation
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  height: 100%;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.header,
.main,
.footer {
  width: 100%;
  text-align: center;
  color: #fff;
}

.header {
  background-color: rgb(185, 143, 224);
}

.main {
  /*background-color: rgb(210, 155, 185);*/
  /* 设置背景图片 */
  background-image: url('./assets/img.png');
  /* 背景图垂直、水平均居中 */
  background-position: center center;
  /* 背景图不平铺 */
  background-repeat: no-repeat;
  /* 当内容高度大于图片高度时，背景图像的位置相对于viewport固定 */
  background-attachment: fixed;
  /* 让背景图基于容器大小伸缩 */
  background-size: cover;
  /* 设置背景颜色，背景图加载过程中会显示背景色 */
  background-color: #bee6e8;
  min-height: calc(100vh - 60px); /* 160px 是 header 和 footer 的高度之和 */
}

.footer {
  background-color: rgb(151, 201, 184);
}
</style>
