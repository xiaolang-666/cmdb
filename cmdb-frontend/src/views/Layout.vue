<template>
  <div class="common-layout">
    <el-container>
      <el-aside :width="isCollapse ? '64px' : '200px'">
         <el-menu
            default-active="2"
            class="el-menu-vertical-demo"
            background-color="#304156"
            text-color="#FFFFFF"
            active-text-color="#ffd04b"
            @open="handleOpen"
            @close="handleClose"
            router
            :collapse="isCollapse"
            :collapse-transition="false"
          >
           
           <div class="logo-title">
             <img src="../assets/img/devops1.png" alt="">
             <span v-if="isTitle">IIOT运维平台</span>
           </div>
           
            <template v-for="menu in this.$router.options.routes" :key="menu"> <!--$router获取路由对象-->

            <!--处理仪表盘-->
            <el-menu-item v-if="menu.path == '/'" :index="menu.children[0].path">
              <el-icon><component :is="menu.children[0].icon"></component></el-icon> <!--显示图标-->
              <span>{{menu.children[0].name}}</span>
            </el-menu-item>

            <!--处理一级菜单有子路由-->
            <el-sub-menu v-else-if="menu.children" :index="menu.path">
              <template #title>
                <el-icon><component :is="menu.icon"></component></el-icon>
                <span>{{ menu.name }}</span>
              </template>
              <!--循环生成二级菜单-->
              <el-menu-item v-for="child in menu.children" :key="child" :index="child.path">
                <el-icon><component :is="child.icon"></component></el-icon> <!--显示图标-->
                <span>{{child.name}}</span>
              </el-menu-item>
            </el-sub-menu>

            </template>

          </el-menu>

      </el-aside>
      <el-container>
        <el-header>
           <!--折叠-->
           <div>
             <el-icon :size="25" @click="toggleCollapse"><Fold/></el-icon>
           </div>
           <!--用户标识-->
           <div>
               <img src="../assets/img/touxiang.png" class="touxiang">
               <el-dropdown>
                <span class="el-dropdown-link">
                  {{username}}
                  <el-icon class="el-icon--right">
                    <arrow-down />
                  </el-icon>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="UserPasswordDialog = true">修改密码</el-dropdown-item>
                    <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
           </div>
        </el-header>
        <el-main>
            <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>

   <!--修改密码对话框-->
  <el-dialog
    v-model="UserPasswordDialog"
    width="30%"
    title="修改密码"
    :before-close="handleClose"
  >
    <el-form :model="UserPasswordForm" label-width="100px" :rules="rules" ref="UserPasswordForm">
      <el-form-item label="原密码：" prop="old_password">
        <el-input
          v-model="UserPasswordForm.old_password"
          type="password"
          show-password
        ></el-input>
      </el-form-item>
      <el-form-item label="新密码：" prop="new_password">
        <el-input
            v-model="UserPasswordForm.new_password"
            type="password"
            show-password
        ></el-input>
      </el-form-item>
      <el-form-item label="再次确认：" prop="confirm_password">
        <el-input
            v-model="UserPasswordForm.confirm_password"
            type="password"
            show-password
        ></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="UserPasswordDialog = false">取消</el-button>
        <el-button type="primary" @click="changePasswordSubmit">确定</el-button>
      </span>
    </template>
  </el-dialog>

</template>

<script>
    export default {
        name: "Layout",
        data() {
            const checkNewOldPassword = (rule, value, callback) => {
                if (value == this.UserPasswordForm.old_password) {
                    callback(new Error('新密码不能与旧密码一样！'))
                } else {
                    return callback()
                }
            };
            const checkNewPassword = (rule, value, callback) => {
                if (value != this.UserPasswordForm.new_password) {
                    callback(new Error('两次输入密码不一致！'))
                } else {
                    return callback()
                }
            };
          return {
            isCollapse: false,  // 导航栏显示与隐藏
            isTitle: true, // 显示与隐藏标题
            username: window.sessionStorage.getItem('username'),
            UserPasswordDialog: false, // 显示与隐藏标题
            UserPasswordForm: {
                username: window.sessionStorage.getItem('username'),
                old_password: '',
                new_password: '',
                confirm_password: ''
            },
            rules: {
                old_password: [
                    {required: true, message: '请输入原密码', trigger: 'blur'},
                    {min: 6, message: '用户名长度应不小于6个字符', trigger: 'blur'}
                ],
                new_password: [
                    {required: true, message: '请输入新密码', trigger: 'blur'},
                    {min: 6, message: '用户名长度应不小于6个字符', trigger: 'blur'},
                    {validator: checkNewOldPassword, trigger: 'blur'}
                ],
                confirm_password: [
                    {required: true, message: '请确认新密码', trigger: 'blur'},
                    {min: 6, message: '用户名长度应不小于6个字符', trigger: 'blur'},
                    {validator: checkNewPassword, trigger: 'blur'}
                ]
            }
          }
        },
        methods: {
          toggleCollapse() {
            this.isCollapse = !this.isCollapse;
            this.isTitle = !this.isTitle;
          },
          logout() {
             window.sessionStorage.clear();
             this.$router.push('/login')
          },
            changePasswordSubmit() {
                // 提交前预验证
                this.$refs.UserPasswordForm.validate((valid) => { // 回调函数中valid布尔值
                    if (valid) {
                        this.$http.post('/change_password/', this.UserPasswordForm)
                        .then(res => {
                            if (res.data.code == 200) {
                                this.$message.success(res.data.msg);
                                this.UserPasswordDialog = false;
                            } else {
                                this.$message.warning(res.data.msg)  // 这里应根据后端返回消息显示
                            }
                        })
                        .catch((error) => {
                            this.$message.error('服务端接口请求错误！'+ error)
                        })
                    } else {
                        this.$message.warning('密码格式错误！')
                    }
                });
            }

        }
    }
</script>

<style scoped>
    .el-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .el-main {
        background: #f5f5f5;
    }
    .common-layout,.el-container,.el-menu-vertical-demo {
        height: 100%;
    }
    .touxiang {
      width: 25px;
      height: 25px;
      border-radius: 3px;
    }
    .logo-title img {
      width: 30px;
      height: 30px;
      margin-left: 15px;
      margin-top: 16px;
    }
    .logo-title span {
      color: white;
      font-weight: bold;
      font-size: 16px;
      margin-left: 10px;
      position: relative;
      bottom: 10px;
    }
    .logo-title {
      margin-bottom: 12px;
    }
</style>