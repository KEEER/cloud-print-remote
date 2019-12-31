'use strict';

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

var $ = function $(sel) {
  return document.querySelector(sel);
};

var MAX_JOB_NUMBER = 1;
var jobTemplate = $('#jobTemplate').innerHTML;
mdc.autoInit.mdcAutoInit.register('MDCTextField', mdc.textfield.MDCTextField);
mdc.autoInit.mdcAutoInit.register('MDCTextFieldHelperText', mdc.textfield.MDCTextFieldHelperText);
mdc.autoInit.mdcAutoInit.register('MDCSwitch', mdc["switch"].MDCSwitch);
var bwStatusIconEl = $('#bw-printer-status-icon');
var bwStatusEl = $('#bw-printer-status'); // start element control

var printerCard = {
  _setBwPrinterStatus: function _setBwPrinterStatus(status, isHalted) {
    if (isHalted) {
      bwStatusIconEl.classList.remove('printer-status__unavaliable');
      bwStatusIconEl.classList.remove('printer-status__busy');
      bwStatusIconEl.classList.remove('printer-status__avaliable');
      bwStatusIconEl.classList.add('printer-status__fixing');
      bwStatusEl.innerText = '维修或调试中';
      return;
    }

    switch (status.state) {
      case 'idle':
        bwStatusIconEl.classList.remove('printer-status__unavaliable');
        bwStatusIconEl.classList.remove('printer-status__busy');
        bwStatusIconEl.classList.remove('printer-status__fixing');
        bwStatusIconEl.classList.add('printer-status__avaliable');
        bwStatusEl.innerText = '就绪';
        break;

      case 'printing':
        bwStatusIconEl.classList.remove('printer-status__unavaliable');
        bwStatusIconEl.classList.remove('printer-status__avaliable');
        bwStatusIconEl.classList.remove('printer-status__fixing');
        bwStatusIconEl.classList.add('printer-status__busy');
        bwStatusEl.innerText = '忙碌中';
        break;

      default:
        bwStatusIconEl.classList.remove('printer-status__busy');
        bwStatusIconEl.classList.remove('printer-status__avaliable');
        bwStatusIconEl.classList.remove('printer-status__fixing');
        bwStatusIconEl.classList.add('printer-status__unavaliable');
        bwStatusEl.innerText = '不可用';
    }
  },
  setPrinterInfo: function setPrinterInfo(name, states, description) {
    console.log('setPrinterInfo: status: ', states);
    $('#printer-info').innerText = name;

    this._setBwPrinterStatus(states.bw, states.halted);

    $('#printer-description').innerText = description;
  }
};
var priceWarningDialog = new mdc.dialog.MDCDialog($('#recharge-dialog'));

var popPriceWarning = function popPriceWarning() {
  $('#total-price').innerText = currentStatus.totalCost / 100;
  $('#total-kredit').innerText = currentStatus.kredit / 100;
  priceWarningDialog.open();
};

var dialogBox = new mdc.dialog.MDCDialog($('#go-print-dialog'));

var popDialog = function popDialog(code) {
  $('#print-code').innerText = code;
  dialogBox.open();
};

var alertBox = new mdc.dialog.MDCDialog($('#alert-dialog'));

var popAlert = function popAlert(message) {
  $('#alert-message').innerText = message;
  alertBox.open();
};

var loadingBox = new mdc.dialog.MDCDialog($('#loading-dialog'));

var startLoading = function startLoading(message) {
  $('#loading-title').innerText = message;
  loadingBox.open();
};

var endLoading = function endLoading() {
  return loadingBox.close();
};

loadingBox.scrimClickAction = loadingBox.escapeKeyAction = '';
var debtBox = new mdc.dialog.MDCDialog($('#debt-dialog'));

var popDebt = function popDebt() {
  $('#debt').innerText = currentStatus.debt / 100;
  debtBox.open();
};

debtBox.scrimClickAction = debtBox.escapeKeyAction = '';

var hideUploadField = function hideUploadField() {
  console.log('hideJob');
  $('#file-zone').classList.add('invisible');
};

