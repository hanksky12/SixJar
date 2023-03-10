import {
  Util
} from './util.js'
import {
  RefreshTokenRequest
} from './request.js'

class ResponseData {
  constructor(data, message, is_success = true) {
    this.data = data
    this.message = message
    this.is_success = is_success
  }
}



export class Ajax {
  static async sendAutoRefresh(request, constantObject) {
    let cloneRequest = request.clone() //fetch 目前禁止同一個request發兩次
 
    let httpHeaders = constantObject.httpHeaders
    let responseData

    let tokenObject = new RefreshTokenRequest()
    let tokenRequest = tokenObject.create(constantObject)
    try {
      responseData = await Ajax.send(request)
    } catch (error) {
      console.log(error.message)
      if (error.message == "Token has expired" || error.message == "Signature has expired") {
        await Ajax.send(tokenRequest)
        request = await Ajax.updateCsrfToken(httpHeaders, cloneRequest) // Request 用過也不能當基礎
        responseData = await Ajax.send(request)
      } else {
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
    jsonResponse = await response.json()
    jsonResponse = Ajax.processStatus(jsonResponse)
    responseData = Ajax.successHandling(jsonResponse)
    return responseData
  }

  static processStatus(response) {
    console.log("processStatus")
    console.log(response)
    if (response.code >= 200 && response.code < 300) {
      console.log("http 200-300")
      return response
    } else {
      console.log("非 http 200")
      let message
      if (response.hasOwnProperty("msg")) {
        console.log("解析msg")
        message = response.msg
      } else if (response.hasOwnProperty("message")) {
        console.log("解析message")
        message = response.message
      } else {
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
    } else {
      let responseData = new ResponseData(response.data, JSON.stringify(response.message))
      return responseData
    }
  }

  static updateCsrfToken(httpHeaders, request) {
    httpHeaders['X-CSRF-TOKEN'] = Util.getCookie("csrf_access_token")
    request = new Request(request, {
      headers: new Headers(httpHeaders)
    })
    return request
  }
}