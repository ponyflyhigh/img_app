<template>
  <view class="album">
    <view class="album-header">
      <text class="album-title">热门专辑</text>
      <navigator url="#" class="more-link">更多 ></navigator>
    </view>
    <!-- 将水平滚动内容移出 swiper 组件 -->
    <view class="select">
      <view class="content">
        <scroll-view scroll-x>
          <view class="box" v-for="(item, index) in 5" :key="index">
            <image src="/static/images/classify1.jpg" mode="aspectFill"></image>
          </view>
        </scroll-view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      albums: [
        { id: 1, cover: '/static/images/album1.jpg' },
        { id: 2, cover: '/static/images/album2.jpg' },
        { id: 3, cover: '/static/images/album3.jpg' },
        { id: 4, cover: '/static/images/album4.jpg' }
      ]
    };
  }
};
</script>

<style scoped>
.album {
  margin-bottom: 15px;
  padding: 0 10px;
}

.album-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2px;
}

.album-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.more-link {
  color: #666;
  font-size: 12px;
}

.album-swiper {
  height: 150px; /* 减小竖向轮播图高度 */
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}

.album-item {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.album-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.select {
  padding-top: 5px;
}

.content {
  width: 100%;
  margin-top: 10px;
}

scroll-view {
  white-space: nowrap;
}

.box {
  width: 100px; /* 减小水平滚动卡片宽度 */
  height: 200px; /* 减小水平滚动卡片高度 */
  display: inline-block;
  margin-right: 8px; /* 减小卡片间距 */
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.box image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>