import requests
import re

def get_base_session(s):
    s.get('https://user.qunar.com/passport/login.jsp')
    get_image(s)
    s.get('https://user.qunar.com/passport/addICK.jsp?ssl')
    resp = s.get('https://rmcsdf.qunar.com/js/df.js?org_id=ucenter.login&js_type=0').text
    session_id = re.findall(r'sessionId=(.*?)&', resp)[0]
    print(session_id)
    s.get(('https://rmcsdf.qunar.com/api/device/challenge.json?'
            'callback=callback_1517117185890&'
            'sessionId={}&'
            'domain=qunar.com&orgId=ucenter.login').format(session_id))
    s.cookies.update({'QN271': session_id})
    pass

def get_image(s):
    resp = s.get('https://user.qunar.com/captcha/api/image?k={en7mni(z&p=ucenter_login&c=ef7d278eca6d25aa6aec7272d57f0a9a')
    with open('q.png','wb') as f:
        f.write(resp.content)

def login(s, username, passwd,vcode):
    data = {
        'loginType':0,
        'username':username,
        'password':passwd,
        'remember':1,
        'vcode':vcode
    }
    url = 'https://user.qunar.com/passport/loginx.jsp'
    resp = s.post(url=url, data=data)
    print(resp.text)

def main():
    s = requests.session()
    get_base_session(s)
    username = input('username:')
    passwd = input('passwd:')
    vcode = input('code:')
    print(dict(s.cookies))
    login(s, username, passwd, vcode)

if __name__ == '__main__':
    main()