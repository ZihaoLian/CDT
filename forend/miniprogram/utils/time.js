function timeFormat(time) {
    time = time >= 10 ? time : '0' + time
    return time
}

function getTime() {
    let time = new Date()
    let year = time.getFullYear()
    let month = timeFormat(time.getMonth())
    let day = timeFormat(time.getDate())
    let hour = timeFormat(time.getHours())
    let minute = timeFormat(time.getMinutes())
    let second = timeFormat(time.getSeconds())

    return (year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second)
}

module.exports = {
    getTime: getTime,
    timeFormat: timeFormat
}


