<template>
    <div class="font-inter bg-neutral-100 text-neutral-700 min-h-screen">
      <!-- 顶部导航栏 -->
      <header class="fixed top-0 left-0 right-0 bg-white shadow-sm z-50 transition-all duration-300" :class="{'shadow bg-glass': isScrolled}">
        <div class="container mx-auto px-4 py-3 flex items-center justify-between">
          <button @click="$router.back()" class="w-10 h-10 flex items-center justify-center rounded-full hover:bg-neutral-100 transition-all">
            <i class="fa-solid fa-arrow-left text-neutral-700"></i>
          </button>
          <h1 class="text-lg font-semibold">支付管理</h1>
          <button class="w-10 h-10 flex items-center justify-center rounded-full hover:bg-neutral-100 transition-all">
            <i class="fa-solid fa-ellipsis-v text-neutral-700"></i>
          </button>
        </div>
      </header>
  
      <!-- 主内容区 -->
      <main class="container mx-auto px-4 pt-20 pb-24">
        <!-- 用户信息卡片 -->
        <div class="bg-white rounded-2xl shadow-card p-5 mb-6 transform hover:translate-y-[-2px] transition-all duration-300">
          <div class="flex items-center">
            <div class="w-16 h-16 rounded-full overflow-hidden mr-4 border-2 border-primary/20">
              <img src="https://picsum.photos/200/200?random=1" alt="User Avatar" class="w-full h-full object-cover">
            </div>
            <div>
              <h2 class="font-bold text-lg">Alex Johnson</h2>
              <p class="text-neutral-500 text-sm">alex.johnson@example.com</p>
            </div>
            <div class="ml-auto">
              <span class="bg-primary/10 text-primary text-xs px-3 py-1 rounded-full">Premium</span>
            </div>
          </div>
        </div>
  
        <!-- 支付方式选择 -->
        <section class="mb-6">
          <h2 class="text-lg font-semibold mb-4 flex items-center">
            <i class="fa-solid fa-wallet text-primary mr-2"></i>
            支付方式
          </h2>
          
          <div class="grid grid-cols-2 gap-3 mb-4">
            <!-- 支付宝国际版 -->
            <div 
              v-for="method in paymentMethods" 
              :key="method.id"
              class="payment-method-card bg-white rounded-xl shadow-sm p-4 border-2 cursor-pointer transition-all duration-300 hover:shadow-card transform hover:translate-y-[-2px]"
              :class="{'border-primary': method.selected, 'border-neutral-200': !method.selected}"
              @click="selectPaymentMethod(method)"
            >
              <div class="flex items-center">
                <div class="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center mr-3">
                  <i :class="`fa-brands ${method.icon} text-xl`" :style="{color: method.color}"></i>
                </div>
                <div>
                  <h3 class="font-medium">{{ method.name }}</h3>
                  <p class="text-xs text-neutral-500">{{ method.region }}</p>
                </div>
              </div>
              <div class="mt-3 flex justify-between items-center">
                <span 
                  class="text-xs px-2 py-1 rounded" 
                  :class="{
                    'bg-primary/10 text-primary': method.selected, 
                    'bg-neutral-200 text-neutral-500': !method.selected
                  }"
                >
                  {{ method.selected ? '已绑定' : '未绑定' }}
                </span>
                <i 
                  class="text-neutral-400" 
                  :class="{
                    'fa-solid fa-check-circle text-primary': method.selected, 
                    'fa-solid fa-plus': !method.selected
                  }"
                ></i>
              </div>
            </div>
          </div>
  
          <button @click="openPaymentModal" class="w-full py-3 bg-white rounded-xl border border-dashed border-neutral-300 text-neutral-500 font-medium flex items-center justify-center transition-all duration-300 hover:bg-neutral-50">
            <i class="fa-solid fa-plus mr-2"></i> 添加支付方式
          </button>
        </section>
  
        <!-- 银行卡管理 -->
        <section class="mb-6">
          <h2 class="text-lg font-semibold mb-4 flex items-center">
            <i class="fa-solid fa-credit-card text-primary mr-2"></i>
            银行卡管理
          </h2>
          
          <div class="relative mb-4">
            <!-- 主银行卡 -->
            <div class="bg-gradient-primary text-white rounded-xl p-5 shadow-lg overflow-hidden relative">
              <div class="absolute top-0 right-0 w-20 h-20 bg-white/10 rounded-full -mr-10 -mt-10"></div>
              <div class="absolute bottom-0 left-0 w-16 h-16 bg-white/10 rounded-full -ml-8 -mb-8"></div>
              
              <div class="flex justify-between items-start mb-4">
                <div>
                  <p class="text-sm opacity-80">主银行卡</p>
                  <h3 class="font-medium">Visa</h3>
                </div>
                <div class="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center">
                  <i class="fa-brands fa-visa"></i>
                </div>
              </div>
              
              <p class="text-sm mb-2">**** **** **** 4242</p>
              
              <div class="flex justify-between text-xs opacity-80">
                <div>
                  <p>持卡人</p>
                  <p class="font-medium mt-1">Alex Johnson</p>
                </div>
                <div>
                  <p>有效期</p>
                  <p class="font-medium mt-1">09/26</p>
                </div>
              </div>
              
              <div class="mt-4 flex justify-between items-center">
                <button class="text-xs bg-white/20 hover:bg-white/30 px-3 py-1 rounded-full transition-all duration-300">
                  设为默认
                </button>
                <div class="flex space-x-3">
                  <button class="text-xs bg-white/20 hover:bg-white/30 w-8 h-8 rounded-full flex items-center justify-center transition-all duration-300">
                    <i class="fa-solid fa-pencil"></i>
                  </button>
                  <button class="text-xs bg-white/20 hover:bg-white/30 w-8 h-8 rounded-full flex items-center justify-center transition-all duration-300">
                    <i class="fa-solid fa-trash"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <button @click="openAddCardModal" class="w-full py-3 bg-white rounded-xl border border-dashed border-neutral-300 text-neutral-500 font-medium flex items-center justify-center transition-all duration-300 hover:bg-neutral-50">
            <i class="fa-solid fa-plus mr-2"></i> 添加银行卡
          </button>
        </section>
  
        <!-- 最近交易记录 -->
        <section>
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-lg font-semibold flex items-center">
              <i class="fa-solid fa-clock-rotate-left text-primary mr-2"></i>
              最近交易
            </h2>
            <a href="#" class="text-primary text-sm font-medium flex items-center">
              查看全部 <i class="fa-solid fa-angle-right ml-1"></i>
            </a>
          </div>
          
          <div class="space-y-3">
            <div v-for="transaction in transactions" :key="transaction.id" class="bg-white rounded-xl shadow-sm p-4 transform hover:translate-y-[-2px] transition-all duration-300">
              <div class="flex justify-between items-center">
                <div class="flex items-center">
                  <div class="w-10 h-10 rounded-lg flex items-center justify-center mr-3" :class="{
                    'bg-primary/10': transaction.type === 'debit',
                    'bg-success/10': transaction.type === 'credit'
                  }">
                    <i 
                      class="text-xl" 
                      :class="{
                        'fa-solid fa-arrow-down text-primary': transaction.type === 'debit',
                        'fa-solid fa-arrow-up text-success': transaction.type === 'credit'
                      }"
                    ></i>
                  </div>
                  <div>
                    <h3 class="font-medium">{{ transaction.title }}</h3>
                    <p class="text-xs text-neutral-500">{{ transaction.date }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <p 
                    class="font-medium" 
                    :class="{
                      'text-danger': transaction.type === 'debit',
                      'text-success': transaction.type === 'credit'
                    }"
                  >
                    {{ transaction.amount }}
                  </p>
                  <p class="text-xs text-neutral-500">{{ transaction.method }}</p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
  
      <!-- 底部导航 -->
      <nav class="fixed bottom-0 left-0 right-0 bg-white shadow-[0_-2px_10px_rgba(0,0,0,0.05)] z-40">
        <div class="grid grid-cols-4 py-3">
          <a href="#" class="flex flex-col items-center text-neutral-500 hover:text-primary transition-all duration-300">
            <i class="fa-solid fa-home text-xl mb-1"></i>
            <span class="text-xs">首页</span>
          </a>
          <a href="#" class="flex flex-col items-center text-neutral-500 hover:text-primary transition-all duration-300">
            <i class="fa-solid fa-bell text-xl mb-1"></i>
            <span class="text-xs">通知</span>
          </a>
          <a href="#" class="flex flex-col items-center text-neutral-500 hover:text-primary transition-all duration-300">
            <i class="fa-solid fa-shopping-cart text-xl mb-1"></i>
            <span class="text-xs">购物车</span>
          </a>
          <a href="#" class="flex flex-col items-center text-primary transition-all duration-300">
            <i class="fa-solid fa-user text-xl mb-1"></i>
            <span class="text-xs">我的</span>
          </a>
        </div>
      </nav>
  
      <!-- 支付方式选择模态框 -->
      <div v-if="showPaymentModal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl w-full max-w-md transform transition-all duration-300 scale-95 opacity-0" :class="{'scale-100 opacity-100': showModalAnimation}">
          <div class="p-5 border-b border-neutral-200">
            <div class="flex justify-between items-center">
              <h3 class="font-bold text-lg">选择支付方式</h3>
              <button @click="closePaymentModal" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-neutral-100 transition-all">
                <i class="fa-solid fa-times"></i>
              </button>
            </div>
          </div>
          
          <div class="p-5 max-h-[60vh] overflow-y-auto">
            <div class="mb-5">
              <p class="text-sm text-neutral-500 mb-3">支付金额</p>
              <div class="bg-neutral-100 rounded-xl p-4">
                <p class="text-2xl font-bold">$29.99</p>
                <p class="text-xs text-neutral-500">高级会员月费</p>
              </div>
            </div>
            
            <p class="text-sm text-neutral-500 mb-3">可用支付方式</p>
            
            <div class="space-y-3 mb-6">
              <div 
                v-for="(option, index) in paymentOptions" 
                :key="index" 
                class="payment-option bg-white rounded-xl p-4 flex items-center cursor-pointer transition-all"
                :class="{
                  'border-primary': selectedPaymentOption === index,
                  'border-neutral-200 hover:border-primary/50': selectedPaymentOption !== index
                }"
                @click="selectPaymentOption(index)"
              >
                <div class="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center mr-3">
                  <i :class="`fa-brands ${option.icon} text-xl`" :style="{color: option.color}"></i>
                </div>
                <div class="flex-1">
                  <h4 class="font-medium">{{ option.name }}</h4>
                  <p class="text-xs text-neutral-500">{{ option.description }}</p>
                </div>
                <i 
                  class="text-neutral-300" 
                  :class="{
                    'fa-solid fa-check-circle text-primary': selectedPaymentOption === index,
                    'fa-regular fa-circle': selectedPaymentOption !== index
                  }"
                ></i>
              </div>
            </div>
            
            <button class="w-full py-3 bg-primary text-white rounded-xl font-medium shadow-button hover:bg-primary/90 transition-all duration-300 flex items-center justify-center">
              <i class="fa-solid fa-credit-card mr-2"></i>
              确认支付 $29.99
            </button>
          </div>
        </div>
      </div>
  
      <!-- 绑定新银行卡模态框 -->
      <div v-if="showAddCardModal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl w-full max-w-md transform transition-all duration-300 scale-95 opacity-0" :class="{'scale-100 opacity-100': showModalAnimation}">
          <div class="p-5 border-b border-neutral-200">
            <div class="flex justify-between items-center">
              <h3 class="font-bold text-lg">添加银行卡</h3>
              <button @click="closeAddCardModal" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-neutral-100 transition-all">
                <i class="fa-solid fa-times"></i>
              </button>
            </div>
          </div>
          
          <div class="p-5">
            <form @submit.prevent="submitCardForm">
              <div class="mb-4">
                <label class="block text-sm font-medium text-neutral-700 mb-1">持卡人姓名</label>
                <input v-model="cardForm.name" type="text" class="w-full px-4 py-3 rounded-xl border border-neutral-300 focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-all" placeholder="输入持卡人姓名">
              </div>
              
              <div class="mb-4">
                <label class="block text-sm font-medium text-neutral-700 mb-1">银行卡号</label>
                <div class="relative">
                  <input v-model="cardForm.number" type="text" class="w-full px-4 py-3 rounded-xl border border-neutral-300 focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-all" placeholder="输入16位银行卡号">
                  <div class="absolute right-3 top-1/2 transform -translate-y-1/2 flex space-x-2">
                    <i class="fa-brands fa-visa text-neutral-400"></i>
                    <i class="fa-brands fa-mastercard text-neutral-400"></i>
                    <i class="fa-brands fa-amex text-neutral-400"></i>
                  </div>
                </div>
              </div>
              
              <div class="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <label class="block text-sm font-medium text-neutral-700 mb-1">有效期</label>
                  <input v-model="cardForm.expiry" type="text" class="w-full px-4 py-3 rounded-xl border border-neutral-300 focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-all" placeholder="MM/YY">
                </div>
                <div>
                  <label class="block text-sm font-medium text-neutral-700 mb-1">CVV安全码</label>
                  <input v-model="cardForm.cvv" type="text" class="w-full px-4 py-3 rounded-xl border border-neutral-300 focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-all" placeholder="三位数">
                </div>
              </div>
              
              <div class="mb-6">
                <label class="block text-sm font-medium text-neutral-700 mb-1">国家/地区</label>
                <select v-model="cardForm.country" class="w-full px-4 py-3 rounded-xl border border-neutral-300 focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-all appearance-none bg-white">
                  <option>中国</option>
                  <option>美国</option>
                  <option>英国</option>
                  <option>澳大利亚</option>
                  <option>加拿大</option>
                  <option>日本</option>
                  <option>韩国</option>
                  <option>新加坡</option>
                  <option>其他</option>
                </select>
              </div>
              
              <div class="flex items-center mb-6">
                <input v-model="cardForm.save" type="checkbox" id="saveCard" class="w-5 h-5 rounded border-neutral-300 text-primary focus:ring-primary/20">
                <label for="saveCard" class="ml-2 text-sm text-neutral-700">保存该卡信息以便未来支付</label>
              </div>
              
              <button type="submit" class="w-full py-3 bg-primary text-white rounded-xl font-medium shadow-button hover:bg-primary/90 transition-all duration-300 flex items-center justify-center">
                <i class="fa-solid fa-plus mr-2"></i>
                添加银行卡
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ChargeOut',
    data() {
      return {
        isScrolled: false,
        showPaymentModal: false,
        showModalAnimation: false,
        showAddCardModal: false,
        selectedPaymentOption: 0,
        cardForm: {
          name: '',
          number: '',
          expiry: '',
          cvv: '',
          country: '中国',
          save: false
        },
        paymentMethods: [
          {
            id: 1,
            name: '支付宝国际',
            region: '中国大陆及全球',
            icon: 'fa-alipay',
            color: '#1677FF',
            selected: true
          },
          {
            id: 2,
            name: 'PayPal',
            region: '全球通用',
            icon: 'fa-paypal',
            color: '#0070BA',
            selected: false
          },
          {
            id: 3,
            name: 'Apple Pay',
            region: 'iOS 设备',
            icon: 'fa-apple',
            color: '#000000',
            selected: false
          },
          {
            id: 4,
            name: 'Google Pay',
            region: 'Android 设备',
            icon: 'fa-google',
            color: '#4285F4',
            selected: false
          }
        ],
        paymentOptions: [
          {
            name: '支付宝国际',
            description: '使用已绑定的支付宝账户',
            icon: 'fa-alipay',
            color: '#1677FF'
          },
          {
            name: 'PayPal',
            description: '连接你的PayPal账户',
            icon: 'fa-paypal',
            color: '#0070BA'
          },
          {
            name: 'Apple Pay',
            description: '使用你的Apple设备支付',
            icon: 'fa-apple',
            color: '#000000'
          },
          {
            name: 'Google Pay',
            description: '使用你的Google账户支付',
            icon: 'fa-google',
            color: '#4285F4'
          }
        ],
        transactions: [
          {
            id: 1,
            title: '订阅续费',
            date: '2025-05-01 14:30',
            amount: '- $9.99',
            method: '支付宝国际',
            type: 'debit'
          },
          {
            id: 2,
            title: '退款',
            date: '2025-04-28 09:15',
            amount: '+ $5.99',
            method: '支付宝国际',
            type: 'credit'
          },
          {
            id: 3,
            title: '购买附加服务',
            date: '2025-04-15 16:42',
            amount: '- $14.99',
            method: 'Visa',
            type: 'debit'
          }
        ]
      }
    },
    methods: {
      selectPaymentMethod(method) {
        if (method.id === 1) {
          this.openPaymentModal();
        } else {
          alert(`即将绑定${method.name}`);
        }
      },
      openPaymentModal() {
        this.showPaymentModal = true;
        this.showModalAnimation = false;
        this.$nextTick(() => {
          setTimeout(() => {
            this.showModalAnimation = true;
          }, 10);
        });
      },
      closePaymentModal() {
        this.showModalAnimation = false;
        setTimeout(() => {
          this.showPaymentModal = false;
        }, 300);
      },
      openAddCardModal() {
        this.showAddCardModal = true;
        this.showModalAnimation = false;
        this.$nextTick(() => {
          setTimeout(() => {
            this.showModalAnimation = true;
          }, 10);
        });
      },
      closeAddCardModal() {
        this.showModalAnimation = false;
        setTimeout(() => {
          this.showAddCardModal = false;
        }, 300);
      },
      submitCardForm() {
        alert('银行卡添加成功！');
        this.closeAddCardModal();
      },
      selectPaymentOption(index) {
        this.selectedPaymentOption = index;
      },
      handleScroll() {
        this.isScrolled = window.scrollY > 10;
      }
    },
    mounted() {
      window.addEventListener('scroll', this.handleScroll);
    },
    beforeDestroy() {
      window.removeEventListener('scroll', this.handleScroll);
    }
  }
  </script>