var showUploadField = function showUploadField() {
  console.log('showJob');
  $('#file-zone').classList.remove('invisible');
};

var addJob =
/*#__PURE__*/
function () {
  var _ref = _asyncToGenerator(
  /*#__PURE__*/
  regeneratorRuntime.mark(function _callee4(fileName, code, id, config, pageCount) {
    var price, el, withCode, pageNumberInfo, priceInfo, doubleSidedSwitch, colorSwitch, copiesTextfield, printButton, deleteJobButton;
    return regeneratorRuntime.wrap(function _callee4$(_context4) {
      while (1) {
        switch (_context4.prev = _context4.next) {
          case 0:
            startLoading('创建任务…');
            console.log('Trying to add job: ', fileName, code, id, config, pageCount);
            price = 0;
            endLoading();
            console.log('Getting price: ', config.colored);
            _context4.next = 7;
            return getPrice(pageCount * config.copies, config.colored);

          case 7:
            price = _context4.sent;
            currentStatus.totalCost += price;

            if (currentStatus.totalCost > currentStatus.kredit) {
              popPriceWarning();
            }

            el = document.createElement('div');
            el.classList.add('job-wrapper');
            el.innerHTML = jobTemplate.replace(/::jobTitle::/g, fileName).replace(/::pageNumber::/g, pageCount).replace(/::price::/g, price / 100).replace(/::code::/g, code);
            $('#job-list').appendChild(el);
            mdc.autoInit.mdcAutoInit();

            withCode = function withCode(value) {
              return "".concat(value, "-").concat(code);
            }; // about info


            pageNumberInfo = $(withCode('#page-number'));
            priceInfo = $(withCode('#price')); // about config

            doubleSidedSwitch = $(withCode('#ds-switch')).MDCSwitch;
            doubleSidedSwitch.checked = config['double-sided'];
            colorSwitch = $(withCode('#c-switch')).MDCSwitch;
            colorSwitch.checked = config.colored;
            copiesTextfield = $(withCode('#c')).MDCTextField;
            copiesTextfield.value = config.copies; // about action

            printButton = $(withCode('#go-print'));
            deleteJobButton = $(withCode('#delete-job'));
            printButton.onclick =
            /*#__PURE__*/
            _asyncToGenerator(
            /*#__PURE__*/
            regeneratorRuntime.mark(function _callee() {
              return regeneratorRuntime.wrap(function _callee$(_context) {
                while (1) {
                  switch (_context.prev = _context.next) {
                    case 0:
                      _context.next = 2;
                      return updateSession(true);

                    case 2:
                      _context.next = 4;
                      return new Promise(function (resolve) {
                        QRCode.toDataURL("https://print.keeer.net/quick-codes?codes=".concat(JSON.stringify(currentStatus.codes)), {
                          errorCorrectionLevel: 'H',
                          type: 'image/png',
                          margin: 1,
                          color: {
                            dark: '#424242FF',
                            light: '#FFFFFFFF'
                          }
                        }, function (_e, res) {
                          return resolve(res);
                        });
                      });

                    case 4:
                      $('#print-qrcode').src = _context.sent;
                      popDialog(code);

                    case 6:
                    case "end":
                      return _context.stop();
                  }
                }
              }, _callee);
            }));
            deleteJobButton.onclick =
            /*#__PURE__*/
            _asyncToGenerator(
            /*#__PURE__*/
            regeneratorRuntime.mark(function _callee2() {
              return regeneratorRuntime.wrap(function _callee2$(_context2) {
                while (1) {
                  switch (_context2.prev = _context2.next) {
                    case 0:
                      startLoading('删除中…');
                      _context2.next = 3;
                      return deleteJob(code);

                    case 3:
                      $(withCode('#job')).remove();
                      currentStatus.totalCost -= price;
                      endLoading();

                    case 6:
                    case "end":
                      return _context2.stop();
                  }
                }
              }, _callee2);
            }));
            console.log('log elements: ', doubleSidedSwitch, colorSwitch, copiesTextfield);
            $(withCode('#copies')).onchange = $(withCode('#double-sided-switch')).onchange = $(withCode('#color-switch')).onchange =
            /*#__PURE__*/
            _asyncToGenerator(
            /*#__PURE__*/
            regeneratorRuntime.mark(function _callee3() {
              var jobPrice;
              return regeneratorRuntime.wrap(function _callee3$(_context3) {
                while (1) {
                  switch (_context3.prev = _context3.next) {
                    case 0:
                      console.log('Value Changed');
                      if (copiesTextfield.value == null || copiesTextfield.value == '') copiesTextfield.value = 1;

                      if (copiesTextfield.value * pageCount > 50) {
                        copiesTextfield.value = Math.floor(50 / pageCount);
                      }

                      if (copiesTextfield.value < 1) copiesTextfield.value = 1;
                      console.log('Value changed');
                      startLoading('更新打印配置…');
                      console.log('sending current status:', id, doubleSidedSwitch.checked, colorSwitch.checked, Number(copiesTextfield.value), code);
                      _context3.next = 9;
                      return updateConfig(id, doubleSidedSwitch.checked, colorSwitch.checked, Number(copiesTextfield.value), code);

                    case 9:
                      _context3.next = 11;
                      return getPrice(pageCount * Number(copiesTextfield.value), colorSwitch.checked);

                    case 11:
                      jobPrice = _context3.sent;
                      currentStatus.totalCost -= price;
                      price = jobPrice;
                      currentStatus.totalCost += price;
                      priceInfo.innerText = jobPrice / 100;

                      if (currentStatus.totalCost > currentStatus.kredit) {
                        popPriceWarning();
                      }

                      endLoading();

                    case 18:
                    case "end":
                      return _context3.stop();
                  }
                }
              }, _callee3);
            }));
            endLoading();

          case 31:
          case "end":
            return _context4.stop();
        }
      }
    }, _callee4);
  }));

  return function addJob(_x, _x2, _x3, _x4, _x5) {
    return _ref.apply(this, arguments);
  };
}(); //end element control


