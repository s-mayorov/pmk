let jq = jQuery
jq(document).foundation()
jq('[data-order]').click(e => {
    let trs = ''
    jq('table').find('input').each((i,o) => {
        if(jq(o).val() != ''){
            jq(o).parents('tr').find('.input').remove()
            trs += '<tr>' + jq(o).parents('tr').html() + '</tr>'
        }
    })
    jq('[data-order-details]').html('<table>' + trs + '</table>')
})

let $ = selector => document.querySelector(selector)
let $$ = selector => document.querySelectorAll(selector)

let vCenter = () => {
    $$('[data-valign]:not(.hide)').forEach(el => {
        el.style.marginTop = (window.innerHeight > el.offsetHeight)
            ? window.innerHeight / 2 - el.offsetHeight / 2 + 'px'
            : ''
    })
}

let throttle = setTimeout(vCenter, 50)
window.onresize = () => {
    clearTimeout(throttle)
    throttle = setTimeout(vCenter, 50)
}

let jsonp = (url, callback) => {
    let callbackName = 'jsonp_callback_' + Math.round(100000 * Math.random())
    window[callbackName] = data => {
        delete window[callbackName]
        document.body.removeChild(script)
        callback(data)
    }
    let script = document.createElement('script')
    script.src = url + (url.indexOf('?') >= 0 ? '&' : '?') + 'callback=' + callbackName
    script.onerror = () => console.error('Script error')
    document.body.appendChild(script)
}
jsonp('http://ipinfo.io', data => switchLang(data.country != 'RU' ? 'EN' : 'RU'))

let switchLang = lang => {
    let selector = '[data-lang]'
    lang = lang || $(`.hide${selector}`).dataset.lang
    $$(selector).forEach(b => b.className = b.dataset.lang == lang ? 'row' : 'row hide')
    vCenter()
}

$$('.lang_switch').forEach(el => (el.onclick = e => switchLang()))

let changeNum = e => {
    let input = e.target,
        val = input.value,
        price = parseFloat(input.parentNode.previousElementSibling.innerHTML),
        summ = input.parentNode.nextElementSibling

    summ.innerHTML = val * price + '₽'
}

$$('input').forEach(el => {
    el.onchange = e => changeNum(e)
    el.onkeyup = e => changeNum(e)
})
