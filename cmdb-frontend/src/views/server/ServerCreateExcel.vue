<template>
    <el-dialog
      :model-value="visible"
      width="30%"
      title="Excel导入"
      @close="dialogClose"
      >
      <el-form :model="form" ref="formRef" :rules="formRules" label-position=“right” label-width="100px" >
        <el-form-item label="模板下载">
            <el-link :href="excelTemplateDown" type="primary">主机导入模板</el-link>
        </el-form-item>

         <el-form-item label="IDC机房" prop="idc">
          <el-select class="m-2" v-model="form.idc" @click="getIdc" placeholder="请选择">
            <el-option v-for="row in idc" :key="row.id" :label="row.name + '-' + row.city" :value="row.id">
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="主机分组" prop="server_group">
          <el-select class="m-2" multiple v-model="form.server_group" @click="getServerGroup" placeholder="请选择">
            <el-option v-for="row in serverGroup" :key="row.id" :label="row.name" :value="row.id">
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="导入数据">
            <el-upload
              :limit="1"
              :file-list="fileList"
              :auto-upload="false"
            >
              <template #trigger>
                <el-button type="primary">选择文件</el-button>
              </template>
              <template #tip>
                <div class="el-upload__tip text-red">
                  导入完成后可通过验证功能批量验证
                </div>
              </template>
            </el-upload>
        </el-form-item>

      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogClose">取消</el-button>
          <el-button type="primary" @click="submit">确定</el-button>
        </span>
      </template>
    </el-dialog>

</template>

<script>
    export default {
        props: {
          visible: Boolean,
        },
        data() {
          return {
            form: [],
            formRules: {
              idc: [
                  {required: true, message: '请选择IDC机房', trigger: 'blur'},
              ],
              server_group: [
                  {required: true, message: '请选择主机分组', trigger: 'blur'},
              ]
            },
            idc: '',
            serverGroup: '',
            excelTemplateDown: 'http://127.0.0.1:9090/api/cmdb/excel_create_host/', // 直接请求后端get方法 需要后端放行 不需要认证
            fileList: [],
          }
        },
        methods: {
            submit() {
              this.$refs.formRef.validate((valid) => {
                if (valid) {
                  let fd = new FormData();
                  fd.append("file", this.fileList[0].raw);
                  fd.append('idc', this.form.idc);
                  fd.append('server_group', this.form.server_group);
                  this.$http.post('/cmdb/excel_create_host/', fd)
                    .then(res => {
                      if (res.data.code == 200){
                        this.$message.success(res.data.msg);
                        this.$parent.getData();  // 调用父组件方法，更新数据
                        this.dialogClose()  // 关闭窗口
                      }
                    })
                } else {
                  this.$message.error('格式错误！')
                }
              })
            },
            // 点击关闭，子组件通知父组件更新属性
            dialogClose() {
              this.$emit('update:visible', false)  // 父组件必须使用v-model
            },
            getIdc() {
              console.log(this.$http.instance);
                this.$http.get('/cmdb/idc/?page_size=50')
                    .then(res => {
                        this.idc = res.data.data;
                    })
            },
            getServerGroup() {
                this.$http.get('/cmdb/server_group/?page_size=50')
                    .then(res => {
                        this.serverGroup = res.data.data;
                    });
            },
        }
    }
</script>