var currentStatus = {
  codes: [],
  kredit: 0,
  totalCost: 0,
  debt: 0
};
var currentPrinter = {
  id: 255,
  ip: '0.0.0.0',
  avaliable: true,
  name: '等待数据',
  description: '等待数据。请确保您已经连接到学校的 Wi-Fi',
  base: null
};

var constructEndpointURL = function constructEndpointURL(path) {
  return new URL(path, currentPrinter.base);
};

var updatePrinter =
/*#__PURE__*/
function () {
  var _ref5 = _asyncToGenerator(
  /*#__PURE__*/
  regeneratorRuntime.mark(function _callee5(silent) {
    var printerConfigs, stillConnected, _loop2, _i, _Object$keys, _ret;

    return regeneratorRuntime.wrap(function _callee5$(_context6) {
      while (1) {
        switch (_context6.prev = _context6.next) {
          case 0:
            if (!silent) startLoading('搜索局域网内的打印终端…');
            _context6.next = 3;
            return fetch('/_api/printer-ips').then(function (res) {
              return res.json();
            });

          case 3:
            printerConfigs = _context6.sent;
            console.log('Get printer config: ', printerConfigs);
            console.log(Object.keys(printerConfigs));
            stillConnected = false;
            _loop2 =
            /*#__PURE__*/
            regeneratorRuntime.mark(function _loop2() {
              var id, ip, base, res, config;
              return regeneratorRuntime.wrap(function _loop2$(_context5) {
                while (1) {
                  switch (_context5.prev = _context5.next) {
                    case 0:
                      id = _Object$keys[_i];
                      ip = printerConfigs[id];
                      if (!silent) startLoading("\u5C1D\u8BD5\u8FDE\u63A5\u5230\u6253\u5370\u673A\uFF1A#".concat(id));
                      base = new URL("https://".concat(ip.replace(/\./g, '-'), ".ip2.kcps.monster"));
                      console.log('Trying printer id: ', id);
                      _context5.prev = 5;
                      _context5.next = 8;
                      return new Promise(function (resolve, reject) {
                        setTimeout(reject, 1500, new Error('Timeout.'));
                        fetch(new URL('/status', base)).then(resolve)["catch"](reject);
                      }).then(function (res) {
                        return res.json();
                      });

                    case 8:
                      res = _context5.sent;

                      if (!(res.status !== 0)) {
                        _context5.next = 11;
                        break;
                      }

                      throw res;

                    case 11:
                      config = res.response;
                      currentPrinter = {
                        id: id,
                        ip: ip,
                        status: config.status,
                        name: config.name,
                        description: config.message,
                        base: base
                      };
                      console.log('Status: ', config);
                      printerCard.setPrinterInfo(currentPrinter.name, currentPrinter.status, currentPrinter.description);
                      stillConnected = true;
                      return _context5.abrupt("return", "break");

                    case 19:
                      _context5.prev = 19;
                      _context5.t0 = _context5["catch"](5);
                      console.log('Failed.', _context5.t0);
                      return _context5.abrupt("return", "continue");

                    case 23:
                    case "end":
                      return _context5.stop();
                  }
                }
              }, _loop2, null, [[5, 19]]);
            });
            _i = 0, _Object$keys = Object.keys(printerConfigs);

          case 9:
            if (!(_i < _Object$keys.length)) {
              _context6.next = 20;
              break;
            }

            return _context6.delegateYield(_loop2(), "t0", 11);

          case 11:
            _ret = _context6.t0;
            _context6.t1 = _ret;
            _context6.next = _context6.t1 === "break" ? 15 : _context6.t1 === "continue" ? 16 : 17;
            break;

          case 15:
            return _context6.abrupt("break", 20);

          case 16:
            return _context6.abrupt("continue", 17);

          case 17:
            _i++;
            _context6.next = 9;
            break;

          case 20:
            $('#printer-logo').src = '/static/img/logo.png';

            if (currentPrinter.base === null || !stillConnected) {
              $('#printer-logo').src = '/static/img/NotConnected.png';
              printerCard.setPrinterInfo('等待数据', {
                bw: {
                  state: 'unavaliable',
                  message: ''
                },
                colored: {
                  state: 'idle',
                  message: ''
                },
                halted: false
              }, '等待数据。请确保您已经连接到学校的 Wi-Fi');
              console.log('No printers Avaliable');
            }

            endLoading();

          case 23:
          case "end":
            return _context6.stop();
        }
      }
    }, _callee5);
  }));

  return function updatePrinter(_x6) {
    return _ref5.apply(this, arguments);
  };
}();

