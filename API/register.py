from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import uuid
import random
import string
import redis
from datetime import datetime, timedelta
from flask_cors import CORS
from flask_mail import Mail, Message
import re
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
logging.basicConfig(level = logging.INFO)

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# 邮箱配置
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = '944845046@qq.com'
app.config['MAIL_PASSWORD'] = 'isroduvafxgnbehj'
app.config['MAIL_DEFAULT_SENDER'] = '944845046@qq.com'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)
migrate = Migrate(app, db)  # 添加这一行

# 连接Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# 用户模型
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    phone = db.Column(db.String(11), unique=True, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    invite_code = db.Column(db.String(20), unique=True, nullable=False)
    inviter_id = db.Column(db.String(36), db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 确保至少有一个联系方式
    __table_args__ = (
        db.CheckConstraint('phone IS NOT NULL OR email IS NOT NULL', name='contact_info_check'),
    )

# 生成随机邀请码
def generate_invite_code(length=8):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for i in range(length))

# 生成随机验证码
def generate_verification_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

# 发送短信验证码
def send_sms_code(phone, code):
    # 这里需要集成实际的短信服务，如阿里云短信、腾讯云短信等
    print(f"模拟发送短信：验证码 {code} 已发送至 {phone}")
    return True

# 发送邮箱验证码
def send_email_code(email, code):
    try:
        msg = Message(
            '验证码 - 您的注册验证码',
            recipients=[email]
        )
        msg.body = f'您的验证码是：{code}，有效期5分钟。'
        mail.send(msg)
        return True
    except Exception as e:
        print(f"发送邮箱验证码失败: {e}")
        return False

# 验证手机号格式
def validate_phone(phone):
    return re.match(r'^1[3-9]\d{9}$', phone) is not None

# 验证邮箱格式
def validate_email(email):
    return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) is not None

# 发送手机号验证码
@app.route('/api/sms', methods=['POST'])
def send_sms_code_route():
    data = request.get_json()
    phone = data.get('phone')
    
    if not phone:
        return jsonify({'success': False, 'message': '手机号不能为空'}), 400
    
    if not validate_phone(phone):
        return jsonify({'success': False, 'message': '无效的手机号格式'}), 400
    
    # 检查是否已有用户使用该手机号
    if User.query.filter_by(phone=phone).first():
        return jsonify({'success': False, 'message': '该手机号已被注册'}), 400
    
    # 生成验证码
    code = generate_verification_code()
    
    # 存储到Redis
    redis_client.setex(f'verification_code:phone:{phone}', 300, code)
    
    # 发送短信
    if send_sms_code(phone, code):
        return jsonify({'success': True, 'message': '验证码已发送，请查收短信'})
    else:
        return jsonify({'success': False, 'message': '验证码发送失败，请稍后再试'}), 500

# 发送邮箱验证码
@app.route('/api/email', methods=['POST'])
def send_email_code_route():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'success': False, 'message': '邮箱不能为空'}), 400
    
    if not validate_email(email):
        return jsonify({'success': False, 'message': '无效的邮箱格式'}), 400
    
    # 检查是否已有用户使用该邮箱
    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': '该邮箱已被注册'}), 400
    
    # 生成验证码
    code = generate_verification_code()
    
    # 存储到Redis
    redis_client.setex(f'verification_code:email:{email}', 300, code)
    
    # 发送邮箱
    if send_email_code(email, code):
        return jsonify({'success': True, 'message': '验证码已发送，请查收邮箱'})
    else:
        return jsonify({'success': False, 'message': '验证码发送失败，请稍后再试'}), 500

