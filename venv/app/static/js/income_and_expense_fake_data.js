import {
  Ajax
} from './ajax.js'
import {
  FakeRequest,
  RefreshTokenRequest
} from './request.js'
import {
  ConditionForm,
  Constant,
  SearchFlow
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
    // let requestObject = new RequestData(this.constantObject)
    let fakeRequest = FakeRequest.create(this.constantObject)
    // let tokenRequest = RefreshTokenRequest.create(this.constantObject)
    // let tokenRequest = requestObject.getRefreshToken()
    let fakeResponse = await Ajax.sendAutoRefresh(fakeRequest, this.constantObject)
    console.log(fakeResponse)
  }
}


class RegisterEvent {
  constructor() {
    this.constantObject = new Constant()
    this.fakeDataObject = new FakeData(this.constantObject)
    this.searchFlowObject = new SearchFlow()
    this.conditionFormObject = new FakeConditionForm()
  }

  initSearch() {
    this.searchFlowObject.searchEvent(this.conditionFormObject, this.fakeDataObject)
    this.searchFlowObject.cleanSearchEvent()
  }

}

var eventObject = new RegisterEvent()
eventObject.initSearch()