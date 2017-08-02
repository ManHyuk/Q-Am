//<![CDATA[
// 사용할 앱의 JavaScript 키를 설정해 주세요.
Kakao.init('5b842b65ed8b32af3945ad1702a761f4');
// 카카오 로그인 버튼을 생성합니다.
Kakao.Auth.createLoginButton({
    container: '#kakao-login-btn',
    success: function (authObj) {
        alert(JSON.stringify(authObj));
    },
    fail: function (err) {
        alert(JSON.stringify(err));
    }
});
//]]>