var updatePrinterInfo =
/*#__PURE__*/
function () {
  var _ref6 = _asyncToGenerator(
  /*#__PURE__*/
  regeneratorRuntime.mark(function _callee6() {
    var res, config;
    return regeneratorRuntime.wrap(function _callee6$(_context7) {
      while (1) {
        switch (_context7.prev = _context7.next) {
          case 0:
            _context7.prev = 0;
            $('#linear-loading-progress').style.opacity = 1;
            _context7.next = 4;
            return fetch(constructEndpointURL('/status')).then(function (res) {
              return res.json();
            });

          case 4:
            res = _context7.sent;

            if (!(res.status !== 0)) {
              _context7.next = 7;
              break;
            }

            throw res;

          case 7:
            config = res.response;
            currentPrinter.description = config.message;
            currentPrinter.status = config.status;
            printerCard.setPrinterInfo(currentPrinter.name, currentPrinter.status, currentPrinter.description);
            _context7.next = 18;
            break;

          case 13:
            _context7.prev = 13;
            _context7.t0 = _context7["catch"](0);
            console.log('Network Changed: ', _context7.t0);
            _context7.next = 18;
            return updatePrinter(true);

          case 18:
            _context7.prev = 18;
            $('#linear-loading-progress').style.opacity = 0;
            return _context7.finish(18);

          case 21:
          case "end":
            return _context7.stop();
        }
      }
    }, _callee6, null, [[0, 13, 18, 21]]);
  }));

  return function updatePrinterInfo() {
    return _ref6.apply(this, arguments);
  };
}();

