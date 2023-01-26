

class ModalOperate
{
  constructor(event) {
    this.button = event.relatedTarget
    this.method = this.button.getAttribute('data-bs-method')
    this.#modal = document.getElementById('exampleModal')
  }
  setTitle() {
  let modalTitle = this.#modal.querySelector('.modal-title')
  modalTitle.textContent =  this.method+'紀錄'
  }
  setBtn() {
    let btn_confirm= this.#modal.querySelector('.btn-confirm')
    btn_confirm.textContent = this.method
    }
  setForm() {
    let selects = this.#modal.querySelectorAll('.form-select')
    let controls = this.#modal.querySelectorAll('.form-control')
      if (this.method == "刪除")
      {
        this.#changeAttribute(this.#setElementsAttributeDisabled,[selects, controls])
      }
      else if (this.method == "新增")
      {
        this.#changeAttribute(this.#removeElementsAttributeDisabled,[selects, controls])
      }
      else if (this.method == "修改")
      {
        this.#changeAttribute(this.#removeElementsAttributeDisabled,[selects, controls])
      }
  }

  #changeAttribute(fun, elements_array)
  {
  $.each(elements_array,function(index, elements){
    fun(elements)
  })
  }

  #setElementsAttributeDisabled(elements)
  {
  $.each(elements,function(index, value){
    value.setAttribute('disabled', "")
  })
  }
  #removeElementsAttributeDisabled(elements)
  {
  $.each(elements,function(index, value){
    value.removeAttribute('disabled')
  })
  }

}

class CurrentRow
{
  constructor(button, method) {
    if (method =="新增")
      this.#array =["0","0","0",getTodayDate(),"0",""]
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
    for (let childNodes of currentRowchildNodes){
      if (childNodes.nodeType === 1){
        this.#array.push(childNodes.textContent)
      }
    }

  }
  getTodayDate() {
    var fullDate = new Date();
    var yyyy = fullDate.getFullYear();
    var MM = (fullDate.getMonth() + 1) >= 10 ? (fullDate.getMonth() + 1) : ("0" + (fullDate.getMonth() + 1));
    var dd = fullDate.getDate() < 10 ? ("0"+fullDate.getDate()) : fullDate.getDate();
    var today = yyyy + "-" + MM + "-" + dd;
    return today;
    }

}

class JarForm{
  constructor(currentRow) {
    document.getElementById('floatingTextarea').value = currentRow.remark
    document.getElementById('money').value = currentRow.money
    document.getElementById('date').value = currentRow.date
    document.getElementById('selectType').value = currentRow.income_and_expense
    document.getElementById('selectJar').value = currentRow.jar_name
  }

  getValue(){
    this.remark = document.getElementById('floatingTextarea').value
    this.money =  document.getElementById('money').value
    this.date =  document.getElementById('date').value
    this.jar_name =  document.getElementById('selectJar').value
    this.income_and_expense =  document.getElementById('selectType').value 

  }


}


// var jarName = {
//   "1":"財務自由",
//   "2":"長期儲蓄",
//   "3":"教育成長",
//   "4":"休閒玩樂",
//   "5":"生活必須",
//   "6":"捐贈付出"
// }

$("#exampleModal").on('show.bs.modal', function (event) {
  //初始化
  let modalObject = new ModalOperate(event)
  modalObject.setTitle()
  modalObject.setBtn()
  modalObject.setForm()
  //賦值
  currentRowObject = new CurrentRow(modalObject.button, modalObject.method)
  console.log(currentRowObject)
  let jarFormObject = new JarForm(currentRowObject)
  //動作
  $("#confirm-change-btn").on("click",function(){
    jarFormObject.getValue()
    console.log(jarFormObject)
    //資料驗證
    //向後端發送ＡＪＡＸ
  
    //處理回應
  
    //改變table
  
  })


})





function status(response) {  
  if (response.status >= 200 && response.status < 300) {  
    return Promise.resolve(response)  
  } else {  
    return Promise.reject(new Error(response.statusText))  
  }  
}

function json(response) {  
  return response.json()  
}

fetch('users.json')  
  .then(status)  
  .then(json)  
  .then(function(data) {  
    console.log('Request succeeded with JSON response', data);  
  })
  .catch(function(error) {  
    console.log('Request failed', error);  
  });









