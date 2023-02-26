<template>
  <el-dialog :model-value="visible" title="修改机房信息" @close="dialogClose" width="30%">

    <el-form :model="row" ref="formRef" :rules="formRules" label-position=“right” label-width="100px">
    <el-form-item label="分组名称：" prop="name">
      <el-input v-model="row.name"></el-input>
    </el-form-item>
    <el-form-item label="备注：">
      <el-input v-model="row.note" type="textarea"></el-input>
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
        row:"",
    },
    data () {
        return {
            formRules: {
              name: [
                  {required: true, message: '请输入分组名称', trigger: 'blur'},
                  {min: 2, message: '分组名称长度应不小于2个字符', trigger: 'blur'}
              ],
            },
        }
    },
    methods: {
        dialogClose(){
            this.$emit("update:visible", false)
            this.$parent.getData();
        },
        submit() {
            this.$refs.formRef.validate((valid) => {
              if (valid) { 
                this.$http.put('/cmdb/server_group/' + this.row.id + '/', this.row)
                  .then(res => {
                    if (res.data.code == 200){
                      this.$message.success('修改成功');
                    //   this.$parent.getData();  // 调用父组件方法，更新数据
                      this.dialogClose()  // 关闭窗口
                    }
                  })
              } else {
                this.$message.error('格式错误！')
              }
            })
          },
    },

}

</script>

<style scoped>

</style>