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

export  class Constant{
    constructor(){
      this.userId = parseInt(Util.getCookie("user_id"))
      this.url = "/api/v1"
      this.httpHeaders = {
        'Content-Type': 'application/json',
        'Accept-Charset': 'utf-8',
        'Accept': 'application/json'
      }
    }
  }