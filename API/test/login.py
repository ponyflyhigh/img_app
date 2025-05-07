import sys
import os
# 将包含 register.py 的目录添加到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from register import app, mail
from flask_mail import Message

# 配置测试环境
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# 测试邮件发送成功
def test_email_sending_success(client, mocker):
    # 模拟邮件发送
    mock_send = mocker.patch.object(mail, 'send')
    
    # 发送测试请求
    response = client.get('/test_email')
    data = response.get_json()
    
    # 验证响应
    assert response.status_code == 200
    assert data['success'] is True
    assert data['message'] == '邮件发送成功'
    
    # 验证邮件发送调用
    mock_send.assert_called_once()
    args, kwargs = mock_send.call_args
    sent_msg = args[0]
    assert isinstance(sent_msg, Message)
    assert sent_msg.subject == '测试邮件'
    assert sent_msg.recipients == ['martinleo666@qq.com']  # 替换为您的邮箱地址
    assert sent_msg.body == '这是一封测试邮件'

# 测试邮件发送失败
def test_email_sending_failure(client, mocker):
    # 模拟邮件发送异常
    mock_send = mocker.patch.object(mail, 'send')
    mock_send.side_effect = Exception('邮件发送失败')

    # 发送测试请求
    print("Sending request to /test_email")
    response = client.get('/test_email')
    print(f"Response status code: {response.status_code}")
    data = response.get_json()

    # 验证响应
    assert response.status_code == 500