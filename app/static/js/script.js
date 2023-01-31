

class ModalOperate
{
  #modal
  constructor() {
    this.#modal = document.getElementById('jarModal')
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
  static currentRowObject 
  static modalObject 
  static jarFormObject 
  #currentRowObject
  #modalObject
  #jarFormObject
  #request
  responseData
  isSuccess

  static preparejarData(currentRowObject,modalObject,jarFormObject){
    console.log('preparejarData')
    Ajax.currentRowObject = currentRowObject
    Ajax.modalObject = modalObject
    Ajax.jarFormObject = jarFormObject

    const id = currentRowObject.id
    const userId = parseInt(Util.getCookie("user_id"))
    const money =  parseInt(jarFormObject.money)
    const income_and_expense = (jarFormObject.income_and_expense =="收入") ? 'income' : 'expense'
    const httpHeaders = {
      'Content-Type' : 'application/json', 
      'Accept-Charset' : 'utf-8', 
      'Accept' : 'application/json',
      'X-CSRF-TOKEN':Util.getCookie("csrf_access_token")}
    let method
    let body
    let URL = "http://127.0.0.1:5001/api/v1/income-and-expense"
    if (Ajax.modalObject.method == '新增')
    {
      method ='POST'
      body={
        "user_id":userId,
        "money":money,
        "date":jarFormObject.date,
        "jar_name":jarFormObject.jar_name,
        "remark":jarFormObject.remark,
        "income_and_expense": income_and_expense

        }
        console.log(body)
    }
    else if (Ajax.modalObject.method == '修改')
    {
      method ='PUT'
      URL+="/"+id
      body={
        "user_id":userId,
        "money":money,
        "date":jarFormObject.date,
        "jar_name":jarFormObject.jar_name,
        "remark":jarFormObject.remark,
        "income_and_expense": income_and_expense
        }
    }
    else if (Ajax.modalObject.method == '刪除')
    {
      method ='DELETE'
      URL+="/"+id
      body={"user_id":userId}
    }
    return  new Request(URL, {method: method, headers: new Headers(httpHeaders),body:JSON.stringify(body)})
  }


   static prepareTokenData(){
    console.log('prepareTokenData')
    const httpHeaders = {
      'Content-Type' : 'application/json', 
      'Accept-Charset' : 'utf-8', 
      'Accept' : 'application/json',
      'X-CSRF-TOKEN':Util.getCookie("csrf_refresh_token")}

    let URL = "http://127.0.0.1:5001/api/v1/token/refresh"
    let method ='POST'
    return new Request(URL, {method: method, headers: new Headers(httpHeaders)})
  }


  static send(request){
    console.log("send")
    console.log(request)
    fetch(request)
    .then(res => res.json())
    .then(Ajax.processStatus)
    .then(Ajax.successHandling)
    .catch(Ajax.failHandling)
    .then(Ajax.send)
    .then(function() {
      return Ajax.preparejarData(Ajax.currentRowObject, Ajax.modalObject, Ajax.jarFormObject)
    })
    .then(Ajax.send)



    // return new Promise((resolve, reject) => {
    //   resolve(true) 
    // })
  }

  static processStatus(response) {  
    console.log("processStatus")
    console.log(response)
    if (response.code >= 200 && response.code < 300) {  
      console.log("http200 OK")
      return Promise.resolve(response)  
     } 
    else {  
      console.log("非 http 200")
      console.log("解析msg ")
      let message = response.msg
      if ( message == ""){
        console.log("解析errors.json ")
        message= response.errors.json
      }
      else{
        console.log("不用")
      }

      return Promise.reject(new Error(message)) 
      
     }  
   }

   static failHandling(error){
    console.log("failHandling")
    console.log(error)
    let message = error.message
    console.log(message)
    if (message=="Token has expired"){
      console.log("msg  Token has expired") //待測

      return new Promise((resolve, reject) => {
        resolve(Ajax.prepareTokenData()) 
      });


      // let promise = Ajax.promise()
      // promise
      // .then(Ajax.send)
      // // .then(Ajax.preparejarData(Ajax.currentRowObject, Ajax.modalObject, Ajax.jarFormObject))
      // .then(function() {
      //   return Ajax.preparejarData(Ajax.currentRowObject, Ajax.modalObject, Ajax.jarFormObject)
      // })

      // .then(Ajax.send)


      request = Ajax.prepareTokenData()
      Ajax.send(request)
      request =Ajax.preparejarData(Ajax.currentRowObject, Ajax.modalObject, Ajax.jarFormObject)
      Ajax.send(request)
    }
    else{
      console.log("msg not Token has expired")
      Util.addAlert(JSON.stringify(message),'danger') //OK
    }
    }


  static promise() {
    return new Promise((resolve, reject) => {
      resolve(Ajax.prepareTokenData()) 
    });
  }




  static successHandling(response){
    console.log("successHandling")
    if (response.message == "token 更新成功"){
      console.log("更新成功")
    }
    else{
      Util.addAlert(JSON.stringify(response.message),'primary')
      let responseData = response.data
      console.log(responseData)
      if (Ajax.modalObject.method == "新增"){

      }
      else if (Ajax.modalObject.method == "修改"){

      }
      else if (Ajax.modalObject.method == "刪除"){

      }}
    }

}


let jarFormObject = new JarForm()
let modalObject = new ModalOperate()
let currentRowObject = new CurrentRow()

$("#jarModal").on('show.bs.modal', function (event) {

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
  // ajaxObject = new Ajax()
  request = Ajax.preparejarData(currentRowObject,modalObject,jarFormObject)
  Ajax.send(request)

})

elements = document.getElementsByName('close')
for (let element of elements){
  element.addEventListener('click',()=>Util.removeAlert())
}
