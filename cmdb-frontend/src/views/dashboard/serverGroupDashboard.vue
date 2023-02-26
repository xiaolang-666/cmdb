<template>
    <div ref="hostChart" style="width: 30%; height: 500px;"></div>
</template>
  
<script>
  import * as echarts from 'echarts';
  export default {
    data() {
        return {
            
        }
    },
    mounted() {
      this.chart = echarts.init(this.$refs.hostChart); //初始化图表
      this.chart.setOption({
        // 在这里设置你的 Echarts 配置
        title: {
            text: 'IDC机房',
            subtext: 'IDC机房数据',
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
            name: 'Access From',
            type: 'pie',
            radius: '50%',
            data: [
                { value: 1048, name: '' },
                { value: 735, name: 'Direct' },
                { value: 580, name: 'Email' },
                { value: 484, name: 'Union Ads' },
                { value: 300, name: 'Video Ads' }
            ],
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
    // 取消图表挂载之前释放资源 防止内存
    beforeUnmount() {
      this.chart.dispose();  
    }
  }
</script>
  