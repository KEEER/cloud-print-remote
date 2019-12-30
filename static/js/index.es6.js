'use strict'

const $ = sel => document.querySelector(sel)
const MAX_JOB_NUMBER = 1
const jobTemplate = $('#jobTemplate').innerHTML
mdc.autoInit.mdcAutoInit.register('MDCTextField', mdc.textfield.MDCTextField)
mdc.autoInit.mdcAutoInit.register('MDCTextFieldHelperText', mdc.textfield.MDCTextFieldHelperText)
mdc.autoInit.mdcAutoInit.register('MDCSwitch', mdc.switch.MDCSwitch)
const bwStatusIconEl = $('#bw-printer-status-icon')
const bwStatusEl = $('#bw-printer-status')

// start element control

const printerCard = {
  _setBwPrinterStatus (status, isHalted) {
    if (isHalted) {
      bwStatusIconEl.classList.remove('printer-status__unavaliable')
      bwStatusIconEl.classList.remove('printer-status__busy')
      bwStatusIconEl.classList.remove('printer-status__avaliable')

      bwStatusIconEl.classList.add('printer-status__fixing')
      bwStatusEl.innerText = '维修或调试中'
      return
    }

    switch (status.state) {
      case 'idle':
        bwStatusIconEl.classList.remove('printer-status__unavaliable')
        bwStatusIconEl.classList.remove('printer-status__busy')
        bwStatusIconEl.classList.remove('printer-status__fixing')

        bwStatusIconEl.classList.add('printer-status__avaliable')
        bwStatusEl.innerText = '就绪'
        break
      case 'printing':
        bwStatusIconEl.classList.remove('printer-status__unavaliable')
        bwStatusIconEl.classList.remove('printer-status__avaliable')
        bwStatusIconEl.classList.remove('printer-status__fixing')

        bwStatusIconEl.classList.add('printer-status__busy')
        bwStatusEl.innerText = '忙碌中'
        break
      default:
      bwStatusIconEl.classList.remove('printer-status__busy')
      bwStatusIconEl.classList.remove('printer-status__avaliable')
      bwStatusIconEl.classList.remove('printer-status__fixing')

      bwStatusIconEl.classList.add('printer-status__unavaliable')
      bwStatusEl.innerText = '不可用'
    }
    
  },
  setPrinterInfo (name, states, description) {
    console.log('setPrinterInfo: status: ', states)
    $('#printer-info').innerText = name
    this._setBwPrinterStatus(states.bw, states.halted)
    $('#printer-description').innerText = description
  }
}

const priceWarningDialog = new mdc.dialog.MDCDialog($('#recharge-dialog'))
const popPriceWarning = () => {
  $('#total-price').innerText = currentStatus.totalCost / 100
  $('#total-kredit').innerText = currentStatus.kredit / 100
  priceWarningDialog.open()
}
const dialogBox = new mdc.dialog.MDCDialog($('#go-print-dialog'))
const popDialog = code => {
  $('#print-code').innerText = code
  dialogBox.open()
}

const alertBox = new mdc.dialog.MDCDialog($('#alert-dialog'))
const popAlert = message => {
  $('#alert-message').innerText = message
  alertBox.open()
}
const loadingBox = new mdc.dialog.MDCDialog($('#loading-dialog'))
const startLoading = message => {
  $('#loading-title').innerText = message
  loadingBox.open()
}
const endLoading = () => loadingBox.close()
loadingBox.scrimClickAction = loadingBox.escapeKeyAction = ''

const debtBox = new mdc.dialog.MDCDialog($('#debt-dialog'))
const popDebt = () => {
  $('#debt').innerText = currentStatus.debt / 100
  debtBox.open()
}
debtBox.scrimClickAction = debtBox.escapeKeyAction = ''

