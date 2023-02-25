
import { Ajax } from './ajax.js'
import {RequestData} from './request.js'
import { Util, Constant } from './util.js'

class RegisterEvent{
  constructor(){
    this.constantObject= new Constant() 

  }

  searchEvent(){
    let that = this
    $('#search_btn').click(()=> {
      Util.removeAlert()
      if (that.#checkCondition()){
        that.#initChart()}
      else{
        Util.addAlert("搜尋條件,怪怪的喔！", 'danger')}
      }
     )
  }

  #checkCondition(){
    if (document.getElementById('selectChart').value  ==""){return false}
    if (Util.checkConditionValue() ==false){return false}
    return true
  }

  cleanSearchEvent(){
    Util.removeAlert()
    $('#clean_search_btn').click(
      ()=> {
        Util.cleanConditionValue()
      }
    )
  }

  async #initChart(){
    let requestObject = new RequestData(this.constantObject)
    let chartRequest = requestObject.getChart()
    let tokenRequest = requestObject.getRefreshToken()
    let chartResponse = await Ajax.sendAutoRefresh(chartRequest, tokenRequest, this.constantObject.httpHeaders)
    let chartResponseJson = JSON.parse(chartResponse.data.chart)
    // console.log(chartResponseJson)
    let jarChart = document.getElementById('jarChart');
    Plotly.newPlot(jarChart, chartResponseJson)
  } 

}

var eventObject = new RegisterEvent()
eventObject.searchEvent()
eventObject.cleanSearchEvent()


