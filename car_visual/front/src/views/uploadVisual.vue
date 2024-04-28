<template>
  <div class="min-h-screen">
    <div class="container flex flex-col items-center mx-auto px-6 py-30 ">
      <div class="upload-box mb-8">
        <button class="button-effect" @click="openFileDialog">上传文件</button>
        <span class="file-status">{{ fileStatusMessage }}</span>
        <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none"
               accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"/>
      </div>
      <div v-if="dataValid" class="vtable">
        <v-vtable :raw-data="data"></v-vtable>
      </div>
    </div>
  </div>
</template>

<script>
import Papa from 'papaparse'
import * as XLSX from 'xlsx'
import {Message} from "element-ui";
import vTable from "../components/vTable.vue"

export default {
  data() {
    return {
      dataValid: false,
      fileName: '',
      data: []
    }
  },
  components: {
    'v-vtable': vTable,
  },
  computed: {
    fileStatusMessage() {
      return this.dataValid ? `${this.fileName}` : '尚未选择文件';
    },
  },
  methods: {
    openFileDialog() {
      this.$refs.fileInput.click()
    },
    handleFileUpload(event) {
      const file = event.target.files[0]
      if (file) {
        this.fileName = file.name;
        this.parseFile(file)
      } else {
        this.fileName = ''
      }
    },
    parseFile(file) {
      // 根据文件类型选择不同的解析方法
      const fileType = file.type
      const reader = new FileReader()
      reader.onload = (e) => {
        let data
        console.log(fileType)
        if (fileType.includes('csv')) {
          data = Papa.parse(e.target.result, {header: true}).data
        } else if (fileType.includes('sheet') || fileType.includes('excel')) {
          const workbook = XLSX.read(e.target.result, {type: 'binary'})
          const sheetName = workbook.SheetNames
          const worksheet = workbook.Sheets[sheetName]
          data = XLSX.utils.sheet_to_json(worksheet)
        }
        this.validateAndVisualizeData(data)
      }
      if (fileType.includes('csv')) {
        reader.readAsText(file)
      } else if (fileType.includes('sheet') || fileType.includes('excel')) {
        reader.readAsBinaryString(file)
      }
      this.dataValid = true
    },
    validateAndVisualizeData(data) {
      // 检查数据是否包含必要的列
      if (data.length > 0 && "ID" in data[0] && "X" in data[0] && "Y" in data[0]) {
        this.dataValid = true
        this.visualizeData(data)
      } else {
        Message({
          type: 'error',
          message: '文件不包含必要的列!',
        })
        this.dataValid = false
      }
    },
    visualizeData(data) {
      Message({
        type: 'success',
        message: '导入文件成功!',
      })
      // 删去data中id为undefined的元素
      data = data.filter(item => item.ID !== undefined);
      this.data = data
      console.log(data)
    }
  }
}
</script>

<style>

.file-status {
  color: red;
  margin-left: 12px;
}

/* 你的样式代码 */
.upload-box {
  position: absolute;
  top: 15%;
  left: 15%;
  width: 300px;
  transform: translate(-50%, -50%);
  margin-bottom: 2em; /* 你可以根据需要调整这个值 */
}

.vtable {
  margin-top: 150px; /* 你可以根据需要调整这个值 */
}

.button-effect {
  display: inline-block;
  width: 60%; /* 或者任何你想要的宽度 */
  margin: 30px auto 30px auto; /* 这将在按钮的上方和下方各添加30px的间距，总共60px */
  padding: 10px 20px;
  color: #03e9f4;
  font-size: 16px;
  text-decoration: none;
  text-transform: uppercase;
  overflow: hidden;
  transition: .5s;
  letter-spacing: 4px;
  cursor: pointer;
  background: rgba(0, 0, 128, 0.8);
  border: none;
  border-radius: 10px;
  box-shadow: 0 15px 25px rgba(0, 0, 0, .6);
}

.button-effect:hover {
  background: #03e9f4;
  color: #fff;
  border-radius: 5px;
  box-shadow: 0 0 5px #03e9f4,
  0 0 25px #03e9f4,
  0 0 50px #03e9f4,
  0 0 100px #03e9f4;
}

.button-effect span {
  position: absolute;
  display: block;
}

.button-effect span:nth-child(1) {
  top: 0;
  left: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #03e9f4);
  animation: btn-anim1 1s linear infinite;
}

/* Repeat other span styles and keyframes here... */

@keyframes btn-anim1 {
  0% {
    left: -100%;
  }
  50%, 100% {
    left: 100%;
  }
}

/* Repeat other keyframes here... */
</style>