const hideUploadField = () => {
  console.log('hideJob')
  $('#file-zone').classList.add('invisible')
}
const showUploadField = () => {
  console.log('showJob')
  $('#file-zone').classList.remove('invisible')
}
const addJob = async (fileName, code, id, config, pageCount) => {
  startLoading('创建任务…')
  console.log('Trying to add job: ', fileName, code, id, config, pageCount)
  let price = 0
  endLoading()
  console.log('Getting price: ', config.colored)
  price = await getPrice(pageCount * config.copies, config.colored)
  currentStatus.totalCost += price
  if (currentStatus.totalCost > currentStatus.kredit) {
    popPriceWarning()
  }
  const el = document.createElement('div')
  el.classList.add('job-wrapper')
  el.innerHTML = jobTemplate
    .replace(/::jobTitle::/g, fileName)
    .replace(/::pageNumber::/g, pageCount)
    .replace(/::price::/g, price / 100)
    .replace(/::code::/g, code)
  $('#job-list').appendChild(el)
  mdc.autoInit.mdcAutoInit()

  const withCode = value => `${value}-${code}`

  // about info
  const pageNumberInfo = $(withCode('#page-number'))
  const priceInfo = $(withCode('#price'))
  // about config
  const doubleSidedSwitch = $(withCode('#ds-switch')).MDCSwitch
  doubleSidedSwitch.checked = config['double-sided']
  const colorSwitch = $(withCode('#c-switch')).MDCSwitch
  colorSwitch.checked = config.colored
  const copiesTextfield = $(withCode('#c')).MDCTextField
  copiesTextfield.value = config.copies
  // about action
  const printButton = $(withCode('#go-print'))
  const deleteJobButton = $(withCode('#delete-job'))

  printButton.onclick = async () => {
    await updateSession(true)
    $('#print-qrcode').src = await new Promise(resolve => {
      QRCode.toDataURL(`https://print.keeer.net/quick-codes?codes=${JSON.stringify(currentStatus.codes)}`, {
        errorCorrectionLevel: 'H',
        type: 'image/png',
        margin: 1,
        color:  { dark: '#000000FF', light: '#F3E5F5FF' }
      }, (_e, res) => resolve(res))
    })
    popDialog(code)
  }

  deleteJobButton.onclick = async () => {
    startLoading('删除中…')
    await deleteJob(code)
    $(withCode('#job')).remove()
    currentStatus.totalCost -= price
    endLoading()
  }

  console.log('log elements: ', doubleSidedSwitch, colorSwitch, copiesTextfield)
  $(withCode('#copies')).onchange = $(withCode('#double-sided-switch')).onchange = $(withCode('#color-switch')).onchange = async () => {
    console.log('Value Changed')
    if (copiesTextfield.value == null || copiesTextfield.value == '') copiesTextfield.value = 1
    if (copiesTextfield.value * pageCount > 50) {
      copiesTextfield.value = Math.floor(50 / pageCount)
    }
    if(copiesTextfield.value < 1) copiesTextfield.value = 1
    
    console.log('Value changed')
    startLoading('更新打印配置…')
    console.log('sending current status:', id, doubleSidedSwitch.checked, colorSwitch.checked, Number(copiesTextfield.value), code)
    await updateConfig(id, doubleSidedSwitch.checked, colorSwitch.checked, Number(copiesTextfield.value), code)
    const jobPrice = await getPrice(pageCount * Number(copiesTextfield.value), colorSwitch.checked)
    currentStatus.totalCost -= price
    price = jobPrice
    currentStatus.totalCost += price
    priceInfo.innerText = jobPrice / 100
    if (currentStatus.totalCost > currentStatus.kredit) {
      popPriceWarning()
    }
    endLoading()
  }
  endLoading()
}
//end element control

let currentStatus = {
  codes: [],
  kredit: 0,
  totalCost: 0,
  debt: 0,
}
let currentPrinter = {
  id: 255,
  ip: '0.0.0.0',
  avaliable: true,
  name: '等待数据',
  description: '等待数据。请确保您已经连接到学校的 Wi-Fi',
  base: null,
}
const constructEndpointURL = path => new URL(path, currentPrinter.base)

const updatePrinter = async silent => {
  if (!silent) startLoading('搜索局域网内的打印终端…')
  const printerConfigs = await fetch('/_api/printer-ips').then(res => res.json())

  console.log('Get printer config: ', printerConfigs)
  console.log(Object.keys(printerConfigs))
  for (let id of Object.keys(printerConfigs)) {
    const ip = printerConfigs[id]
    if (!silent) startLoading(`尝试连接到打印机：#${id}`)
    const base = new URL(`https://${ip.replace(/\./g, '-')}.ip.kcps.monster`)
    console.log('Trying printer id: ', id)
  
    try {
      const res = await new Promise((resolve, reject) => {
        setTimeout(reject, 1500, new Error('Timeout.'))
        fetch(new URL('/status', base)).then(resolve).catch(reject)
      }).then(res => res.json())
      
      if (res.status !== 0) throw res
      const config = res.response
      currentPrinter = {
        id,
        ip,
        status: config.status,
        name: config.name,
        description: config.message,
        base,
      }
      console.log('Status: ', config)
      printerCard.setPrinterInfo(currentPrinter.name, currentPrinter.status, currentPrinter.description)
      break
    } catch (e) {
      console.log('Failed.', e)
      continue
    }
  }
  $('#printer-logo').src = '/static/img/logo.png'
  if (currentPrinter.base === null) {
    $('#printer-logo').src = '/static/img/NotConnected.png'
    printerCard.setPrinterInfo('等待数据', {
        bw: { state:'unavaliable', message:'' },
        colored: { state:'idle', message:'' },
        halted: false,
    }, '等待数据。请确保您已经连接到学校的 Wi-Fi')
    console.log('No printers Avaliable')
  }
  endLoading()
}

const updatePrinterInfo = async () => {
  try {
    $('#linear-loading-progress').style.opacity = 1
    const res = await fetch(constructEndpointURL('/status')).then(res => res.json())
    if (res.status !== 0) throw res
    const config = res.response
    currentPrinter.description = config.message
    currentPrinter.status = config.status
    printerCard.setPrinterInfo(currentPrinter.name, currentPrinter.status, currentPrinter.description)
  } catch(e) {
    console.log('Network Changed: ', e)
    await updatePrinter(true)
  } finally {
    $('#linear-loading-progress').style.opacity = 0
  }
}

