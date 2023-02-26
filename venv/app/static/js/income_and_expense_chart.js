
import { Ajax } from './ajax.js'
import { ChartRequest,RefreshTokenRequest } from './request.js'
import { Constant ,SearchFlow, ConditionForm } from './util.js'


class ChartConditionForm extends ConditionForm{
  check(event){
    if (super.check(event)== false){return false}
    if (document.getElementById('selectChart').value  == ""){return false}
    return true
  }
}


class Chart{
  constructor(constantObject) {
    this.constantObject = constantObject
}
  async execute(){
    // let requestObject = new RequestData(this.constantObject)
    let chartRequest = ChartRequest.create(this.constantObject)
    // let tokenRequest = requestObject.getRefreshToken()
    // let tokenRequest = RefreshTokenRequest.create(this.constantObject)
    let chartResponse = await Ajax.sendAutoRefresh(chartRequest, this.constantObject)

    let chartResponseJson = JSON.parse(chartResponse.data.chart)
    // console.log(chartResponseJson)
    let jarChart = document.getElementById('jarChart');
    Plotly.newPlot(jarChart, chartResponseJson)
  } 
}


class RegisterEvent{
  constructor(){
    this.constantObject= new Constant()
    this.chartObject= new Chart(this.constantObject)
    this.searchFlowObject= new SearchFlow()
    this.conditionFormObject= new ChartConditionForm()
  }

  initSearch(){
    this.searchFlowObject.searchEvent(this.conditionFormObject,this.chartObject)
    this.searchFlowObject.cleanSearchEvent()
  }

}

var eventObject = new RegisterEvent()
eventObject.initSearch()


