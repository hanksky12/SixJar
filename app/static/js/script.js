

var modal = document.getElementById('exampleModal')

modal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    let button = event.relatedTarget
    // Extract info from data-bs-* attributes
    let method = button.getAttribute('data-bs-method')
    let modalTitle = modal.querySelector('.modal-title')
    let btn_confirm= modal.querySelector('.btn-confirm')
    modalTitle.textContent =  method+'紀錄'
    btn_confirm.textContent = method
    let selects = modal.querySelectorAll('.form-select')
    let controls = modal.querySelectorAll('.form-control')
      if (method == "刪除")
      {
        changeAttribute(setElementsAttributeDisabled,[selects, controls])
      }
      else if (method == "新增")
      {
        changeAttribute(removeElementsAttributeDisabled,[selects, controls])
        //帶入table值
      }
      else if (method == "修改")
      {
        changeAttribute(removeElementsAttributeDisabled,[selects, controls])
      }
      //基本驗證
      //向後端發送ＡＪＡＸ
      //處理回應


})



function changeAttribute(fun, elements_array)
{
    for (let elements of elements_array)
    {
        fun(elements)
    }
}


function setElementsAttributeDisabled(elements)
{
      for (let i=0;i<elements.length;i++)
        elements.item(i).setAttribute('disabled', "")
}

function removeElementsAttributeDisabled(elements)
{
      for (let i=0;i<elements.length;i++)
        elements.item(i).removeAttribute('disabled')
}






