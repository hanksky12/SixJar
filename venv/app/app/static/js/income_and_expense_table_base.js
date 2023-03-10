import {
  IncomeAndExpenseTable
} from './incomeAndExpenseTable.js'
import {
  JarModal,
  CurrentRow,
  JarForm
  
} from './modalAndForm.js'
import {
  Util,
  Constant,
  ConditionFlow,
  ConditionForm
} from './util.js'

class RegisterEvent {
  constructor() {
    this.constantObject = new Constant()
    this.currentRowObject = new CurrentRow()
    this.jarFormObject = new JarForm()
    this.jarModalObject = new JarModal()
    this.incomeAndExpenseTableObject = new IncomeAndExpenseTable(this.constantObject)
    this.searchFlowObject = new ConditionFlow()
    this.conditionFormObject = new ConditionForm()
  }

  initModalAndForm() {
    let that = this
    $("#jarModal").on('show.bs.modal', function (event) {
       //order is very important
      Util.removeAlert()
      that.jarModalObject.connect(event)
      that.currentRowObject.getInfo(that.jarModalObject.button, that.jarModalObject.method, Util.getTodayDate())
      console.log("印出initModalAndForm")
      console.log(that.currentRowObject)
      console.log(that.currentRowObject.remark)
      that.jarFormObject.setValue(that.currentRowObject)
    })
  }

  initSearch() {
    this.searchFlowObject.conditionEvent(this.conditionFormObject, this.incomeAndExpenseTableObject)
    this.searchFlowObject.cleanSearchEvent()
  }

  clickForm() {
    let that = this
    $("#confirm-change-btn").on("click", function (event) {
      that.jarFormObject.click(
        event,
        that.constantObject,
        that.currentRowObject,
        that.jarModalObject,
        that.incomeAndExpenseTableObject)
    })
  }
}

var eventObject = new RegisterEvent()
eventObject.initModalAndForm()
eventObject.initSearch()
eventObject.clickForm()