var deleteJob =
/*#__PURE__*/
function () {
  var _ref7 = _asyncToGenerator(
  /*#__PURE__*/
  regeneratorRuntime.mark(function _callee7(code) {
    var token;
    return regeneratorRuntime.wrap(function _callee7$(_context8) {
      while (1) {
        switch (_context8.prev = _context8.next) {
          case 0:
            _context8.next = 2;
            return requestJobToken(code);

          case 2:
            token = _context8.sent;
            return _context8.abrupt("return", fetch(constructEndpointURL('/delete-job'), {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                token: token
              })
            }));

          case 4:
          case "end":
            return _context8.stop();
        }
      }
    }, _callee7);
  }));

  return function deleteJob(_x7) {
    return _ref7.apply(this, arguments);
  };
}();

var createJob = function createJob() {
  return fetch('/_api/job-token').then(function (res) {
    return res.json();
  });
};

var requestJobToken = function requestJobToken(code) {
  return fetch("/_api/job-token?code=".concat(code)).then(function (res) {
    return res.json();
  });
};

var getPrice =
/*#__PURE__*/
function () {
  var _ref8 = _asyncToGenerator(
  /*#__PURE__*/
  regeneratorRuntime.mark(function _callee8(pageCount, colored) {
    var url;
    return regeneratorRuntime.wrap(function _callee8$(_context9) {
      while (1) {
        switch (_context9.prev = _context9.next) {
          case 0:
            url = new URL('/_api/calculate-price', location);
            url.search = new URLSearchParams({
              config: JSON.stringify({
                'page-count': pageCount,
                colored: colored
              }),
              printer_id: currentPrinter.id
            });
            console.log(url);
            _context9.next = 5;
            return fetch(url).then(function (res) {
              return res.json();
            }).then(function (response) {
              if (response.status === 0) return response.result;
              console.log('Error: ', response);
            });

          case 5:
            return _context9.abrupt("return", _context9.sent);

          case 6:
          case "end":
            return _context9.stop();
        }
      }
    }, _callee8);
  }));

  return function getPrice(_x8, _x9) {
    return _ref8.apply(this, arguments);
  };
}();

var requestAllInfo =
/*#__PURE__*/
function () {
  var _ref9 = _asyncToGenerator(
  /*#__PURE__*/
  regeneratorRuntime.mark(function _callee9(codes, timestamp, sign) {
    return regeneratorRuntime.wrap(function _callee9$(_context10) {
      while (1) {
        switch (_context10.prev = _context10.next) {
          case 0:
            _context10.next = 2;
            return fetch(constructEndpointURL('/get-configs'), {
              method: 'post',
              body: JSON.stringify({
                codes: codes,
                timestamp: timestamp,
                sign: sign
              }),
              headers: {
                'Content-Type': 'application/json'
              }
            }).then(function (res) {
              return res.json();
            });

          case 2:
            return _context10.abrupt("return", _context10.sent);

          case 3:
          case "end":
            return _context10.stop();
        }
      }
    }, _callee9);
  }));

  return function requestAllInfo(_x10, _x11, _x12) {
    return _ref9.apply(this, arguments);
  };
}();

var updateConfig =
/*#__PURE__*/
function () {
  var _ref10 = _asyncToGenerator(
  /*#__PURE__*/
  regeneratorRuntime.mark(function _callee10(id, doubleSided, withColor, copies, code) {
    return regeneratorRuntime.wrap(function _callee10$(_context11) {
      while (1) {
        switch (_context11.prev = _context11.next) {
          case 0:
            _context11.t0 = fetch;
            _context11.t1 = constructEndpointURL('/set-config');
            _context11.t2 = {
              'Content-Type': 'application/json'
            };
            _context11.t3 = JSON;
            _context11.t4 = id;
            _context11.t5 = {
              copies: copies,
              colored: withColor,
              'double-sided': doubleSided
            };
            _context11.next = 8;
            return requestJobToken(code);

          case 8:
            _context11.t6 = _context11.sent;
            _context11.t7 = {
              id: _context11.t4,
              config: _context11.t5,
              token: _context11.t6
            };
            _context11.t8 = _context11.t3.stringify.call(_context11.t3, _context11.t7);
            _context11.t9 = {
              method: 'POST',
              headers: _context11.t2,
              body: _context11.t8
            };

            _context11.t10 = function (res) {
              return res.json();
            };

            _context11.next = 15;
            return (0, _context11.t0)(_context11.t1, _context11.t9).then(_context11.t10);

          case 15:
            return _context11.abrupt("return", _context11.sent);

          case 16:
          case "end":
            return _context11.stop();
        }
      }
    }, _callee10);
  }));

  return function updateConfig(_x13, _x14, _x15, _x16, _x17) {
    return _ref10.apply(this, arguments);
  };
}();

