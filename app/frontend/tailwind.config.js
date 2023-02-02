/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{vue,html,js}"],
  theme: {

    extend: {
      colors: {
        'dark': {
          100: '#3c3c3c',
          200: '#323232',
          300: '#2d2d2d',
          400: '#222222',
          500: '#1f1f1f',
          600: '#1c1c1e',
          700: '#1b1b1b',
          800: '#181818',
          900: '#0f0f0f',
        },
        'jelly-bean': {  DEFAULT: '#2978A0',  50: '#DCEDF6',  100: '#CCE5F2',  200: '#ABD5EA',  300: '#8BC4E1',  400: '#6AB4D9',  500: '#4AA3D1',  600: '#3190C0',  700: '#2978A0',  800: '#216080',  900: '#18475F'},
      },
    },
  },
  plugins: [],
}
