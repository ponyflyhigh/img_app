<template>
  <view class="container">
    <uni-card :is-shadow="false" is-full>
      <text class="uni-h6">八字计算器表单，用于收集用户出生信息并计算八字命盘</text>
    </uni-card>
    
    <uni-section title="八字信息" type="line">
      <view class="example">
        <uni-forms ref="baziFormRef" :rules="rules" :modelValue="formData">
          <!-- 阴阳历选择 -->
          <uni-forms-item label="出生日期类型" required name="calendarType">
            <uni-data-checkbox v-model="formData.calendarType" :localdata="calendarTypes" />
          </uni-forms-item>
          
          <!-- 日期时间选择 -->
          <uni-forms-item label="出生日期" required name="birthDateTime">
            <uni-datetime-picker type="datetime" v-model="formData.birthDateTime" />
          </uni-forms-item>
          
          <!-- 性别选择 -->
          <uni-forms-item label="性别" required name="gender">
            <uni-data-checkbox v-model="formData.gender" :localdata="genders" />
          </uni-forms-item>
        </uni-forms>
        
        <view class="button-group">
          <button type="default" @click="resetForm">重置</button>
          <button type="primary" @click="submitForm">计算八字</button>
        </view>
      </view>
    </uni-section>
    
    <!-- 八字计算结果 -->
    <uni-section title="八字结果" type="line" v-if="baziResult">
      <view class="result-container">
        <view class="result-item">
          <text class="result-label">公历时间:</text>
          <text class="result-value">{{ baziResult.solarDate || '-' }}</text>
        </view>
        <view class="result-item">
          <text class="result-label">农历时间:</text>
          <text class="result-value">{{ baziResult.lunarDate || '功能开发中' }}</text>
        </view>
        <view class="result-item">
          <text class="result-label">年柱:</text>
          <text class="result-value">{{ baziResult.yearColumn || '-' }}</text>
        </view>
        <view class="result-item">
          <text class="result-label">月柱:</text>
          <text class="result-value">{{ baziResult.monthColumn || '-' }}</text>
        </view>
        <view class="result-item">
          <text class="result-label">日柱:</text>
          <text class="result-value">{{ baziResult.dayColumn || '-' }}</text>
        </view>
        <view class="result-item">
          <text class="result-label">时柱:</text>
          <text class="result-value">{{ baziResult.hourColumn || '-' }}</text>
        </view>
      </view>
    </uni-section>
    
    <!-- 加载中提示 -->
    <view class="loading-mask" v-if="loading">
      <text>计算中...</text>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue';
import LunarCalendar from 'lunar-javascript';

// 表单引用
const baziFormRef = ref(null);

// 表单数据
const formData = reactive({
  calendarType: 0, // 0: 公历，1: 农历
  birthDateTime: '',
  gender: 0 // 0: 男，1: 女
});

// 表单验证规则
const rules = reactive({
  calendarType: {
    rules: [{ required: true, errorMessage: '请选择出生日期类型' }]
  },
  birthDateTime: {
    rules: [{ required: true, errorMessage: '请选择出生日期' }]
  },
  gender: {
    rules: [{ required: true, errorMessage: '请选择性别' }]
  }
});

// 下拉选项数据
const calendarTypes = [
  { text: '公历', value: 0 },
  { text: '农历', value: 1 }
];

const genders = [
  { text: '男', value: 0 },
  { text: '女', value: 1 }
];

// 计算结果和加载状态
const baziResult = ref(null);
const loading = ref(false);

// 八字计算器类
class AccurateBaziCalculator {
  constructor() {
    this.tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"];
    this.dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"];
    this.month_zhi = ["寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"];
  }

  // 公历转农历
  _solarToLunar(year, month, day) {
    const solar = new LunarCalendar.Solar(year, month, day);
    const lunar = solar.getLunar();
    return {
      year: lunar.getYear(),
      month: lunar.getMonth(),
      day: lunar.getDay(),
      isLeap: lunar.isLeapMonth()
    };
  }

  // 获取节气信息
  _getSolarTerm(year, month, day) {
    const solar = new LunarCalendar.Solar(year, month, day);
    return solar.getTerm();
  }

  // 真太阳时校正
  _adjustSolarTime(year, month, day, hour, minute, lng = 120.0) {
    const delta = (lng - 120.0) * 4;
    return new Date(year, month - 1, day, hour, minute).getTime() + delta * 60 * 1000;
  }

  // 年柱计算（考虑立春）
  _getYearGanzhi(year, month, day) {
    // 计算立春日期
    const solar = new LunarCalendar.Solar(year, 2, 4); // 立春通常在2月4日左右
    const springFestival = solar.getTerm();
    
    if (springFestival === '立春') {
      // 检查具体日期是否在立春之后
      const springDate = new Date(year, 1, 4); // 注意月份从0开始
      const targetDate = new Date(year, month - 1, day);
      
      if (targetDate < springDate) {
        year -= 1; // 在立春前，算上一年
      }
    }
    
    const offset = (year - 4) % 60;
    return `${this.tiangan[offset % 10]}${this.dizhi[offset % 12]}`;
  }

  // 月柱计算（严格按照Python逻辑实现）
  _getMonthGanzhi(year, lunarMonth) {
    const yearGan = (year - 4) % 10;
    const startMap = { 0: 2, 1: 4, 2: 6, 3: 8, 4: 0, 5: 2, 6: 4, 7: 6, 8: 8, 9: 0 };
    const monthGan = (startMap[yearGan] + lunarMonth - 1) % 10;
    return `${this.tiangan[monthGan]}${this.month_zhi[lunarMonth - 1]}`;
  }

