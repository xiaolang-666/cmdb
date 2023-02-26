<template>
  <el-dialog
      :model-value="visible"
      width="30%"
      title="创建机房"
      @close="dialogClose"
      >
      <el-form :model="form" ref="formRef" :rules="formRules" label-position=“right” label-width="100px" >
        <el-form-item label="机房名称：" prop="name">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="城市：" prop="city">
          <el-input v-model="form.city"></el-input>
        </el-form-item>
        <el-form-item label="运营商：" prop="provider">
          <el-input v-model="form.provider"></el-input>
        </el-form-item>
        <el-form-item label="备注：">
          <el-input v-model="form.note" type="textarea"></el-input>
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
        name: "IdcCreate",
        props: {
          visible: Boolean,
        },
        data() {
          return {
            form: {
              'name': '',
              'city': '',
              'provider': '',
              'note': ''
            },
            formRules: {
              name: [
                  {required: true, message: '请输入机房名称', trigger: 'blur'},
                  {min: 2, message: '机房名称长度应不小于2个字符', trigger: 'blur'}
              ],
              city: [
                  {required: true, message: '请输入城市', trigger: 'blur'},
                  {min: 2, message: '城市长度应不小于2个字符', trigger: 'blur'}
              ],
              provider: [
                  {required: true, message: '请输入运营商', trigger: 'blur'},
                  {min: 2, message: '运营商长度应不小于2个字符', trigger: 'blur'}
              ]
            },
          }
        },
        methods: {
            submit() {
              this.$refs.formRef.validate((valid) => {
                if (valid) {
                  console.log(this.form)
                  this.$http.post('/cmdb/idc/', this.form)
                    .then(res => {
                      if (res.data.code == 200){
                        this.$message.success('创建成功');
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
              this.$parent.getData();  // 调用父组件方法，更新数据
            }
        }
    }

</script>


<style scoped>

</style>>
