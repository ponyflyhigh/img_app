<template>
    <div class="login-container">
      <div class="login-box">
        <h1>账号登录</h1>
        <p>智能服务 · 开启体验</p>
  
        <!-- 选择登录方式 -->
        <div class="method-selector">
          <button 
            :class="{ 'active': loginMethod === 'phone' }" 
            @click="setLoginMethod('phone')"
          >
            手机号
          </button>
          <button 
            :class="{ 'active': loginMethod === 'email' }" 
            @click="setLoginMethod('email')"
          >
            邮箱
          </button>
        </div>
  
        <form @submit.prevent="handleLogin">
          <!-- 手机号登录 -->
          <div v-if="loginMethod === 'phone'">
            <div class="form-item">
              <label>手机号</label>
              <input type="tel" v-model="phone" placeholder="请输入手机号">
              <p class="error-message" v-if="errors.phone">{{ errors.phone }}</p>
            </div>
          </div>
  
          <!-- 邮箱登录 -->
          <div v-if="loginMethod === 'email'">
            <div class="form-item">
              <label>邮箱</label>
              <input type="email" v-model="email" placeholder="请输入邮箱">
              <p class="error-message" v-if="errors.email">{{ errors.email }}</p>
            </div>
          </div>
  
          <div class="form-item">
            <label>登录密码</label>
            <input type="password" v-model="password" placeholder="请输入密码">
            <p class="error-message" v-if="errors.password">{{ errors.password }}</p>
          </div>
  
          <button type="submit" class="submit-btn" :disabled="loading">
            {{ loading ? '登录中...' : '立即登录' }}
          </button>
  
          <p class="register-link">
            <navigator url="/pages/register/register">没有账号？立即注册</navigator>
          </p>
  
          <p class="hint">本系统基于人工智能技术，仅供参考，重大决定请谨慎</p>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';

  // 登录状态和数据
  const loginMethod = ref('phone');
  const phone = ref('');
  const email = ref('');
  const password = ref('');
  const loading = ref(false);
  const errors = ref({
    phone: '',
    email: '',
    password: ''
  });
  const apiBaseUrl = ref('http://localhost:5000/api');
  
  // 工具函数
  const validatePhone = (phone) => {
    return /^1[3-9]\d{9}$/.test(phone);
  };
  
  const validateEmail = (email) => {
    return /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email);
  };
  
  const showToast = (message, icon = 'none') => {
    uni.showToast({
      title: message,
      icon: icon,
      duration: 2000
    });
  };
  
  // 处理登录方法切换
  const setLoginMethod = (method) => {
    loginMethod.value = method;
    resetErrors();
  };
  
  // 重置错误信息
  const resetErrors = () => {
    errors.value = {
      phone: '',
      email: '',
      password: ''
    };
  };
  
  // 处理登录提交
  const handleLogin = async () => {
    resetErrors();
    let isValid = true;

    // 表单验证
    if (loginMethod.value === 'phone') {
      if (!phone.value) {
        errors.value.phone = '请输入手机号';
        isValid = false;
      } else if (!validatePhone(phone.value)) {
        errors.value.phone = '请输入有效的手机号';
        isValid = false;
      }
    } else {
      if (!email.value) {
        errors.value.email = '请输入邮箱';
        isValid = false;
      } else if (!validateEmail(email.value)) {
        errors.value.email = '请输入有效的邮箱地址';
        isValid = false;
      }
    }

    if (!password.value) {
      errors.value.password = '请输入密码';
      isValid = false;
    } else if (password.value.length < 6) {
      errors.value.password = '密码长度至少6位';
      isValid = false;
    }

    // 如果验证不通过，显示第一条错误信息
    if (!isValid) {
      const firstError = Object.values(errors.value).find(msg => msg);
      if (firstError) {
        showToast(firstError, 'none');
      }
      return;
    }

    loading.value = true;

    try {
      let response, data;

      if (loginMethod.value === 'phone') {
        response = await uni.request({
          url: `${apiBaseUrl.value}/login_by_phone`,
          method: 'POST',
          header: {
            'Content-Type': 'application/json'
          },
          data: {
            phone: phone.value,
            password: password.value
          }
        });
      } else {
        response = await uni.request({
          url: `${apiBaseUrl.value}/login_by_email`,
          method: 'POST',
          header: {
            'Content-Type': 'application/json'
          },
          data: {
            email: email.value,
            password: password.value
          }
        });
      }

      data = response.data;

      if (response.statusCode === 200) {
        showToast('登录成功','success');
        uni.setStorageSync('token', data.data.token);
        setTimeout(() => {
          uni.switchTab({
            url: '/pages/index/index'
          });
        }, 1500);
      } else {
        if (data.message) {
          if (data.message.includes('手机号') || data.message.includes('邮箱')) {
            loginMethod.value === 'phone' 
              ? errors.value.phone = data.message 
              : errors.value.email = data.message;
          } else if (data.message.includes('密码')) {
            errors.value.password = data.message;
          } else {
            showToast(data.message, 'none');
          }
        } else {
          showToast('登录失败', 'none');
        }
      }
    } catch (error) {
      console.error('登录出错:', error);
      showToast('网络错误，请稍后重试', 'none');
    } finally {
      loading.value = false;
    }
  };
  </script>
  
  <style scoped>
  .login-container {
    width: 100%;
    min-height: 100vh;
    background-color: #1c1c1c;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40rpx;
    box-sizing: border-box;
  }
  
  .login-box {
    width: 680rpx;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 16rpx;
    padding: 60rpx 40rpx;
    box-sizing: border-box;
  }
  
  h1 {
    font-size: 36rpx;
    font-weight: bold;
    color: #fff;
    text-align: center;
    margin-bottom: 20rpx;
  }
  
  p {
    font-size: 24rpx;
    color: #999;
    text-align: center;
    margin-bottom: 40rpx;
  }
  
  .method-selector {
    display: flex;
    justify-content: center;
    margin-bottom: 40rpx;
  }
  
  .method-selector button {
    width: 200rpx;
    height: 80rpx;
    background-color: #333;
    color: #fff;
    border: none;
    font-size: 28rpx;
    margin: 0 10rpx;
    border-radius: 8rpx;
  }
  
  .method-selector button.active {
    background-color: #e5b165;
    color: #1c1c1c;
  }
  
  .form-item {
    margin-bottom: 30rpx;
  }
  
  .form-item label {
    display: block;
    font-size: 28rpx;
    color: #fff;
    margin-bottom: 10rpx;
  }
  
  .form-item input {
    width: 100%;
    height: 88rpx;
    background-color: #333;
    border-radius: 8rpx;
    padding: 0 20rpx;
    box-sizing: border-box;
    font-size: 28rpx;
    color: #fff;
  }
  
  .error-message {
    color: #ff6b6b;
    text-align: left;
    margin-top: 5rpx;
    font-size: 24rpx;
  }
  
  .submit-btn {
    width: 100%;
    height: 96rpx;
    background-color: #e5b165;
    color: #1c1c1c;
    border-radius: 8rpx;
    text-align: center;
    line-height: 96rpx;
    font-size: 32rpx;
    font-weight: bold;
    margin-top: 40rpx;
    border: none;
  }
  
  .submit-btn:disabled {
    background-color: #999;
    color: #fff;
    cursor: not-allowed;
  }
  
  .register-link {
    margin-top: 30rpx;
    text-align: center;
  }
  
  .register-link navigator {
    font-size: 28rpx;
    color: #e5b165;
    text-decoration: underline;
  }
  
  .hint {
    margin-top: 40rpx;
    text-align: center;
    font-size: 24rpx;
    color: #999;
  }
  </style> 