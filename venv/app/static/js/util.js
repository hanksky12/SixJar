import { AbstractForm } from './abstract.js'
import { Ajax } from './ajax.js'
export class Util {
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
    if (type == 'primary') //type= danger, primary, warning, success
      icon = '<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Info:"><use xlink:href="#info-fill"/></svg>'
    else
      icon = '<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>'
    wrapper.innerHTML = '<div class="alert alert-' + type + ' alert-dismissible" role="alert">' + icon + message +
      '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'
    alertPlaceholder.append(wrapper)
  }

  static async sendAjaxAndResonseToAlert(request, constantObject) {
    let responseData = await Ajax.sendAutoRefresh(request, constantObject)
    const type = responseData.is_success?'primary' :'danger'
    Util.addAlert(responseData.message, type)
    return responseData
  }

  static getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i].trim();
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }


  static getConditionValue(temp) {
    if ($('#selectTypeForSearch').val()){temp["income_and_expense"] = $('#selectTypeForSearch').val()=="收入"?"income":"expense"}
    if ($('#selectJarForSearch').val()){temp["jar_name"] = $('#selectJarForSearch').val()}
    let idArray = ['minimum_money','maximum_money',"earliest_date","latest_date"]
    for (let id of idArray) { if ($("#"+id).val()){temp[id] = $("#"+id).val()}}
    return temp;
  }

  static checkConditionValue() {
    let earliest_date = document.getElementById('earliest_date').value 
    let latest_date = document.getElementById('latest_date').value 
    let minimum_money = parseInt(document.getElementById('minimum_money').value )
    let maximum_money = parseInt(document.getElementById('maximum_money').value )
    if (minimum_money == 0){return false}
    if ((earliest_date && latest_date)&& (earliest_date > latest_date)){return false}
    if ((minimum_money && maximum_money) && (minimum_money > maximum_money)){return false}
    return true
  }

  static cleanConditionValue() {
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
      }
    )
  }

  static createRequest(url, method, httpHeaders, body) {
    if (body == undefined) {
      return new Request(url, {
        method: method,
        headers: new Headers(httpHeaders)
      })
    } else {
      return new Request(url, {
        method: method,
        headers: new Headers(httpHeaders),
        body: JSON.stringify(body)
      })
    }
  }

}

export class Constant {
  constructor() {
    this.userId = parseInt(Util.getCookie("user_id"))
    this.url = "/api/v1"
    this.httpHeaders = {
      'Content-Type': 'application/json',
      'Accept-Charset': 'utf-8',
      'Accept': 'application/json'
    }
  }
}

export class ConditionForm extends AbstractForm{
  constructor() {
      super('condition-form')
  }
  check(event){
    if (this.autoBootstrapValid(event)== false) {return false}
    if (Util.checkConditionValue() ==false){return false}
    return true
  }
}

export class ConditionFlow {

  conditionEvent(conditionObject, successObject, butId = '#search_btn'){
    $(butId).click((event)=> {
      let toastLiveExample = document.getElementById('liveToast')
      var toast = new bootstrap.Toast(toastLiveExample)
      toast.show()
      Util.removeAlert()
      if (conditionObject.check(event)){
        successObject.execute()}
      else{
        Util.addAlert("設定的條件，怪怪的呦！", 'danger')}
      }
     )
  }

  cleanSearchEvent(cleanBtnId='#clean_search_btn'){
    Util.removeAlert()
    $(cleanBtnId).click(()=> {
        Util.cleanConditionValue()
      }
    )
  }
}


