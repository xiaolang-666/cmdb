<template>
    <div class="main">
        <div class="login_box">
            <div class="title">
                DevOps运维平台
            </div>
            <div class="login_form">
                <el-form :model="form" ref="form" :rules="rules" label-width="60px">
                    <el-form-item prop="username">
                      <el-input v-model="form.username"
                                placeholder="用户名"
                                :prefix-icon="User"
                      />
                    </el-form-item>
                    <el-form-item prop="password">
                      <el-input v-model="form.password" placeholder="密码" @keydown.enter="onSubmit" :prefix-icon="Lock" type="password"/>
                    </el-form-item>
                </el-form>
                <el-form-item>
                  <el-button type="primary" @click="onSubmit" >登录</el-button>
                </el-form-item>
            </div>
        </div>
    </div>
</template>

<script>
    import {User, Lock} from "@element-plus/icons-vue"
    export default {
        name: "Login",
        data() {
            return {
                form: {
                    username: '',
                    password: ''
                },
                rules: {
                    username: [
                        {required: true, message: '请输入用户名', trigger: 'blur'},
                        {min: 3, message: '用户名长度应不小于3个字符', trigger: 'blur'}
                    ],
                    password: [
                        {required: true, message: '请输入密码', trigger: 'blur'},
                        {min: 6, message: '用户名长度应不小于6个字符', trigger: 'blur'}
                    ]
                }
            }
        },
        methods: {
          onSubmit() {
              // 提交前预验证
              this.$refs.form.validate((valid) => {  //回调函数中valid布尔值
                  if (valid) {
                        this.$http.post('/login/', this.form)
                            .then(res=> {
                                if (res.data.code == 200) {
                                    this.$message.success('登录成功');
                                    // 保存token到会话存储
                                    window.sessionStorage.setItem('token', res.data.token);
                                    window.sessionStorage.setItem('username', res.data.username);
                                    this.$router.push("/dashboard")
                                } else {
                                    this.$message.warning(res.data.msg)
                                }
                            })
                  } else {
                      this.$message.warning('用户名或密码格式错误！')
                  }
              })
          }
        },
        setup() {
            return {
                User, Lock
            }
        }
    }
</script>

<style scoped>
    .main {
        background-image: url("../assets/img/login_background.jpg");
        background-size: 100% 100%;
        height: 100%;
    }
    .login_box {
        width: 400px;
        height: 300px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 5px 20px 0 #f5f5f5;
        position: absolute;
        top: 0;
        bottom: 0;
        right: 0;
        left: 0;
        margin: auto;
    }
    .title {
        font-size: 20px;
        font-weight: bold;
        color: dodgerblue;
        text-align: center;
        margin-top: 30px;
    }
    .login_form {
        margin-right: 50px;
        margin-top: 30px;
    }
    .login_form .el-button {
        margin-left: 175px;
    }
</style>