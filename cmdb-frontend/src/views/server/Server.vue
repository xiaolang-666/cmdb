
<template>
  <el-card class="box-card">

      <!-- 搜索 -->
      <div style="margin-bottom: 10px;display: flex;align-items: center;justify-content: space-between">
        <div>
            <el-row>
                <el-col :span="12">
                    <el-input
                      v-model="urlParams.search"
                      placeholder="请输入关键字"
                      @keyup.enter="onSearch"
                      clearable
                      @clear="onSearch"
                      class="search"
                    />
                </el-col>
                <el-col :span="2">
                    <el-button type="primary" @click="onSearch"><el-icon><search /></el-icon>&nbsp;搜索</el-button>
                </el-col>
            </el-row>
        </div>
          <div>
            <div class="header-bar-right">
                <!-- 主机创建 -->
                <el-button type="primary"  @click="createDialogVisible = true"><el-icon><plus /></el-icon>&nbsp;主机创建</el-button>
                <!-- 导入excel表格创建 -->
                <el-button type="success"  @click="excelDialogVisible = true"><el-icon><FolderAdd /></el-icon>&nbsp;导入excel</el-button>
                <!-- 导入云主机 -->
                <el-button type="warning"  @click="cloudlDialogVisible = true"><el-icon><MostlyCloudy/></el-icon>&nbsp;导入云主机</el-button>
                <!--展示列弹出框-->
                <el-popover placement="left" :width="100" v-model:visible='columnVisible'>
                  <template #reference>
                    <el-button type="info" @click="columnVisible = true"><el-icon><setting /></el-icon>&nbsp;展示列</el-button>
                  </template>
                    <el-checkbox v-model="showColumn.name">主机别名</el-checkbox>
                    <el-checkbox v-model="showColumn.hostname" disabled>主机名称</el-checkbox>
                    <el-checkbox v-model="showColumn.idc">IDC机房</el-checkbox>
                    <el-checkbox v-model="showColumn.server_group">主机分组</el-checkbox>
                    <el-checkbox v-model="showColumn.machine_type">机器类型</el-checkbox>
                    <el-checkbox v-model="showColumn.os_version">系统版本</el-checkbox>
                    <el-checkbox v-model="showColumn.public_ip">公网IP</el-checkbox>
                    <el-checkbox v-model="showColumn.private_ip">私有IP</el-checkbox>
                    <el-checkbox v-model="showColumn.cpu_num">CPU数量</el-checkbox>
                    <el-checkbox v-model="showColumn.cpu_model">CPU型号</el-checkbox>
                    <el-checkbox v-model="showColumn.memory">内存</el-checkbox>
                    <el-checkbox v-model="showColumn.disk">硬盘</el-checkbox>
                    <el-checkbox v-model="showColumn.put_shelves_date">上架日期</el-checkbox>
                    <el-checkbox v-model="showColumn.off_shelves_date">下架日期</el-checkbox>
                    <el-checkbox v-model="showColumn.expire_datetime">租约过期时间</el-checkbox>
                    <el-checkbox v-model="showColumn.is_verified" disabled>SSH验证状态</el-checkbox>
                    <el-checkbox v-model="showColumn.note">备注</el-checkbox>
                    <el-checkbox v-model="showColumn.update_time">更新时间</el-checkbox>
                    <el-checkbox v-model="showColumn.create_time">创建时间</el-checkbox>

                    <div style="text-align: right; margin: 0">
                      <el-button size="small" type="text" @click="columnVisible = false">取消</el-button>
                      <el-button size="small" type="primary" @click="saveColumn">确认</el-button>
                    </div>
                </el-popover>
            </div>

          </div>
      </div>



      <!-- 表格 -->
      <el-table
        ref="Table"
        :data="tableData"
        @selection-change="handleSelectionChange"
        border="true"
        prop
        style="width: 100%"
        :header-cell-style="{ background: '#F0F2F5' }">

      <el-table-column type="selection" width="55"/>  <!--启用多选-->
      <el-table-column prop="name" label="主机别名" width="130" fixed="left" sortable v-if="showColumn.name"/>
      <el-table-column prop="hostname" label="主机名" width="130" sortable v-if="showColumn.hostname"/>
      <el-table-column prop="idc" label="IDC机房" sortable v-if="showColumn.idc">
        <template #default="scope">
          <img src="../../assets/img/aliyun.png" style="width: 18px;height: 18px" v-if="scope.row.idc.provider == '阿里云'">
          <img src="../../assets/img/tencent.png" style="width: 18px;height: 18px" v-else-if="scope.row.idc.provider == '腾讯云'">
          <el-icon :size="18" color="#409EFC" v-else><office-building/></el-icon>
          {{scope.row.idc.name}}-{{scope.row.idc.city}}
        </template>
      </el-table-column>

      <el-table-column prop="server_group" label="主机分组" width="150" sortable v-if="showColumn.server_group">
        <template #default="scope">
          <el-tag class="ml-2" type="info" v-for="group in scope.row.server_group" :key="group.id">{{group.name}}</el-tag>
        </template>
      </el-table-column>

      <el-table-column prop="machine_type" label="机器类型" width="110" sortable v-if="showColumn.machine_type">
        <template #default="scope">
          <span v-if="scope.row.machine_type == 'vm'">虚拟机</span>
          <span v-else-if="scope.row.machine_type == 'cloud_vm'">云主机</span>
          <span v-else>物理机</span>
        </template>
      </el-table-column>

      <el-table-column prop="os_version" label="系统版本" sortable :show-overflow-tooltip="true" v-if="showColumn.os_version"/>
      <el-table-column prop="public_ip" label="公网IP" width="180" sortable v-if="showColumn.public_ip"/>
      <el-table-column prop="private_ip"  label="私网IP" width="140" sortable v-if="showColumn.private_ip">
        <template #default="scope">
          <el-tag type="info" v-for="(ip,index) in scope.row.private_ip" :key="index">{{ip}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="cpu_num" label="CPU" width="70" sortable v-if="showColumn.cpu_num"/>
      <el-table-column prop="cpu_model" label="CPU型号" sortable v-if="showColumn.cpu_model"/>
      <el-table-column prop="memory" label="内存" width="70" sortable v-if="showColumn.memory"/>
      <el-table-column prop="disk" label="硬盘" width="200" sortable v-if="showColumn.disk">
        <template #default="scope">
        <table style="background: #ebeef5;width: 100%" v-if="scope.row.disk">  <!--表格背景设置灰色，表格内默认白色-->
          <thead>
            <tr>
              <th>设备</th>
              <th>类型</th>
              <th>容量</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(disk, index) in scope.row.disk" :key="index">
              <td>{{disk.device}}</td>
              <td>{{disk.type}}</td>
              <td>{{disk.size}}</td>
            </tr>
          </tbody>
        </table>
        <span v-else>{{scope.row.disk}}</span>
      </template>
      </el-table-column>
      <el-table-column prop="put_shelves_date" label="上架日期" sortable v-if="showColumn.put_shelves_date"/>
      <el-table-column prop="off_shelves_date" label="下架日期" sortable v-if="showColumn.off_shelves_date"/>
      <el-table-column prop="expire_datetime" label="租约过期时间" sortable v-if="showColumn.expire_datetime"/>
      <el-table-column prop="is_verified" label="SSH状态" width="82" sortable v-if="showColumn.is_verified" fixed="right">
        <template #default="scope">
          <el-tag type="success" v-if="scope.row.is_verified == 'verified'">已验证</el-tag>
          <el-tag type="warning" v-if="scope.row.is_verified == 'unverified'">未验证</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="note" label="备注"  v-if="showColumn.note"/>
      <el-table-column prop="update_time" label="更新时间" sortable v-if="showColumn.update_time"/>
      <el-table-column prop="create_time" label="创建时间" sortable v-if="showColumn.create_time"/>


        <!--操作栏-->
        <el-table-column label="操作" align="left" width="200" fixed="right" >
          <template #default="scope">

            <el-button
              size="small"
              type="primary"
              @click="handleEdit(scope.$index, scope.row)"
              >编辑</el-button>

            <el-button
              size="small"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)"
              >删除</el-button>

              <el-button
              size="small"
              type="success"
              @click="handleSync(scope.$index, scope.row)"
              >同步</el-button>
          </template>
        </el-table-column>

      </el-table>

      <!--分页-->
      <div style="margin-top: 20px">
        <el-pagination
          v-model:currentPage="currentPage"
          :page-sizes="[10, 15, 20, 25, 30]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          background
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange">
        </el-pagination>
      </div>

  </el-card>
  <!-- 使用组件 -->
  <ServerEdit v-model:visible="editDialogVisible" :form="row"></ServerEdit>
  <ServerCreate v-model:visible="createDialogVisible"></ServerCreate>
  <ServerCreateExcel v-model:visible="excelDialogVisible"></ServerCreateExcel>
  <ServerCreateCloud v-model:visible="cloudlDialogVisible"></ServerCreateCloud>
