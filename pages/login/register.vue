<template>
  <div class="register-login-container">
    <div class="container">
      <h1>{{ formType === 'login' ? '账号登录' : '账号注册' }}</h1>
      <p>智能服务 · 开启体验</p>

      <!-- 选择登录/注册方式 -->
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

      <form @submit.prevent="handleSubmit">
        <!-- 手机号登录/注册表单 -->
        <div v-if="loginMethod === 'phone'">
          <div class="form-item">
            <label for="phone">手机号</label>
            <input type="tel" id="phone" v-model="phone" placeholder="请输入手机号">
            <p class="error-message" v-if="error.phone">{{ error.phone }}</p>
          </div>

          <div class="form-item code-item" v-if="formType === 'register'">
            <input type="number" id="code" v-model="verificationCode" placeholder="请输入验证码">
            <button class="get-code-btn" :disabled="isCountingDown" @click="getVerificationCode">
              {{ countdown > 0 ? `${countdown}s` : '获取验证码' }}
            </button>
            <p class="error-message" v-if="error.code">{{ error.code }}</p>
          </div>
        </div>

        <!-- 邮箱登录/注册表单 -->
        <div v-if="loginMethod === 'email'">
          <div class="form-item">
            <label for="email">邮箱</label>
            <input type="email" id="email" v-model="email" placeholder="请输入邮箱">
            <p class="error-message" v-if="error.email">{{ error.email }}</p>
          </div>

          <div class="form-item code-item" v-if="formType === 'register'">
            <input type="number" id="emailCode" v-model="emailVerificationCode" placeholder="请输入邮箱验证码">
            <button class="get-code-btn" :disabled="isEmailCountingDown" @click="getEmailVerificationCode">
              {{ emailCountdown > 0 ? `${emailCountdown}s` : '获取验证码' }}
            </button>
            <p class="error-message" v-if="error.emailCode">{{ error.emailCode }}</p>
          </div>
        </div>

        <!-- 通用字段 -->
        <div class="form-item" v-if="formType === 'register'">
          <label for="inviteCode">邀请码（选填）</label>
          <input type="text" id="inviteCode" v-model="inviteCode" placeholder="填写邀请码可获取额外福利">
        </div>

        <div class="form-item" v-if="formType === 'register'">
          <label for="username">账号名</label>
          <input type="text" id="username" v-model="username" placeholder="请输入账号名">
          <p class="error-message" v-if="error.username">{{ error.username }}</p>
        </div>

        <div class="form-item">
          <label for="password">{{ formType === 'login' ? '登录密码' : '设置密码' }}</label>
          <input type="password" id="password" v-model="password" placeholder="请输入密码">
          <p class="error-message" v-if="error.password">{{ error.password }}</p>
        </div>

        <button type="submit" class="submit-btn" :disabled="isLoading">
          {{ isLoading ? (formType === 'login' ? '登录中...' : '注册中...') : (formType === 'login' ? '立即登录' : '立即注册') }}
        </button>

        <p class="login-link" v-if="formType === 'register'">
          <navigator url="/pages/login/login">已有账号？返回登录</navigator>
        </p>

        <p class="login-link" v-if="formType === 'login'">
          <navigator url="/pages/login/register">没有账号？立即注册</navigator>
        </p>

        <p class="hint">本系统基于人工智能技术，仅供参考，重大决定请谨慎</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 数据定义
