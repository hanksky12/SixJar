import {
  Util
} from './util.js'



export class JarRequest {

  static create(constantObject, currentRowObject, modalObject, jarFormObject) {
    console.log('prepareJarData')
    const id = currentRowObject.id
    const userId = constantObject.userId
    let url = constantObject.url + "/income-and-expense"
    let httpHeaders = constantObject.httpHeaders
    httpHeaders['X-CSRF-TOKEN'] = Util.getCookie("csrf_access_token")
    let body = {
      "user_id": userId,
      "money": parseInt(jarFormObject.money),
      "date": jarFormObject.date,
      "jar_name": jarFormObject.jar_name,
      "remark": jarFormObject.remark,
      "income_and_expense": (jarFormObject.income_and_expense == "收入") ? 'income' : 'expense'
    }
    let method
    if (modalObject.method == '新增') {
      method = 'POST'
    } else if (modalObject.method == '修改') {
      method = 'PUT'
      url += "/" + id
    } else if (modalObject.method == '刪除') {
      method = 'DELETE'
      url += "/" + id
      body = {
        "user_id": userId
      }
    }
    return Util.createRequest(url, method, httpHeaders, body)
  }
}

export class RefreshTokenRequest {

  static create(constantObject) {
    console.log('prepareTokenData')
    let httpHeaders = constantObject.httpHeaders
    httpHeaders['X-CSRF-TOKEN'] = Util.getCookie("csrf_refresh_token")
    const url = constantObject.url + "/token/refresh"
    return Util.createRequest(url, "POST", httpHeaders)
  }
}


export class ChartRequest {

  static create(constantObject) {
    console.log('prepareChartData')
    let url = constantObject.url + "/income-and-expense/chart"
    let temp = {
      user_id: constantObject.userId,
      sortOrder: 'desc'
    }
    if ($('#selectChart').val()) {
      temp["chart_type"] = $('#selectChart').val()
    }
    temp = Util.getConditionValue(temp)
    url += '?' + (new URLSearchParams(temp)).toString();
    console.log(url)
    return Util.createRequest(url, "GET", constantObject.httpHeaders)
  }
}

export class FakeRequest {

  static create(constantObject) {
    console.log('prepareFakeData')
    let url = constantObject.url + "/income-and-expense/fake-data"
    let body = {
      user_id: constantObject.userId
    }
    if ($('#selectRecordsNumber').val()) {
      body["number"] = $('#selectRecordsNumber').val()
    }
    body = Util.getConditionValue(body)
    console.log(body)
    return Util.createRequest(url, "POST", constantObject.httpHeaders, body)
  }
}

export class UserRequest {

  static create(constantObject) {
    console.log('prepareUserData')
    const url = constantObject.url + "/users/" + constantObject.userId
    return Util.createRequest(url, "GET", constantObject.httpHeaders)
  }
}

export class UserLoginRequest {

  static create(constantObject, mail, password) {
    console.log('prepareUserLoginData')
    const url = constantObject.url + "/users/login"
    const body = {
      "email": mail,
      "password": password,
      "remember_me": true
    }
    return Util.createRequest(url, "POST", constantObject.httpHeaders, body)
  }
}


// export class RequestData {
//     #constantObject
//     constructor(constantObject) {
//       this.#constantObject = constantObject
//     }
// getJar(currentRowObject, modalObject, jarFormObject) {
//   console.log('prepareJarData')
//   const id = currentRowObject.id
//   const userId = this.#constantObject.userId
//   let url = this.#constantObject.url + "/income-and-expense"
//   let httpHeaders = this.#constantObject.httpHeaders
//   httpHeaders['X-CSRF-TOKEN'] = Util.getCookie("csrf_access_token")
//   let body = {
//     "user_id": userId,
//     "money": parseInt(jarFormObject.money),
//     "date": jarFormObject.date,
//     "jar_name": jarFormObject.jar_name,
//     "remark": jarFormObject.remark,
//     "income_and_expense": (jarFormObject.income_and_expense == "收入") ? 'income' : 'expense'
//   }
//   let method
//   if (modalObject.method == '新增') {
//     method = 'POST'
//   } else if (modalObject.method == '修改') {
//     method = 'PUT'
//     url += "/" + id
//   } else if (modalObject.method == '刪除') {
//     method = 'DELETE'
//     url += "/" + id
//     body = {
//       "user_id": userId
//     }
//   }
//   //  console.log(body)  
//   return this.#createRequest(url, method, httpHeaders, body)
// }

// getRefreshToken() {
//   console.log('prepareTokenData')
//   let httpHeaders = this.#constantObject.httpHeaders
//   httpHeaders['X-CSRF-TOKEN'] = Util.getCookie("csrf_refresh_token")
//   const url = this.#constantObject.url + "/token/refresh"
//   return this.#createRequest(url, "POST", httpHeaders)
// }

// getChart(){
//   console.log('prepareChartData')
//   let url = this.#constantObject.url + "/income-and-expense/chart"
//   let temp = {user_id:this.#constantObject.userId,
//     sortOrder:'desc'}
//   if ($('#selectChart').val()){temp["chart_type"] = $('#selectChart').val()}
//   temp = Util.getConditionValue(temp)
//   url += '?' + ( new URLSearchParams( temp ) ).toString();
//   console.log(url)
//   return this.#createRequest(url, "GET", this.#constantObject.httpHeaders)
// }

// getFake(){
//   console.log('prepareFakeData')
//   let url = this.#constantObject.url + "/income-and-expense/fake-data"
//   let body = {user_id:this.#constantObject.userId}
//   if ($('#selectRecordsNumber').val()){body["number"] = $('#selectRecordsNumber').val()}
//   body = Util.getConditionValue(body)
//   console.log(body)
//   return this.#createRequest(url, "POST", this.#constantObject.httpHeaders, body)
// }


// getUser() {
//   console.log('prepareUserData')
//   const url = this.#constantObject.url + "/users/" + this.#constantObject.userId
//   return this.#createRequest(url, "GET", this.#constantObject.httpHeaders)
// }

// getUserLogin(mail, password) {
//   console.log('prepareUserLoginData')
//   const url = this.#constantObject.url + "/users/login"
//   const body = {
//     "email": mail,
//     "password": password,
//     "remember_me": true
//   }
//   return this.#createRequest(url, "POST", this.#constantObject.httpHeaders, body)
// }

// #createRequest(url, method, httpHeaders, body) {
//   if (body == undefined) {
//     return new Request(url, {
//       method: method,
//       headers: new Headers(httpHeaders)
//     })
//   } else {
//     return new Request(url, {
//       method: method,
//       headers: new Headers(httpHeaders),
//       body: JSON.stringify(body)
//     })
//   }
// }
// }