# 注册API
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 验证是手机号注册还是邮箱注册
    register_type = None
    identifier = None
    
    if 'phone' in data and data['phone']:
        register_type = 'phone'
        identifier = data['phone']
        # 验证手机号格式
        if not validate_phone(identifier):
            return jsonify({'success': False, 'message': '无效的手机号格式'}), 400
    elif 'email' in data and data['email']:
        register_type = 'email'
        identifier = data['email']
        # 验证邮箱格式
        if not validate_email(identifier):
            return jsonify({'success': False, 'message': '无效的邮箱格式'}), 400
    else:
        return jsonify({'success': False, 'message': '请提供手机号或邮箱'}), 400
    
    # 验证其他必填字段
    code = data.get('code')
    username = data.get('username')
    password = data.get('password')
    invite_code = data.get('invite_code')  # 邀请码（选填）
    
    if not all([code, username, password]):
        return jsonify({'success': False, 'message': '请填写所有必填字段'}), 400
    
    # 验证密码长度
    if len(password) < 6:
        return jsonify({'success': False, 'message': '密码长度至少6位'}), 400
    
    # 检查验证码
    redis_key = f'verification_code:{register_type}:{identifier}'
    stored_code = redis_client.get(redis_key)
    if not stored_code or stored_code.decode('utf-8') != code:
        return jsonify({'success': False, 'message': '验证码错误或已过期'}), 400
    
    # 检查标识符是否已注册
    if register_type == 'phone':
        if User.query.filter_by(phone=identifier).first():
            return jsonify({'success': False, 'message': '该手机号已被注册'}), 400
    else:
        if User.query.filter_by(email=identifier).first():
            return jsonify({'success': False, 'message': '该邮箱已被注册'}), 400
    
    # 生成用户自己的邀请码
    user_invite_code = generate_invite_code()
    
    # 创建用户对象
    user_data = {
        'username': username,
        'password_hash': bcrypt.generate_password_hash(password).decode('utf-8'),
        'invite_code': user_invite_code
    }
    
    if register_type == 'phone':
        user_data['phone'] = identifier
    else:
        user_data['email'] = identifier
    
    user = User(**user_data)
    
    # 处理邀请码逻辑
    if invite_code:
        inviter = User.query.filter_by(invite_code=invite_code).first()
        if inviter:
            user.inviter_id = inviter.id
    
    # 保存用户到数据库
    db.session.add(user)
    db.session.commit()
    
    # 从Redis中删除验证码
    redis_client.delete(redis_key)
    
    # 生成JWT token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'success': True, 
        'message': '注册成功',
        'data': {
            'user_id': user.id,
            'username': user.username,
            'phone': user.phone,
            'email': user.email,
            'invite_code': user.invite_code,
            'token': access_token
        }
    })

# 登录API
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    password = data.get('password')
    
    if not password:
        return jsonify({'success': False, 'message': '请输入密码'}), 400
    
    # 判断是手机号登录还是邮箱登录
    if 'phone' in data and data['phone']:
        identifier_type = 'phone'
        identifier = data['phone']
        user = User.query.filter_by(phone=identifier).first()
    elif 'email' in data and data['email']:
        identifier_type = 'email'
        identifier = data['email']
        user = User.query.filter_by(email=identifier).first()
    else:
        return jsonify({'success': False, 'message': '请提供手机号或邮箱'}), 400
    
    if not user:
        return jsonify({'success': False, 'message': f'该{identifier_type}未注册'}), 401
    
    if not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({'success': False, 'message': '密码错误'}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'success': True,
        'message': '登录成功',
        'data': {
            'user_id': user.id,
            'username': user.username,
            'phone': user.phone,
            'email': user.email,
            'invite_code': user.invite_code,
            'token': access_token
        }
    })

# 获取用户信息API
@app.route('/api/user', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'success': False, 'message': '用户不存在'}), 404
    
    # 获取邀请统计信息
    invited_count = User.query.filter_by(inviter_id=user_id).count()
    
    return jsonify({
        'success': True,
        'data': {
            'user_id': user.id,
            'username': user.username,
            'phone': user.phone,
            'email': user.email,
            'invite_code': user.invite_code,
            'invited_count': invited_count,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 创建数据库表
    app.run(host='0.0.0.0', debug=True)