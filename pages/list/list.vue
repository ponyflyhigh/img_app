<template>
	<view class="container">
		<view class="menu">
			<uni-segmented-control :current="current" :values="items" @clickItem="onClickItem" styleType="button" activeColor="#4cd964"></uni-segmented-control>
		</view>
		<view v-if="data.length > 0" class="response-text">
		<view v-for="(item, index) in data" :key="item._id" class="item">
		  <text>序号: {{ index + 1 }}</text>
		  <text>昵称: {{ item.nickname }}</text>

		  <image 
			:src="item.url" 
			:style="{ width: item.imageWidth + 'px', height: item.imageHeight + 'px' }"
			@load="handleImageLoad(index)">
		  </image>
		</view>
		<view v-if="hasMore" class="loading-more" @click="loadMore">加载更多</view>
		<uni-load-more status="loading"></uni-load-more>
	</view>
	  <view v-else class="response-text">
		{{ responseText }}
	  </view>
	  <!-- 导航栏 -->
  
	</view>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue';
  // 定义并初始化 loading 和 responseText
  const loading = ref(false);
  const responseText = ref('点击按钮发送请求');
  // 定义响应式变量来存储获取到的数据
  const data = ref([]);
  // 定义当前页码
  const currentPage = ref(1);
  // 定义是否还有更多数据
  const hasMore = ref(true);
  // 定义当前选中的分段控件索引
  const current = ref(0);
  const items = ['all', 'cat', 'dog'];
  // 定义分段控件的选项列表
const onClickItem = (e) => {
  if (current.value !== e.currentIndex) {
    current.value = e.currentIndex;
    const selectedCategory = items[current.value];
    // 假设后端接受 category 参数来筛选类型
    fetchData(1, selectedCategory);
  }
};


  // 定义网络请求函数
const fetchData = (page = currentPage.value, category = '') => {
  loading.value = true;
  uni.request({
    url: "https://tea.qingnian8.com/tools/petShow",
    method: 'GET',
    data: {
      limit: 5,
      page: page,
      // 假设后端使用 category 参数来筛选类型
      category: category
    },
	header: {
      'access-key': '878293'
    },
    success: (res) => {
      console.log(res.data);
      if (res.statusCode === 200 && res.data.data) {
        if (res.data.data.length === 0) {
          hasMore.value = false;
        } else {
          if (page === 1) {
            data.value = res.data.data;
          } else {
            data.value = [...data.value, ...res.data.data];
          }
        }
      } else {
        responseText.value = '服务器返回错误';
      }
      responseText.value = '请求成功';
    },
    fail: (err) => {
      console.error(err);
      responseText.value = '请求失败，请重试';
    },
    complete: () => {
      loading.value = false;
    }
  });
};
  
  // 组件挂载完成后自动调用 fetchData 函数
  onMounted(() => {
    fetchData();
    // 监听页面滚动事件
    const scrollListener = () => {
      const query = uni.createSelectorQuery();
      query.select('.container').boundingClientRect((rect) => {
        const windowHeight = uni.getSystemInfoSync().windowHeight;
        if (rect.bottom <= windowHeight + 100) { // 添加额外的100px缓冲区
          if (hasMore.value &&!loading.value) {
            loadMore();
          }
        }
      }).exec();
    };
    uni.onPageScroll(scrollListener);
    
    // 启用下拉刷新
    uni.startPullDownRefresh({
      success: () => {
        console.log('开始下拉刷新');
      }
    });
    
    // 监听下拉刷新事件
    uni.onPullDownRefresh(() => {
      handleRefresh();
    });
    
    // 在组件卸载时移除滚动事件监听器
    onUnmounted(() => {
      uni.offPageScroll(scrollListener);
      // 停止下拉刷新监听
      uni.offPullDownRefresh();
    });
  });
  
  // 加载更多数据的函数
  const loadMore = () => {
    currentPage.value++;
    fetchData();
  };
  
  // 下拉刷新处理函数
  const handleRefresh = () => {
    currentPage.value = 1; // 重置当前页码为1
    hasMore.value = true; // 重置加载更多标志
    fetchData(); // 获取第一页数据
  };
  
  // 处理图片加载事件，获取图片原始尺寸
  const handleImageLoad = (index) => {
	const item = data.value[index];
	uni.getImageInfo({
	  src: item.smallPicurl,
	  success: (res) => {
		item.imageWidth = res.width;
		item.imageHeight = res.height;
	  },
	  fail: (err) => {
		console.error('获取图片尺寸失败', err);
	  }
	});
  };



  </script>
  
  <style scoped>
  .container {
	padding: 20px;
  }
  
  .response-text {
	margin-top: 20px;
  }
  
  .loading-more {
	text-align: center;
	color: #007aff;
	margin-top: 20px;
	cursor: pointer;
  }
  
  .item {
	margin-bottom: 20px;
	border: 1px solid #ccc;
	padding: 10px;
	border-radius: 5px;
  }
  </style>