

class ModalOperate {
  #modal
  constructor(event) {
    this.button = event.relatedTarget
    this.method = this.button.getAttribute('data-bs-method')
    this.#modal = document.getElementById('jarModal')
    this.#setTitle()
    this.#setBtn()
    this.#setForm()
  }

  // connect(event) {

  // }

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

}

class CurrentRow {
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

class JarForm {
  constructor() {
    this.form = document.getElementById('jar-form')
    this.#autoRemoveAlert()
  }

  setValue(currentRow) {
    document.getElementById('floatingTextarea').value = currentRow.remark
    document.getElementById('money').value = currentRow.money
    document.getElementById('date').value = currentRow.date
    document.getElementById('selectType').value = currentRow.income_and_expense
    document.getElementById('selectJar').value = currentRow.jar_name
  }
  getValue() {
    this.remark = document.getElementById('floatingTextarea').value
    this.money = document.getElementById('money').value
    this.date = document.getElementById('date').value
    this.jar_name = document.getElementById('selectJar').value
    this.income_and_expense = document.getElementById('selectType').value
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

  #autoRemoveAlert(){
  elements = document.getElementsByName('close')
  for (let element of elements) {
    element.addEventListener('click', () => Util.removeAlert())
  }
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
   getJar(constantObject, currentRowObject, modalObject, jarFormObject) {
    constantObject =  $.extend(true, {}, constantObject);
    console.log('preparejarData')
    const id = currentRowObject.id
    const userId = constantObject.userId
    constantObject.httpHeaders['X-CSRF-TOKEN'] = Util.getCookie("csrf_access_token")
    let body = {
        "user_id": userId,
        "money": parseInt(jarFormObject.money),
        "date": jarFormObject.date,
        "jar_name": jarFormObject.jar_name,
        "remark": jarFormObject.remark,
        "income_and_expense": (jarFormObject.income_and_expense == "收入") ? 'income' : 'expense'
      }
    let method
    let URL = constantObject.url + "/income-and-expense"
    if (modalObject.method == '新增') 
    {
      method = 'POST'
    }
    else if (modalObject.method == '修改') 
    {
      method = 'PUT'
      URL += "/" + id
    }
    else if (modalObject.method == '刪除') 
    {
      method = 'DELETE'
      URL += "/" + id
      body = { "user_id": userId }
    }
    console.log(body)
    return new Request(URL, { method: method, headers: new Headers(constantObject.httpHeaders), body: JSON.stringify(body) })
  }

   getToken(constantObject) {
    constantObject =  $.extend(true, {}, constantObject);
    console.log('prepareTokenData')
    constantObject.httpHeaders['X-CSRF-TOKEN'] = Util.getCookie("csrf_refresh_token")
    const URL = constantObject.url + "/token/refresh"
    return new Request(URL, { method: 'POST', headers: new Headers(httpHeaders) })
  }
}

class Ajax {
  static responseData
  static async sendJar(jarRequest,tokenRequest) {
    try 
    {
      await Ajax.send(jarRequest)
    }
    catch (error) 
    {
      let message = error.message
      console.log(message)
      if (message == "Token has expired") {
        await Ajax.send(tokenRequest)
        await Ajax.send(jarRequest)
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
      
      let message
      if (response.hasOwnProperty("msg")){
        console.log("解析msg")
        message = response.msg
      }
      else if (response.hasOwnProperty("message")){ 
        console.log("解析message")
        message = response.message
      }
      else{ 
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
  constructor(){
    this.userId = parseInt(Util.getCookie("user_id"))
    this.url = "http://127.0.0.1:5001/api/v1"
    this.httpHeaders = {
      'Content-Type': 'application/json',
      'Accept-Charset': 'utf-8',
      'Accept': 'application/json'
    }
  }
}


class IncomeAndExpenseTable{
  constructor(basicUrl, userId){
    this.table = $('#table')
    this.url = basicUrl+"/income-and-expense/search"
    this.userId = userId

    this.table
    .bootstrapTable('destroy')//先清空
    .bootstrapTable({
      //分頁相關
      sidePagination: "server",//方式：client ,server 
      cache: false,   //是否使用缓存，默认为 true，所以一般情况下需要设置一下这个属性
      uniqueId:"id", // 用來指定某個field當作方法removeByUniqueId,updateByUniqueId..的搜尋欄位
      pagination:true,  //是否顯示分頁
      pageList: [ 10, 20, 25, 50 ], //可供選擇的每頁的行數 ,選擇後更改pageSize
      pageNumber:1,//初始頁
      pageSize:5,//每頁筆數
      onPageChange:function(currentPage, pageSize) {
        console.log("目前頁數:"+currentPage+",一頁顯示:"+pageSize+"筆");
      },
      formatRecordsPerPage:function(pageSize) {
        return '&nbsp;&nbsp;每頁顯示' + pageSize + '筆';
      },
      formatShowingRows:function(fromIndex, toIndex, totalSize) {
        let currentPage = Math.ceil(fromIndex / this.pageSize)      //目前第幾頁
        let totalPageCount = Math.ceil(totalSize / this.pageSize)//總共幾頁
        return '第'+currentPage+'頁&nbsp;&nbsp;共'+totalPageCount+'頁'
      }	,
    
      //排序相關
      sortable:true, //開啟排序，會在onSort重抓參數後，自動像後端發送目前參數的request
      sortOrder:"desc",//預設 大到小
      // search:true, //******顯示搜索框****// 參數向後端帶 不實做
      // searchOnEnterKey:false, //******回车后执行搜索****//
  
      //外觀
      height: 550,
      theadClasses: "thead-dark",
      classes:"table table-striped table-hover border-primary table-bordered table-sm table-dark",
      striped: true,  //間隔顏色
      //表格定義
      columns: [
        {
          field: 'id',
          title: 'Id',
          align: 'center',
          class:"hide_column" //到ＣＳＳ做設定
          // visible:false//隱藏  直接用連dom都抓不到
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
          align: 'center',
          width:150,
        }, {
          field: 'date',
          title: '日期',
          sortable: true,
          align: 'center',
          width:150,
        }, {
          field: 'money',
          title: '金額(元)',
          sortable: true,
          align: 'center',
          width:160,
  
        },{
          field: 'remark',
          title: '備註',
          align: 'center',
          width:200,
        },{
          field: 'operate',
          title: '操作',
          align: 'center',
          width:130, 
          formatter: this.#operateFormatter
        }
      ],
  
      //Ajax定義
      method : 'get',
      contentType: "application/json",
      url : this.url,   
      queryParams : this.#queryParams,
      dataField: "data",//後端回來裝data的key,
      totalField:"total",// 後端返回含有total的key：總記錄數
      onLoadError: function () {
        // showTips("數據載入失敗！");
    },
      responseHandler:(res)=>{
        //不建議更改，會影響bootstrap 抓取total
        return res},
    })
  }
  
  searchEvent(){
    $('#search_btn').click(function() {
    //自己實作的
    this.table.bootstrapTable('refresh', {
      pageNumber :1
    });
  })
  }

  cleanSearchEvent(){$('#clean_search_btn').click(function() {
    let idArray = [
      'selectTypeForSearch',
      'selectJarForSearch',
      'minimum_money',
      'maximum_money',
      'earliest_date',
      'latest_date'
      ]
    $.each(idArray, function (index, id) {
      document.getElementById(id).value = ""
    })

    // document.getElementById('selectTypeForSearch').value = ""
    // document.getElementById('selectJarForSearch').value = ""
    // document.getElementById('minimum_money').value = ""
    // document.getElementById('maximum_money').value = ""
    // document.getElementById('earliest_date').value = ""
    // document.getElementById('latest_date').value = ""
  })
  }

  changeDisplayRecord(modalObject, responseData){
    if (modalObject.method == "刪除"){
      console.log("刪除畫面")
      console.log(currentRowObject.id)
      $table.bootstrapTable('removeByUniqueId', currentRowObject.id); 
    }
    else if (modalObject.method == "修改"){
      console.log("修改畫面")
      console.log(currentRowObject.id)
      $table.bootstrapTable('updateByUniqueId', {
        id: currentRowObject.id, 
        replace:true,
        row: {
          income_and_expense: responseData.income_and_expense,
          jar_name: responseData.jar_name,
          date: responseData.date,
          money: responseData.money,
          remark: responseData.remark
        }});
    }
    else if (modalObject.method == "新增"){
      console.log("新增畫面")
      $table.bootstrapTable('insertRow', {
        index: 1,
        row: {
          id: responseData.id,
          income_and_expense: responseData.income_and_expense,
          jar_name: responseData.jar_name,
          date: responseData.date,
          money: responseData.money,
          remark: responseData.remark
        }
  });
    }

  }

  #queryParams(params){
    let temp = {
      limit : params.limit, // 必填 因為一次只要顯示一頁,所以這邊等於一頁的頁數即可 受pageSize影響
      page: (params.offset / params.limit) + 1, //必填 從offset 推算頁數
      sortOrder: params.order, //找sortOrder的參數
      user_id:this.userId
    }
    if (params.sort){temp["sort"] = params.sort} //如果有點擊欄位，就會抓到欄位名稱
    if ($('#selectTypeForSearch').val()){
      temp["income_and_expense"] = $('#selectTypeForSearch').val()=="收入"?"income":"expense"
    }
    if ($('#selectJarForSearch').val()){temp["jar_name"] = $('#selectJarForSearch').val()}
    let idArray = ['minimum_money','maximum_money',"earliest_date","latest_date"]
    for (let id of idArray) { if ($("#"+id).val()){temp[id] = $("#"+id).val()}}
    return temp
  }

 #operateFormatter(value, row, index) {
  return [
    '<button type="button" class="btn btn-warning btnSelect" data-bs-toggle="modal" data-bs-target="#jarModal" data-bs-method="修改">',
    '修改',
    '</button>  ',
    '<button type="button" class="btn btn-danger btnSelect" data-bs-toggle="modal" data-bs-target="#jarModal" data-bs-method="刪除">',
    '刪除',
    '</button>'
  ].join('')
}
}


//////////////////////////////////////////////////////////////////////////////////////////////////////////

// let jarFormObject = new JarForm()
// let modalObject = new ModalOperate()
// let currentRowObject = new CurrentRow()
// let  constantObject= new Constant() 
// let incomeAndExpenseTableObject = new IncomeAndExpenseTable(constantObject.url, constantObject.userId)

// window.ajaxOptions = {
//   beforeSend: function (xhr) {
//     //重設cookie
//     // xhr.setRequestHeader('custom-auth-token', 'custom-auth-token')
//   }
// }

//  sendRequestAndChangeTable = async function(constantObject,currentRowObject, modalObject, jarFormObject) {
//   let requestObject = await new RequestData()
//   jarRequest = requestObject.getJar(constantObject, currentRowObject, modalObject, jarFormObject)
//   tokenRequest = requestObject.getToken(constantObject)
//   await Ajax.sendJar(jarRequest,tokenRequest)
//   console.log("responseData")
//   console.log(Ajax.responseData)

// }

// $("#jarModal").on('show.bs.modal', function (event) {
//   console.log("初始化modal")
//   //初始化
//   modalObject.connect(event)
//   modalObject.setTitle()
//   modalObject.setBtn()
//   modalObject.setForm()
//   //賦值
//   currentRowObject.getInfo(modalObject.button, modalObject.method, Util.getTodayDate())
//   console.log(currentRowObject)
//   jarFormObject.setValue(currentRowObject)
// })

// $("#confirm-change-btn").on("click", function (event) {
//   console.log("檢查form")
//   jarFormObject.autoBootstrapValid(event)
//   jarFormObject.getValue()
//   sendRequestAndChangeTable(constantObject, currentRowObject, modalObject, jarFormObject)
// })




class RegisterEvent{
  constantObject= new Constant() 

initModalAndForm(){
  $("#jarModal").on('show.bs.modal', function (event) {
    console.log("初始化modal")
    //初始化
    modalObject = new ModalOperate(event)
    //賦值
    currentRowObject = new CurrentRow()
    currentRowObject.getInfo(modalObject.button, modalObject.method, Util.getTodayDate())
    console.log(currentRowObject)
    jarFormObject = new JarForm()
    jarFormObject.setValue(currentRowObject)
    })
  } 

initTable(){
    console.log("初始化table")
    incomeAndExpenseTableObject = new IncomeAndExpenseTable(constantObject.url, constantObject.userId)
    incomeAndExpenseTableObject.searchEvent()
    incomeAndExpenseTableObject.cleanSearchEvent()
  }

sendForm(){
    $("#confirm-change-btn").on("click", function (event) {
      console.log("檢查form")
      jarFormObject.autoBootstrapValid(event)
      jarFormObject.getValue()
      this.sendRequestAndChangeTable(constantObject, currentRowObject, modalObject, jarFormObject)
    })
  }

  sendRequestAndChangeTable = async function(constantObject,currentRowObject, modalObject, jarFormObject) {
    let requestObject = await new RequestData()
    jarRequest = requestObject.getJar(constantObject, currentRowObject, modalObject, jarFormObject)
    tokenRequest = requestObject.getToken(constantObject)
    await Ajax.sendJar(jarRequest,tokenRequest)
    console.log("responseData")
    console.log(Ajax.responseData)
    incomeAndExpenseTableObject.changeDisplayRecord(modalObject,Ajax.responseData)
    
  }


}

eventObject = new RegisterEvent()
eventObject.initModalAndForm()
eventObject.initTable()
eventObject.sendForm()
