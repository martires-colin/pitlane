import Login from "@/views/Login.vue"
import { mount } from "@vue/test-utils"

describe("Login.vue", () => {
    it('Login page renders', () => {
        const wrapper = mount(Login)
        expect(wrapper.exists()).toBe(true)
      })
})