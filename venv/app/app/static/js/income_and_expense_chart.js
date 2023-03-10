
import { ChartRequest } from './request.js'
import { Constant ,ConditionFlow, ConditionForm ,Util} from './util.js'


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
    let chartRequest = ChartRequest.create(this.constantObject)
    let chartResponse = await Util.sendAjaxAndResonseToAlert(chartRequest, this.constantObject)
    if (chartResponse.is_success){
      let chartResponseJson = JSON.parse(chartResponse.data.chart)
      let jarChart = document.getElementById('jarChart');
      Plotly.newPlot(jarChart, chartResponseJson)
    }
    else{
      Util.addAlert("發生錯誤，繪圖失敗！")
    }

  } 
}


class RegisterEvent{
  constructor(){
    this.constantObject= new Constant()
    this.chartObject= new Chart(this.constantObject)
    this.searchFlowObject= new ConditionFlow()
    this.conditionFormObject= new ChartConditionForm()
  }

  initSearch(){
    this.searchFlowObject.conditionEvent(this.conditionFormObject,this.chartObject)
    this.searchFlowObject.cleanSearchEvent()
  }

}

var eventObject = new RegisterEvent()
eventObject.initSearch()





