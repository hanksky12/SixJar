

class ModalOperate {
  #modal
  constructor() {
    this.#modal = document.getElementById('jarModal')
  }

  connect(event) {
    this.button = event.relatedTarget
    this.method = this.button.getAttribute('data-bs-method')
  }

  setTitle() {
    let modalTitle = this.#modal.querySelector('.modal-title')
    modalTitle.textContent = this.method + '紀錄'
  }
  setBtn() {
    let btn_confirm = this.#modal.querySelector('.btn-confirm')
    btn_confirm.textContent = this.method
  }
  setForm() {
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

}

class CurrentRow {
  #array
  getInfo(button, method) {
    if (method == "新增")
      this.#array = ["0", "", "", Util.getTodayDate(), 0, ""]
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

class JarForm {
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
      // event.preventDefault()
      // event.stopPropagation()
      this.form.classList.add('was-validated')
      throw new Error("基礎驗證未通過")
    }
    else {
      console.log("基礎驗證通過")
      this.form.classList.add('was-validated')
    }
  }
  getValue() {
    this.remark = document.getElementById('floatingTextarea').value
    this.money = document.getElementById('money').value
    this.date = document.getElementById('date').value
    this.jar_name = document.getElementById('selectJar').value
    this.income_and_expense = document.getElementById('selectType').value
  }
}

class Util {
  static getTodayDate() {
    let fullDate = new Date();
    let yyyy = fullDate.getFullYear();
    let MM = (fullDate.getMonth() + 1) >= 10 ? (fullDate.getMonth() + 1) : ("0" + (fullDate.getMonth() + 1));
    let dd = fullDate.getDate() < 10 ? ("0" + fullDate.getDate()) : fullDate.getDate();
    let today = yyyy + "-" + MM + "-" + dd;
    return today;
  }

  static removeAlert() {
    let alertPlaceholder = document.getElementById('liveAlertPlaceholder')
    let alertDiv = document.getElementById('alert')
    if (alertDiv)
      alertPlaceholder.removeChild(alertDiv)
  }

  static addAlert(message, type) {
    let alertPlaceholder = document.getElementById('liveAlertPlaceholder')
    let wrapper = document.createElement('div')
    let id = document.createAttribute('id')
    id.value = 'alert'
    wrapper.setAttributeNode(id)
    let icon
    if (type == 'primary')    //type= danger, primary, warning, success
      icon = '<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Info:"><use xlink:href="#info-fill"/></svg>'
    else
      icon = '<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>'
    wrapper.innerHTML = '<div class="alert alert-' + type + ' alert-dismissible" role="alert">' + icon + message +
      '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'
    alertPlaceholder.append(wrapper)
  }

  static getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i].trim();
      if (c.indexOf(name) == 0) { return c.substring(name.length, c.length); }
    }
    return "";
  }
}
class RequestData{
  static httpHeaders = {
    'Content-Type': 'application/json',
    'Accept-Charset': 'utf-8',
    'Accept': 'application/json'
  }

  constructor(currentRowObject, modalObject, jarFormObject) {
    this.currentRowObject = currentRowObject
    this.modalObject = modalObject
    this.jarFormObject = jarFormObject
  }
   getJar() {
    console.log('preparejarData')
    const id = this.currentRowObject.id
    const userId = Constant.userId
    RequestData.httpHeaders['X-CSRF-TOKEN'] = Util.getCookie("csrf_access_token")
    let body = {
        "user_id": userId,
        "money": parseInt(this.jarFormObject.money),
        "date": this.jarFormObject.date,
        "jar_name": this.jarFormObject.jar_name,
        "remark": this.jarFormObject.remark,
        "income_and_expense": (this.jarFormObject.income_and_expense == "收入") ? 'income' : 'expense'
      }
    let method
    let URL = Constant.url + "/income-and-expense"
    if (this.modalObject.method == '新增') 
    {
      method = 'POST'
    }
    else if (this.modalObject.method == '修改') 
    {
      method = 'PUT'
      URL += "/" + id
    }
    else if (this.modalObject.method == '刪除') 
    {
      method = 'DELETE'
      URL += "/" + id
      body = { "user_id": userId }
    }
    console.log(body)
    return new Request(URL, { method: method, headers: new Headers(RequestData.httpHeaders), body: JSON.stringify(body) })
  }

