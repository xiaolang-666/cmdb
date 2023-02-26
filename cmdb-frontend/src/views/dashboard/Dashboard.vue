<template>
    <div class="container">
        <!-- 仪表盘放idc机房信息 -->
        <idcDashboard></idcDashboard>
        <!-- host -->
        <serverDashboard></serverDashboard>
    </div>
</template>
  
<script>
    import idcDashboard from "./idcDashboard.vue"
    import serverDashboard from "./serverDashboard.vue";
    export default {
        components: {idcDashboard, serverDashboard},
        data () {
            return {
                
            }
        }
    }
</script>

<style scoped>
.container {
    display: flex; /* 扩展和收缩 flex 容器内的元素，以最大限度地填充可用空间。*/
    align-items: center; /* 对齐方式 */
    justify-content: space-between;  /* 放大缩小同步 */
}

</style>