
import { IncomeAndExpenseTable } from './incomeAndExpenseTable.js'
import { JarModal,CurrentRow, JarForm } from './modalAndForm.js'
import { Util, Constant } from './util.js'

class RegisterEvent{
  constructor(){
    this.constantObject= new Constant() 
    this.currentRowObject = new CurrentRow()
    this.jarFormObject = new JarForm()
    this.jarModalObject = new JarModal()
    this.incomeAndExpenseTableObject = new IncomeAndExpenseTable(this.constantObject)
  }

initModalAndForm(){
  let that = this 
  $("#jarModal").on('show.bs.modal', function (event) {
      console.log("初始化modal")
      Util.removeAlert()
      that.jarModalObject.connect(event)
      that.currentRowObject.getInfo(that.jarModalObject.button, that.jarModalObject.method, Util.getTodayDate())
      that.jarFormObject.setValue(that.currentRowObject)
      }
    )
  } 

initTable(){
    console.log("初始化table")
    this.incomeAndExpenseTableObject.searchEvent()
    this.incomeAndExpenseTableObject.cleanSearchEvent()
  }

sendForm(){
  let that = this 
    $("#confirm-change-btn").on("click", function (event) 
      {
      that.jarFormObject.clickForm(
        event,
        that.constantObject,
        that.currentRowObject,
        that.jarModalObject,
        that.incomeAndExpenseTableObject)
      }
    ) 
  }
}

var eventObject = new RegisterEvent()
eventObject.initModalAndForm()
eventObject.initTable()
eventObject.sendForm()
