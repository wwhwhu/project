<template>
  <div class="chart" ref="chart" :style="{ width: '1400px', height: '600px' }"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'CombinedScatterChart',
  props: {
    allCarData: Array
  },
  mounted() {
    this.$nextTick(()=>{
      this.initChart()
    })
    // this.initChart();
  },
  methods: {
    initChart() {
      console.log('Car Data Array:', this.allCarData);
      const chart = echarts.init(this.$refs.chart);
      const options = {
        // 配置图片上方白边宽
        backgroundColor: '#fff',
        grid: {
          top: '15%',
        },
        title: {
          text: 'Combined Car Coordinates',
          padding: 30
        },
        tooltip: {
          trigger: 'item',
          formatter: (params) => {
            return `${params.seriesName}<br/>X: ${params.value[0]}, Y: ${params.value[1]}`;
          }
        },
        legend: {
          data: this.allCarData.map(car => car.name),
          padding: 30
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
        series: this.allCarData.map((car, index) => ({
          name: car.name,
          type: 'scatter',
          symbolSize: 10 + index * 5, // 稍微增加每个系列的符号大小
          data: car.data.map(item => [item.x, item.y])
        }))
      };
      console.log(options)
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
