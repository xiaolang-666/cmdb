<template>
  <md-editor id="editor"
    :sanitize="sanitize"
    @onSave="onSave"
    @config="config"
    v-model="text" />
  <div v-html="html"></div>
</template>

<script setup>
import TurndownService from 'turndown';
import {ElMessage}  from "element-plus";
import { ref } from 'vue'; // 引入 Vue 3 的 ref 函数，用于定义响应式变量。
import MdEditor from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
import sanitizeHtml from 'sanitize-html'; // 防止xss攻击 自动过滤不安全的内容
import http from "../../api/http"


const sanitize = (html) => sanitizeHtml(html);
const text = ref(''); // 定义 text 和 html 两个响应式变量，分别用于保存文本和 HTML 内容。
const html = ref('');
const config = {
  toc: true,
  tocFolded: true
};

//定义 onSave 事件处理函数，它接收两个参数 v 和 h，
// v 是编辑器中的文本内容，h 是一个 Promise 对象，它在解析编辑器中的 Markdown 文本后返回一个 HTML 字符串。在函数中，首先打印 v，然后等待 h 解析完成，并将解析后的 HTML 字符串传递给 saveData 函数
const onSave = (v, h) => {
  h.then((html) => {
    saveData(html);
  });
};


//定义 fetchData 异步函数，用于从服务器获取 HTML 内容，并将其保存在 html 变量中。如果发生错误，则打印错误信息
// const fetchData = async () => {
//   try {
//     const response = await http.get('/document/iiot/1/');
//     html.value = response.data.note;
//   } catch (error) {
//     ElMessage.error("请求服务接口错误！");
//     return Promise.reject(error);
//   }
// };
const fetchData = () => {
  http.get('/document/iiot/1/').then(
    res => {
      if (res.data.code==200){
        const turndownService = new TurndownService();
        const markdown = turndownService.turndown(res.data.data.note);
        text.value=markdown
      }
    }
  )
}

//定义 saveData 异步函数，用于将 HTML 内容发送到服务器进行保存。如果发生错误，则打印错误信息
// const saveData = async (html) => {
//   try {
//     const response = await http.put('/document/iiot/1/', form);
//     console.log(form)
//     if (response.data.code == 200){
//       ElMessage.success(response.data,msg)
//     }
//   } catch (error) {
//     ElMessage.error("请求服务接口错误！");
//     return Promise.reject(error);
//   }
// };
const saveData = (html) => {
  http.put('/document/iiot/1/', {name: "iiot_document", "note": html}).then(
    res => {
      if (res.data.code==200){
        ElMessage.success(res.data.msg)
      }
    }
  )
};


//定义 mounted 函数，用于在组件挂载后调用 fetchData 函数，以获取并显示服务器上的 HTML 内容。
const mounted = () => {
  fetchData();
};


//定义 setup 函数，用于将 text、html 和 onSave 绑定到组件实例上，并将它们作为返回值。
const setup = () => {
  return {
    text,
    html,
    sanitize,
    onSave,
    config,
    fetchData,
  };
};

mounted()
</script>

<style scoped>
#editor {
  height: 100%;
  margin: 0;
  padding: 0;
}

#editor {
  box-sizing: border-box;
}
</style>