</template>

<script>

// 导入组件
import ServerEdit from './ServerEdit';
import ServerCreate from './ServerCreate';
import ServerCreateExcel from '@/views/server/ServerCreateExcel';
import ServerCreateCloud from './ServerCreateCloud';

export default {
    // 注册组件
    components: {ServerEdit,ServerCreate,ServerCreateExcel, ServerCreateCloud},
    data() {
      return {
        tableData: [],
        currentPage: 1, // 默认开始页面
        pageSize: 10, // 定义每页显示多少条数据
        total: 0,  // 总数据条数
        urlParams: {   // URL查询参数，传递服务端，放这里方便修改值
          page_num: 1,  //定义每页显示多少条
          page_size: this.pageSize,
          search: '', // 如果没有输入关键字，默认为空
        },
        editDialogVisible: false,  //编辑对话框是否显示  默认不显示
        row: "",
        createDialogVisible: false, //新建主机
        excelDialogVisible: false, //excel导入主机
        cloudlDialogVisible: false, //新建云主机
        columnVisible: false, // 可展示列显示与隐藏
        showColumn: {
          name: false,
          hostname: true,
          idc: true,
          server_group: false,
          machine_type: false,
          os_version: false,
          public_ip: true,
          private_ip: true,
          cpu_num: true,
          cpu_model: false,
          memory: true,
          disk: true,
          put_shelves_date: false,
          off_shelves_date: false,
          expire_datetime: false,
          is_verified: true,
          update_time: false,
          create_time: false,
          note: false
        },

      }
    },
    created() {
      // 加载页面之前获取数据
      this.getData()
      // 从浏览器本地存储获取历史存储展示
      const columnSet = localStorage.getItem(this.$route.path + '-columnSet');
      if (columnSet) {  // 如果本地有数据就展示
        this.showColumn = JSON.parse(columnSet)
      }
    },

    methods: {
        getData() {
          this.$http.get('/cmdb/server/',{params: this.urlParams})
              .then(res => {
                  this.tableData = res.data.data;
                  console.log(res.data.data)
                  this.total = res.data.count;
              })
        },
        // 分页：监听【选择每页数量】的事件
        handleSizeChange(pageSize) {
            // console.log(pageSize)
            this.pageSize = pageSize; // 重新设置分页显示
            this.urlParams.page_size = pageSize;  // 将最新值设置到数据里，用于下面用新值重新获取数据
            this.getData()
        },
        // 分页：监听【点击页码】的事件
        handleCurrentChange(currentPage) {
            // console.log(currentPage)
            this.currentPage = currentPage; // 重新设置分页显示
            this.urlParams.page_num = currentPage;
            this.getData()
        },
        handleEdit(index, row){
          this.editDialogVisible=true,
          this.row=row
        },
        // 操作栏：删除
        handleDelete(index, row) {
            console.log(index, row);
            this.$confirm("你确定要删除选中的吗？", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning"
              })
              .then(() => {  // 点击确定
                this.$http.delete('/cmdb/server/'+ row.id + '/')
                      .then(res => {
                        console.log(res.data)
                        if(res.data.code == 200) {
                          this.$message.success('删除成功');
                          this.tableData.splice(index, 1); // 根据表格索引临时删除数据
                        } else {
                          this.$message.warning(res.data.msg);
                        }
                    });
              })
        },
        // 主机同步
        handleSync(index, row){
          const urlParam = {
            hostname: row.hostname
          };
          this.$http.get("/cmdb/host_collect/", {params: urlParam})
            .then(res =>{
              if (res.data.code == 200){
                this.getData()
                this.$message.success(res.data.msg)
              } else {
                // 如果主机信息同步失败则把验证信息修改为未验证(后端实现) 前端则重新加载一下数据
                this.getData()
              }
            })},
        // 查询提交（携带search重新查询）
        onSearch() {
            this.getData()
        },
        saveColumn() {
          // 将可显示的字段存储到浏览器本地存储
          localStorage.setItem(this.$route.path + '-columnSet', JSON.stringify(this.showColumn));
          this.columnVisible = false;
        },

    },

};
</script>

<style scoped>

</style>
