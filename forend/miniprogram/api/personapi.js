const app = getApp()

const subapi = `${app.globalData.host}/api/v1/person`

module.exports = {
    login() {
        return app.get(`${subapi}/person/${app.globalData.userInfo.openId}/`)
    },

    newUser() {
        return app.post(`${subapi}/people/`, app.globalData.userInfo.openId)
    },

    updateUser(data) {
        return app.put(`${subapi}/person/${app.globalData.userInfo.openId}/`, data)
    }
}