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
        }
      },
    },
  },
  plugins: [],
}
