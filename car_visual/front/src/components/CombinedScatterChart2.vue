<template>
  <div class="chart" ref="chart" :style="{ width: '1400px', height: '800px' }"></div>
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
      const chart = echarts.init(this.$refs.chart);
      const series = [];

      // 遍历 allCarData，根据不同的 ID 分组数据
      const idSet = new Set(this.allCarData.map(car => car.ID));
      idSet.forEach(id => {
        const data = this.allCarData.filter(car => car.ID === id).map(item => [item.X, item.Y]);
        series.push({
          name: id,
          type: 'scatter',
          symbolSize: 10, //稍微增加每个系列大小
          data: data
        });
      });

      const options = {
        backgroundColor: '#2f416d',
        grid: {
          top: '15%',
        },
        title: {
          text: 'Combined Car Coordinates',
          padding: 30,
          left: 'center',
          textStyle: {
            fontSize: 30,
            color: '#FFFFFF'
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: (params) => {
            return `${params.seriesName}<br/>X: ${params.value[0]}, Y: ${params.value[1]}`;
          }
        },
        legend: {
          data: Array.from(idSet), // 将 Set 转换为数组作为图例数据
          padding: 80,
          textStyle: { //图例文字的样式
            color: '#fff',
            fontSize: 30
          },
        },
        xAxis: {
          type: 'value',
          scale: true,
          name: 'X',
          splitLine: {
            show: false
          },
          axisLine: {
            lineStyle: {
              color: '#FFFFFF'
            }
          },
          nameTextStyle: {
            fontSize: 25
          },
          axisLabel: {
            textStyle: {
              color: '#FFFFFF',
              fontSize: 25
            }
          }
        },
        yAxis: {
          type: 'value',
          scale: true,
          name: 'Y',
          splitLine: {
            show: false
          },
          axisLine: {
            lineStyle: {
              color: '#FFFFFF'
            }
          },
          nameTextStyle: {
            fontSize: 25
          },
          axisLabel: {
            textStyle: {
              color: '#FFFFFF',
              fontSize: 25
            }
          }
        },
        series: series // 将分组后的数据添加到系列中
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
