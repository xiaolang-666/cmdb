<template>
  <div ref="hostChart" style="width: 50%; height: 500px;"></div>
</template>

<script>
  import * as echarts from 'echarts';
  export default {
    data() {
      return {
        host_status: [],
      }
    },
    mounted() {
      this.chart = echarts.init(this.$refs.hostChart, 'dark');
      this.renderChart();
    },

    beforeUnmount() {
      this.chart.dispose();
    },

    methods: {
      renderChart() {
        this.chart.setOption({
          title: {
            text: '主机在线状态',
            left: 'center'
          },
          tooltip: {
            trigger: 'item'
          },
          legend: {
            orient: 'vertical',
            left: 'left'
          },
          series: [
            {
              name: '主机状态',
              type: 'pie',
              radius: '50%',
              data: this.host_status,
              label: {
                show: true,
                formatter: '{b}: {c}'
              },
              color: ['green', 'red', {type: 'linear', x: 0, y: 0, x2: 1, y2: 1, colorStops: [{offset: 0, color: 'red'}, {offset: 1, color: 'blue'}]}],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        });
      },

      getHostDashboard() {
        this.$http.get('/cmdb/server_dashboard/').then(res => {
          if (res.data.code === 200) {
            this.host_status = res.data.data
            this.renderChart();
          }
        });
      },
    },

    created() {
      this.getHostDashboard();
    },
  }
</script>