const loginMethod = ref('phone');
const formType = ref('register');
const phone = ref('');
const email = ref('');
const verificationCode = ref('');
const emailVerificationCode = ref('');
const inviteCode = ref('');
const username = ref('');
const password = ref('');
const countdown = ref(0);
const emailCountdown = ref(0);
const isCountingDown = ref(false);
const isEmailCountingDown = ref(false);
const isLoading = ref(false);
const error = ref({
  phone: '',
  email: '',
  code: '',
  emailCode: '',
  username: '',
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

// 处理登录/注册方式切换
const setLoginMethod = (method) => {
  loginMethod.value = method;
  resetErrors();
};

// 重置错误信息
const resetErrors = () => {
  error.value = {
    phone: '',
    email: '',
    code: '',
    emailCode: '',
    username: '',
    password: ''
  };
};

// 获取手机验证码
const getVerificationCode = async () => {
  error.value.phone = '';
  if (!validatePhone(phone.value)) {
    error.value.phone = '请输入有效的手机号';
    showToast('请输入有效的手机号', 'none');
    return;
  }
  if (isCountingDown.value) return;
  
  try {
    const response = await uni.request({
      url: `${apiBaseUrl.value}/send_sms_code`,
      method: 'POST',
      data: {
        phone: phone.value
      }
    });
    
    const data = response.data;
    if (response.statusCode === 200) {
      isCountingDown.value = true;
      countdown.value = 60;
      
      const timer = setInterval(() => {
        countdown.value--;
        if (countdown.value <= 0) {
          clearInterval(timer);
          isCountingDown.value = false;
        }
      }, 1000);
      
      showToast('验证码已发送，请查收短信', 'success');
    } else {
      error.value.phone = data.message || '验证码发送失败';
      showToast(error.value.phone, 'none');
    }
  } catch (err) {
    console.error('获取手机验证码出错:', err);
    error.value.phone = '网络错误，请稍后重试';
    showToast(error.value.phone, 'none');
  }
};

// 获取邮箱验证码
const getEmailVerificationCode = async () => {
  error.value.email = '';
  if (!validateEmail(email.value)) {
    error.value.email = '请输入有效的邮箱地址';
    showToast('请输入有效的邮箱地址', 'none');
    return;
  }
  if (isEmailCountingDown.value) return;
  
  try {
    const response = await uni.request({
      url: `${apiBaseUrl.value}/email`,
      method: 'POST',
      data: {
        email: email.value
      }
    });
    
    const data = response.data;
    if (response.statusCode === 200) {
      isEmailCountingDown.value = true;
      emailCountdown.value = 60;
      
      const timer = setInterval(() => {
        emailCountdown.value--;
        if (emailCountdown.value <= 0) {
          clearInterval(timer);
          isEmailCountingDown.value = false;
        }
      }, 1000);
      
      showToast('验证码已发送，请查收邮箱', 'success');
    } else {
      error.value.email = data.message || '验证码发送失败';
      showToast(error.value.email, 'none');
    }
  } catch (err) {
    console.error('获取邮箱验证码出错:', err);
    error.value.email = '网络错误，请稍后重试';
    showToast(error.value.email, 'none');
  }
};

// 处理表单提交
const handleSubmit = async () => {
  resetErrors();
  let isValid = true;
  
  // 表单验证
  if (loginMethod.value === 'phone') {
    if (!phone.value) {
      error.value.phone = '请输入手机号';
      isValid = false;
    } else if (!validatePhone(phone.value)) {
      error.value.phone = '请输入有效的手机号';
      isValid = false;
    }
    
    if (formType.value === 'register' && !verificationCode.value) {
      error.value.code = '请输入验证码';
      isValid = false;
    }
  } else if (loginMethod.value === 'email') {
    if (!email.value) {
      error.value.email = '请输入邮箱';
      isValid = false;
    } else if (!validateEmail(email.value)) {
      error.value.email = '请输入有效的邮箱地址';
      isValid = false;
    }
    
    if (formType.value === 'register' && !emailVerificationCode.value) {
      error.value.emailCode = '请输入验证码';
      isValid = false;
    }
  }
  
  if (formType.value === 'register') {
    if (!username.value) {
      error.value.username = '请输入账号名';
      isValid = false;
    }
  }
  
  if (!password.value) {
    error.value.password = '请输入密码';
    isValid = false;
  } else if (password.value.length < 6) {
    error.value.password = '密码长度至少6位';
    isValid = false;
  }
  
  // 如果验证不通过，显示第一条错误信息
  if (!isValid) {
    const firstError = Object.values(error.value).find(msg => msg);
    if (firstError) {
      showToast(firstError, 'none');
    }
    return;
  }
  
  isLoading.value = true;
  
  try {
    let response, data;
    
    // 注册请求
    if (formType.value === 'register') {
      if (loginMethod.value === 'phone') {
        response = await uni.request({
          url: `${apiBaseUrl.value}/register_by_phone`,
          method: 'POST',
          data: {
            phone: phone.value,
            code: verificationCode.value,
            username: username.value,
            password: password.value,
            inviteCode: inviteCode.value
          }
        });
      } else {
        response = await uni.request({
          url: `${apiBaseUrl.value}/register_by_email`,
          method: 'POST',
          data: {
            email: email.value,
            code: emailVerificationCode.value,
            username: username.value,
            password: password.value,
            inviteCode: inviteCode.value
          }
        });
      }
    } 
    // 登录请求
    else {
      if (loginMethod.value === 'phone') {
        response = await uni.request({
          url: `${apiBaseUrl.value}/login_by_phone`,
          method: 'POST',
          data: {
            phone: phone.value,
            password: password.value
          }
        });
      } else {
        response = await uni.request({
          url: `${apiBaseUrl.value}/login_by_email`,
          method: 'POST',
          data: {
            email: email.value,
            password: password.value
          }
        });
      }
    }
    
    data = response.data;
    
    if (response.statusCode === 200) {
      showToast(formType.value === 'register' ? '注册成功' : '登录成功', 'success');
      uni.setStorageSync('token', data.data.token);
      
      setTimeout(() => {
        // 注册成功后跳转到登录页
        if (formType.value === 'register') {
          uni.navigateBack({
            delta: 1,
            success: () => {
              console.log('导航回登录页成功');
            },
            fail: (err) => {
              console.error('导航回登录页失败:', err);
              // 如果navigateBack失败，使用navigateTo
              uni.navigateTo({
                url: '/pages/login/login'
              });
            }
          });
        } 
        // 登录成功后跳转到首页
        else {
          uni.switchTab({
            url: '/pages/index/index'
          });
        }
      }, 1500);
    } else {
      console.error('API响应错误:', response);
      if (data.message) {
        if (data.message.includes('手机号') || data.message.includes('邮箱')) {
          loginMethod.value === 'phone' 
            ? error.value.phone = data.message 
            : error.value.email = data.message;
        } else if (data.message.includes('验证码')) {
          loginMethod.value === 'phone' 
            ? error.value.code = data.message 
            : error.value.emailCode = data.message;
        } else if (data.message.includes('密码')) {
          error.value.password = data.message;
        } else {
          showToast(data.message, 'none');
        }
      } else {
        showToast(formType.value === 'register' ? '注册失败' : '登录失败', 'none');
      }
    }
  } catch (err) {
    console.error(`${formType.value === 'register' ? '注册' : '登录'}出错:`, err);
    showToast('网络错误，请稍后重试', 'none');
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* 样式保持不变 */
</style>  
<style scoped>
.register-login-container {
  width: 100%;
  min-height: 100vh;
  background-color: #1c1c1c;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40rpx;
  box-sizing: border-box;
}

.container {
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

.code-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.code-item input {
  width: 400rpx;
}

.get-code-btn {
  width: 240rpx;
  height: 88rpx;
  background-color: #e5b165;
  color: #1c1c1c;
  border-radius: 8rpx;
  text-align: center;
  line-height: 88rpx;
  font-size: 28rpx;
  border: none;
}

.get-code-btn[disabled] {
  background-color: #999;
  color: #fff;
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

.login-link {
  margin-top: 30rpx;
  text-align: center;
}

.login-link navigator {
  font-size: 28rpx;
  color: #e5b165;
  text-decoration: underline;
  cursor: pointer;
}

.hint {
  margin-top: 40rpx;
  text-align: center;
  font-size: 24rpx;
  color: #999;
}

.error-message {
  color: #ff6b6b;
  text-align: left;
  margin-top: 5rpx;
  font-size: 24rpx;
}
</style>