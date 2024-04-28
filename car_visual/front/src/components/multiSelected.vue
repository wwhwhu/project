<template>
  <div class="dropdown">
    <dt @click="showDropdownF">
      <a>
        <span class="hida" v-if="!selectedValues.length">选择车辆ID...</span>
        <p class="multiSel" v-else>{{ selectedLabels }}</p>
      </a>
    </dt>
    <dd v-if="showDropdown">
      <div>
        <ul>
          <li v-for="id in optionIds" :key="id">
            <input type="checkbox" :value="id" v-model="selectedValues"
                   :disabled="selectedValues.length > 4 && !selectedValues.includes(id)"/>
            {{ id }}
          </li>
        </ul>
      </div>
    </dd>
    <button @click="confirmSelection">Confirm</button>
    <div v-if="confirmDraw" class="confirmation">
      <p>当前已经选择{{ selectedValues.length }}个ID轨迹，分别是{{ selectedLabels }}，绘图如下：</p>
      <!-- 当选择多于一个时，显示CombinedScatterChart组件 -->
      <CombinedScatterChart2 v-if="selectedValues.length > 1" :allCarData="filteredData"/>
      <!-- 否则，显示ScatterChart组件 -->
      <ScatterChart2 v-else :carData="filteredData"/>
    </div>
  </div>
</template>

<script>
import ScatterChart2 from '../components/ScatterChart2';
import CombinedScatterChart2 from '../components/CombinedScatterChart2';

export default {
  props: {
    optionIds: {
      type: Array,
      required: true
    },
    rawData: {
      type: Array,
      required: true,
    },
  },
  components: {
    ScatterChart2,
    CombinedScatterChart2
  },
  data() {
    return {
      selectedValues: [],
      showDropdown: false,
      confirmDraw: false
    };
  },
  methods: {
    confirmSelection() {
      if (this.selectedValues.length < 1) {
        alert("Please select at least one option.");
        return;
      } else if (this.selectedValues.length > 5) {
        alert("Please select at most 5 options.");
        return;
      }
      // 在这里做进一步处理，例如提交数据
      console.log("Selected Items: ", this.selectedValues);
      this.showDropdown = false; // 可以选择在选择后关闭下拉菜单
      this.confirmDraw = true;
    },
    showDropdownF() {
      this.showDropdown = !this.showDropdown
      this.confirmDraw = false
      console.log(this.optionIds)
    }
  },
  computed: {
    selectedLabels() {
        return this.optionIds
            .filter(id => this.selectedValues.includes(id))
            .join(', '); // 以逗号分隔
    },
    filteredData() {
      return this.rawData.filter(dataItem => this.selectedValues.includes(dataItem.ID));
    },
  },
};
</script>

<style scoped>
body {
  font: normal 14px/100% "Andale Mono", AndaleMono, monospace;
  color: #fff;
  padding: 50px;
  width: 300px;
  margin: 0 auto;
  background-color: #374954;
}

.dropdown {
  margin-top: 20px;
}

.hida {
  margin: 0 auto;
}

a {
  color: #fff;
}

.confirmation p {
  font-size: 36px; /* 设置字体大小 */
  font-family: Arial;
  color: #424ed2; /* 设置字体颜色 */
  font-weight: bold; /* 设置字体粗细，400 相当于 normal，700 相当于 bold */
}

.dropdown dd,
.dropdown dt {
  margin: 0px;
  padding: 0px;
}

.dropdown ul {
  margin: -1px 0 0 0;
}

.dropdown dd {
  position: relative;
}

.dropdown a,
.dropdown a:visited {
  color: #fff;
  text-decoration: none;
  outline: none;
  font-size: 12px;
}

.dropdown dt a {
  background-color: #4F6877;
  display: block;
  padding: 8px 20px 5px 10px;
  min-height: 25px;
  line-height: 24px;
  overflow: hidden;
  border: 0;
  width: 302px;
}

.dropdown dt a span,
.multiSel span {
  cursor: pointer;
  display: inline-block;
  padding: 0 3px 2px 0;
  text-align: center;
  height: 30px
}

.dropdown dd ul {
  background-color: #395e75;
  border: 0;
  color: #fff;
  /*display: none;*/
  margin: 0 auto;
  padding: 2px 15px 2px 5px;
  /*position: absolute;*/
  top: 2px;
  width: 302px;
  list-style: none;
  height: 100px;
  overflow: auto;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
}

.dropdown span.value {

}

.dropdown dd ul li a {
  padding: 5px;
  display: block;
}

.dropdown dd ul li a:hover {
  background-color: #fff;
}

.dropdown dt {
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
}

button {
  background-color: #6BBE92;
  width: 302px;
  border: 0;
  padding: 10px 0;
  margin: 5px 0;
  text-align: center;
  color: #fff;
  font-weight: bold;
}
</style>