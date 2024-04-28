<template>
  <div class="chart" ref="chart" :style="{ width: '1300px', height: '750px' }"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'ScatterChart2',
  props: {
    carData: Array
  },
  mounted() {
    this.initChart();
  },
  methods: {
    initChart() {
      console.log('Car Data Array:', this.carData);
      const chart = echarts.init(this.$refs.chart);
      const options = {
        backgroundColor: '#2f416d', // 设置背景色为白色
        grid: {
          top: '15%',
        },
        title: {
          text: `Car Coordinates for ID ${this.carData[0]?.ID || 'Unknown'}`,
          padding: 30,
          left: 'left', // 设置标题居中对齐
          textStyle: {
            // 设置标题文字大小
            fontSize: 30,
            color: '#FFFFFF'
          }
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
          },
          // 设置坐标轴颜色和字体
          axisLine: {
            lineStyle: {
              color: '#FFFFFF' // 轴线颜色
            }
          },
          nameTextStyle :{
            fontSize: 25
          },
          axisLabel: {
            textStyle: {
              color: '#FFFFFF', // 标签字体颜色
              fontSize: 25 // 标签字体大小
            }
          }
        },
        yAxis: {
          type: 'value',
          scale: true,
          name: 'Y',
          splitLine: {
            show: false // 不显示y轴的分割线
          },
          nameTextStyle :{
            fontSize: 25
          },
          // 设置坐标轴颜色和字体
          axisLine: {
            lineStyle: {
              color: '#FFFFFF' // 轴线颜色
            },
          },
          axisLabel: {
            textStyle: {
              color: '#FFFFFF', // 标签字体颜色
              fontSize: 25 // 标签字体大小
            },
            fontSize: 25
          }
        },
        series: [{
          symbolSize: 15,
          name: this.carData.map(item => [item.ID]),
          data: this.carData.map(item => [item.X, item.Y]),
          type: 'scatter',
          itemStyle: {
            color: '#dd5' // 数据点颜色
          }
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
  border-radius: 500px;
  margin-bottom: 100px;
}
</style>
