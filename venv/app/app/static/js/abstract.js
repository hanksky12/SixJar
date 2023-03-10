export class AbstractModal {
  constructor(id) {
    this.modal = document.getElementById(id)
    this.bootstrapModal = new bootstrap.Modal(this.modal, {
      keyboard: false
    })
  }
  hide() {
    this.bootstrapModal.hide()
  }
  show() {
    this.bootstrapModal.show()
  }
}

export class AbstractForm {
  constructor(id) {
    this.form = document.getElementById(id)
  }

  autoBootstrapValid(event) {
    if (!this.form.checkValidity()) {
      console.log("基礎驗證未通過")
      this.form.classList.add('was-validated')
      return false
    } else {
      console.log("基礎驗證通過")
      this.form.classList.add('was-validated')
      return true
    }
  }
}