import { Util } from './util.js'
import { Ajax } from './ajax.js'
import {UserRequest, UserLoginRequest, JarRequest} from './request.js'
import { AbstractForm, AbstractModal } from './abstract.js'



export  class CurrentRow {
  #array
  getInfo(button, method, today) {
      if (method == "新增"){
        this.#array = ["0", "", "", today, 0, ""]}
      else{
        this.#array = []
        this.takeCurrentRowDataToArray(button)
        this.id = this.#array[0];
        this.income_and_expense = this.#array[1];
        this.jar_name = this.#array[2];
        this.date = this.#array[3];
        this.money = this.#array[4];
        this.remark = this.#array[5];
    }
  }

  takeCurrentRowDataToArray(button) {
      let currentRowchildNodes = button.parentNode.parentNode.childNodes
      for (let childNodes of currentRowchildNodes) {
      if (childNodes.nodeType === 1) {
          this.#array.push(childNodes.textContent)
        }
      }
    }
  }

class PasswordModal extends AbstractModal {
  constructor() {
    super('passwordModal')
  }
}

export class JarModal extends AbstractModal {
    constructor() {
      super('jarModal')
    }
  
    connect(event) {
      this.button = event.relatedTarget
      this.method = this.button.getAttribute('data-bs-method')
      this.#setTitle()
      this.#setBtn()
      this.#setForm()
    }
  
    #setTitle() {
      let modalTitle = this.modal.querySelector('.modal-title')
      modalTitle.textContent = this.method + '紀錄'
    }
    #setBtn() {
      let btn_confirm = this.modal.querySelector('.btn-confirm')
      btn_confirm.textContent = this.method
    }
    #setForm() {
      let selects = this.modal.querySelectorAll('.form-select')
      let controls = this.modal.querySelectorAll('.form-control')
      if (this.method == "刪除") {
        this.#changeAttribute(this.#setElementsAttributeDisabled, [selects, controls])
      }
      else if (this.method == "新增") {
        this.#changeAttribute(this.#removeElementsAttributeDisabled, [selects, controls])
      }
      else if (this.method == "修改") {
        this.#changeAttribute(this.#removeElementsAttributeDisabled, [selects, controls])
      }
    }
  
    #changeAttribute(fun, elements_array) {
      $.each(elements_array, function (index, elements) {
        fun(elements)
      })
    }
  
    #setElementsAttributeDisabled(elements) {
      $.each(elements, function (index, value) {
        value.setAttribute('disabled', "")
      })
    }
    #removeElementsAttributeDisabled(elements) {
      $.each(elements, function (index, value) {
        value.removeAttribute('disabled')
      })
    }
  }
  

  
export  class JarForm extends AbstractForm{
    constructor() {
        super('jar-form')
    }

    setValue(currentRow) {
        document.getElementById('floatingTextarea').value = currentRow.remark
        document.getElementById('money').value = currentRow.money
        document.getElementById('date').value = currentRow.date
        document.getElementById('selectType').value = currentRow.income_and_expense
        document.getElementById('selectJar').value = currentRow.jar_name
    }


    async click(event,constantObject,currentRowObject,jarModalObject,incomeAndExpenseTableObject)
    {
      this.#getValue()
      if (this.autoBootstrapValid(event)== false) return
      if (this.#isChange(currentRowObject, jarModalObject) == false) return
      if (await this.#inputPassword(jarModalObject,constantObject)== false) return
      await this.#sendRequestAndChangeDisplay(constantObject,currentRowObject,jarModalObject,incomeAndExpenseTableObject)
      jarModalObject.hide()
    }

    async #inputPassword(jarModalObject,constantObject){
      if (jarModalObject.method!="刪除") {return true}
      jarModalObject.hide()
      let userPasswordObject = new UserPasswordFlow()
      if (await userPasswordObject.check(constantObject)){return true}
      return false
    }


    #isChange(currentRow, modalObject){
        if (modalObject.method=="刪除") return true
        if (this.money !=currentRow.money) return true
        if (this.remark !=currentRow.remark) return true
        if (this.date !=currentRow.date) return true
        if (this.income_and_expense !=currentRow.income_and_expense) return true
        if (this.jar_name !=currentRow.jar_name) return true
        Util.addAlert("沒有變更", 'danger')
        modalObject.hide()
        return false
    }

    async #sendRequestAndChangeDisplay(constantObject,currentRowObject,jarModalObject, incomeAndExpenseTableObject) {
      console.log("sendRequestAndChangeDisplay")
      let jarRequest = JarRequest.create(constantObject,currentRowObject,jarModalObject, this)
      let responseData = await Util.sendAjaxAndResonseToAlert(jarRequest, constantObject)
      incomeAndExpenseTableObject.changeDisplayRecord(jarModalObject, currentRowObject, responseData.data)

    }

    #getValue() {
        this.remark = document.getElementById('floatingTextarea').value
        this.money = document.getElementById('money').value
        this.date = document.getElementById('date').value
        this.jar_name = document.getElementById('selectJar').value
        this.income_and_expense = document.getElementById('selectType').value
      }
    }

export class UserPasswordFlow{
  async check(constantObject){
    let passwordModalObject = new PasswordModal() 
    passwordModalObject.show()
    let passwordFormObject = new PasswordForm()
    let is_pass = await passwordFormObject.checkPassword(constantObject)
    if (is_pass){
      passwordModalObject.hide()
      return true}
    Util.addAlert("密碼錯誤，請檢查長度是否介於2-10", 'danger')
    return false
  }


}

class PasswordForm extends AbstractForm{
  constructor() {
    super('password-form')
  }

   checkPassword(constantObject){
    let that = this
    return new Promise
    (
      function (resolve, reject) {
        $("#send-password-btn").on("click", (event)=> {
          // console.log("點擊送出按鈕")
          let is_pass = that.autoBootstrapValid(event)?true:false
          resolve(is_pass)
          })
      }
    )
    .then((is_pass)=>{
      if (is_pass){is_pass = that.#sendRequest(constantObject)}
      return is_pass
      }
    )
  }


  async #sendRequest(constantObject) {
    console.log("送出使用者密碼驗證")
    let userRequest = UserRequest.create(constantObject)
    let userResponse = await Ajax.sendAutoRefresh(userRequest,  constantObject)
    let password = document.getElementById('inputPassword').value
    let userLoginRequest = UserLoginRequest.create(constantObject,userResponse.data.email, password)
    let userLoginResponse = await Ajax.sendAutoRefresh(userLoginRequest, constantObject)
    if (userLoginResponse.is_success){return true}
    console.log("密碼錯誤")
    return false
  }
}