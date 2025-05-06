<template>
  <view class="container">
    <h1>选择支付方式</h1>

    <!-- 支付方式选择 -->
    <view class="payment-methods">
      <view 
        class="payment-method" 
        :class="{ active: selectedPayment === 'wechat' }"
        @click="selectPayment('wechat')"
      >
        <image 
          class="payment-icon" 
          src="https://picsum.photos/30/30?random=1" 
          mode="aspectFill"
        ></image>
        微信支付
      </view>
      <view 
        class="payment-method" 
        :class="{ active: selectedPayment === 'alipay' }"
        @click="selectPayment('alipay')"
      >
        <image 
          class="payment-icon" 
          src="https://picsum.photos/30/30?random=2" 
          mode="aspectFill"
        ></image>
        支付宝
      </view>
    </view>

    <!-- 充值金额选择 -->
    <view class="amount-choice">
      <text>选择充值金额：</text>
      <view class="amounts">
        <view 
          v-for="(amount, index) in amounts" 
          :key="index" 
          class="amount-item" 
          :class="{ active: selectedAmount === amount }"
          @click="selectAmount(amount)"
        >
          {{ amount }}元
        </view>
      </view>
      <view class="custom-amount">
        <input 
          type="text" 
          placeholder="自定义金额" 
          v-model="customAmount" 
          @input="onCustomAmountInput"
        />
      </view>
    </view>

    <!-- 微信支付二维码区域 -->
    <view class="qrcode-area" :class="{ active: selectedPayment === 'wechat' && (selectedAmount > 0 || customAmount > 0) }">
      <view class="qrcode-container">
        <image 
          class="qrcode-image" 
          src="https://picsum.photos/200/200?random=3" 
          mode="aspectFill"
        ></image>
        <text>请使用微信扫描二维码支付</text>
      </view>
    </view>

    <!-- 支付宝二维码区域 -->
    <view class="qrcode-area" :class="{ active: selectedPayment === 'alipay' && (selectedAmount > 0 || customAmount > 0) }">
      <view class="qrcode-container">
        <image 
          class="qrcode-image" 
          src="https://picsum.photos/200/200?random=4" 
          mode="aspectFill"
        ></image>
        <text>请使用支付宝扫描二维码支付</text>
      </view>
    </view>

    <!-- 支付按钮 -->
    <button class="pay-button" @click="confirmPayment">确认支付</button>

    <!-- 支付状态提示 -->
    <view class="payment-status">
      <text>支付完成前请不要关闭此页面</text>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue';
import { onLoad } from '@dcloudio/uni-app';

// 支付方式选择（wechat-微信，alipay-支付宝）
const selectedPayment = ref('wechat');

// 金额选择相关
const amounts = ref([10, 20, 50, 100]);
const selectedAmount = ref(10);
const customAmount = ref('');

// 页面加载时执行
onLoad(() => {
  console.log('充值页面加载');
});

// 选择支付方式
const selectPayment = (paymentMethod) => {
  selectedPayment.value = paymentMethod;
};

// 选择充值金额
const selectAmount = (amount) => {
  selectedAmount.value = amount;
  customAmount.value = '';
};

// 自定义金额输入处理
const onCustomAmountInput = () => {
  // 如果输入了自定义金额，则清空固定金额选择
  if (customAmount.value) {
    selectedAmount.value = 0;
  }
};

// 确认支付


const confirmPayment = async () => {
  let amount = selectedAmount.value;
  if (customAmount.value) {
    amount = parseFloat(customAmount.value);
  }
  if (selectedPayment.value === 'wechat') {
    const response = await uni.request({
      url: 'http://localhost:3000/wechat/pay',
      method: 'POST',
      data: { amount }
    });
    // 处理微信支付响应，展示二维码
    const qrcodeUrl = response.data.code_url;
    // 这里可以更新二维码图片的src
  } else if (selectedPayment.value === 'alipay') {
    uni.redirectTo({
      url: `/pages/alipay/alipay?amount=${amount}`
    });
  }
};
</script>

<style scoped>
.container {
  max-width: 400px;
  margin: 0 auto;
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

h1 {
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

/* 支付方式选择 */
.payment-methods {
  display: flex;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  overflow: hidden;
}

.payment-method {
  flex: 1;
  text-align: center;
  padding: 10px;
  cursor: pointer;
  background-color: white;
  transition: background-color 0.3s;
}

.payment-method.active {
  background-color: #07c160;
  color: white;
}

.payment-icon {
  width: 30px;
  height: 30px;
  vertical-align: middle;
  margin-right: 5px;
}

/* 充值金额选择 */
.amount-choice {
  margin: 20px 0;
}

.amounts {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-top: 10px;
}

.amount-item {
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.amount-item:hover {
  border-color: #07c160;
}

.amount-item.active {
  background-color: #07c160;
  color: white;
  border-color: #07c160;
}

/* 自定义金额输入 */
.custom-amount {
  margin-top: 15px;
}

.custom-amount input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

/* 二维码区域 */
.qrcode-area {
  margin: 20px 0;
  text-align: center;
  display: none;
}

.qrcode-area.active {
  display: block;
}

.qrcode-container {
  background-color: white;
  padding: 15px;
  border-radius: 10px;
  display: inline-block;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.qrcode-image {
  width: 200px;
  height: 200px;
  background-color: #eee;
  margin-bottom: 10px;
}

/* 支付按钮 */
.pay-button {
  background-color: #07c160;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  font-size: 16px;
  margin-top: 20px;
}

/* 支付状态提示 */
.payment-status {
  margin-top: 15px;
  text-align: center;
  color: #666;
}
</style>