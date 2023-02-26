<template>
    <el-dialog
      :model-value="visible"
      width="40%"
      title="导入云主机"
      @close="dialogClose"
      >
    <el-steps :space="200" :active="active" align-center style="margin-bottom: 10%">
      <el-step title="公有云"></el-step>
      <el-step title="访问凭据"></el-step>
      <el-step title="导入确认"></el-step>
    </el-steps>

    <el-form :model="form" ref="formRef" :rules="formRules" label-position="right" label-width="155px">
      <!--第一步-->
      <div v-show="active == 1">
        <el-form-item prop="cloud" label-width="180px">
            <el-radio-group v-model="form.cloud">
              <el-radio label="aliyun"><img src="../../assets/img/aliyun.png"></el-radio>
              <el-radio label="tencent" disabled>腾讯云暂时不可用<img src="../../assets/img/tencent.png"></el-radio>
            </el-radio-group>
        </el-form-item>
      </div>
      <!--第二步-->
      <div v-show="active == 2">
        <el-form-item label="AccessKey ID" prop="secret_id">
          <el-input v-model="form.secret_id" clearable></el-input>
        </el-form-item>
        <el-form-item label="AccessKey Secret" prop="secret_key">
          <el-input v-model="form.secret_key" clearable></el-input>
          <el-link v-if="form.cloud == 'aliyun'" href="https://ram.console.aliyun.com/manage/ak" target="_blank" type="primary">如何获取AccessKey？</el-link>
          <el-link v-if="form.cloud == 'tencent'" href="https://console.cloud.tencent.com/cam/capi" target="_blank" type="primary">如何获取AccessKey？</el-link>
        </el-form-item>
      </div>
      <!--第三步-->
      <div v-show="active == 3">
        <el-form-item label="选择区域" prop="region">
          <el-select class="m-2" v-model="form.region" @click="getCloudRegion" placeholder="请选择" style="width: 100%">
            <el-option v-for="row in cloudRegion" :key="row.region_id" :label="row.region_name" :value="row.region_id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="选择分组" prop="server_group">
          <el-select class="m-2" v-model="form.server_group" @click="getServerGroup" multiple placeholder="请选择" style="width: 100%">
            <el-option v-for="row in serverGroup" :key="row.id" :label="row.name" :value="row.id">
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="SSH连接" required>
          <el-col :span="1.5">
            <el-tag size="large" type="info">IP</el-tag>
          </el-col>
          <el-col :span="7" :offset="1">
            <el-radio-group v-model="form.ssh_ip">
              <el-radio label="public" >公网</el-radio>
              <el-radio label="private" >内网</el-radio>
            </el-radio-group>
          </el-col>
          <el-col :span="1.5">
            <el-tag size="large" type="info">端口</el-tag>
          </el-col>
          <el-col :span="5">
            <el-form-item prop="ssh_port">
              <el-input v-model="form.ssh_port"></el-input>
            </el-form-item>
          </el-col>
        </el-form-item>

      </div>
    </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogClose" v-if="active == 1">取消</el-button>
          <el-button type="primary" @click="dialogToggle('pre')" v-if="active > 1">上一步</el-button>
          <el-button type="primary" @click="dialogToggle('next')" v-if="active < 3">下一步</el-button>
          <el-button type="primary" @click="submit" v-if="active == 3">确定</el-button>
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
            form: {
              "request_type": '',  // 后端根据这个参数判断是要请求数据还是创建数据请求数据和创建数据都走post方法
              'cloud': '',
              'secret_id': '',
              'secret_key': '',
              'region': '',
              'server_group': '',
              'ssh_ip': 'private',  // public或private
              'ssh_port': 22
            },
            formRules: {
              cloud: [
                  {required: true, message: '请选择', trigger: 'blur'}
              ],
              secret_id: [
                  {required: true, message: '请输入密钥ID', trigger: 'blur'},
                  {min: 20, message: '密钥ID长度应不小于20个字符', trigger: 'blur'}
              ],
              secret_key: [
                  {required: true, message: '请输入密钥Key', trigger: 'blur'},
                  {min: 20, message: '密钥Key长度应不小于20个字符', trigger: 'blur'}
              ],
              region: [
                  {required: true, message: '请选择IDC机房', trigger: 'change'},
              ],
              server_group: [
                  {required: true, message: '请选择主机分组', trigger: 'change'},
              ],
              ssh_port: [
                  {required: true, message: '请输入端口', trigger: 'blur'},
              ],
            },
            cloudRegion: '',
            active: 1,
            idc: '',
            serverGroup: '',
          }
        },
        methods: {
            submit() {
              this.form.request_type = "createServer";
              this.$refs.formRef.validate((valid) => {
                  if (valid) {
                    if (this.form.cloud == 'aliyun') {
                      this.$http.post('/cmdb/aliyun_cloud/', this.form)
                      .then(res => {
                        if (res.data.code == 200){
                          this.$message.success('导入云主机成功');
                          this.$parent.getData();
                          this.dialogClose()  // 关闭窗口
                        }
                      })
                    } else if (this.form.cloud == 'tencent') {
                      this.$http.post('/cmdb/tencent_cloud/', this.form)
                      .then(res => {
                        if (res.data.code == 200){
                          this.$message.success('导入云主机成功');
                          this.$parent.getData();
                          this.dialogClose()  // 关闭窗口
                        } else {
                            this.$message.error(res.data.msg)
                        }
                      })
                    }
                    this.cloudDialogVisible = false;
                  } else {
                      this.$message.error('格式错误！')
                  }
                });
            },
            // 点击关闭，子组件通知父组件更新属性
            dialogClose() {
              this.$emit('update:visible', false)  // 父组件必须使用v-model
            },
            // 云主机导入第一步和第二步对话框切换
            dialogToggle(action) {
                if (action == 'pre') {
                    if (this.active-- < 2) {
                      this.active = 1;
                    }
                } else if (action == 'next') {
                    if (this.active++ > 3) {
                      this.active = 1;
                    }
                }
            },
            // 获取区域
            getCloudRegion() {
                this.form.request_type = "getRegion";
                if (this.form.cloud == 'aliyun') {
                   // 携带密钥请求
                   this.$http.post('/cmdb/aliyun_cloud/', this.form)
                    .then(res => {
                        if (res.data.code == 200){
                          this.cloudRegion = res.data.data;
                        }  
                    });
                } else if (this.form.cloud == 'tencent') {
                    this.$http.get('/cmdb/tencent_cloud/', {params: this.form})
                      .then(res => {
                          this.cloudRegion = res.data.data;
                      });
                } else {
                    this.$message.error('请选择公有云！');
                }
            },
            getIdc() {
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
