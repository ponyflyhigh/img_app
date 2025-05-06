<template>
  <div class="chat-container">
    <!-- 顶部导航栏 -->
    <div class="header">
      <div class="back-arrow" @click="navigateBack">←</div>
      <div class="title">新对话</div>
      <div class="sub-title">doubao.com</div>
    </div>

    <!-- 聊天内容区域 -->
    <div class="chat-content" ref="chatContentRef">
      <!-- 欢迎提示 -->
      <div class="welcome-message">
        <div class="avatar"></div>
        <div class="prompt">聊聊新话题</div>
      </div>

      <!-- 聊天消息列表 -->
      <div class="message-list">
        <div
          v-for="(msg, index) in chatMessages"
          :key="index"
          class="message-item"
          :class="{ 'self-message': msg.type ==='self' }"
        >
          <div class="message-content" v-if="msg.type === 'text' || msg.type ==='self'">
            <div class="bubble" :class="{ 'self-bubble': msg.type ==='self' }">
              {{ msg.content }}
            </div>
          </div>
          <div class="message-content" v-else-if="msg.type === 'file'">
            <div class="file-message" :class="{ 'self-file': msg.type ==='self' }">
              <a :href="msg.content" target="_blank">
                <i class="fa fa-file-o"></i> {{ getFileName(msg.content) }}
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部输入区域 -->
    <div class="bottom-bar">
      <div class="toolbar">
        <button class="tool-btn" @click="toggleEmoji">
          <i class="fa fa-smile-o"></i>
        </button>
        <button class="tool-btn" @click="openFileUpload">
          <i class="fa fa-paperclip"></i>
        </button>
      </div>

      <div class="input-area">
        <input
          v-model="message"
          ref="inputRef"
          class="message-input"
          placeholder="输入消息..."
          @keydown.enter="sendMessage"
        >

        <div class="send-btn" @click="sendMessage">
          <i class="fa fa-paper-plane"></i>
        </div>
      </div>

      <!-- 文件选择器 -->
      <input
        type="file"
        ref="fileInputRef"
        class="hidden"
        @change="handleFileSelect"
        multiple
      >
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import axios from 'axios';

// 状态管理
const chatContentRef = ref(null);
const inputRef = ref(null);
const fileInputRef = ref(null);

const message = ref('');
const chatMessages = ref([
  { type: 'text', content: '你好！我是豆包，有什么可以帮助你的？' },
  { type: 'text', content: '可以问我任何问题，或者让我帮你生成内容。' }
]);

// 自动滚动到底部
const scrollToBottom = () => {
  if (chatContentRef.value) {
    chatContentRef.value.scrollTop = chatContentRef.value.scrollHeight;
  }
};

// 发送消息
const sendMessage = async () => {
  if (message.value.trim() === '') return;

  try {
    const response = await axios.post('http://127.0.0.1:5000/chat', 
      { message: message.value },
      {
        headers: {
          'Content-Type': 'application/json'
        },
        timeout: 10000 // 10秒超时
      }
    );

    console.log(response.data);
    chatMessages.value.push({
      type:'self',
      content: message.value
    });
    message.value = '';
    scrollToBottom();
  } catch (error) {
    console.error('Error sending message:', error);
  }
};

// 文件上传
const openFileUpload = () => {
  fileInputRef.value.click();
};

const handleFileSelect = (event) => {
  const files = event.target.files;
  if (files.length === 0) return;

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const fileUrl = URL.createObjectURL(file);

    chatMessages.value.push({
      type:'self',
      content: fileUrl,
      fileName: file.name
    });
  }

  scrollToBottom();
  fileInputRef.value.value = ''; // 重置文件选择器
};

// 获取文件名
const getFileName = (fileUrl) => {
  // 从URL中提取文件名
  const fileName = fileUrl.split('/').pop();
  return fileName.length > 20? fileName.substring(0, 17) + '...' : fileName;
};

// 导航回退
const navigateBack = () => {
  // 这里可以添加导航回退逻辑
  console.log('导航回退');
};

// 切换表情面板
const toggleEmoji = () => {
  // 这里可以添加表情面板逻辑
  console.log('打开表情面板');
};

// 监听消息变化，自动滚动到底部
watch(chatMessages, () => {
  scrollToBottom();
});

// 页面加载完成后聚焦输入框
onMounted(() => {
  scrollToBottom();
});

// 组件卸载时清理资源
onUnmounted(() => {
  // 无需清理语音相关资源，因为已去除语音功能
});
</script>

<style scoped>
/* 基础样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

body {
  background-color: #f5f5f5;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f8f8f8;
}

/* 头部样式 */
.header {
  display: flex;
  align-items: center;
  padding: 16px;
  background: white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.back-arrow {
  font-size: 24px;
  margin-right: 16px;
  cursor: pointer;
}

.title {
  flex: 1;
  text-align: center;
  font-size: 18px;
  font-weight: 500;
}

.sub-title {
  text-align: center;
  font-size: 14px;
  color: #666;
}

/* 聊天内容区域 */
.chat-content {
  flex: 1;
  overflow-y: auto;
  background: #f8f8f8;
  padding: 16px;
}

.welcome-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px 0;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #e6f2ff;
  margin-bottom: 16px;
  background-image: url('https://picsum.photos/80/80');
  background-size: cover;
}

.prompt {
  font-size: 16px;
  color: #999;
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message-item {
  display: flex;
  align-items: flex-start;
  max-width: 80%;
}

.self-message {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.bubble {
  padding: 10px 16px;
  border-radius: 18px;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  position: relative;
}

.self-bubble {
  background-color: #4CAF50;
  color: white;
}

.file-message {
  padding: 10px 16px;
  border-radius: 18px;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.self-file {
  background-color: #4CAF50;
  color: white;
}

a {
  color: inherit;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 底部输入区域 */
.bottom-bar {
  padding: 8px 16px;
  background: white;
  box-shadow: 0 -1px 4px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.toolbar {
  display: flex;
  gap: 16px;
  padding-bottom: 8px;
}

.tool-btn {
  background: none;
  border: none;
  color: #666;
  font-size: 20px;
  cursor: pointer;
  padding: 4px;
}

.input-area {
  display: flex;
  gap: 8px;
  align-items: center;
  position: relative;
}

.message-input {
  flex: 1;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  padding: 10px 16px;
  height: 40px;
  resize: none;
  font-size: 16px;
  outline: none;
}

.send-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
}

.send-btn:hover {
  background-color: #45a049;
}

.hidden {
  display: none;
}
</style>