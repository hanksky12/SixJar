import { Util } from './util.js'

export class RequestData{
    getJar(constantObject, currentRowObject, modalObject, jarFormObject) {
     constantObject =  $.extend(true, {}, constantObject);
     console.log('prepareJarData')
     const id = currentRowObject.id
     const userId = constantObject.userId
     constantObject.httpHeaders['X-CSRF-TOKEN'] = Util.getCookie("csrf_access_token")
     let body = {
         "user_id": userId,
         "money": parseInt(jarFormObject.money),
         "date": jarFormObject.date,
         "jar_name": jarFormObject.jar_name,
         "remark": jarFormObject.remark,
         "income_and_expense": (jarFormObject.income_and_expense == "收入") ? 'income' : 'expense'
       }
     let method
     let URL = constantObject.url + "/income-and-expense"
     if (modalObject.method == '新增') 
     {
       method = 'POST'
     }
     else if (modalObject.method == '修改') 
     {
       method = 'PUT'
       URL += "/" + id
     }
     else if (modalObject.method == '刪除') 
     {
       method = 'DELETE'
       URL += "/" + id
       body = { "user_id": userId }
     }
     console.log(body)
     return new Request(URL, { method: method, headers: new Headers(constantObject.httpHeaders), body: JSON.stringify(body) })
   }
 
    getToken(constantObject) {
     constantObject =  $.extend(true, {}, constantObject);
     console.log('prepareTokenData')
     constantObject.httpHeaders['X-CSRF-TOKEN'] = Util.getCookie("csrf_refresh_token")
     const URL = constantObject.url + "/token/refresh"
     return new Request(URL, { method: 'POST', headers: new Headers(constantObject.httpHeaders) })
   }
 }
 
 export class Ajax {
   static responseData
   static async sendJar(request, tokenRequest, httpHeaders) {
     let cloneRequest = request.clone()//fetch 目前禁止同一個request發兩次
     try 
     {
       await Ajax.send(request)
     }
     catch (error) 
     {
       let message = error.message
       console.log(message)
       if (message == "Token has expired") {
         await Ajax.send(tokenRequest)
         request = await Ajax.updateCsrfToken(httpHeaders, cloneRequest)// Request 用過也不能當基礎
         await Ajax.send(request)
       }
       else {
         Util.addAlert(JSON.stringify(message), 'danger') 
       }
     }
   }
 
   static async send(request) {
     console.log("send")
     let response 
     let jsonResponse
     response = await fetch(request)
     jsonResponse = await Ajax.json(response)
     jsonResponse = await Ajax.processStatus(jsonResponse)
     await Ajax.successHandling(jsonResponse)
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
       console.log("更新成功") //單純更新token 不定義response.data 
     }
     else {
       Util.addAlert(JSON.stringify(response.message), 'primary')
       console.log(response.data)
       Ajax.responseData = response.data //唯一成功才取 response.data 
     }
   }
 
   static updateCsrfToken(httpHeaders, request) {
     httpHeaders['X-CSRF-TOKEN'] = Util.getCookie("csrf_access_token")
     request = new Request(request, {headers: new Headers(httpHeaders)})
     return request
   }
 }
 