  // 日柱计算
  _getDayGanzhi(dateObj) {
    const baseDate = new Date(1949, 9, 1); // 1949-10-01 甲子日
    const daysDiff = Math.floor((dateObj - baseDate) / (24 * 60 * 60 * 1000));
    return `${this.tiangan[daysDiff % 10]}${this.dizhi[daysDiff % 12]}`;
  }

  // 时柱计算
  _getHourGanzhi(dtObj, dayGan) {
    const hour = dtObj.getHours();
    const minute = dtObj.getMinutes();
    let zhi;
    
    if ((hour === 23 && minute >= 0) || (hour === 0 && minute < 1)) {
      zhi = "子";
    } else {
      const zhiIndex = Math.floor((hour + 1) / 2) % 12;
      zhi = this.dizhi[zhiIndex];
    }
    
    const startMap = { 
      "甲": 0, "乙": 2, "丙": 4, "丁": 6, "戊": 8,
      "己": 0, "庚": 2, "辛": 4, "壬": 6, "癸": 8 
    };
    
    const ganIndex = (startMap[dayGan] + this.dizhi.indexOf(zhi)) % 10;
    return `${this.tiangan[ganIndex]}${zhi}`;
  }

  calculate(year, month, day, hour, minute, isLunar = false, lng = 120.0) {
    try {
      // 处理真太阳时
      const correctedTime = this._adjustSolarTime(year, month, day, hour, minute, lng);
      const correctedDate = new Date(correctedTime);
      
      let lunarInfo;
      if (isLunar) {
        // 如果是农历输入，直接使用
        lunarInfo = {
          year,
          month,
          day,
          isLeap: false // 暂不处理闰月
        };
      } else {
        // 公历转农历
        lunarInfo = this._solarToLunar(
          correctedDate.getFullYear(),
          correctedDate.getMonth() + 1,
          correctedDate.getDate()
        );
      }
      
      // 计算年柱（考虑立春）
      const yearColumn = this._getYearGanzhi(
        correctedDate.getFullYear(),
        correctedDate.getMonth() + 1,
        correctedDate.getDate()
      );
      
      // 计算月柱
      const monthColumn = this._getMonthGanzhi(lunarInfo.year, lunarInfo.month);
      
      // 计算日柱
      const dayColumn = this._getDayGanzhi(correctedDate);
      
      // 计算时柱
      const hourColumn = this._getHourGanzhi(correctedDate, dayColumn[0]);
      
      // 获取节气信息
      const term = this._getSolarTerm(
        correctedDate.getFullYear(),
        correctedDate.getMonth() + 1,
        correctedDate.getDate()
      );
      
      return {
        solarDate: correctedDate.toLocaleString(),
        lunarDate: `${lunarInfo.year}年${lunarInfo.month}月${lunarInfo.day}日${lunarInfo.isLeap ? '闰' : ''}`,
        yearColumn,
        monthColumn,
        dayColumn,
        hourColumn,
        solarTerm: term || '无'
      };
    } catch (e) {
      return { error: `计算错误：${e.message}` };
    }
  }
}

// 重置表单
const resetForm = () => {
  formData.calendarType = 0;
  formData.birthDateTime = '';
  formData.gender = 0;
  baziResult.value = null;
};

// 提交表单并计算八字
const submitForm = async () => {
  try {
    // 验证表单
    await baziFormRef.value.validate();
    
    loading.value = true;
    
    const { calendarType, birthDateTime } = formData;
    const [datePart, timePart] = birthDateTime.split(' ');
    const [year, month, day] = datePart.split('-').map(Number);
    const [hour, minute] = timePart.split(':').map(Number);

    if (isNaN(year) || isNaN(month) || isNaN(day) || isNaN(hour) || isNaN(minute)) {
      throw new Error('日期时间格式不正确');
    }

    const calculator = new AccurateBaziCalculator();
    const result = calculator.calculate(
      year,
      month,
      day,
      hour,
      minute,
      calendarType === 1
    );

    if (result.error) {
      throw new Error(result.error);
    }

    baziResult.value = result;
    
    uni.showToast({
      title: '计算成功',
      icon: 'success'
    });
  } catch (err) {
    console.error(err);
    uni.showToast({
      title: err.message || '计算失败',
      icon: 'none'
    });
  } finally {
    loading.value = false;
  }
};

// 生命周期钩子
onMounted(() => {
  // 组件挂载后执行的初始化逻辑
  console.log('组件已挂载');
  
  // 测试 LunarCalendar 导入
  try {
    console.log('LunarCalendar 是否正确导入:', typeof LunarCalendar === 'object');
    console.log('LunarCalendar.Solar 是否存在:', typeof LunarCalendar.Solar === 'function');
    
    // 创建一个测试实例
    const testSolar = new LunarCalendar.Solar(2024, 8, 15);
    console.log('测试 Solar 实例:', testSolar);
  } catch (error) {
    console.error('LunarCalendar 测试失败:', error);
  }
});
</script>

<style lang="scss">
.example {
  padding: 15px;
  background-color: #fff;
}

.button-group {
  margin-top: 15px;
  display: flex;
  justify-content: space-around;
}

.result-container {
  padding: 15px;
  background-color: #f8f8f8;
  border-radius: 5px;
}

.result-item {
  display: flex;
  margin-bottom: 10px;
}

.result-label {
  width: 100px;
  color: #666;
}

.result-value {
  flex: 1;
  color: #333;
}

.loading-mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.loading-mask text {
  padding: 10px 20px;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  border-radius: 5px;
}
</style>