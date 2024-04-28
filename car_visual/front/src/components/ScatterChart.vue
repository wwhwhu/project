<template>
  <div class="chart" ref="chart" :style="{ width: '600px', height: '400px' }"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'ScatterChart',
  props: {
    carData: Array
  },
  mounted() {
    this.initChart();
  },
  methods: {
    initChart() {
      const chart = echarts.init(this.$refs.chart);
      const options = {
        title: {
          text: `Car Coordinates for ${this.carData[0]?.name || 'Unknown'}`
        },
        tooltip: {
          trigger: 'item',
          formatter: (params) => {
            return `X: ${params.value[0]}<br/>Y: ${params.value[1]}`;
          }
        },
        xAxis: {
          type: 'value',
          scale: true,
          name: 'X',
          splitLine: {
            show: false // 不显示x轴的分割线
          }
        },
        yAxis: {
          type: 'value',
          scale: true,
          name: 'Y',
          splitLine: {
            show: false // 不显示y轴的分割线
          }
        },
        series: [{
          symbolSize: 20,
          data: this.carData.map(item => [item.x, item.y]),
          type: 'scatter'
        }]
      };
      chart.setOption(options);
    }
  }
}
</script>

<style scoped>
.chart {
  margin-top: 20px;
}
</style>
