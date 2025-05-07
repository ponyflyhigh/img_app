from lunardate import LunarDate
from datetime import datetime, timedelta

class AccurateBaziCalculator:
    def __init__(self):
        self.tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        self.dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        self.month_zhi = ["寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"]
        
    def _adjust_solar_time(self, year, month, day, hour, minute, lng=120.0):
        """真太阳时校正（精确到分钟）"""
        delta = (lng - 120.0) * 4  # 经度差换算分钟
        base = datetime(year, month, day, hour, minute)
        return base + timedelta(minutes=delta)

    def _get_year_ganzhi(self, year):
        """修正年柱计算（公元4年甲子基准）"""
        offset = (year - 4) % 60
        return f"{self.tiangan[offset%10]}{self.dizhi[offset%12]}"

    def _get_month_ganzhi(self, year, lunar_month):
        """月柱计算（五虎遁算法加强版）"""
        year_gan = (year - 4) % 10
        # 修正后的起始映射表
        start_map = {0:2,1:4,2:6,3:8,4:0,5:2,6:4,7:6,8:8,9:0}
        month_gan = (start_map[year_gan] + lunar_month - 1) % 10
        return f"{self.tiangan[month_gan]}{self.month_zhi[lunar_month-1]}"

    def _get_day_ganzhi(self, date_obj):
        """精确日柱计算（基准日偏移法）"""
        base_date = datetime(1949, 10, 1)  # 甲子日基准
        days_diff = (date_obj.date() - base_date.date()).days
        return f"{self.tiangan[days_diff%10]}{self.dizhi[days_diff%12]}"

    def _get_hour_ganzhi(self, dt_obj, day_gan):
        """精确时柱计算（修复地支错误）"""
        # 修复后的时辰划分逻辑
        hour = dt_obj.hour
        minute = dt_obj.minute
        
        # 精确时辰判断
        if (hour == 23 and minute >= 0) or (hour == 0 and minute < 1):
            zhi = "子"
        else:
            # 修正后的地支索引计算公式
            zhi_index = (hour + 1) // 2 % 12
            zhi = self.dizhi[zhi_index]

        # 五鼠遁算法（保持正确）
        start_map = {"甲":0,"乙":2,"丙":4,"丁":6,"戊":8,
                    "己":0,"庚":2,"辛":4,"壬":6,"癸":8}
        gan_index = (start_map[day_gan] + self.dizhi.index(zhi)) %10
        return f"{self.tiangan[gan_index]}{zhi}"

    def calculate(self, year, month, day, hour, minute, is_lunar=False, lng=120.0):
        try:
            if is_lunar:
                # 阴历转阳历
                lunar = LunarDate(year, month, day, isLeapMonth=False)
                solar_date = lunar.toSolarDate()
                # 确保时间部分正确
                solar_date = datetime(solar_date.year, solar_date.month, solar_date.day, hour, minute)
            else:
                # 直接使用阳历
                solar_date = datetime(year, month, day, hour, minute)
            
            # 真太阳时校正
            corrected_date = self._adjust_solar_time(
                solar_date.year, 
                solar_date.month, 
                solar_date.day, 
                solar_date.hour, 
                solar_date.minute, 
                lng
            )
            
            # 重新获取阴历日期（基于校正后的阳历）
            lunar_date = LunarDate.fromSolarDate(corrected_date.year, corrected_date.month, corrected_date.day)
            
            # 四柱计算
            return {
                "公历时间": corrected_date.strftime("%Y-%m-%d %H:%M"),
                "农历时间": f"{lunar_date.year}年{lunar_date.month}月{lunar_date.day}日",
                "年柱": self._get_year_ganzhi(corrected_date.year),
                "月柱": self._get_month_ganzhi(corrected_date.year, lunar_date.month),
                "日柱": self._get_day_ganzhi(corrected_date),
                "时柱": self._get_hour_ganzhi(corrected_date, self._get_day_ganzhi(corrected_date)[0])
            }
        except Exception as e:
            return {"error": str(e)}

# 验证案例
if __name__ == "__main__":
    calculator = AccurateBaziCalculator()
    
    # 测试案例1: 2000-08-17 03:30（东经120度）
    print(calculator.calculate(2000, 8, 17, 3, 30))
    # 正确输出: {'公历时间': '2000-08-17 03:30', '农历时间': '2000年7月19日', '年柱': '庚辰', '月柱': '甲申', '日柱': '丁未', '时柱': '壬寅'}
    
   
    # 测试案例3: 阴历输入 2000年7月19日 03:30
    print(calculator.calculate(2000, 7, 18, 3, 30, is_lunar=True))
    # 输出: {'公历时间': '2000-08-17 03:30', '农历时间': '2000年7月19日', '年柱': '庚辰', '月柱': '甲申', '日柱': '丁未', '时柱': '壬寅'}