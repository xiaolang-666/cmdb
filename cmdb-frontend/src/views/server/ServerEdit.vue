<template>
<el-dialog
  :model-value="visible"
  width="40%"
  title="修改主机"
  @close="dialogClose"
  >
  <el-form :model="form" ref="formRef" :rules="formRules" label-position=“right” label-width="100px" >
    <el-form-item label="机器名称" prop="name">
        <el-input v-model="form.name" placeholder="例如: 测试机"></el-input> 
    </el-form-item>

      <el-form-item label="主机名称" prop="hostname">
        <el-input v-model="form.hostname" disabled></el-input>
      </el-form-item>

    <el-form-item label="IDC机房" prop="idc">
    <el-select class="m-2" v-model="form.idc" @click="getIdc" placeholder="请选择">
      <el-option v-for="row in idc" :key="row.id" :label="`${row.city}-${row.name}`" :value="row.id">
      </el-option>
    </el-select>
    </el-form-item>

    <el-form-item label="主机分组" prop="server_group">
    <el-select class="m-2" v-model="form.server_group" @click="getServerGroup" multiple placeholder="请选择">
      <el-option v-for="row in serverGroup" :key="row.id" :label="row.name" :value="row.id">
      </el-option>
    </el-select>
    </el-form-item>

    <el-form-item label="SSH凭据" prop="credential">
    <el-select class="m-2" v-model="form.credential_id" @click="getCredential" placeholder="请选择凭据">
      <el-option v-for="row in credential" :key="row.id" :label="`${row.name}-${row.username}`" :value="row.id">
      </el-option>
    </el-select>
    </el-form-item>

    <el-form-item label="SSH连接" required>
      <el-col :span="1.5">
        <el-tag size="large" type="info">IP</el-tag>
      </el-col>
      <el-col :span="10">
        <el-form-item prop="ssh_ip">
          <el-input v-model="form.ssh_ip"></el-input>
        </el-form-item>
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

    <el-form-item label="备注">
		  <el-input v-model="form.note" type="textarea"></el-input>
		</el-form-item>
  </el-form>

<div>
<!--主机详情，默认不展示 自动获取的数据不支持修改-->
	<br>
	<el-divider content-position="left">
	  <el-button @click="serverDetailVisible ?  serverDetailVisible = false : serverDetailVisible = true" plain>更多详情 </el-button>
    <el-tag class="ml-2" type="danger"><el-icon><InfoFilled/></el-icon>以下是自动采集的数据不建议修改</el-tag>
	</el-divider>

	<div v-show="serverDetailVisible">
		<el-form-item label="机器类型：" prop="machine_type">
		  <el-input v-model="form.machine_type"></el-input>
		</el-form-item>
		<el-form-item label="系统版本：" prop="os_version">
		  <el-input v-model="form.os_version"></el-input>
		</el-form-item>
		<el-form-item label="公网IP" prop="public_ip">
		  <el-input v-model="form.public_ip"></el-input>
		</el-form-item>
		<el-form-item label="私有IP" prop="private_ip">
		  <el-input v-model="form.private_ip"></el-input>
		</el-form-item>
		<el-form-item label="CPU数量" prop="cpu_num">
		  <el-input v-model="form.cpu_num"></el-input>
		</el-form-item>
		<el-form-item label="CPU型号" prop="cpu_model">
		  <el-input v-model="form.cpu_model"></el-input>
		</el-form-item>
		<el-form-item label="内存" prop="memory">
		  <el-input v-model="form.memory"></el-input>
		</el-form-item>

		<el-form-item label="硬盘" prop="disk">
		  <el-input v-model="diskDetail"></el-input>
		</el-form-item>

		<el-form-item label="上架日期" prop="put_shelves_date">
		  <el-date-picker v-model="form.put_shelves_date" type="date" value-format="YYYY-MM-DD" placeholder="请选择日期">
		  </el-date-picker>
		</el-form-item>
		<el-form-item label="下架日期" prop="off_shelves_date">
		  <el-date-picker v-model="form.off_shelves_date" type="date" value-format="YYYY-MM-DD" placeholder="请选择日期">
		  </el-date-picker>
		</el-form-item>
		<el-form-item label="租约过期时间" prop="expire_datetime">
		  <el-date-picker v-model="form.expire_datetime" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" placeholder="请选择时间">
		  </el-date-picker>
		</el-form-item>
	</div>
</div>

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
        form:"",
    },
    data () {
        return {
            idc: '',
            serverGroup: '',
            credential: '',
            serverDetailVisible: false,
            diskDetail: "",
            formRules: {
              idc: [
                  {required: true, message: '请选择IDC机房', trigger: 'change'},
              ],
              server_group: [
                  {required: true, message: '请选择主机分组', trigger: 'change'},
              ],
              name: [
                  {required: true, message: '请输入机器名称', trigger: 'blur'},
                  {min: 2, message: '主机名长度应不小于2个字符', trigger: 'blur'}
              ],
              hostname: [
                  {required: true, message: '请输入主机名称', trigger: 'blur'},
                  {min: 4, message: '主机名长度不小于4个字符', trigger: 'blur'}
              ],
              ssh_ip: [
                  {required: true, message: '请输入SSH IP地址', trigger: 'blur'},
                  {min: 7, message: '主机名长度不小于8个字符', trigger: 'blur'}
              ],
              ssh_port: [
                  {required: true, message: '请输入SSH端口', trigger: 'blur'},
                  // {min: 2, message: 'SSH端口长度不小于2个数字', trigger: 'blur'},
                  // {type: 'number', message: 'SSH端口必须是数字', trigger: 'blur'}
              ],
              credential_id: [
                  {required: true, message: '请选择SSH连接凭据', trigger: 'change'},
              ],
            },
        }
    },
    methods: {
        dialogClose(){
            this.$emit("update:visible", false)  // 触发父组件
            this.$parent.getData();
        },
        submit() {
            this.$refs.formRef.validate((valid) => {
              if (valid) { 
                this.$http.put('/cmdb/server/' + this.form.id + '/', this.form)
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
        getCredential() {
            this.$http.get('/config/credential/?page_size=50')
                .then(res => {
                    this.credential = res.data.data;
                });
        },
    },
    // 监听窗口打开，
    watch: {
      visible(){
        if (this.visible){
        this.form.idc = this.form.idc.id;
        const group = this.form.server_group;
        this.form.server_group = [];
        for(let i in group){
          this.form.server_group.push(group[i].id)
        }
        this.diskDetail = JSON.stringify(this.form.disk);
        this.getIdc();
        this.getServerGroup();
        this.getCredential();
        }
      },
    },
}

</script>

<style scoped>

</style>