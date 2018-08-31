var e = function (selector) {
    return document.querySelector(selector)
}

var all = function (selector) {
    return document.querySelectorAll(selector)
}

var find = function (elem, selector) {
    return elem.querySelector(selector)
}

var log = console.log.bind(console)

var bindEvent = function(elem, eventName, callback) {
    elem.addEventListener(eventName, callback)
}

var bindAll = function(elems, eventName, callback) {
    for (var e of elems) {
        bindEvent(e, eventName, callback)
    }
}

var bindEvents = function() {
    menus = all('.menu')
    bindAll(menus, 'mouseover', function(){
        var elem = event.currentTarget
        var lst = find(elem, '.menu-dropdown').classList
        if (lst.contains('menu-hide')) {
            lst.remove('menu-hide')
        }
        elem.classList.add('menu-highlight')
    })
    bindAll(menus, 'mouseout', function(elem){
        var elem = event.currentTarget
        var lst = find(elem, '.menu-dropdown').classList
        if (!lst.contains('menu-hide')) {
            lst.add('menu-hide')
        }
        elem.classList.remove('menu-highlight')
    })
}
bindEvents()
