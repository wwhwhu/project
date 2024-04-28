<template>
  <div>
    <h1 style="font-size: 48px; font-family: Arial, sans-serif; font-weight: bolder; color: #424ed2;">数&nbsp;&nbsp;据&nbsp;&nbsp;可&nbsp;&nbsp;视&nbsp;&nbsp;化</h1>
    <!-- 显示数据列表 -->
    <div v-if="slicedData.length > 0">
      <h2>示例数据 (最多显示20条)</h2>
      <table class="rwd-table">
        <tr>
          <th>ID</th>
          <th>X</th>
          <th>Y</th>
          <th v-if="hasSpeed">Speed</th>
          <th v-if="hasAcceleration">Acceleration</th>
        </tr>
        <tr v-for="(item, index) in slicedData" :key="index">
          <td data-th="ID">{{ item.ID }}</td>
          <td data-th="X">{{ item.X }}</td>
          <td data-th="Y">{{ item.Y }}</td>
          <td v-if="item.Speed" data-th="Speed">{{ item.Speed }}</td>
          <td v-if="item.Acceleration" data-th="Acceleration">{{ item.Acceleration }}</td>
        </tr>
      </table>
    </div>
    <!-- 显示不同 ID 的数量 -->
    <div v-if="uniqueIdsCount" class="text">
      <p>不同ID的数量: {{ uniqueIdsCount }}</p>
      <p>选择图中要显示的ID轨迹 (1 到 {{ seletedNum }}) 个: </p>
      <br/>
    </div>
    <v-multiSelected :option-ids="optionIds" :rawData="rawData"></v-multiSelected>
  </div>
</template>

<script>
import multiSelected from "@/components/multiSelected";

export default {
  props: {
    rawData: {
      type: Array,
      required: true,
    },
  },
  watch: {
    // 观察 rawData 的变化
    rawData: {
      handler() {
        this.initializeSelectedIds();
      },
      deep: true // 如果你需要深度观察对象内部变化，需要设置这个属性为 true
    }
  },
  components: {
    'v-multiSelected': multiSelected
  },
  data() {
    return {
      optionIds: [],  // 选中的 ID
    };
  },
  computed: {
    // 数组切片，最多显示20条数据
    slicedData() {
      return this.rawData.slice(0, 20);
    },
    // 获取不同 ID 的数量
    uniqueIdsCount() {
      const uniqueIds = new Set(this.rawData.map(item => item.ID));
      return uniqueIds.size;
    },
    seletedNum(){
      // 返回uniqueIdsCount()与5大的那个
      const uniqueIds = new Set(this.rawData.map(item => item.ID));
      return Math.min(uniqueIds.size, 5);
    },
    hasSpeed() {
      return this.rawData.some(item => 'Speed' in item);
    },
    hasAcceleration() {
      return this.rawData.some(item => 'Acceleration' in item);
    },
  },
  methods: {
    initializeSelectedIds() {
      const uniqueIds = new Set(this.rawData.map(item => item.ID));
      this.optionIds = Array.from(uniqueIds);
    }
  },
};
</script>

<style scoped>

p {
  font-size: 36px; /* 设置字体大小 */
  font-family: Arial;
  color: #424ed2; /* 设置字体颜色 */
  font-weight: bold; /* 设置字体粗细，400 相当于 normal，700 相当于 bold */
}

h2{
  font-size: 36px; /* 设置字体大小 */
  font-family: Arial;
  color: #424ed2; /* 设置字体颜色 */
  font-weight: bold; /* 设置字体粗细，400 相当于 normal，700 相当于 bold */
}

.text{
  margin-top: 50px;
  padding: 20px;
}

.rwd-table {
  margin: 1em auto;
  min-width: 300px; /* adjust to your needs */
  background: #34495E;
  color: #fff;
  border-radius: .4em;
  overflow: hidden;
}

.rwd-table tr {
  border-top: 1px solid #ddd;
  border-bottom: 1px solid #ddd;
  border-color: #2f416d;
}

.rwd-table th {
  display: none; /* for accessibility, use a visually hidden method here instead! Thanks, reddit! */
}

.rwd-table td {
  display: block;
}

.rwd-table td:first-child {
  padding-top: .5em;
}

.rwd-table td:last-child {
  padding-bottom: .5em;
}

.rwd-table td:before {
  content: attr(data-th)": ";
  font-weight: bold;
  width: 6.5em; /* magic number :( adjust according to your own content */
  display: inline-block;
}

@media (min-width: 480px) { /* Adjust this breakpoint to your needs */
  .rwd-table td:before {
    display: none;
  }
}

@media (min-width: 480px) {
  .rwd-table th, .rwd-table td {
    display: table-cell;
    padding: .25em .5em;
  }

  .rwd-table th:first-child, .rwd-table td:first-child {
    padding-left: 0;
  }

  .rwd-table th:last-child, .rwd-table td:last-child {
    padding-right: 0;
  }
}

/* Presentational styling, this is not part of the responsive table solution */
body {
  padding: 0 2em;
  font-family: 'Montserrat', sans-serif;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  color: #444;
  background: #eee;
}

h1 {
  font-weight: normal;
  letter-spacing: -1px;
  color: #34495E;
}

.rwd-table th, .rwd-table td:before {
  color: #dd5;
}
</style>

