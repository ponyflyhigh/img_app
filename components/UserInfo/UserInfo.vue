<template>
	<view class="userinfo" @click="changeUsername">
	  <image :src="avatarUrl" mode="" class="avatar"></image>
	  <view class="username">{{ username }}</view>
	</view>
</template>

<script>
export default {
  name: "UserInfo",
  props: {
    avatarUrl: {
      type: String,
      required: true
    },
    username: {
      type: String,
      default: '默认用户'
    }
  },
  setup(props, { emit }) {
    const changeUsername = () => {
      const newUsername = '新用户名';
      emit('update:username', newUsername);
    };

    return {
      changeUsername
    };
  }
};
</script>