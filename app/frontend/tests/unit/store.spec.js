// By Colin Martires

import { createStore } from 'vuex'

test('set user notifications', () => {
  const store = createStore({
    state: {
        user: {
            notificationPreferences: {
                lightsOutNotif: false,
                upcomingRacesNotif: false,
                completeNotif: false,
                driverStandingsNotif: false
            }
        }   
    },
    mutations: {
      SET_NOTIFICATION_PREFERENCES(state, data) {
        state.user.notificationPreferences.lightsOutNotif = data.lightsOutNotif
        state.user.notificationPreferences.upcomingRacesNotif = data.upcomingRacesNotif
        state.user.notificationPreferences.completeNotif = data.completeNotif
        state.user.notificationPreferences.driverStandingsNotif = data.driverStandingsNotif
        state.user.notificationPreferences.constructorStandingsNotif = data.constructorStandingsNotif
      }
    }
  })

  store.commit('SET_NOTIFICATION_PREFERENCES', {
    lightsOutNotif: true,
    upcomingRacesNotif: true,
    completeNotif: false,
    driverStandingsNotif: false,
    constructorStandingsNotif: true
  })

  expect(store.state.user.notificationPreferences.lightsOutNotif).toBe(true)
  expect(store.state.user.notificationPreferences.upcomingRacesNotif).toBe(true)
  expect(store.state.user.notificationPreferences.completeNotif).toBe(false)
  expect(store.state.user.notificationPreferences.driverStandingsNotif).toBe(false)
  expect(store.state.user.notificationPreferences.constructorStandingsNotif).toBe(true)
})
