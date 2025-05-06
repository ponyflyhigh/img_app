<template>
  <view class="theme">
    <view class="title">
      <text class="title-text">专题精选</text>

        <navigator url="#" class="more-link">更多 ></navigator>
    </view>
    <view class="themeItem">
    <navigator url="" class="box" v-if="!isMore">
      <view class="mask">明星美女</view>
      <view class="tab">3天前更新</view>
      <image class="pic" src="/static/images/preview1.jpg" mode="aspectFill"></image>
      
    </navigator>
    <navigator url="" class="box more" v-if="isMore">
      <image class="pic" src="/static/images/preview1.jpg" mode="aspectFill"></image>
      <view class="mask">
        <uni-icons type="more-filled" size="34" color="#fff"></uni-icons>
        <view class="text">更多</view>
      </view>
    </navigator>
  </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      categories: [0, 1, 2, 3, 4, 5, 6, 7] // 控制渲染 8 个 theme-item
    };
  }
};
</script>

<style scoped>
/* 可按需添加样式 */
.theme {
  padding: 10px;
}
.title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.title-text {
  font-size: 18px;
}
.more {
  color: #666;
}
.content {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}
</style>