const deleteJob = async code => {
  const token = await requestJobToken(code)
  return fetch(constructEndpointURL('/delete-job'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ token })
  })
}

const createJob = () => fetch('/_api/job-token').then(res => res.json())
const requestJobToken = code => fetch(`/_api/job-token?code=${code}`).then(res => res.json())
const getPrice = async (pageCount, colored) => {
  const url = new URL('/_api/calculate-price', location)
  url.search = new URLSearchParams({
    config: JSON.stringify({ 'page-count': pageCount, colored }),
    printer_id: currentPrinter.id,
  })
  console.log(url)
  return await fetch(url).then(res => res.json()).then(response => {
    if (response.status === 0) return response.result
    console.log('Error: ', response)
  })
}

const requestAllInfo = async (codes, timestamp, sign) => {
  return await fetch(constructEndpointURL('/get-configs'), {
    method: 'post',
    body: JSON.stringify({
      codes,
      timestamp,
      sign,
    }),
    headers: {
      'Content-Type': 'application/json',
    },
  }).then(res => res.json())
}

const updateConfig = async (id, doubleSided, withColor, copies, code) => {
  return await fetch(constructEndpointURL('/set-config'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      id,
      config: {
        copies,
        colored: withColor,
        'double-sided': doubleSided,
      },
      token: await requestJobToken(code),
    }),
  }).then(res => res.json())
}

const uploadFile = async fileObject => {
  startLoading('上传文件中…')

  const fileForm = new FormData()
  fileForm.append('file', fileObject)
  const token = await createJob()
  if (typeof token['status'] !== 'undefined' && token.status === 1){
    popAlert('您上传的文件数量已经达到最大允许值')
  }
  fileForm.append('token', JSON.stringify(token))
  return await fetch(constructEndpointURL('/job'), {
    method: 'POST',
    body: fileForm,
  }).then(res => res.json()).then(response => {
    endLoading()
    if (response.status === 0) {
      response = response.response
      addJob(fileObject.name, response.code, response.id, response.config, response['page-count'])
    }
  })
}

// get the session and update the currentStatus
const getSession = async () => await fetch('/_api/session').then(res => res.json())

const updateSession = async silent => {
  if (!silent) startLoading('获取数据…')
  else $('#linear-loading-progress').style.opacity = 1
  const sessionObject = await getSession()
  // get job info
  if (currentPrinter.base !== null) {
    const jobInfo = await requestAllInfo(sessionObject.codes, sessionObject.timestamp, sessionObject.sign)
    console.log('Got job info: ', jobInfo)
    if (jobInfo.status === 0) {
      for (let config of jobInfo.response) {
        console.log('Loading Job: ', config)
        // detect whether the job exists
        if ($(`#job-${config.code}`) === null)
          addJob(config.file, config.code, '', config.config, config.pageCount)
      }
    }
  }
  if (sessionObject.debt > 0) {
    currentStatus.debt = sessionObject.debt
    popDebt()
  }
  currentStatus.kredit = sessionObject.kredit
  $('#kredit').innerText = Number(currentStatus.kredit) / 100
  currentStatus.codes = sessionObject.codes
  if (!silent) endLoading()
  else $('#linear-loading-progress').style.opacity = 0
}

const dragAndDropZone = document.getElementById('file-zone')
const infoBox = document.getElementById('upload-info')
const file = document.getElementById('file')

const  setMessage = message => {
  infoBox.style.opacity = 1
  infoBox.innerText = message
}

dragAndDropZone.ondragover = dragAndDropZone.ondragenter = evt => {
  evt.preventDefault()
  dragAndDropZone.classList.add('file-drop-zone__focused')
  infoBox.style.opacity = 0
}
dragAndDropZone.ondragleave = evt => {
  evt.preventDefault()
  dragAndDropZone.classList.remove('file-drop-zone__focused')
  setMessage('拖拽文件到这里')
}
dragAndDropZone.ondrop = evt => {
  evt.preventDefault()
  dragAndDropZone.classList.remove('file-drop-zone__focused')
  console.log(evt.dataTransfer.files[0])
  const currentFile = evt.dataTransfer.files[0]
  if (currentFile.type !== 'application/pdf') {
    setMessage('请上传 PDF 文件')
    return
  }
  file.files = evt.dataTransfer.files
  
  setMessage(`正在上传${evt.dataTransfer.files[0].name}`)
  uploadFile(evt.dataTransfer.files[0])
}
file.addEventListener('change', e => {
  console.log('Event change', e)
  const currentFile = file.files[0]
  console.log('file: ', currentFile)
  if (currentFile.type !== 'application/pdf') {
    setMessage('请上传 PDF 文件')
    return
  }
  setMessage(`正在上传 ${currentFile.name}`)
  // TODO
  uploadFile(currentFile)
})

;(async() => {
  await updatePrinter(false)
  await updateSession(false)
  setInterval(updatePrinterInfo, 10000)
  setInterval(updateSession, 30000, true)
})()
