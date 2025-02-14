/**
* Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community Edition) available.
* Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
* Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
* http://opensource.org/licenses/MIT
* Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
*/
/**
 * 函数柯里化
 *
 * @example
 *     function add (a, b) {return a + b}
 *     curry(add)(1)(2)
 *
 * @param {Function} fn 要柯里化的函数
 *
 * @return {Function} 柯里化后的函数
 */
export const curry = (fn) => {
    const judge = (...args) => {
        const result = args.length === fn.length ? fn(...args) : arg => judge(...args, arg)
        return result
    }
    return judge
}

/**
 * 判断是否是对象
 *
 * @param {Object} obj 待判断的
 *
 * @return {boolean} 判断结果
 */
export const isObject = (obj) => {
    return obj !== null && typeof obj === 'object'
}

/**
 * 规范化参数
 *
 * @param {Object|string} type vuex type
 * @param {Object} payload vuex payload
 * @param {Object} options vuex options
 *
 * @return {Object} 规范化后的参数
 */
export const unifyObjectStyle = (type, payload, options) => {
    let newType = type
    let newPayload = payload
    let newOptions = options
    if (isObject(type) && type.type) {
        newOptions = newPayload
        newPayload = newType
        newType = newType.type
    }

    if (NODE_ENV !== 'production') {
        if (typeof type !== 'string') {
            console.warn(`expects string as the type, but found ${typeof type}.`)
        }
    }

    return { newType, newPayload, newOptions }
}

/**
 * 以 baseColor 为基础生成随机颜色
 *
 * @param {string} baseColor 基础颜色
 * @param {number} count 随机颜色个数
 *
 * @return {Array} 颜色数组
 */
export const randomColor = (baseColor, count) => {
    const segments = baseColor.match(/[\da-z]{2}/g)
    // 转换成 rgb 数字
    for (let i = 0; i < segments.length; i++) {
        segments[i] = parseInt(segments[i], 16)
    }
    const ret = []
    // 生成 count 组颜色，色差 20 * Math.random
    for (let i = 0; i < count; i++) {
        ret[i] = '#'
            + Math.floor(segments[0] + (Math.random() < 0.5 ? -1 : 1) * Math.random() * 20).toString(16)
            + Math.floor(segments[1] + (Math.random() < 0.5 ? -1 : 1) * Math.random() * 20).toString(16)
            + Math.floor(segments[2] + (Math.random() < 0.5 ? -1 : 1) * Math.random() * 20).toString(16)
    }
    return ret
}

/**
 * min max 之间的随机整数
 *
 * @param {number} min 最小值
 * @param {number} max 最大值
 *
 * @return {number} 随机数
 */
export const randomInt = (min, max) => {
    return Math.floor(Math.random() * (max - min + 1) + min)
}

/**
 * 异常处理
 *
 * @param {Object} err 错误对象
 * @param {Object} ctx 上下文对象，这里主要指当前的 Vue 组件
 */
export const catchErrorHandler = (err, ctx) => {
    const { data } = err
    if (data) {
        if (!data.code || data.code === 404) {
            ctx.exceptionCode = {
                code: '404',
                msg: '当前访问的页面不存在'
            }
        } else if (data.code === 403) {
            ctx.exceptionCode = {
                code: '403',
                msg: 'Sorry，您的权限不足!'
            }
        } else {
            console.error(err)
            ctx.bkMessageInstance = ctx.$bkMessage({
                theme: 'error',
                message: err.message || err.data.msg || err.statusText
            })
        }
    } else {
        console.error(err)
        ctx.bkMessageInstance = ctx.$bkMessage({
            theme: 'error',
            message: err.message || err.data.msg || err.statusText
        })
    }
}

/**
 * 获取字符串长度，中文算两个，英文算一个
 *
 * @param {string} str 字符串
 *
 * @return {number} 结果
 */
export const getStringLen = (str) => {
    let len = 0
    for (let i = 0; i < str.length; i++) {
        if (str.charCodeAt(i) > 127 || str.charCodeAt(i) === 94) {
            len += 2
        } else {
            len += 1
        }
    }
    return len
}

/**
 * 转义特殊字符
 *
 * @param {string} str 待转义字符串
 *
 * @return {string} 结果
 */
export const escape = str => String(str).replace(/([.*+?^=!:${}()|[\]\/\\])/g, '\\$1')

/**
 * 对象转为 url query 字符串
 *
 * @param {*} param 要转的参数
 * @param {string} key key
 *
 * @return {string} url query 字符串
 */
