

import {
    ExchangeRateRequest
  } from './request.js'
  import {
    Util,
    Constant
  } from './util.js'


class ExchangeRate{

    constructor() {
        let base_currency_str = document.getElementById('base-currency').value
        this.base_currency = base_currency_str.split(';')[0].split(':')[1]
        this.target_currency = document.getElementById('target-currency').value
        this.other_target_currency = document.getElementById('other-target-currency').value
        // console.log(this.base_currency, this.target_currency,this.other_target_currency)
      }


    checkValue() {
        if (this.target_currency==="" & this.other_target_currency===""){
            console.log("兩者皆為空")
            return false
        }
        if (this.target_currency!=="" & this.other_target_currency!==""){
            console.log("兩者都不為空")
            return false
        }
        if (this.base_currency===this.target_currency || this.base_currency===this.other_target_currency){
            console.log("基礎與目標相等")
            return false
        }
        if (this.other_target_currency!=="")
            this.target_currency= this.other_target_currency
        return true
    }


}


class ChangeSaving{
    constructor(exchangeRateObject,responseData) {
        this.exchangeRateObject = exchangeRateObject
        this.responseData = responseData
      }
    changeRate(){
        document.getElementById("base-currency").value =
         `目前單位:${this.exchangeRateObject.target_currency}; 目標匯率轉換：1 ${this.exchangeRateObject.base_currency} = ${this.responseData.data.rate} ${this.exchangeRateObject.target_currency}` ;
    }
    changeSaving(){
        const savingsList = document.querySelectorAll('.money');
        $.each(savingsList, (index, elements)=> {
            const moneyText = elements.textContent.replace("元", "");
            // console.log(moneyText)
            elements.textContent = Math.round((parseInt(moneyText) * this.responseData.data.rate)).toString()+ '元'
          })
    }
}


class RegisterEvent {
    constructor() {
      this.constantObject = new Constant()
    }
  
    initGet(){
      let that = this
        $("#change_btn").on('click', async () =>{
            const exchangeRateObject = new ExchangeRate()//送出當下再取值
            if (exchangeRateObject.checkValue() === false) {
                Util.addAlert("條件設定矛盾，必須選填單一幣別，或是目標與基礎幣別必須不相等", 'danger')
                return}
            const exchangeRateRequest = ExchangeRateRequest.create(that.constantObject, exchangeRateObject.base_currency, exchangeRateObject.target_currency)
            let responseData = await Util.sendAjaxAndResonseToAlert(exchangeRateRequest, that.constantObject)
            if (responseData.message !== '"查詢成功"') return
            const changeSaving = new ChangeSaving(exchangeRateObject,responseData)
            changeSaving.changeRate()
            changeSaving.changeSaving()
        }
      )
    }
  }
  
  
  var eventObject = new RegisterEvent()
  eventObject.initGet()