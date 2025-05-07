<template>
	<view class="user-info-container">
		<!-- 阴阳历选择 -->
		<view class="form-item">
			<text class="label">出生日期</text>
			<picker mode="selector" range="{{['公历','农历']}}" @change="handleCalendarTypeChange">
				<view class="picker">
					{{calendarTypes[calendarTypeIndex]}}
				</view>
			</picker>
		</view>

		<!-- 日期选择 -->
		<view class="form-item">
			<picker mode="date" :value="birthDate" @change="handleDateChange">
				<view class="picker">
					{{birthDate}}
				</view>
			</picker>
		</view>

		<!-- 性别选择 -->
		<view class="form-item">
			<text class="label">性别</text>
			<radio-group @change="handleGenderChange">
				<label class="radio-item">
					<radio value="0" :checked="gender === '0'" />
					<text>男</text>
				</label>
				<label class="radio-item">
					<radio value="1" :checked="gender === '1'" />
					<text>女</text>
				</label>
			</radio-group>
		</view>

		<!-- 出生地点选择 -->
		<view class="form-item">
			<text class="label">出生地点</text>
			<picker mode="region" @change="handleRegionChange">
				<view class="picker">
					{{province + city + district}}
				</view>
			</picker>
		</view>

		<!-- 操作按钮 -->
		<view class="button-group">
			<button type="default" @click="handleCancel">取消</button>
			<button type="primary" @click="handleSave">保存</button>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			// 阴阳历类型索引
			calendarTypeIndex: 0,
			// 可选的阴阳历类型
			calendarTypes: ['公历', '农历'],
			// 出生日期
			birthDate: '1990-01-01',
			// 性别：0为男，1为女
			gender: '0',
			// 省市区信息
			province: '请选择省',
			city: '市',
			district: '区',
		};
	},
	methods: {
		// 处理阴阳历类型选择
		handleCalendarTypeChange(e) {
			this.calendarTypeIndex = e.detail.value;
		},

		// 处理日期选择
		handleDateChange(e) {
			this.birthDate = e.detail.value;
		},

		// 处理性别选择
		handleGenderChange(e) {
			this.gender = e.detail.value;
		},

		// 处理地区选择
		handleRegionChange(e) {
			const region = e.detail.value;
			this.province = region[0];
			this.city = region[1];
			district = region[2];
		},

		// 处理取消操作
		handleCancel() {
			// 这里可以添加取消时的逻辑，例如返回上一页
			uni.navigateBack();
		},

		// 处理保存操作
		handleSave() {
			// 这里可以添加保存数据的逻辑
			const userInfo = {
				calendarType: this.calendarTypes[this.calendarTypeIndex],
				birthDate: this.birthDate,
				gender: this.gender === '0' ? '男' : '女',
				location: this.province + this.city + this.district,
			};

			// 打印用户信息（在实际应用中可以发送到服务器）
			console.log('保存的用户信息:', userInfo);

			// 显示保存成功的提示
			uni.showToast({
				title: '保存成功',
				icon: 'success',
				duration: 2000,
			});
		},
	},
};
</script>

<style>
.user-info-container {
	padding: 30rpx;
}

.form-item {
	margin-bottom: 40rpx;
}

.label {
	display: block;
	margin-bottom: 20rpx;
	font-weight: bold;
}

.picker {
	height: 80rpx;
	line-height: 80rpx;
	border-bottom: 1rpx solid #e0e0e0;
	padding-left: 20rpx;
}

.radio-item {
	display: inline-block;
	margin-right: 40rpx;
}

.button-group {
	margin-top: 60rpx;
	display: flex;
	justify-content: space-around;
}
</style>