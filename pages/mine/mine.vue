<template>
  <view class="user-container pageBg">
    <!-- 背景渐变容器 -->
    
    <!-- 内容容器 -->
    <view class="content-container">
      <view class="userInfo">
        <view class="avatar">
          <image src="/static/images/classify1.jpg" mode="aspectFill"></image>
        </view>
        <view class="ip">100.100.100.100</view>
        <view class="address">来自于:{{ address }}</view>
      </view>
      
      <!-- 功能列表 -->
      <view class="function-list">
        <navigator url="/pages/mine/userInfo" class="function-item">
          <text>完善资料</text>
        </navigator>
        <navigator url="/pages/mine/charge" class="function-item">
          <text>支付设置</text>
        </navigator>
        <navigator url="/pages/mine/chargeOut" class="function-item">
          <text>海外支付设置</text>
        </navigator>
        <view class="function-item" @click="openLocation">
          <text>查看位置</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue';
import { onLoad } from '@dcloudio/uni-app';

// 新增地址变量
const address = ref('山东');

const openLocation = () => {
  uni.getLocation({
    type: 'gcj02',
    geocode: true, // 启用地址解析
    success: function (res) {
      const latitude = res.latitude;
      const longitude = res.longitude;
      // 获取地址信息
      if (res.address) {
        address.value = res.address;
      } else {
        address.value = '未知地址';
      }
      uni.openLocation({
        latitude: latitude,
        longitude: longitude,
        success: function () {
          console.log('success');
        }
      });
    },
    fail: function () {
      address.value = '无法获取地址';
    }
  });
};

// 页面加载时执行
onLoad(() => {
  console.log('mine页面加载');
});
</script>

<style lang="scss">
.user-container {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
}

.bg-gradient {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    linear-gradient(to bottom, rgba(0,0,0,0), #fff),
    linear-gradient(to right, red, green);
  z-index: 1;
}

.content-container {
  position: relative;
  z-index: 2;
  padding: 20px;
}

.userInfo {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.8); /* 添加半透明背景使内容更清晰 */
  border-radius: 10px;
  margin-bottom: 20px;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-right: 15px;
  background-color: #e0e0e0;
  overflow: hidden; /* 确保图片不会超出圆形边界 */
  
  image {
    width: 100%;
    height: 100%;
    object-fit: cover; /* 使用 object-fit 确保图片正确填充 */
  }
}

.ip {
  font-size: 12px;
  color: #999;
  margin-top: 10px;
}

.address {
  font-size: 14px;
  color: #333;
  margin-top: 5px;
}

.function-list {
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  overflow: hidden; /* 确保圆角生效 */
}

.function-item {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  font-size: 16px;
  color: #333;
}

.function-item:last-child {
  border-bottom: none;
}
</style>