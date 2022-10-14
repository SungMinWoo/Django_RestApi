const contentContainer = document.getElementById('content-container')
const loginForm = document.getElementById('login-form')
const searchForm = document.getElementById('search-form')
const baseEndpoint = 'http://localhost:8000/api'
/* const는 변하지 않는 변수에 사용함, var은 변경될 수 있는 상수수*/
if (loginForm){
    //handle login form
    loginForm.addEventListener('submit', handleLogin)
}
if (searchForm){
    searchForm.addEventListener('submit', handleSearch)
}

function handleLogin(event){
    event.preventDefault()
    const loginEndpoint = `${baseEndpoint}/token/`
    let loginFormData = new FormData(loginForm) // form 데이터 가져오기
    let loginObjectData = Object.fromEntries(loginFormData) // 이 함수를 쓰면 json 형태로 값을 가져와줌 username:'~~'
    let bodyStr = JSON.stringify(loginObjectData) // 소통 가능한 js형태로 바꿈 'username':'~~'
    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: bodyStr
    }
    fetch(loginEndpoint, options) // 실행, requests.post
    .then(response=>{
        return response.json()
    })
    .then(authData =>{ // 데이터 불러옴
        handleAuthData(authData, getProductList)
    })
    .catch(err=>{
        console.log('err', err)
    })
}

function handleSearch(event){
    event.preventDefault()
    let formData = new FormData(searchForm)
    let data = Object.fromEntries(formData)
    let searchParams = new URLSearchParams(data)
    const endpoint = `${baseEndpoint}/search/?${searchParams}`
    const headers = {
        "Content-Type": "application/json",
    }
    const authToken = localStorage.getItem('access')
    if (authToken){
        headers['Authorization'] = `Bearer ${authToken}`
    }
    const options = {
        method: "GET",
        headers: headers
    }
    fetch(endpoint, options) // 실행, requests.get
    .then(response=>{
        return response.json()
    })
    .then(data => {
        const validData = isTokenNotValid(data)
        if (validData && contentContainer){
            contentContainer.innerHTML = ""
            if (data) {
                let htmlStr  = ""
                for (let result of data.results) {
                    htmlStr += "<li>"+ result.title + "</li>"
                }
                contentContainer.innerHTML = htmlStr
                if (data.results.length === 0) {
                    contentContainer.innerHTML = "<p>No results found</p>"
                }
            } else {
                contentContainer.innerHTML = "<p>No results found</p>"
            }
        }
    })
    .catch(err=>{
        console.log('err', err)
    })
}


function handleAuthData(authData, callback){ // 사용자 스토리지에 jwt 추가
    localStorage.setItem('access', authData.access)
    localStorage.setItem('refresh', authData.refresh)
    if (callback) {
        callback()
    }
}

function writeToContainer(data){ // 데이터 추가
    if (contentContainer){
        contentContainer.innerHTML = '<pre>' + JSON.stringify(data, null, 4) + '</pre>' //stringfy 정렬하려면 null, 4 삽입
    }
}

function getFetchOptions(method, body){ // 중복코드 최소화
    return {
        method: method === null ? "GET": method,
        headers:{
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem('access')}`
        },
        body: body ? body : null
    }
}

function isTokenNotValid(jsonData) { // 토큰이 일치하지 않을때
    if (jsonData.code && jsonData.code === "token_not_valid"){
        // run a refresh token fetch
        alert("Please login again")
        return false
    }
    return true
}

function validateJWTToken() { // 토큰 확인
    // fetch
    const endpoint = `${baseEndpoint}/token/verify/`
    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            token: localStorage.getItem('access')
        })
    }
    fetch(endpoint, options)
    .then(response=>response.json())
    .then(x=> {
        // refresh token
    })
}

function getProductList(){
    const endpoint = `${baseEndpoint}/products/`
    const options = getFetchOptions()
    fetch(endpoint, options)
    .then(response=>{
        return response.json()
    })
    .then(data=> {
        const validData = isTokenNotValid(data)
        if (validData) {
            writeToContainer(data)
        }
    })
}

validateJWTToken()
//getProductList()