  static getToken() {
    console.log('prepareTokenData')
    RequestData.httpHeaders['X-CSRF-TOKEN'] = Util.getCookie("csrf_refresh_token")
    const URL = RequestData.url + "/token/refresh"
    return new Request(URL, { method: 'POST', headers: new Headers(RequestData.httpHeaders) })
  }
}

class Ajax {
  static responseData
  static async sendJar(requestData) {
    try 
    {
      await Ajax.send(requestData.getJar())
    }
    catch (error) 
    {
      let message = error.message
      console.log(message)
      if (message == "Token has expired") {
        await Ajax.send(RequestData.getToken())
        await Ajax.send(requestData.getJar())
      }
      else {
        Util.addAlert(JSON.stringify(message), 'danger') 
      }
    }
  }

  static async send(request) {
    console.log("send")
    let response 
    let jsonResponse 
    response = await fetch(request)
    jsonResponse = await Ajax.json(response)
    jsonResponse = await Ajax.processStatus(jsonResponse)
    await Ajax.successHandling(jsonResponse)
  }

  static json(res) {
    return res.json()}
  
  static processStatus(response) {
    console.log("processStatus")
    console.log(response)
    if (response.code >= 200 && response.code < 300) {
      console.log("http 200-300")
      return response
    }
    else {
      console.log("非 http 200")
      let message = response.msg
      if (message == "") {
        console.log("解析errors.json ")
        message = response.errors.json
      }
      throw new Error(message)
    }
  }

  static successHandling(response) {
    console.log("successHandling")
    if (response.message == "token 更新成功") {
      console.log("更新成功") //單純更新token 不定義response.data 
    }
    else {
      Util.addAlert(JSON.stringify(response.message), 'primary')
      console.log(response.data)
      Ajax.responseData = response.data //唯一成功才取 response.data 
    }
  }
}