var uploadFile =
/*#__PURE__*/
function () {
  var _ref11 = _asyncToGenerator(
  /*#__PURE__*/
  regeneratorRuntime.mark(function _callee11(fileObject) {
    var fileForm, token;
    return regeneratorRuntime.wrap(function _callee11$(_context12) {
      while (1) {
        switch (_context12.prev = _context12.next) {
          case 0:
            startLoading('上传文件中…');
            fileForm = new FormData();
            fileForm.append('file', fileObject);
            _context12.next = 5;
            return createJob();

          case 5:
            token = _context12.sent;

            if (typeof token['status'] !== 'undefined' && token.status === 1) {
              popAlert('您上传的文件数量已经达到最大允许值');
            }

            fileForm.append('token', JSON.stringify(token));
            _context12.next = 10;
            return fetch(constructEndpointURL('/job'), {
              method: 'POST',
              body: fileForm
            }).then(function (res) {
              return res.json();
            }).then(function (response) {
              endLoading();

              if (response.status === 0) {
                response = response.response;
                console.log('Creating job card: ', response);
                addJob(fileObject.name, response.code, response.id, response.config, response['page-count']);
              }
            });

          case 10:
            return _context12.abrupt("return", _context12.sent);

          case 11:
          case "end":
            return _context12.stop();
        }
      }
    }, _callee11);
  }));

  return function uploadFile(_x18) {
    return _ref11.apply(this, arguments);
  };
}(); // get the session and update the currentStatus


var getSession =
/*#__PURE__*/
function () {
  var _ref12 = _asyncToGenerator(
  /*#__PURE__*/
  regeneratorRuntime.mark(function _callee12() {
    return regeneratorRuntime.wrap(function _callee12$(_context13) {
      while (1) {
        switch (_context13.prev = _context13.next) {
          case 0:
            _context13.next = 2;
            return fetch('/_api/session').then(function (res) {
              return res.json();
            });

          case 2:
            return _context13.abrupt("return", _context13.sent);

          case 3:
          case "end":
            return _context13.stop();
        }
      }
    }, _callee12);
  }));

  return function getSession() {
    return _ref12.apply(this, arguments);
  };
}();

