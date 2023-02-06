import { Util } from './util.js'

export class ModalOperate {
    #modal
    #bootstrapModal
    constructor() {
      this.#modal = document.getElementById('jarModal')
      this.#bootstrapModal = new bootstrap.Modal(this.#modal, { keyboard: false})
    }
  
    connect(event) {
      this.button = event.relatedTarget
      this.method = this.button.getAttribute('data-bs-method')
      this.#setTitle()
      this.#setBtn()
      this.#setForm()
    }
  
    #setTitle() {
      let modalTitle = this.#modal.querySelector('.modal-title')
      modalTitle.textContent = this.method + '紀錄'
    }
    #setBtn() {
      let btn_confirm = this.#modal.querySelector('.btn-confirm')
      btn_confirm.textContent = this.method
    }
    #setForm() {
      let selects = this.#modal.querySelectorAll('.form-select')
      let controls = this.#modal.querySelectorAll('.form-control')
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
    hide(){
        this.#bootstrapModal.hide()
        // Util.removeAlert()
    }
  }
  
export  class CurrentRow {
    #array
    getInfo(button, method, today) {
        if (method == "新增")
        this.#array = ["0", "", "", today, 0, ""]
        else
        this.#array = []
        this.takeCurrentRowDataToArray(button)
        this.id = this.#array[0];
        this.income_and_expense = this.#array[1];
        this.jar_name = this.#array[2];
        this.date = this.#array[3];
        this.money = this.#array[4];
        this.remark = this.#array[5];
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
  
export  class JarForm {
    constructor() {
        this.form = document.getElementById('jar-form')
    }

    setValue(currentRow) {
        document.getElementById('floatingTextarea').value = currentRow.remark
        document.getElementById('money').value = currentRow.money
        document.getElementById('date').value = currentRow.date
        document.getElementById('selectType').value = currentRow.income_and_expense
        document.getElementById('selectJar').value = currentRow.jar_name
    }
    autoBootstrapValid(event) {
        if (!this.form.checkValidity()) {
        console.log("基礎驗證未通過")
        this.form.classList.add('was-validated')
        throw new Error("基礎驗證未通過")
        }
        else {
        console.log("基礎驗證通過")
        this.form.classList.add('was-validated')
        }
    }

    isChange(currentRow, modalObject){
        self.#getValue()
        if (this.money !=currentRow.money) return true
        if (this.remark !=currentRow.remark) return true
        if (this.date !=currentRow.date) return true
        if (this.income_and_expense !=currentRow.income_and_expense) return true
        if (this.jar_name !=currentRow.jar_name) return true
        Util.addAlert("沒有變更", 'danger')
        modalObject.hide()
        return false
    }

    #getValue() {
        this.remark = document.getElementById('floatingTextarea').value
        this.money = document.getElementById('money').value
        this.date = document.getElementById('date').value
        this.jar_name = document.getElementById('selectJar').value
        this.income_and_expense = document.getElementById('selectType').value
    }

    }
  