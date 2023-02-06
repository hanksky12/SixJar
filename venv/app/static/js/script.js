
import { IncomeAndExpenseTable } from './incomeAndExpenseTable.js'
import { ModalOperate,CurrentRow, JarForm } from './modalAndForm.js'
import { Ajax, RequestData } from './ajax.js'
import { Util, Constant } from './util.js'

class RegisterEvent{
  constructor(){
    this.constantObject= new Constant() 
    this.currentRowObject = new CurrentRow()
    this.jarFormObject = new JarForm()
    this.modalObject = new ModalOperate()
    this.incomeAndExpenseTableObject = new IncomeAndExpenseTable(this.constantObject)
  }

initModalAndForm(){
  let that = this 
  $("#jarModal").on('show.bs.modal', function (event) {
    console.log("初始化modal")
    Util.removeAlert()
    that.modalObject.connect(event)
    that.currentRowObject.getInfo(that.modalObject.button, that.modalObject.method, Util.getTodayDate())
    console.log(that.currentRowObject)
    that.jarFormObject.setValue(that.currentRowObject)
    })
} 

initTable(){
    console.log("初始化table")
    this.incomeAndExpenseTableObject.searchEvent()
    this.incomeAndExpenseTableObject.cleanSearchEvent()
  }

sendForm(){
  let that = this 
    $("#confirm-change-btn").on("click", function (event) {
      that.jarFormObject.autoBootstrapValid(event)
      if (that.jarFormObject.isChange(that.currentRowObject, that.modalObject)) {
        that.#sendRequestAndChangeTable()}
    })
  }

  #sendRequestAndChangeTable = async function() {
    let requestObject = new RequestData()
    let jarRequest = requestObject.getJar(this.constantObject, this.currentRowObject, this.modalObject, this.jarFormObject)
    let tokenRequest = requestObject.getToken(this.constantObject)
    await Ajax.sendJar(jarRequest, tokenRequest, this.constantObject.httpHeaders)
    this.incomeAndExpenseTableObject.changeDisplayRecord(this.modalObject, this.currentRowObject,Ajax.responseData)
    this.modalObject.hide()
  }
}

var eventObject = new RegisterEvent()
eventObject.initModalAndForm()
eventObject.initTable()
eventObject.sendForm()