var updateSession =
/*#__PURE__*/
function () {
  var _ref13 = _asyncToGenerator(
  /*#__PURE__*/
  regeneratorRuntime.mark(function _callee13(silent) {
    var sessionObject, jobInfo, _iteratorNormalCompletion, _didIteratorError, _iteratorError, _iterator, _step, config;

    return regeneratorRuntime.wrap(function _callee13$(_context14) {
      while (1) {
        switch (_context14.prev = _context14.next) {
          case 0:
            if (!silent) startLoading('获取数据…');else $('#linear-loading-progress').style.opacity = 1;
            _context14.next = 3;
            return getSession();

          case 3:
            sessionObject = _context14.sent;

            if (!(currentPrinter.base !== null)) {
              _context14.next = 29;
              break;
            }

            _context14.next = 7;
            return requestAllInfo(sessionObject.codes, sessionObject.timestamp, sessionObject.sign);

          case 7:
            jobInfo = _context14.sent;
            console.log('Got job info: ', jobInfo);

            if (!(jobInfo.status === 0)) {
              _context14.next = 29;
              break;
            }

            _iteratorNormalCompletion = true;
            _didIteratorError = false;
            _iteratorError = undefined;
            _context14.prev = 13;

            for (_iterator = jobInfo.response[Symbol.iterator](); !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
              config = _step.value;
              console.log('Loading Job: ', config); // detect whether the job exists

              if ($("#job-".concat(config.code)) === null) addJob(config.file, config.code, '', config.config, config['page-count']);
            }

            _context14.next = 21;
            break;

          case 17:
            _context14.prev = 17;
            _context14.t0 = _context14["catch"](13);
            _didIteratorError = true;
            _iteratorError = _context14.t0;

          case 21:
            _context14.prev = 21;
            _context14.prev = 22;

            if (!_iteratorNormalCompletion && _iterator["return"] != null) {
              _iterator["return"]();
            }

          case 24:
            _context14.prev = 24;

            if (!_didIteratorError) {
              _context14.next = 27;
              break;
            }

            throw _iteratorError;

          case 27:
            return _context14.finish(24);

          case 28:
            return _context14.finish(21);

          case 29:
            if (sessionObject.debt > 0) {
              currentStatus.debt = sessionObject.debt;
              popDebt();
            }

            currentStatus.kredit = sessionObject.kredit;
            $('#kredit').innerText = Number(currentStatus.kredit) / 100;
            currentStatus.codes = sessionObject.codes;
            if (!silent) endLoading();else $('#linear-loading-progress').style.opacity = 0;

          case 34:
          case "end":
            return _context14.stop();
        }
      }
    }, _callee13, null, [[13, 17, 21, 29], [22,, 24, 28]]);
  }));

  return function updateSession(_x19) {
    return _ref13.apply(this, arguments);
  };
}();

var dragAndDropZone = document.getElementById('file-zone');
var infoBox = document.getElementById('upload-info');
var file = document.getElementById('file');

var setMessage = function setMessage(message) {
  infoBox.style.opacity = 1;
  infoBox.innerText = message;
};

dragAndDropZone.ondragover = dragAndDropZone.ondragenter = function (evt) {
  evt.preventDefault();
  dragAndDropZone.classList.add('file-drop-zone__focused');
  infoBox.style.opacity = 0;
};

dragAndDropZone.ondragleave = function (evt) {
  evt.preventDefault();
  dragAndDropZone.classList.remove('file-drop-zone__focused');
  setMessage('拖拽文件到这里');
};

dragAndDropZone.ondrop = function (evt) {
  evt.preventDefault();
  dragAndDropZone.classList.remove('file-drop-zone__focused');
  console.log(evt.dataTransfer.files[0]);
  var currentFile = evt.dataTransfer.files[0];

  if (currentFile.type !== 'application/pdf') {
    setMessage('请上传 PDF 文件');
    return;
  }

  file.files = evt.dataTransfer.files;
  setMessage("\u6B63\u5728\u4E0A\u4F20".concat(evt.dataTransfer.files[0].name));
  uploadFile(evt.dataTransfer.files[0]);
};

file.addEventListener('change', function (e) {
  console.log('Event change', e);
  var currentFile = file.files[0];
  console.log('file: ', currentFile);

  if (currentFile.type !== 'application/pdf') {
    setMessage('请上传 PDF 文件');
    return;
  }

  setMessage("\u6B63\u5728\u4E0A\u4F20 ".concat(currentFile.name)); // TODO

  uploadFile(currentFile);
});

_asyncToGenerator(
/*#__PURE__*/
regeneratorRuntime.mark(function _callee14() {
  return regeneratorRuntime.wrap(function _callee14$(_context15) {
    while (1) {
      switch (_context15.prev = _context15.next) {
        case 0:
          _context15.next = 2;
          return updatePrinter(false);

        case 2:
          _context15.next = 4;
          return updateSession(false);

        case 4:
          setInterval(updatePrinterInfo, 10000);
          setInterval(updateSession, 30000, true);

        case 6:
        case "end":
          return _context15.stop();
      }
    }
  }, _callee14);
}))();
