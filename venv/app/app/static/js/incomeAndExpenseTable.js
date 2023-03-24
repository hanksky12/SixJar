import { Util } from './util.js'
import { Ajax } from './ajax.js'
import {RefreshTokenRequest} from './request.js'

export class IncomeAndExpenseTable{
    constructor(constantObject){
        this.constantObject=constantObject
        this.url = constantObject.url+"/income-and-expense/list"
        this.table = $('#table')
        this.table
        .bootstrapTable('destroy')
        .bootstrapTable({

        //分頁相關
        sidePagination: "server",//方式：client ,server 
        cache: false,   //使用缓存，默认为 true，所以一般情况下需要设置一下这个属性
        uniqueId:"id", // 指定field當作方法removeByUniqueId,updateByUniqueId..的搜尋欄位
        pagination:true,  //顯示分頁
        pageList: [ 10, 20, 25, 50 ], //可供選擇的每頁的行數 ,選擇後更改pageSize
        pageNumber:1,//初始頁
        pageSize:10,//每頁筆數
        formatRecordsPerPage:(pageSize)=> {return '&nbsp;&nbsp;每頁顯示' + pageSize + '筆';},
        formatShowingRows:function(fromIndex, toIndex, totalSize) {
            let currentPage = Math.ceil(fromIndex / this.pageSize)      //目前第幾頁
            let totalPageCount = Math.ceil(totalSize / this.pageSize) //總共幾頁
            return '第'+currentPage+'頁&nbsp;&nbsp;共'+totalPageCount+'頁'
          }	,

        //排序相關
        sortable:true, //開啟排序，會在onSort重抓參數後，自動像後端發送目前參數的request
        sortOrder:"desc",//預設 大到小
    
        //外觀
        height: 550,
        theadClasses: "thead-blue",

        classes:"table table-striped table-hover border-primary table-bordered table-sm  text-nowrap",
        striped: true,  //間隔顏色
        rowStyle: function(row, index) {
            let classes = ['bg-type1','bg-type2','bg-type3','bg-type4','bg-type5', 'bg-type6']
            let style 
            if (row["income_and_expense"] =="income") {
                style= {classes: classes[0]}
            }
            else{
             style={classes: classes[1]} 
            }
            return style
        },
        
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
            formatter: (data)=>{ return data == "income" ? "收入" : "支出"}
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
        dataField: "data",//後端回來裝data的key,
        totalField:"total",// 後端返回含有total的key：總記錄數
        queryParams : (params)=>{return this.#queryParams(params)}, //因為（）＝>會做this 的傳遞 把IncomeAndExpenseTable傳到下一層
        onLoadError: (status, jqXHR)=> {
            console.log(status)
            console.log(jqXHR["responseJson"])
            if (status==401) {
                return this.#refreshToken()}
            else {
                return Util.addAlert("表單資料load失敗！", 'danger')}
            }, //更新token
        responseHandler:(res)=>{return res},//不建議更改，會影響bootstrap 抓取total 
      })
    }


    execute(){
      this.table.bootstrapTable('refresh', {pageNumber :1})
    }
  
    changeDisplayRecord(jarModalObject, currentRowObject, responseData){
      if (jarModalObject.method == "刪除"){
        console.log("刪除畫面id:"+currentRowObject.id)
        this.table.bootstrapTable('removeByUniqueId', currentRowObject.id); 
      }
      else if (jarModalObject.method == "修改"){
        console.log("修改畫面id:"+currentRowObject.id)
        this.table.bootstrapTable('updateByUniqueId', {
            id: currentRowObject.id, 
            replace:false,//有出現的做部分更換
            row: {
              income_and_expense: responseData.income_and_expense,
              jar_name: responseData.jar_name,
              date: responseData.date,
              money: responseData.money,
              remark: responseData.remark
            }
          }
        )
      }
      else if (jarModalObject.method == "新增"){
        console.log("新增畫面")
        this.table.bootstrapTable('insertRow', {
            index: 0,
            row: {
              id: responseData.id,
              income_and_expense: responseData.income_and_expense,
              jar_name: responseData.jar_name,
              date: responseData.date,
              money: responseData.money,
              remark: responseData.remark
            }
          }
        )
        this.table.bootstrapTable('scrollTo','bottom');
      }
    }
  
    #queryParams(params){
      let temp = {
        limit : params.limit, // 必填 因為一次只要顯示一頁,所以這邊等於一頁的頁數即可 受pageSize影響
        page: (params.offset / params.limit) + 1, //必填 從offset 推算頁數
        sortOrder: params.order, //找sortOrder的參數
        user_id:this.constantObject.userId
      }
      if (params.sort){temp["sort"] = params.sort} //如果有點擊欄位，就會抓到欄位名稱
      temp = Util.getConditionValue(temp)
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

  async #refreshToken(){
    let tokenObject = new RefreshTokenRequest()
    let tokenRequest = tokenObject.create(this.constantObject)
    await Ajax.send(tokenRequest)
    await this.table.bootstrapTable('refresh')
}
}
  
  

