import { Util } from './util.js'

class ResponseData  {
  constructor(data, message, is_success = true){
    this.data = data
    this.message = message
    this.is_success = is_success
}
}

export class RequestData{
  #constantObject
  constructor(constantObject){
    this.#constantObject = constantObject
  }
    getJar(currentRowObject, modalObject, jarFormObject) {
      console.log('prepareJarData')
      const id = currentRowObject.id
      const userId = this.#constantObject.userId
      let url = this.#constantObject.url + "/income-and-expense"
      let httpHeaders = this.#constantObject.httpHeaders
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
      if (modalObject.method == '新增') 
      {
        method = 'POST'
      }
      else if (modalObject.method == '修改') 
      {
        method = 'PUT'
        url += "/" + id
      }
      else if (modalObject.method == '刪除') 
      {
        method = 'DELETE'
        url += "/" + id
        body = { "user_id": userId }
      }
    //  console.log(body)  
    return this.#createRequest(url,method,httpHeaders,body)
   }
 
  getRefreshToken() {
     console.log('prepareTokenData')
     let httpHeaders = this.#constantObject.httpHeaders
     httpHeaders['X-CSRF-TOKEN'] = Util.getCookie("csrf_refresh_token")
     const url = this.#constantObject.url + "/token/refresh"
    return this.#createRequest(url,"POST",httpHeaders)
   }

  getUser() {
    console.log('prepareUserData')
    const url = this.#constantObject.url + "/users/" + this.#constantObject.userId
    return this.#createRequest(url,"GET",this.#constantObject.httpHeaders)
  }

  getUserLogin(mail, password) {
    console.log('prepareUserLoginData')
    const url = this.#constantObject.url + "/users/login"
    const body = {
      "email": mail,
      "password": password,
      "remember_me": true
    }
    return this.#createRequest(url,"POST",this.#constantObject.httpHeaders,body)
  }

  #createRequest(url,method,httpHeaders,body){
    if (body ==undefined) {
      return new Request(url, { method: method, headers: new Headers(httpHeaders) })}
    else{
      return new Request(url, { method: method, headers: new Headers(httpHeaders) , body: JSON.stringify(body)})
    }
  }

 }
 
 export class Ajax {
   static responseData
   static async sendAutoRefresh(request, tokenRequest, httpHeaders) {
     let cloneRequest = request.clone()//fetch 目前禁止同一個request發兩次
     let responseData
     try {
      responseData = await Ajax.send(request)
     }
     catch (error) {
       console.log(error.message)
       if (error.message == "Token has expired") {
         await Ajax.send(tokenRequest)
         request = await Ajax.updateCsrfToken(httpHeaders, cloneRequest)// Request 用過也不能當基礎
         responseData = await Ajax.send(request)
       }
       else {
         responseData = new ResponseData({}, error.message, false)
       }
     }
     return responseData 
   }
 
   static async send(request) {
    console.log("send")
    let response 
    let jsonResponse
    let responseData
    response = await fetch(request)
    jsonResponse = await Ajax.json(response)
    jsonResponse = await Ajax.processStatus(jsonResponse)
    responseData =  await Ajax.successHandling(jsonResponse)
    return responseData
   }
 
   static json(res) {
     return res.json()}
   
   static processStatus(response) {
     console.log("processStatus")
     console.log(response)
     if (response.code >= 200 && response.code < 300) {
       console.log("http 200-300")
       return response
     }
     else {
       console.log("非 http 200")
       let message
       if (response.hasOwnProperty("msg")){
         console.log("解析msg")
         message = response.msg
       }
       else if (response.hasOwnProperty("message")){ 
         console.log("解析message")
         message = response.message
       }
       else{ 
         console.log("解析errors.json ")
         message = response.errors.json
       }
       throw new Error(message)
     }
   }
 
   static successHandling(response) {
     console.log("successHandling")
     if (response.message == "token 更新成功") {
       console.log("更新成功") //單純更新token 不定義responseData
     }
     else {
      let responseData = new ResponseData(response.data, JSON.stringify(response.message))
      return responseData
     }
   }
 
   static updateCsrfToken(httpHeaders, request) {
     httpHeaders['X-CSRF-TOKEN'] = Util.getCookie("csrf_access_token")
     request = new Request(request, {headers: new Headers(httpHeaders)})
     return request
   }
 }



 