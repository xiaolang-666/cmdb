<template>
  <el-dialog
      :model-value="visible"
      width="30%"
      title="创建凭据"
      @close="dialogClose"
      >
      <el-form :model="form" ref="formRef" :rules="formRules" label-position=“right” label-width="100px" >
        <el-form-item label="凭据名称" prop="name">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username"></el-input>
        </el-form-item>
        <el-form-item label="认证方式" prop="auth_mode">
          <el-select v-model="form.auth_mode" placeholder="请选择">
            <el-option v-for="row in auth_mode" :key="row.id" :label="row.name" :value="row.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password"></el-input>
        </el-form-item>
        <el-form-item label="秘钥">
          <el-input v-model="form.private_key" type="textarea"></el-input>
        </el-form-item>
        <el-form-item label="备注">
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
        name: "CredentialCreate",
        props: {
          visible: Boolean,
        },
        data() {
          return {
            form: {
              'name': '',
              'username': '',
              'auth_mode': '',
              'password': '',
              'private_key': '',
              'note': '',
            },
            // 认证模式 id 要跟数据库保持一致
            auth_mode: [
              {
                id:1,
                name:"密码",
              },{
                id:2,
                name:"秘钥",
              }],
            formRules: {
              name: [
                  {required: true, message: '请输入凭据名称', trigger: 'blur'},
                  {min: 2, message: '凭据名称长度应不小于2个字符', trigger: 'blur'}
              ],
              username: [
                  {required: true, message: '请输入用户名', trigger: 'blur'},
                  {min: 2, message: '用户名长度应不小于2个字符', trigger: 'blur'}
              ],
              auth_mode: [
                  {required: true, message: '请选择认证方式', trigger: 'blur'},
                  // {min: 2, message: '运营商长度应不小于2个字符', trigger: 'blur'}
              ]
            },
          }
        },
        methods: {
            submit() {
              this.$refs.formRef.validate((valid) => {
                if (valid) {
                  this.$http.post('/config/credential/', this.form)
                    .then(res => {
                      if (res.data.code == 200){
                        this.$message.success(res.data.msg);
                        this.$parent.getData();  // 调用父组件方法，更新数据
                        this.dialogClose()  // 关闭窗口
                      } else {
                        this.$message.warning(res.data.msg);
                      }
                    })
                } else {
                  this.$message.error('格式错误！')  // 表单未验证通过提示"格式错误8"
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
