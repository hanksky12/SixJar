
import {
  FakeRequest,

} from './request.js'
import {
  Util,
  ConditionForm,
  Constant,
  ConditionFlow,
  SSEFlow
} from './util.js'

class FakeConditionForm extends ConditionForm {
  check(event) {
    if (super.check(event) == false) {
      return false
    }
    if (document.getElementById('selectRecordsNumber').value == "") {
      return false
    }
    return true
  }
}

class FakeData {
  constructor(constantObject) {
    this.constantObject = constantObject
  }
  async execute() {
    let fakeRequest = FakeRequest.create(this.constantObject,"新增")
    let responseData = await Util.sendAjaxAndResonseToAlert(fakeRequest, this.constantObject)
    let sse = new SSEFlow(responseData.data.task_id,this.constantObject)
    await sse.updataProcessBar()
  }
}


class RegisterEvent {
  constructor() {
    this.constantObject = new Constant()
    this.fakeDataObject = new FakeData(this.constantObject)
    this.conditionFlowObject = new ConditionFlow()
    this.conditionFormObject = new FakeConditionForm()
  }

  initPost() {
    this.conditionFlowObject.conditionEvent(this.conditionFormObject, this.fakeDataObject,'#insert_btn')
    this.conditionFlowObject.cleanSearchEvent()
  }

  initDelete(){
    let that = this
      $("#delete_all_btn").on('click', async () =>{
        // let userPasswordObject = new UserPasswordFlow()
        // if (await userPasswordObject.check(that.constantObject)==false){return}
        let fakeRequest = FakeRequest.create(that.constantObject, "刪除")
        await Util.sendAjaxAndResonseToAlert(fakeRequest, that.constantObject)
      }
    )
  }

  initSocket(){
    $(document).ready( ()=> {
      //不適合移到click內不，不是當下回傳結果，只能在整個頁面監聽
      const socket = io.connect();
      socket.on("message", function (data) {
        Util.addAlert(data,"primary")
      })
    })
  }
}



var eventObject = new RegisterEvent()
eventObject.initPost()
eventObject.initDelete()
// eventObject.initSocket()



