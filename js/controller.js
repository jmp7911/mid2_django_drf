const url = `http://52.78.247.51/`


const $logout = document.getElementById('logout')
const $login = document.getElementById('login')
const $profile = document.getElementById('profile')
const $join = document.getElementById('join')

$logout.addEventListener('click', async (e) => {
  // res = await securedApiRequest('rest-auth/logout/', 'POST')
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
  window.location.href='index.html'
})
function loginFormSubmit(f) {
    let formData =  new FormData(f);

    const requestBody = {};
    formData.forEach((value, key) => requestBody[key] = value);
    
    fetch(url+'rest-auth/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify(requestBody)
    }).then((response) => {
        if (!response.ok) {
            alert('이메일 또는 비밀번호를 다시 확인해 주세요')
        } else {
            response.json().then((data) => {
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);
                localStorage.setItem('user', JSON.stringify(data.user))
                alert('로그인 성공!');
                window.location.href='index.html'
            })
        }
    })


    return false
}

function registerFormSubmit(f) {
    let formData =  new FormData(f);

    const requestBody = {};
    formData.forEach((value, key) => requestBody[key] = value);


    fetch(url+'rest-auth/registration/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify(requestBody)
    }).then((response) => {
        if (response.ok) {
            response.json().then((data) => {
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);
                localStorage.setItem('user', JSON.stringify(data.user))
                alert('회원가입을 축하드립니다!');
                window.location.href='index.html'
            },(fail) => {
                console.log(fail)
            })
        } else {
            response.json().then((data) => {
                for(let key in data) {
                    document.getElementById(key).innerText = data[key].toString()
                }
            })
        }
    })


    return false
}

function boardWriteSubmit(f) {
    let formData =  new FormData(f);

    const requestBody = {};
    formData.forEach((value, key) => requestBody[key] = value);

    const user = localStorage.getItem('user')
    const userData = JSON.parse(user)

    requestBody['user'] = userData['pk']
    const res = securedApiRequest('quote/', 'POST', requestBody)

    res.then((response) => {
        window.location.href='view.html?id='+response.id
    })

    return false
}
async function refreshToken() {
    const response = await fetch(url+'rest-auth/token/refresh/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ refresh: localStorage.getItem('refresh_token')})
    });

    const data = await response.json();
    if (!response.ok) {
        viewByAuthentication(false)
        alert('로그인 시간이 만료되었습니다. 다시 로그인 해주세요');
        window.location.href="login.html";
    }

    viewByAuthentication(true)
    // 새로운 액세스 토큰 저장
    localStorage.setItem('access_token', data.access);
    return data.access;
}

function getToken() {
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
        console.error('Access token not found');
        alert('로그인 해주세요');
        window.location.href="login.html";
    }

    const payload = JSON.parse(atob(accessToken.split('.')[1]));
    const exp = payload.exp;
    const now = Date.now() / 1000;

    // 토큰이 만료되면 새로운 토큰을 요청
    if (now > exp) {
        return refreshToken();
    }
    
    viewByAuthentication(true)
    return Promise.resolve(accessToken);
}

async function securedApiRequest(endpoint, method, requestBody={}) {
    try {
        const token = await getToken();
        let init = {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            method: method,
        }
        if (method != 'GET') {
            init['body'] = JSON.stringify(requestBody)
        }
        const response = await fetch(url+endpoint, init);

        if (!response.ok) {
            throw new Error('api error');
        }
        // 응답 처리
        const data = await response.json();
        console.log(data);
        return data;
    } catch (error) {
        console.error('Error during secured API request', error);
    }
}

function viewByAuthentication(flag) {
  if (flag) {
    $login.style.display = 'none'
    $join.style.display = 'none'
    $profile.style.display = 'inline-block'
    $logout.style.display = 'inline-block'
  } else {
    $login.style.display = 'inline-block'
    $join.style.display = 'inline-block'
    $profile.style.display = 'none'
    $logout.style.display = 'none'
  }

}
