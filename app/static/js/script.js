

class ModalOperate
{
  #modal
  constructor() {
    this.#modal = document.getElementById('exampleModal')
  }

  connect(event){
    this.button = event.relatedTarget
    this.method = this.button.getAttribute('data-bs-method')
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
  #array

  getInfo(button, method) {
    if (method =="新增")
      this.#array =["0","","",Util.getTodayDate(),0,""]
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
}

class JarForm{
  constructor() {
    // this.form = document.querySelectorAll('.needs-validation')
    this.form = document.getElementById('jar-form')
  }

  setValue(currentRow){
    document.getElementById('floatingTextarea').value = currentRow.remark
    document.getElementById('money').value = currentRow.money
    document.getElementById('date').value = currentRow.date
    document.getElementById('selectType').value = currentRow.income_and_expense
    document.getElementById('selectJar').value = currentRow.jar_name

  }
  autoBootstrapValid(event){
    if (!this.form.checkValidity()) {
      console.log("基礎驗證未通過")
      // event.preventDefault()
      // event.stopPropagation()
      this.form.classList.add('was-validated')
      throw new Error("基礎驗證未通過")
    }
    else
    {
      console.log("基礎驗證通過")
      this.form.classList.add('was-validated')
    }
  }
  getValue(){
    this.remark = document.getElementById('floatingTextarea').value
    this.money =  document.getElementById('money').value
    this.date =  document.getElementById('date').value
    this.jar_name =  document.getElementById('selectJar').value
    this.income_and_expense =  document.getElementById('selectType').value 

  }
}

class Util
{
  static getTodayDate() {
    let fullDate = new Date();
    let yyyy = fullDate.getFullYear();
    let MM = (fullDate.getMonth() + 1) >= 10 ? (fullDate.getMonth() + 1) : ("0" + (fullDate.getMonth() + 1));
    let dd = fullDate.getDate() < 10 ? ("0"+fullDate.getDate()) : fullDate.getDate();
    let today = yyyy + "-" + MM + "-" + dd;
    return today;
    }

  static removeAlert(){
    let  alertPlaceholder = document.getElementById('liveAlertPlaceholder')
    let alertDiv = document.getElementById('alert')
    if (alertDiv)
      alertPlaceholder.removeChild(alertDiv)
  }
  
  static addAlert(message, type){
    let  alertPlaceholder = document.getElementById('liveAlertPlaceholder')
    let wrapper = document.createElement('div')
    let id= document.createAttribute('id')
    id.value = 'alert'
    wrapper.setAttributeNode(id)
    let icon
    if (type == 'primary')    //type= danger, primary, warning, success
      icon= '<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Info:"><use xlink:href="#info-fill"/></svg>'
    else  
      icon= '<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>'
    wrapper.innerHTML = '<div class="alert alert-' + type + ' alert-dismissible" role="alert">' + icon + message + 
    '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'
    alertPlaceholder.append(wrapper)
  }

  static getCookie(cname){
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name)==0) { return c.substring(name.length,c.length); }
    }
    return "";
  }

}




class Ajax
{
  #currentRowObject
  #modalObject
  #jarFormObject
  #request
  constructor(currentRowObject,modalObject,jarFormObject) {
    this.#currentRowObject= currentRowObject
    this.#modalObject = modalObject
    this.#jarFormObject = jarFormObject
  }

  prepareData(){
    const id = this.#currentRowObject.id
    const userId = parseInt(Util.getCookie("user_id"))
    const httpHeaders = {
      'Content-Type' : 'application/json', 
      'Accept-Charset' : 'utf-8', 
      'Accept' : 'application/json',
      'X-CSRF-TOKEN':Util.getCookie("csrf_access_token")}
    let method
    let body
    let URL = "http://127.0.0.1:5001/api/v1/income-and-expense"
    if (this.#modalObject.method == '新增')
    {
      method ='POST'
      body={
        "user_id":userId,
        "money":jarFormObject.money,
        "date":jarFormObject.date,
        "jar_name":jarFormObject.jar_name,
        "remark":jarFormObject.remark,
        "income_and_expense":()=> (jarFormObject.income_and_expense =="收入") ? 'income' : 'expense'

        }
    }
    else if (this.#modalObject.method == '修改')
    {
      method ='PUT'
      URL+="/"+id
      body={
        "user_id":userId,
        "money":jarFormObject.money,
        "date":jarFormObject.date,
        "jar_name":jarFormObject.jar_name,
        "remark":jarFormObject.remark,
        "income_and_expense":()=> (jarFormObject.income_and_expense =="收入") ? 'income' : 'expense'
        }
    }
    else if (this.#modalObject.method == '刪除')
    {
      method ='DELETE'
      URL+="/"+id
      body={"user_id":userId}
    }
    this.#request = new Request(URL, {method: method, headers: new Headers(httpHeaders),body:JSON.stringify(body)})
  }
  send(){
    fetch(this.#request)
    .then(this.#processStatus)
    .then(this.#successfullyHandling)
    .catch((res) =>res.then(this.#failHandling)
    );
  }

  #processStatus(response) {  
    if (response.status >= 200 && response.status < 300) {  
       return Promise.resolve(response.json())  
     } 
     else {  
      return Promise.reject(response.json())  
     }  
   }

   #successfullyHandling(res){
    console.log(res)
    if (res.code == 200)
      {
        Util.addAlert(JSON.stringify(res.message),'primary')
        this.responseData = JSON.parse(res.data)
        this.isSuccess = true
      }
    else
      Util.addAlert(JSON.stringify(res.message),'danger')
      this.isSuccess = false
  }

  #failHandling(res){
      console.log(res.errors.json)
      Util.addAlert(JSON.stringify(res.errors.json),'danger')
      this.isSuccess = false
    }

}

let jarFormObject = new JarForm()
let modalObject = new ModalOperate()
let currentRowObject = new CurrentRow()

$("#exampleModal").on('show.bs.modal', function (event) {

  console.log("初始化modal")
  //初始化
  modalObject.connect(event)
  modalObject.setTitle()
  modalObject.setBtn()
  modalObject.setForm()
  //賦值
  currentRowObject.getInfo(modalObject.button, modalObject.method)
  console.log(currentRowObject)
  jarFormObject.setValue(currentRowObject)

})

$("#confirm-change-btn").on("click",function(event){
  console.log("檢查form")
  jarFormObject.autoBootstrapValid(event)
  jarFormObject.getValue()
  ajaxObject = new Ajax(currentRowObject,modalObject,jarFormObject)
  ajaxObject.prepareData()
  ajaxObject.send()
  if (ajaxObject.isSuccess){
    //關閉
    //變更畫面 使用 ajaxObject.responseData
  }

})

elements = document.getElementsByName('close')
for (let element of elements){
  element.addEventListener('click',()=>Util.removeAlert(message=''))
}
