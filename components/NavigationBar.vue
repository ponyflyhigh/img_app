<template>
  <view class="navigation-bar">
    <navigator v-for="item in navItems" :key="item.title" :url="item.url">
      <image :src="item.icon" class="nav-icon"></image>
      <text class="nav-title">{{ item.title }}</text>
    </navigator>
  </view>
</template>

<script>
export default {
  data() {
    return {
      navItems: [
        { title: '聊天背景', icon: '/static/swiper/人像.png', url: '/pages/req/req' },
        { title: '头像', icon: '/static/swiper/人像.png', url: '#' },
        { title: '表情', icon: '/static/swiper/人像.png', url: '#' },
        { title: '头像挂件', icon: '/static/swiper/人像.png', url: '#' }
      ]
    };
  }
};
</script>

<style scoped>
.navigation-bar {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 20px;
}

.navigator {
  text-decoration: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: inherit;
}

.nav-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-bottom: 5px;
}

.nav-title {
  font-size: 14px;
}
</style>