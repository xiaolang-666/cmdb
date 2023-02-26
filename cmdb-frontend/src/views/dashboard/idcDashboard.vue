<template>
  <div ref="idcChart" style="width: 50%; height: 500px;"></div>
</template>

<script>
  import * as echarts from 'echarts';
  export default {
    data() {
      return {
        idc_topFive: [],
      }
    },
    mounted() {
      this.chart = echarts.init(this.$refs.idcChart, 'dark');
      this.renderChart();
    },

    beforeUnmount() {
      this.chart.dispose();
    },

    methods: {
      renderChart() {
        this.chart.setOption({
          title: {
            text: '机房机器数量TOP-FIVE',
            left: 'center',
            textStyle: {
              // fontWeight: 'normal',
              // fontSize: 18,
              // textAlign: 'center',
              // color:'red',
            },
          },
          tooltip: {  
          trigger: 'axis',  //触发x轴
          axisPointer: {    //触发位置
            type: 'shadow', //阴影
          },
        },
          dataset: [
            {
              dimensions: ['idc_name', 'idc_number'],
              source: this.idc_topFive
            },
            {
              transform: {
                type: 'sort',
                config: { dimension: 'idc_number', order: 'desc' }
              }
            }
          ],
          xAxis: {
            type: 'category',
            name: '机房名称',
            axisLabel: { interval: 0, rotate: 30}
          },
          yAxis: {
            name: '机器数量',
            axisLabel: {show: false}
          },
          series: {
            type: 'bar',
            encode: { x: 'idc_name', y: 'idc_number' },
            datasetIndex: 1,
            label: {
              show: true,
              position: 'top',
            },
            itemStyle: {  //项样式
              emphasis: {
                // 鼠标移动到柱状图上时的高亮样式
                color: '#FF9800',
              },
              // 设置柱状图的颜色
                color: '#03A9F4',
            },
          }
        });
      },

      getIdcDashboard() {
        this.$http.get('/cmdb/idc_dashboard/').then(res => {
          if (res.data.code === 200) {
            this.idc_topFive = res.data.data
            this.renderChart();
          }
        });
      },
    },

    created() {
      this.getIdcDashboard();
    },
  }
</script>
