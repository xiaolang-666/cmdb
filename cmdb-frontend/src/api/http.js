import axios from "axios";
import {ElMessage}  from "element-plus";

// 创建实例
const instance = axios.create({
  baseURL: "http://127.0.0.1:9090/api",
  timeout: 6000,
});

// 请求拦截器
instance.interceptors.request.use(
  (config) => {
      const token = window.sessionStorage.getItem('token');
      if(token) {
          config.headers = {
              'Authorization': 'token ' + token
          }
      }
      return config
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
instance.interceptors.response.use(
  (res) => {
    // 在响应后做些什么
    if (res.data.code != 200) {
      // 这里根据后端返回消息显示
      // console.log("服务器异常")
      ElMessage.warning(res.data.msg)
    }
    return res;
  },
  (error) => {
    // console.log(error);
    ElMessage.error("请求服务接口错误！");
    return Promise.reject(error);
  }
);

export default instance;