export const json2Query = (param, key) => {
    const mappingOperator = '='
    const separator = '&'
    let paramStr = ''

    if (param instanceof String || typeof param === 'string'
            || param instanceof Number || typeof param === 'number'
            || param instanceof Boolean || typeof param === 'boolean'
    ) {
        paramStr += separator + key + mappingOperator + encodeURIComponent(param)
    } else {
        Object.keys(param).forEach((p) => {
            const value = param[p]
            const k = (key === null || key === '' || key === undefined)
                ? p
                : key + (param instanceof Array ? '[' + p + ']' : '.' + p)
            paramStr += separator + json2Query(value, k)
        })
    }
    return paramStr.substr(1)
}

/**
 * 字符串转换为驼峰写法
 *
 * @param {string} str 待转换字符串
 *
 * @return {string} 转换后字符串
 */
export const camelize = (str) => {
    return str.replace(/-(\w)/g, (strMatch, p1) => p1.toUpperCase())
}

/**
 * 获取元素的样式
 *
 * @param {Object} elem dom 元素
 * @param {string} prop 样式属性
 *
 * @return {string} 样式值
 */
export const getStyle = (elem, prop) => {
    if (!elem || !prop) {
        return false
    }

    // 先获取是否有内联样式
    let value = elem.style[camelize(prop)]

    if (!value) {
        // 获取的所有计算样式
        let css = ''
        if (document.defaultView && document.defaultView.getComputedStyle) {
            css = document.defaultView.getComputedStyle(elem, null)
            value = css ? css.getPropertyValue(prop) : null
        }
    }

    return String(value)
}

/**
 *  获取元素相对于页面的高度
 *
 *  @param {Object} node 指定的 DOM 元素
 */
export const getActualTop = (node) => {
    let actualTop = node.offsetTop
    let current = node.offsetParent

    while (current !== null) {
        actualTop += current.offsetTop
        current = current.offsetParent
    }

    return actualTop
}

/**
 *  获取元素相对于页面左侧的宽度
 *
 *  @param {Object} node 指定的 DOM 元素
 */
export const getActualLeft = (node) => {
    let actualLeft = node.offsetLeft
    let current = node.offsetParent

    while (current !== null) {
        actualLeft += current.offsetLeft
        current = current.offsetParent
    }

    return actualLeft
}

/**
 * document 总高度
 *
 * @return {number} 总高度
 */
export const getScrollHeight = () => {
    let scrollHeight = 0
    let bodyScrollHeight = 0
    let documentScrollHeight = 0

    if (document.body) {
        bodyScrollHeight = document.body.scrollHeight
    }

    if (document.documentElement) {
        documentScrollHeight = document.documentElement.scrollHeight
    }

    scrollHeight = (bodyScrollHeight - documentScrollHeight > 0) ? bodyScrollHeight : documentScrollHeight

    return scrollHeight
}

/**
 * 滚动条在 y 轴上的滚动距离
 *
 * @return {number} y 轴上的滚动距离
 */
export const getScrollTop = () => {
    let scrollTop = 0
    let bodyScrollTop = 0
    let documentScrollTop = 0

    if (document.body) {
        bodyScrollTop = document.body.scrollTop
    }

    if (document.documentElement) {
        documentScrollTop = document.documentElement.scrollTop
    }

    scrollTop = (bodyScrollTop - documentScrollTop > 0) ? bodyScrollTop : documentScrollTop

    return scrollTop
}

/**
 * 浏览器视口的高度
 *
 * @return {number} 浏览器视口的高度
 */
export const getWindowHeight = () => {
    const windowHeight = document.compatMode === 'CSS1Compat'
        ? document.documentElement.clientHeight
        : document.body.clientHeight

    return windowHeight
}

/**
 * 日期格式化 按照yyyy-MM-dd HH:MM:SS格式化
 * @param date
 * @returns {string}
 */
export const dateFormatter = (date) => {
    const month = (date.getMonth() + 1).toString()
        .padStart(2, '0')
    const strDate = date.getDate().toString()
        .padStart(2, '0')
    const hh = date.getHours().toString()
        .padStart(2, '0')
    const mm = date.getMinutes().toString()
        .padStart(2, '0')
    const ss = date.getSeconds().toString()
        .padStart(2, '0')
    return `${date.getFullYear()}-${month}-${strDate} ${hh}:${mm}:${ss}`
}
