
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
            <!-- 主机组创建 -->
            <div class="header-bar-right">
                <el-button type="primary"  @click="createDialogVisible = true"><el-icon><plus /></el-icon>&nbsp;分组创建</el-button>

                <!--展示列弹出框-->
                <el-popover placement="left" :width="100" v-model:visible='columnVisible'>
                  <template #reference>
                    <el-button type="primary" @click="columnVisible = true"><el-icon><setting /></el-icon>&nbsp;展示列</el-button>
                  </template>
                    <el-checkbox v-model="showColumn.name" disabled>分组名称</el-checkbox>
                    <el-checkbox v-model="showColumn.note">备注</el-checkbox>
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
        border
        prop
        style="width: 100%"
        :header-cell-style="{ background: '#F0F2F5' }"
      >
        <el-table-column type="selection" width="55" />  <!--启用多选-->
        <el-table-column prop="name" label="分组名称"  v-if="showColumn.name" sortable/>
        <el-table-column prop="note" label="备注" v-if="showColumn.note" />
        <el-table-column prop="create_time" label="创建时间" v-if="showColumn.create_time" sortable/>

        <!--操作栏-->
        <el-table-column label="操作" align="left">
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
  <ServerGroupEdit v-model:visible="editDialogVisible" :row="row"></ServerGroupEdit>
  <ServerGroupCreate v-model:visible="createDialogVisible"></ServerGroupCreate>

</template>

<script>

import ServerGroupEdit from './ServerGroupEdit';
import ServerGroupCreate from './ServerGroupCreate'

export default {
    components: {ServerGroupEdit,ServerGroupCreate},
    data() {
      return {
        tableData: [],
        currentPage: 1, // 默认开始页面
        pageSize: 10, // 默认每页的数据条数
        total: 0,  // 总数据条数
        urlParams: {   // URL查询参数，传递服务端，放这里方便修改值
          page_num: 1,
          page_size: this.pageSize,
          search: '', // 如果没有输入关键字，默认为空
        },
        editDialogVisible: false,  //编辑对话框是否显示  默认不显示
        row: "",
        createDialogVisible: false,
        columnVisible: false, // 可展示列显示与隐藏
        showColumn: {
          name: true,  // 分组名称默认展示 不支持不选择
          note: true,
          create_time: false
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
          this.$http.get('/cmdb/server_group/',{params: this.urlParams})
              .then(res => {
                  this.tableData = res.data.data;  
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
          // console.log(row)
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
                this.$http.delete('/cmdb/server_group/'+ row.id + '/')
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
