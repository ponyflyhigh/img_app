<template>
  <view class="home">
    <!-- 轮播图 -->
    <view class="uni-margin-wrap">
      <swiper class="swiper-container" :circular="true" :indicator-dots="indicatorDots" :autoplay="autoplay" :interval="interval" :duration="duration">
        <swiper-item v-for="(img, index) in swiperImages" :key="index">
          <view class="image-wrapper">
            <view v-if="isLoading[index]" class="loading-placeholder">
              <text>加载中...</text>
            </view>
            <image 
              class="swiper-image" 
              :src="img" 
              mode="aspectFill"
              @error="handleImageError(index)"
              @load="handleImageLoad(index)"
              v-show="!isLoading[index]"
            ></image>
            <view v-if="imageLoadErrors[index]" class="error-placeholder">
              <text>图片加载失败</text>
            </view>
          </view>
        </swiper-item>
      </swiper>
    </view>
    <!-- 导航栏 -->
    <NavigationBar />
    <!-- 头条优先 -->
    <Headline />
    <!-- 热门专辑 -->
      <CommonTitle />
      
    <!-- 分类标签 -->
    <Categories @category-change="handleCategoryChange" />
  </view>
</template>

<script setup>
import { ref } from 'vue'
// 导入组件
import NavigationBar from '@/components/NavigationBar.vue'
import Headline from '@/components/Headline.vue'
// 使用与其他组件一致的路径格式
import CommonTitle from '@/components/CommonTitle/CommonTitle.vue'
import Categories from '@/components/Categories.vue'

// 轮播图相关响应式数据
const swiperImages = ref([
  '/static/swiper/1.jpg',
  '/static/swiper/2.jpg',
  '/static/swiper/3.jpg'
])
const indicatorDots = ref(true)
const autoplay = ref(true)
const interval = ref(3000)
const duration = ref(500)
const imageLoadErrors = ref([false, false, false])
const isLoading = ref([true, true, true])

// 处理图片加载错误的方法
const handleImageError = (index) => {
  console.error(`图片 ${index + 1} 加载失败`)
  imageLoadErrors.value[index] = true
  isLoading.value[index] = false
}

// 处理图片加载成功的方法
const handleImageLoad = (index) => {
  console.log(`图片 ${index + 1} 加载成功`)
  isLoading.value[index] = false
}

// 分类相关响应式数据和方法
const currentCategory = ref('精选')
const handleCategoryChange = (category) => {
  console.log(`Selected category: ${category}`)
  currentCategory.value = category
  // 这里可以添加加载新分类数据的逻辑
}
</script>

<style scoped>
.uni-margin-wrap {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
}

.swiper-container {
  height: 300rpx;
  border-radius: 12rpx;
  overflow: hidden;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
  border: 1rpx solid #eaeaea;
}

.image-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}

.swiper-image {
  width: 100%;
  height: 100%;
  display: block;
}

.error-placeholder, .loading-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #f5f5f5;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #999;
  font-size: 14px;
}

.home {
  padding: 10px;
}

</style>