class Constant{
  static userId = parseInt(Util.getCookie("user_id"))
  static url = "http://127.0.0.1:5001/api/v1"
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////
let $table = $('#table')
let jarFormObject = new JarForm()
let modalObject = new ModalOperate()
let currentRowObject = new CurrentRow()


function operateFormatter(value, row, index) {
  return [
    '<button type="button" class="btn btn-warning btnSelect" data-bs-toggle="modal" data-bs-target="#jarModal" data-bs-method="修改">',
    '修改',
    '</button>  ',
    '<button type="button" class="btn btn-danger btnSelect" data-bs-toggle="modal" data-bs-target="#jarModal" data-bs-method="刪除">',
    '刪除',
    '</button>'
  ].join('')
}
window.ajaxOptions = {
  beforeSend: function (xhr) {
    //重設cookie
    // xhr.setRequestHeader('custom-auth-token', 'custom-auth-token')
  }
}

function initTable() {
  $table
  .bootstrapTable('destroy')//先清空
  .bootstrapTable({
    //裝飾
    height: 550,
    theadClasses: "thead-dark",
    classes:"table table-striped table-hover border-primary table-bordered table-sm table-dark",
    toolbar:"#toolbar",
    striped: true,  //間隔顏色
    //表格定義
    columns: [
      {
        field: 'id',
        title: 'Id',
        align: 'center',
        width:20, 
        visible:false//隱藏
      }, {
        field: 'income_and_expense',
        title: '類型',
        align: 'center',
        width:60,
        formatter: (data)=>{ return data == "income" ? "收入" : "支出"}//轉換
      },
      {
        field: 'jar_name',
        title: '帳戶',
        sortable: true,//可以被發送request排序的欄位
        align: 'center'
      }, {
        field: 'date',
        title: '日期',
        sortable: true,
        align: 'center'
      }, {
        field: 'money',
        title: '金額(元)',
        sortable: true,
        align: 'center',

      },{
        field: 'remark',
        title: '備註',
        align: 'center'
      },{
        field: 'operate',
        title: '操作',
        align: 'center',
        width:130, 
        clickToSelect: false,
        // events: window.operateEvents,
        formatter: operateFormatter
      }
    ],
    //Ajax定義
    method : 'get',
    contentType: "application/json",
    url : "http://127.0.0.1:5001/api/v1/income-and-expense/search",   
    queryParams : (params)=> {
      let temp = {
        limit : params.limit, // 因為一次只要顯示一頁,所以這邊等於一頁的頁數即可
        offset : params.offset, // SQL语句起始索引
        page : (params.offset / params.limit) + 1, //当前页码 
        sortOrder: params.order, //找sortOrder的參數
        user_id:Constant.userId
      }
      if (params.sort){temp["sort"] = params.sort} //如果有點擊欄位，就會抓到欄位名稱
      if ($('#selectTypeForSearch').val()){
        temp["income_and_expense"] = $('#selectTypeForSearch').val()=="收入"?"income":"expense"
      }
      if ($('#selectJarForSearch').val()){temp["jar_name"] = $('#selectJarForSearch').val()}
      let idArray = ['minimum_money','maximum_money',"earliest_date","latest_date"]
      for (let id of idArray) { if ($("#"+id).val()){temp[id] = $("#"+id).val()}}
      return temp
    },
    // dataField: "data",//後端回來裝data的key(用responseHandler處理掉), 後端分頁時需返回含有total：總記錄數
    responseHandler:(res)=>{return res.data},
    //分頁相關
    sidePagination: "server",//分页方式：client ,server 服务端分页
    cache: false,   //是否使用缓存，默认为 true，所以一般情况下需要设置一下这个属性
    uniqueId:"Id", // 用來指定某個title當作方法removeByUniqueId,updateByUniqueId..的搜尋欄位
    pageList: [10, 25, 50, 100],        //可供選擇的每頁的行數
    pageNumber:1,//初始頁
    pageSize:5,//單頁記錄數
    pagination: true,  //是否顯示分頁
    //排序相關
    onSort:function(name,order)
    {//當有欄位排序的三角被點擊時,用這個刷新固有參數
      $table.bootstrapTable('refreshOptions', {sortName:name,sortOrder:order})
    },
    sortable:true, //開啟排序，會在onSort重抓參數後，自動像後端發送目前參數的request
    sortOrder:"asc",//預設
    // search:true, //******顯示搜索框****// 參數向後端帶 不實做
    // searchOnEnterKey:false, //******回车后执行搜索****//
  })
}

initTable()

$('#search_btn').click(function() {
  //自己實作的
	$table.bootstrapTable('refresh', {
		url : "http://127.0.0.1:5001/api/v1/income-and-expense/search"
	});
})


 sendRequestAndChangeTable = async function(currentRowObject, modalObject, jarFormObject) {
  let requestData = await new RequestData(currentRowObject, modalObject, jarFormObject)
  await Ajax.sendJar(requestData)
  console.log("responseData")
  console.log(Ajax.responseData)
  if (modalObject.method == "刪除"){
    $table.bootstrapTable('removeByUniqueId', currentRowObject.id); 
  }
  else if (modalObject.method == "修改"){
    $table.bootstrapTable('updateByUniqueId', {
      id: currentRowObject.id, 
      replace:true,
      row: {
        income_and_expense: Ajax.responseData.income_and_expense,
        jar_name: Ajax.responseData.jar_name,
        date: Ajax.responseData.date,
        money: Ajax.responseData.money,
        remark: Ajax.responseData.remark
      }
 });
  }
  else if (modalObject.method == "新增"){
    $table.bootstrapTable('insertRow', {
      index: 1,
      row: {
        id:Ajax.responseData.id,
        income_and_expense: Ajax.responseData.income_and_expense,
        jar_name: Ajax.responseData.jar_name,
        date: Ajax.responseData.date,
        money: Ajax.responseData.money,
        remark: Ajax.responseData.remark
      }
});
  }
}

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

$("#confirm-change-btn").on("click", function (event) {
  console.log("檢查form")
  jarFormObject.autoBootstrapValid(event)
  jarFormObject.getValue()
  sendRequestAndChangeTable(currentRowObject, requestData, modalObject)
})

elements = document.getElementsByName('close')
for (let element of elements) {
  element.addEventListener('click', () => Util.removeAlert())
}

