<template>
<view class="notice">
<view class="left">
<uni-icons type="sound-filled" size="30" ></uni-icons>
<text class="text">公告</text>
</view>
<view class="center">
<swiper vertical autoplay interval="1500" duration="300" circulary>
<swiper-item v-for="item in 4">文字内容</swiper-item>
</swiper>
</view>

<view class="right"></view>
<uni-icons type="right" size="16"></uni-icons>

</view>
</template>

<script>
export default {
  data() {
    return {
      // 轮播的标题数据
      headlines: [
        { tag: '头条优先', title: '这组壁纸，太绝了！！' },
        { tag: '最新', title: '探索未知的世界！' },
        { tag: '热点', title: '全新科技，震撼发布！' }
      ]
    };
  }
};
</script>

<style scoped>
.headline-carousel {
  background-color: #f8f8f8;
  padding: 10px 20px;
  margin-bottom: 20px;
  border-radius: 10px;
  font-size: 16px;
  color: #333;
}
.headline-item {
  display: flex;
  align-items: center;
}
.tag {
  background-color: #ccc;
  color: white;
  padding: 3px 8px;
  border-radius: 5px;
  margin-right: 10px;
}
.title {
  font-weight: bold;
}
.notice {
  width: 340px;
  height: 30px;
  background-color: #b9b1b1;
  margin: 0 auto;
  border-radius: 80px;
  display: flex;
  .left{
  width:140rpx;
  display: flex;
  align-items: center;
  justify-content:center;
  .text{
    font-size: 14px;
    color: #1df1e0;}
  }
  .center{
   flex: 1;
  }
  .right{
    width:140rpx;
    display: flex;
    align-items: center;
    justify-content:center;
  }
  .text{
    font-size: 14px;
    color: #fff;
  }
  .uni-icons{
    color: #fff;
  }
}
</style>