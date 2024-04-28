<template>
  <div v-if="!isRegistering" class="login-box">
    <h2>Register</h2>
    <form @submit.prevent="submitRegister">
      <!-- 注册表单内容 -->
      <div class="user-box">
        <input type="text" v-model="phone" required>
        <label>Phone</label>
      </div>
      <div class="user-box">
        <input type="password" v-model="password" required>
        <label>Password</label>
      </div>
      <a href="#" @click="submitRegister">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        Register
      </a>
      <p>
        <a href="#" @click="toggleRegister" class="no-style">Already have an account?</a>
      </p>
    </form>
  </div>

  <div v-else class="login-box">
    <h2>Login</h2>
    <form @submit.prevent="submitForm">
      <!-- 登录表单内容 -->
      <div class="user-box">
        <input type="text" v-model="phone" required>
        <label>Phone</label>
      </div>
      <div class="user-box">
        <input type="password" v-model="password" required>
        <label>Password</label>
      </div>
      <a href="#" @click="submitForm">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        Login
      </a>
      <p>
        <a href="#" @click="toggleRegister" class="no-style">Don't have an account?</a>
      </p>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      phone: '',
      password: '',
      isRegistering: false, // 切换注册和登录的标识
    };
  },
  methods: {
    submitForm() {
      // 登录逻辑...
      console.log("Form submitted:", this.phone, this.password);
      // 不为空校验
      if (!this.phone || !this.password) {
        alert('Please fill in all fields.');
        return;
      }

      // 构造要发送的数据对象
      const formData = {
        phone: this.phone,
        password: this.password,
      };

      // 发送 POST 请求到服务器
      axios.post('http://127.0.0.1:3000/login', formData)
          .then(response => {
            // 处理服务器响应
            console.log('Server response:', response);
            // 如果response.data部委空且返回数据中的password字段与当前用户一样，则登录成功
            if (response.data.length > 0 && response.data[0].password === this.password) {
              // 登录成功，跳转到首页
              this.$router.push('/pageChoice');
              // 给出提示
              alert('Login successful.');
            } else {
              // 登录失败，给出提示
              alert('Password or PhoneNumber Error! Please try again.');
            }
            // 清空表单数据
            this.phone = '';
            this.password = '';
          })
          .catch(error => {
            // 处理错误
            console.error('Error:', error);
            // 前端给出提示
            alert('Login failed. Please try again.');
          });
    },
    submitRegister() {
      console.log("Register form submitted:", this.phone, this.password);
      // 确保phone和password字段不为空
      if (!this.phone || !this.password) {
        alert('Phone and password are required.');
        return;
      }

      // 准备发送到后端的数据
      const userData = {
        phone: this.phone,
        password: this.password,
      };

      // 使用axios发送POST请求到注册API
      axios.post('http://127.0.0.1:3000/register', userData)
          .then(response => {
            // 这里处理成功的响应
            console.log(response.data);
            // 可能你需要在成功后做些事情，例如跳转到登录页面
            // 登录成功，跳转到首页
            this.$router.push('/pageChoice');
            // 给出提示
            alert('Register and Login successfully.');
          })
          .catch(error => {
            // 处理错误的响应
            console.error(error.response.data);
            alert(error.response.data.message);  // 假设后端会返回一个包含错误信息的message字段
          });
    },
    toggleRegister() {
      this.isRegistering = !this.isRegistering;
    }
  },
};
</script>

<style scoped>
html {
  height: 100%;
}

body {
  margin: 0;
  padding: 0;
  font-family: sans-serif;
  background: linear-gradient(#141e30, #243b55);
}

.no-style {
  color: inherit;
  text-decoration: none;
}

.aa {
  display: flex;
  flex-grow: 1;
  overflow: hidden;
}

.login-box {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 400px;
  padding: 40px;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 128, 0.8);
  box-sizing: border-box;
  box-shadow: 0 15px 25px rgba(0, 0, 0, .6);
  border-radius: 10px;
}

.login-box h2 {
  margin: 0 0 30px;
  padding: 0;
  color: #fff;
  text-align: center;
}

.login-box .user-box {
  position: relative;
}

.login-box .user-box input {
  width: 100%;
  padding: 10px 0;
  font-size: 16px;
  color: #fff;
  margin-bottom: 30px;
  border: none;
  border-bottom: 1px solid #fff;
  outline: none;
  background: transparent;
}

.login-box .user-box label {
  position: absolute;
  top: 0;
  left: 0;
  padding: 10px 0;
  font-size: 16px;
  color: #fff;
  pointer-events: none;
  transition: .5s;
}

.login-box .user-box input:focus ~ label,
.login-box .user-box input:valid ~ label {
  top: -20px;
  left: 0;
  color: #03e9f4;
  font-size: 12px;
}

.login-box form a {
  position: relative;
  display: inline-block;
  padding: 10px 20px;
  color: #03e9f4;
  font-size: 16px;
  text-decoration: none;
  text-transform: uppercase;
  overflow: hidden;
  transition: .5s;
  margin-top: 40px;
  letter-spacing: 4px
}

.login-box a:hover {
  background: #03e9f4;
  color: #fff;
  border-radius: 5px;
  box-shadow: 0 0 5px #03e9f4,
  0 0 25px #03e9f4,
  0 0 50px #03e9f4,
  0 0 100px #03e9f4;
}

.login-box a span {
  position: absolute;
  display: block;
}

.login-box a span:nth-child(1) {
  top: 0;
  left: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #03e9f4);
  animation: btn-anim1 1s linear infinite;
}

@keyframes btn-anim1 {
  0% {
    left: -100%;
  }
  50%, 100% {
    left: 100%;
  }
}

.login-box a span:nth-child(2) {
  top: -100%;
  right: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(180deg, transparent, #03e9f4);
  animation: btn-anim2 1s linear infinite;
  animation-delay: .25s
}

@keyframes btn-anim2 {
  0% {
    top: -100%;
  }
  50%, 100% {
    top: 100%;
  }
}

.login-box a span:nth-child(3) {
  bottom: 0;
  right: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(270deg, transparent, #03e9f4);
  animation: btn-anim3 1s linear infinite;
  animation-delay: .5s
}

@keyframes btn-anim3 {
  0% {
    right: -100%;
  }
  50%, 100% {
    right: 100%;
  }
}

.login-box a span:nth-child(4) {
  bottom: -100%;
  left: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(360deg, transparent, #03e9f4);
  animation: btn-anim4 1s linear infinite;
  animation-delay: .75s
}

@keyframes btn-anim4 {
  0% {
    bottom: -100%;
  }
  50%, 100% {
    bottom: 100%;
  }
}
</style>
